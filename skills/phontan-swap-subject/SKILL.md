---
name: phontan-swap-subject
description: >
  Swap two schedule cells in the Phontan school timetable (โรงเรียนอนุบาลเมืองพนมไพร).
  Use this skill whenever the user asks to swap, exchange, or trade a
  subject/period between two class slots — even if they don't say "swap"
  explicitly (e.g. "ย้าย X ไปอยู่ที่ Y แล้วเอา Y มาอยู่ที่ X", "แลกคาบ",
  "สลับวิชา", "ย้ายวิชาหลักไปช่วงเช้า"). The skill checks for teacher
  collisions and (with --cascade) automatically resolves them by chaining
  follow-up swaps within the same grade.
---

# Schedule Cell Swap — โรงเรียนอนุบาลเมืองพนมไพร

## What this skill does

Swaps two schedule cells (subject + teacher) across any combination of the
3 schedule sheets (ป.1-3, ป.4-6, ม.1-3) with **collision-aware** logic that
**calls the workbook's own VBA macros** as the single source of truth.

Workflow:

1. **Calls `mainCheckDuplicate`** at the start — the workbook's official
   audit macro. Output goes to Excel's Immediate window (Debug.Print) and
   matches what a school admin would do manually.
2. Reads both cells, computes the swap.
3. **Calls `IsDuplicateTeacher` via `Application.Run`** for every
   `(day, period)` slot — VBA decides whether a slot contains a collision.
   Python only counts which names repeat (since VBA returns Boolean).
4. Detects any **new** teacher collision (same teacher at the same
   `(day, period)` across 9 grades) — pre-existing duplicates captured in
   step 3 are treated as baseline and not reported as new.
5. In `--cascade` mode, when a collision is found, the script auto-searches
   the *same grade* (any day, any period) for a partner swap that resolves
   the collision, and applies it. Repeats until clean or `MAX_CASCADE_DEPTH`
   (10 rounds) is hit.
6. If unresolvable, rolls back all attempted swaps. The workbook is only
   saved when a fully-clean plan is found (or with `--force`).
7. On success, runs `ChangeCellColor` on all 3 sheets and saves.

**Why call VBA instead of re-implementing in Python?** The workbook's own
VBA function `IsDuplicateTeacher` (in `Main.bas`) is the school's authoritative
collision rule. If the school updates the VBA (e.g. adds new placeholder
strings or changes the exclusion list), the Python skill automatically picks
up the change — no double-maintenance.

## Spec format

Each cell is identified by `sheet/day/grade/period`:

| Part   | Values |
|--------|--------|
| sheet  | `p13` `p46` `m13` |
| day    | `mon` `tue` `wed` `thu` `fri` |
| grade  | `p1` `p2` `p3` `p4` `p5` `p6` `m1` `m2` `m3` |
| period | `1`=09-10  `2`=10-11  `3`=11-12  `4`=13-14  `5`=14-15  `6`=15-16 |

Grade must belong to the stated sheet (e.g. `p4` must use sheet `p46`).

## Running

```powershell
python "C:\Users\saich\.claude\skills\phontan-swap-subject\scripts\swap_subject.py" <spec_a> <spec_b> [--cascade] [--dry-run] [--force]
```

Flags:
- `--dry-run`   show plan, write nothing
- `--cascade`   auto-resolve resulting collisions (recommended)
- `--force`     commit even with unresolved collisions

Output: detailed report at `swap_subject_output.txt` (UTF-8). The console
prints only a one-line pointer to it (Thai-safe under cp874).

## Translating user requests → swap plans

When the user says things like:

> "ย้ายคณิตศาสตร์ ม.2 จันทร์ บ่าย ไปเช้า"
> "แลกคาบครู X ที่..."
> "วิชาหลัก ๆ หนัก ๆ ให้อยู่ช่วงเช้า"

1. Identify the source cell (which grade, day, period contains the heavy subject).
2. Find a partner cell on the same grade & day in the morning (or use the
   skill's bundled helper `dump_schedule.py`-style logic to list candidates).
3. Run with `--dry-run --cascade` first to see the full plan.
4. If the plan looks acceptable, re-run without `--dry-run` to commit.
5. After commit, run `phontan-teacher-analysis` to confirm totals unchanged.
6. Open Excel for the user to review.

## How cascade resolution works

1. **Round 1** = the user's intended swap. Compute new collisions
   (post-swap duplicates minus baseline).
2. For each new collision, identify which cell on the offending grade
   currently holds the duplicated teacher at the colliding slot.
3. Search same-grade candidate partners (any day, any period), preferring
   ones close to the colliding slot. Reject candidates whose teacher
   would re-introduce the same duplicate.
4. Tentatively apply each candidate; accept if it reduces the new-collision
   count. Repeat until zero new collisions or depth limit reached.
5. Visited cells (already moved in this run) are never moved again — prevents
   ping-pong loops.
6. If the cascade fails, every tentative swap is rolled back and the workbook
   stays untouched.

## Baseline duplicates

The workbook usually has ~17 pre-existing "duplicates" — most are protected
school-wide blocks (lunch, scouts, prayer ceremony, ส่งเสริมทักษะชีวิต, etc.)
or genuine cross-class teaching by the same teacher in the same period. The
script captures these as **baseline** before any swap and ignores them when
deciding whether a swap "created" a new collision.

## After a successful swap

The script automatically:
1. Runs `ChangeCellColor` on sheets 9, 10, 12 — see
   [[feedback_run_changecellcolor_after_edit]].
2. Saves the workbook.

You should then:
1. Run `phontan-teacher-analysis` to confirm totals unchanged.
2. Open Excel: `Start-Process "...xlsm"`.

## Example session — heavy-subject promotion

User: "ย้าย คณิตศาสตร์ ม.2 จันทร์ บ่าย ไปเช้า"

```powershell
# Dry-run with cascade to see the full plan
python ".../swap_subject.py" m13/mon/m2/5 m13/mon/m2/3 --cascade --dry-run

# If acceptable, commit
python ".../swap_subject.py" m13/mon/m2/5 m13/mon/m2/3 --cascade
```

Real cascade observed: Round 1 swap put ครูสรัญญา into ม.2 จันทร์ คาบ 11-12,
but ม.1 จันทร์ คาบ 11-12 already had ครูสรัญญา. Round 2 swapped ม.1 จันทร์
คาบ 11-12 ↔ ม.1 จันทร์ คาบ 10-11 to move her out, achieving zero new
collisions in 2 rounds.

## Key technical notes

- **VBA-driven collision detection**:
  - `mainCheckDuplicate` is invoked at startup (audit run; output → Immediate window).
  - `IsDuplicateTeacher(names)` is called per-slot via `xl.Application.Run`.
  - Python fallback exists for the rare case the VBA call fails (e.g. macro
    project not loaded). The fallback mirrors the VBA logic line-for-line
    so behaviour is identical.
- **Safe-attach pattern**: reuses running Excel instance, never calls Quit
  on the user's session — see [[feedback_excel_dont_close_user_file]].
- **Bare macro name** for Thai filenames — see
  [[feedback_run_macro_thai_filename]].
- **Layout constants** identical to `analyze_teachers.py`:
  `DAY_BASES = mon:3, tue:9, wed:15, thu:21, fri:27`;
  `PERIOD_COLS = 1:3, 2:4, 3:5, 4:7, 5:8, 6:9`;
  subject_row = base + grade_idx × 2, teacher_row = subject_row + 1.
- **Merge-cell aware**: reads and writes via `MergeArea.Cells(1,1)` so
  merged subject/teacher cells round-trip correctly.
- **UTF-8 output file**: console is cp874 on Thai Windows; the script
  writes the human-readable report to `swap_subject_output.txt` and prints
  only the path to stdout.
