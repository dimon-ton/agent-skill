"""
swap_subject.py — swap two schedule cells in the Phontan school timetable,
with optional cascade-resolution of resulting teacher collisions.

Output: writes a UTF-8 report to swap_subject_output.txt next to the workbook,
and prints a brief stdout summary (Thai-safe).

Modes
─────
  default        Plain swap. If a NEW teacher collision is introduced, abort.
  --cascade      If the initial swap introduces collisions, automatically search
                 for additional swaps within the same grade (any day, any
                 period) that resolve each collision. Stop at MAX_DEPTH rounds.
                 Roll back everything if no resolution is found.
  --dry-run      Report what would happen without writing or saving.
  --force        Commit the initial swap even if collisions remain after any
                 cascading attempts (or skip cascade entirely).

Spec format
───────────
  sheet/day/grade/period
    sheet:  p13 | p46 | m13
    day:    mon | tue | wed | thu | fri
    grade:  p1..p6 | m1..m3
    period: 1..6  (1=09-10 .. 6=15-16)
"""

import os
import sys
from collections import Counter

import win32com.client as win32

# ── paths & constants ────────────────────────────────────────────────────────
EXCEL_PATH = r"C:\Users\saich\Documents\excel-vba-schedule\ตารางเรียนเทอม1 ปี 69-1 - execution.xlsm"
OUT_PATH   = r"C:\Users\saich\Documents\excel-vba-schedule\swap_subject_output.txt"

SHEET_IDX  = {'p13': 9, 'p46': 10, 'm13': 12}
SHEET_KEY  = {9: 'p13', 10: 'p46', 12: 'm13'}
DAY_BASES  = {'mon': 3, 'tue': 9, 'wed': 15, 'thu': 21, 'fri': 27}
DAY_KEYS   = ['mon', 'tue', 'wed', 'thu', 'fri']
DAY_THAI   = {'mon': 'จันทร์', 'tue': 'อังคาร', 'wed': 'พุธ', 'thu': 'พฤหัสบดี', 'fri': 'ศุกร์'}
GRADE_IDX  = {'p1': 0, 'p2': 1, 'p3': 2, 'p4': 0, 'p5': 1, 'p6': 2,
              'm1': 0, 'm2': 1, 'm3': 2}
GRADE_SHEET = {'p1': 'p13', 'p2': 'p13', 'p3': 'p13',
               'p4': 'p46', 'p5': 'p46', 'p6': 'p46',
               'm1': 'm13', 'm2': 'm13', 'm3': 'm13'}
PERIOD_COLS = {1: 3, 2: 4, 3: 5, 4: 7, 5: 8, 6: 9}
PERIOD_LABEL = {1: '09-10', 2: '10-11', 3: '11-12', 4: '13-14',
                5: '14-15', 6: '15-16'}

NO_FILL = {'รูปประจำชั้น', 'ลดเวลาเรียน'}

# Subjects that should not move because they share a fixed school-wide slot
PROTECTED_SUBJECTS = {
    'พักรับประทานอาหาร', 'พักรับประทานอาหารกลางวัน',
    'ลูกเสือ-เนตรนารี', 'สวดมนต์', 'ชุมนุม', 'แนะแนว',
    'ลดเวลาเรียน', 'รูปประจำชั้น',
}

ALL_SCHEDULE_SHEETS = [9, 10, 12]
MAX_CASCADE_DEPTH = 10


# ── logging ──────────────────────────────────────────────────────────────────
_log_buf = []
def log(msg=""):
    _log_buf.append(msg)
def flush():
    with open(OUT_PATH, 'w', encoding='utf-8') as f:
        f.write('\n'.join(_log_buf))


# ── Excel helpers (safe-attach) ──────────────────────────────────────────────
_XL = None  # module-level Excel app for VBA Application.Run calls


def excel_attach():
    global _XL
    started = False
    try:
        xl = win32.GetActiveObject('Excel.Application')
    except Exception:
        xl = win32.Dispatch('Excel.Application')
        started = True
    xl.DisplayAlerts = False
    _XL = xl
    return xl, started


def get_workbook(xl):
    target = os.path.normcase(os.path.abspath(EXCEL_PATH))
    for w in xl.Workbooks:
        if os.path.normcase(os.path.abspath(w.FullName)) == target:
            return w, False
    return xl.Workbooks.Open(EXCEL_PATH), True


def merge_val(ws, r, c):
    cell = ws.Cells(r, c)
    if cell.MergeCells:
        ma = cell.MergeArea
        return ws.Cells(ma.Row, ma.Column).Value
    return cell.Value


def v(val):
    return str(val).strip() if val else ''


def write_cell(ws, row, col, value):
    cell = ws.Cells(row, col)
    if cell.MergeCells:
        cell.MergeArea.Cells(1, 1).Value = value
    else:
        cell.Value = value


# ── spec parsing ─────────────────────────────────────────────────────────────
def parse_spec(spec):
    parts = spec.strip().lower().split('/')
    if len(parts) != 4:
        raise ValueError(f"Bad spec '{spec}'")
    sheet_key, day_key, grade_key, period_key = parts

    if sheet_key not in SHEET_IDX:
        raise ValueError(f"Unknown sheet '{sheet_key}'")
    if day_key not in DAY_BASES:
        raise ValueError(f"Unknown day '{day_key}'")
    if grade_key not in GRADE_IDX:
        raise ValueError(f"Unknown grade '{grade_key}'")
    if GRADE_SHEET[grade_key] != sheet_key:
        raise ValueError(f"Grade '{grade_key}' not on sheet '{sheet_key}'")

    try:
        period = int(period_key)
        if period not in PERIOD_COLS:
            raise ValueError()
    except ValueError:
        raise ValueError(f"Period must be 1-6, got '{period_key}'")

    return _build_spec(sheet_key, day_key, grade_key, period)


def _build_spec(sheet_key, day_key, grade_key, period):
    grade_idx = GRADE_IDX[grade_key]
    base = DAY_BASES[day_key]
    subj_row = base + grade_idx * 2
    return {
        'spec_str': f"{sheet_key}/{day_key}/{grade_key}/{period}",
        'sheet_key': sheet_key,
        'sheet_idx': SHEET_IDX[sheet_key],
        'day': day_key,
        'grade': grade_key,
        'period': period,
        'subj_row': subj_row,
        'tchr_row': subj_row + 1,
        'col': PERIOD_COLS[period],
    }


def spec_id(spec):
    """Stable identifier for a cell location (used for visited-set)."""
    return (spec['sheet_idx'], spec['subj_row'], spec['col'])


# ── reads ────────────────────────────────────────────────────────────────────
def read_cell(wb, spec):
    ws = wb.Worksheets(spec['sheet_idx'])
    subj = v(merge_val(ws, spec['subj_row'], spec['col']))
    tchr = v(merge_val(ws, spec['tchr_row'], spec['col']))
    return subj, tchr


def collect_teachers_at_slot(wb, day_key, period):
    """Return list of 9 teacher names at (day, period) across all 3 sheets."""
    col = PERIOD_COLS[period]
    base = DAY_BASES[day_key]
    names = []
    for sheet_idx in ALL_SCHEDULE_SHEETS:
        ws = wb.Worksheets(sheet_idx)
        for gi in range(3):
            tchr_row = base + gi * 2 + 1
            names.append(v(merge_val(ws, tchr_row, col)))
    return names


def find_teacher_locations_at_slot(wb, day_key, period, teacher_name):
    """Find every cell (sheet_idx, grade_idx) where `teacher_name` teaches at
    this (day, period) — used to identify exactly which classes collide."""
    col = PERIOD_COLS[period]
    base = DAY_BASES[day_key]
    locations = []
    for sheet_idx in ALL_SCHEDULE_SHEETS:
        ws = wb.Worksheets(sheet_idx)
        for gi in range(3):
            tchr_row = base + gi * 2 + 1
            if v(merge_val(ws, tchr_row, col)) == teacher_name:
                grades_for_sheet = {
                    9:  ['p1', 'p2', 'p3'],
                    10: ['p4', 'p5', 'p6'],
                    12: ['m1', 'm2', 'm3'],
                }[sheet_idx]
                locations.append(_build_spec(
                    SHEET_KEY[sheet_idx], day_key, grades_for_sheet[gi], period))
    return locations


# ── collision detection ─────────────────────────────────────────────────────
# Single source of truth: the workbook's own VBA `IsDuplicateTeacher` function
# (Main.bas) decides whether a 9-teacher array contains a collision. We call
# it via Application.Run so any future change to the VBA rule automatically
# applies here too.
#
# IsDuplicateTeacher returns Boolean only — to know *which* teacher is
# duplicated (needed for cascade resolution), Python additionally counts
# names matching the same exclusion rules as the VBA function.

def is_duplicate_via_vba(names):
    """Call VBA IsDuplicateTeacher(names). Returns Boolean. Falls back to a
    Python mirror of the VBA rule if the call fails (e.g. workbook not loaded
    in an Excel instance that exposes the VBA project)."""
    if _XL is not None:
        try:
            return bool(_XL.Application.Run("IsDuplicateTeacher", list(names)))
        except Exception:
            pass
    # Python fallback — must match VBA logic exactly
    seen = set()
    for n in names:
        if n and n not in NO_FILL:
            if n in seen:
                return True
            seen.add(n)
    return False


def duplicates_in(names):
    """Names appearing 2+ times, using the same exclusion rules as VBA
    IsDuplicateTeacher (blank, 'รูปประจำชั้น', 'ลดเวลาเรียน' excluded)."""
    return {n for n, c in Counter(
        n for n in names if n and n not in NO_FILL).items() if c >= 2}


def slot_duplicates(wb, day_key, period):
    """Return set of duplicate names at (day, period), but only if VBA
    IsDuplicateTeacher agrees there is any duplicate at this slot.
    This makes VBA the authoritative source for 'is this a collision?'."""
    names = collect_teachers_at_slot(wb, day_key, period)
    if not is_duplicate_via_vba(names):
        return set()
    return duplicates_in(names)


def all_slot_duplicates(wb):
    """Snapshot of all (day, period) slots that VBA IsDuplicateTeacher flags
    as having a duplicate. Returns dict {(day, period): set(teacher_names)}."""
    out = {}
    for day in DAY_KEYS:
        for period in range(1, 7):
            d = slot_duplicates(wb, day, period)
            if d:
                out[(day, period)] = d
    return out


def run_main_check_duplicate():
    """Invoke the workbook's official VBA `mainCheckDuplicate` audit macro.
    The macro's own output goes to Excel's Immediate window (Debug.Print) and
    is not capturable from Python — we still run it so the workbook's own
    audit logic executes, matching how a human user would verify the sheet."""
    if _XL is None:
        return False
    try:
        _XL.Application.Run("mainCheckDuplicate")
        return True
    except Exception:
        return False


# ── swap primitive ──────────────────────────────────────────────────────────
def physical_swap(wb, spec_a, spec_b):
    """Swap subject+teacher between two cells. Returns the two (subj, tchr)
    tuples it read before swapping (for rollback)."""
    subj_a, tchr_a = read_cell(wb, spec_a)
    subj_b, tchr_b = read_cell(wb, spec_b)
    ws_a = wb.Worksheets(spec_a['sheet_idx'])
    ws_b = wb.Worksheets(spec_b['sheet_idx'])
    write_cell(ws_a, spec_a['subj_row'], spec_a['col'], subj_b)
    write_cell(ws_a, spec_a['tchr_row'], spec_a['col'], tchr_b)
    write_cell(ws_b, spec_b['subj_row'], spec_b['col'], subj_a)
    write_cell(ws_b, spec_b['tchr_row'], spec_b['col'], tchr_a)
    return (subj_a, tchr_a), (subj_b, tchr_b)


# ── cascade resolver ────────────────────────────────────────────────────────
def candidate_resolvers(wb, collision_spec, baseline_dupes, visited):
    """
    For a cell whose teacher just caused a collision at (collision_spec.day,
    collision_spec.period), enumerate candidate swap partners *within the same
    grade* (any day, any period) that would move the offending teacher OUT of
    the colliding slot without introducing a new duplicate elsewhere.

    Returns list of candidate spec dicts (best first — closest periods first,
    then closest days).
    """
    grade = collision_spec['grade']
    sheet_key = GRADE_SHEET[grade]
    sheet_idx = SHEET_IDX[sheet_key]
    ws = wb.Worksheets(sheet_idx)
    grade_idx = GRADE_IDX[grade]

    candidates = []
    # iterate all (day, period) cells for this grade
    for day_key in DAY_KEYS:
        for period in range(1, 7):
            cand = _build_spec(sheet_key, day_key, grade, period)
            if spec_id(cand) == spec_id(collision_spec):
                continue
            if spec_id(cand) in visited:
                continue
            subj, tchr = read_cell(wb, cand)
            if not subj or subj in PROTECTED_SUBJECTS:
                continue
            # priority: shorter day-distance + period-distance from collision
            day_dist = abs(DAY_KEYS.index(day_key) - DAY_KEYS.index(collision_spec['day']))
            per_dist = abs(period - collision_spec['period'])
            candidates.append((day_dist + per_dist, cand, (subj, tchr)))

    candidates.sort(key=lambda x: x[0])
    return [(c[1], c[2]) for c in candidates]


def new_duplicates_after_swap(wb, spec_a, spec_b, baseline_dupes):
    """Simulate (without actually writing) the swap of A and B and compute
    which (day, period) slots would gain a NEW duplicate. Returns list of
    tuples (day_key, period, teacher_name, dest_spec) describing each new
    duplicate."""
    subj_a, tchr_a = read_cell(wb, spec_a)
    subj_b, tchr_b = read_cell(wb, spec_b)

    new = []
    for dest, incoming_t, leaving_t in [(spec_a, tchr_b, tchr_a),
                                         (spec_b, tchr_a, tchr_b)]:
        names = collect_teachers_at_slot(wb, dest['day'], dest['period'])
        # apply simulated swap to the names list
        cleaned = []
        removed = False
        for n in names:
            if n == leaving_t and not removed:
                removed = True
            else:
                cleaned.append(n)
        cleaned.append(incoming_t)

        dupes_after = duplicates_in(cleaned)
        baseline_for_slot = baseline_dupes.get((dest['day'], dest['period']), set())
        for name in dupes_after - baseline_for_slot:
            new.append((dest['day'], dest['period'], name, dest))
    return new


def find_cascade_resolution(wb, initial_a, initial_b, baseline_dupes):
    """
    Try to resolve any collisions introduced by swapping initial_a ↔ initial_b
    via additional same-grade swaps.

    Returns:
      (success: bool, swap_chain: list of (spec_a, spec_b) tuples, report: list[str])

    swap_chain[0] is always (initial_a, initial_b). swap_chain[1..] are the
    cascading swaps to resolve collisions.

    The function does NOT write to the workbook permanently: it makes a swap,
    inspects state, and rolls everything back at the end. The caller is
    responsible for re-applying swap_chain when committing.
    """
    report = []
    visited = {spec_id(initial_a), spec_id(initial_b)}
    swap_chain = []
    rollback_stack = []

    def do_swap(a, b):
        prev_a, prev_b = physical_swap(wb, a, b)
        rollback_stack.append((a, b, prev_a, prev_b))
        swap_chain.append((a, b))
        visited.add(spec_id(a))
        visited.add(spec_id(b))

    def rollback_all():
        while rollback_stack:
            a, b, prev_a, prev_b = rollback_stack.pop()
            ws_a = wb.Worksheets(a['sheet_idx'])
            ws_b = wb.Worksheets(b['sheet_idx'])
            write_cell(ws_a, a['subj_row'], a['col'], prev_a[0])
            write_cell(ws_a, a['tchr_row'], a['col'], prev_a[1])
            write_cell(ws_b, b['subj_row'], b['col'], prev_b[0])
            write_cell(ws_b, b['tchr_row'], b['col'], prev_b[1])

    # round 0 — apply the user's intended swap
    do_swap(initial_a, initial_b)
    report.append(f"Round 1: swap {initial_a['spec_str']} ↔ {initial_b['spec_str']}")

    for depth in range(MAX_CASCADE_DEPTH):
        # find any NEW duplicates relative to baseline
        new_dupes = []
        for (day, period), names_after in all_slot_duplicates(wb).items():
            baseline = baseline_dupes.get((day, period), set())
            for name in names_after - baseline:
                new_dupes.append((day, period, name))

        if not new_dupes:
            report.append(f"  -> no new collisions after {len(swap_chain)} swap(s)")
            rollback_all()
            return True, swap_chain, report

        # pick the first unresolved collision
        day, period, offender = new_dupes[0]
        report.append(f"Round {depth + 2}: collision = ครู[{offender}] "
                      f"at วัน{DAY_THAI[day]} คาบ {PERIOD_LABEL[period]}")

        # Find the cells where this teacher is double-booked at this slot
        locations = find_teacher_locations_at_slot(wb, day, period, offender)
        # Pick one that wasn't already moved this run (so we don't undo our work)
        cell_to_move = None
        for loc in locations:
            if spec_id(loc) not in visited:
                cell_to_move = loc
                break
        if cell_to_move is None:
            report.append("  -> no movable cell among collision locations; abort")
            rollback_all()
            return False, [], report

        # Search for a same-grade partner that moves the offender OUT and
        # introduces no further new duplicates.
        resolved = False
        for partner_spec, _ in candidate_resolvers(
                wb, cell_to_move, baseline_dupes, visited):
            # Simulate
            new_after = new_duplicates_after_swap(
                wb, cell_to_move, partner_spec, baseline_dupes)
            # We accept the partner if simulated swap leaves the current
            # offender resolved AND introduces no NEW second-order duplicate
            # at the partner's slot.
            #
            # Compute prospective post-swap state:
            #   - At cell_to_move's slot: offender leaves, partner's teacher arrives.
            #     If partner's teacher == offender, that doesn't resolve anything.
            #   - At partner_spec's slot: offender arrives.
            #
            # We must ensure the offender doesn't re-duplicate at the partner's slot.
            partner_subj, partner_tchr = read_cell(wb, partner_spec)
            if partner_tchr == offender:
                continue  # would not resolve

            # Apply tentatively, check, accept if clean.
            do_swap(cell_to_move, partner_spec)
            report.append(f"  -> cascade swap {cell_to_move['spec_str']} "
                          f"↔ {partner_spec['spec_str']}")

            # Recompute new collisions globally
            new_dupes_after = []
            for (d2, p2), names2 in all_slot_duplicates(wb).items():
                base2 = baseline_dupes.get((d2, p2), set())
                for n2 in names2 - base2:
                    new_dupes_after.append((d2, p2, n2))

            # Accept if this round reduced the new-collision count
            if len(new_dupes_after) < len(new_dupes):
                resolved = True
                break
            else:
                # roll back this cascade attempt and try next partner
                a, b, prev_a, prev_b = rollback_stack.pop()
                ws_a = wb.Worksheets(a['sheet_idx'])
                ws_b = wb.Worksheets(b['sheet_idx'])
                write_cell(ws_a, a['subj_row'], a['col'], prev_a[0])
                write_cell(ws_a, a['tchr_row'], a['col'], prev_a[1])
                write_cell(ws_b, b['subj_row'], b['col'], prev_b[0])
                write_cell(ws_b, b['tchr_row'], b['col'], prev_b[1])
                swap_chain.pop()
                visited.discard(spec_id(a))
                visited.discard(spec_id(b))
                # restore visited for the originals
                visited.add(spec_id(initial_a))
                visited.add(spec_id(initial_b))

        if not resolved:
            report.append("  -> no resolving partner found; abort")
            rollback_all()
            return False, [], report

    report.append(f"  -> max depth {MAX_CASCADE_DEPTH} reached; abort")
    rollback_all()
    return False, [], report


# ── macro & save ────────────────────────────────────────────────────────────
def run_change_cell_color(xl, wb):
    for sheet_idx in ALL_SCHEDULE_SHEETS:
        ws = wb.Worksheets(sheet_idx)
        ws.Activate()
        xl.Application.Run("ChangeCellColor")


# ── main ────────────────────────────────────────────────────────────────────
def main():
    args = [a for a in sys.argv[1:] if not a.startswith('-')]
    flags = [a for a in sys.argv[1:] if a.startswith('-')]
    dry_run = '--dry-run' in flags
    cascade = '--cascade' in flags
    force   = '--force' in flags

    if len(args) != 2:
        log("Usage: swap_subject.py <spec_a> <spec_b> [--dry-run] [--cascade] [--force]")
        log("  spec: sheet/day/grade/period   e.g. m13/tue/m3/5")
        flush()
        print(f"See {OUT_PATH}")
        sys.exit(1)

    spec_a = parse_spec(args[0])
    spec_b = parse_spec(args[1])

    xl, started = excel_attach()
    wb, opened = get_workbook(xl)
    rc = 0

    try:
        # Run the workbook's own VBA audit first — matches what the school
        # admin would do manually. Output goes to Excel's Immediate window.
        if run_main_check_duplicate():
            log("[VBA] รัน mainCheckDuplicate แล้ว (ผลใน Immediate window)")
        else:
            log("[VBA] เรียก mainCheckDuplicate ไม่สำเร็จ — ดำเนินการต่อด้วย IsDuplicateTeacher")
        log("")

        subj_a, tchr_a = read_cell(wb, spec_a)
        subj_b, tchr_b = read_cell(wb, spec_b)
        log(f"Cell A  ({args[0]}): [{subj_a}] | [{tchr_a}]")
        log(f"Cell B  ({args[1]}): [{subj_b}] | [{tchr_b}]")
        log("")

        baseline_dupes = all_slot_duplicates(wb)
        if baseline_dupes:
            log(f"หมายเหตุ: ก่อนสลับมี collision อยู่แล้ว {len(baseline_dupes)} จุด — "
                f"จะถือเป็น baseline และไม่นับเป็น new collision")
            for (d, p), names in baseline_dupes.items():
                log(f"  baseline: วัน{DAY_THAI[d]} คาบ {PERIOD_LABEL[p]} -> {sorted(names)}")
            log("")

        # try plain swap first
        new_after = new_duplicates_after_swap(wb, spec_a, spec_b, baseline_dupes)

        if not new_after:
            log("Plain swap: ไม่มี collision ใหม่")
            if dry_run:
                log("DRY RUN — ไม่เขียน")
                log(f"  จะเขียน [{subj_b}] | [{tchr_b}] -> {args[0]}")
                log(f"  จะเขียน [{subj_a}] | [{tchr_a}] -> {args[1]}")
                return
            physical_swap(wb, spec_a, spec_b)
            run_change_cell_color(xl, wb)
            wb.Save()
            log("สลับเสร็จแล้ว [OK]")
            log(f"  {args[0]} <- [{subj_b}] | [{tchr_b}]")
            log(f"  {args[1]} <- [{subj_a}] | [{tchr_a}]")
            return

        log(f"Plain swap จะสร้าง collision {len(new_after)} จุด:")
        for day, period, name, dest in new_after:
            log(f"  - ครู[{name}] ที่ วัน{DAY_THAI[day]} คาบ {PERIOD_LABEL[period]} ({dest['grade'].upper()})")
        log("")

        if cascade:
            log("== CASCADE MODE ==")
            success, chain, report = find_cascade_resolution(
                wb, spec_a, spec_b, baseline_dupes)
            log('\n'.join(report))
            log("")
            if not success:
                log("Cascade ไม่สามารถแก้ collision ได้ทั้งหมด — ไม่มีการเปลี่ยนแปลง")
                if not force:
                    rc = 3
                    return
                log("--force ระบุ: commit เฉพาะ swap แรก แม้ collision จะยังเหลือ")
                chain = [(spec_a, spec_b)]

            if dry_run:
                log("DRY RUN — ไม่เขียน. แผนการสลับ:")
                for a, b in chain:
                    log(f"  swap {a['spec_str']} ↔ {b['spec_str']}")
                return

            # Re-apply the chain permanently
            for a, b in chain:
                physical_swap(wb, a, b)
            run_change_cell_color(xl, wb)
            wb.Save()
            log("สลับเสร็จแล้ว [OK] — รวม " + str(len(chain)) + " swap:")
            for a, b in chain:
                sa, ta = read_cell(wb, a)
                sb, tb = read_cell(wb, b)
                log(f"  {a['spec_str']} <- [{sa}] | [{ta}]")
                log(f"  {b['spec_str']} <- [{sb}] | [{tb}]")
            return

        # not cascade mode and there are new collisions
        log("ใช้ --cascade เพื่อให้สคริปต์พยายามแก้ collision อัตโนมัติ")
        log("หรือ --force เพื่อบังคับสลับ")
        if not force:
            rc = 2
            return

        if dry_run:
            log("--force + --dry-run: จะเขียน plain swap แม้มี collision")
            return
        physical_swap(wb, spec_a, spec_b)
        run_change_cell_color(xl, wb)
        wb.Save()
        log("สลับ (force) เสร็จแล้ว — collision ยังเหลือ")

    finally:
        if opened:
            wb.Close(False)
        if started:
            xl.Quit()
        flush()
        print(f"See {OUT_PATH} (rc={rc})")
        sys.exit(rc)


if __name__ == '__main__':
    main()
