"""
Teacher workload analysis for โรงเรียนอนุบาลเมืองพนมไพร
Reads the schedule Excel (.xlsm) and outputs per-teacher subject breakdown.
Usage: python analyze_teachers.py [output_file]
"""
import os
import re
import sys
import win32com.client as win32
from collections import defaultdict

EXCEL_PATH = r"C:\Users\saich\Documents\excel-vba-schedule\ตารางเรียนเทอม1 ปี 69-1 - execution.xlsm"

SKIP = {
    'พักรับประทานอาหาร', 'พักรับประทานอาหารกลางวัน',
    'ส่งเสริมทักษะชีวิต(กีฬา/เกษตร)', 'เศรษฐกิจพอเพียง(ลงแปลงเกษตร)',
    'ลูกเสือ-เนตรนารี', 'สวดมนต์', 'ซ่อมเสริม (คำพื้นฐานไทย)',
    'ซ่อมเสริม(คำพื้นฐานไทย)', 'ชุมนุม', 'แนะแนว', 'เศรษฐกิจพอเพียง',
    'ลดเวลาเรียน', 'รูปประจำชั้น',
}

PERIODS = [(3,'09-10'), (4,'10-11'), (5,'11-12'), (7,'13-14'), (8,'14-15'), (9,'15-16')]

SHEETS_INFO = [
    (9,  ['ป.1','ป.2','ป.3'], 'ป.1-3'),
    (10, ['ป.4','ป.5','ป.6'], 'ป.4-6'),
    (12, ['ม.1','ม.2','ม.3'], 'ม.1-3'),
]

DAYS = ['จันทร์','อังคาร','พุธ','พฤหัสบดี','ศุกร์']
DAY_BASES = [3, 9, 15, 21, 27]


def merge_val(ws, r, c):
    cell = ws.Cells(r, c)
    if cell.MergeCells:
        ma = cell.MergeArea
        return ws.Cells(ma.Row, ma.Column).Value
    return cell.Value


def val(v):
    return str(v).strip() if v else ''


def normalize_subject(subj, tab_name):
    if tab_name == 'ม.1-3':
        return re.sub(r'\d+$', '', subj).strip()
    return subj


def analyze(wb):
    # teacher -> { 'ป.1-3': count, 'ป.4-6': count, 'ม.1-3': count }
    tab_counts = defaultdict(lambda: {'ป.1-3': 0, 'ป.4-6': 0, 'ม.1-3': 0})
    # teacher -> list of {tab, grade, day, period, subject}
    records = defaultdict(list)

    for ws_1based, grades, tab_name in SHEETS_INFO:
        ws = wb.Worksheets(ws_1based)
        for di, base in enumerate(DAY_BASES):
            day = DAYS[di]
            for gi, grade in enumerate(grades):
                sr = base + gi * 2
                tr = base + gi * 2 + 1
                for col, period in PERIODS:
                    subj = val(merge_val(ws, sr, col))
                    teacher = val(merge_val(ws, tr, col))
                    if not teacher.startswith('ครู'):
                        continue
                    if not subj or subj in SKIP:
                        continue
                    tab_counts[teacher][tab_name] += 1
                    records[teacher].append({
                        'tab': tab_name, 'grade': grade,
                        'day': day, 'period': period,
                        'subject': normalize_subject(subj, tab_name),
                    })

    return tab_counts, records


def format_output(tab_counts, records):
    lines = []

    # Summary table
    SEP = '=' * 90
    lines.append(SEP)
    lines.append('สรุปภาระงานครู — คาบสอนต่อสัปดาห์')
    lines.append(SEP)
    lines.append(f"{'ครู':<20} {'ป.1-3':>8} {'ป.4-6':>8} {'ม.1-3':>8} {'รวม':>8}")
    lines.append('-' * 55)

    all_teachers = sorted(tab_counts.keys(),
                          key=lambda t: -(tab_counts[t]['ป.1-3'] + tab_counts[t]['ป.4-6'] + tab_counts[t]['ม.1-3']))
    grand_total = 0
    for t in all_teachers:
        c = tab_counts[t]
        total = c['ป.1-3'] + c['ป.4-6'] + c['ม.1-3']
        grand_total += total
        lines.append(f"{t:<20} {c['ป.1-3']:>8} {c['ป.4-6']:>8} {c['ม.1-3']:>8} {total:>8}")

    lines.append('-' * 55)
    totals = {'ป.1-3': 0, 'ป.4-6': 0, 'ม.1-3': 0}
    for c in tab_counts.values():
        for k in totals:
            totals[k] += c[k]
    lines.append(f"{'รวมทั้งหมด':<20} {totals['ป.1-3']:>8} {totals['ป.4-6']:>8} {totals['ม.1-3']:>8} {grand_total:>8}")
    lines.append('')

    # Per-teacher detail
    for t in all_teachers:
        recs = records[t]
        lines.append(SEP)
        total = tab_counts[t]['ป.1-3'] + tab_counts[t]['ป.4-6'] + tab_counts[t]['ม.1-3']
        lines.append(f"{t}  (รวม {total} คาบ/สัปดาห์)")
        lines.append('-' * 60)

        # Subject → {grade: count}
        subj_grade = defaultdict(lambda: defaultdict(int))
        for r in recs:
            subj_grade[r['subject']][r['grade']] += 1

        grade_order = ['ป.1','ป.2','ป.3','ป.4','ป.5','ป.6','ม.1','ม.2','ม.3']
        subj_totals = {s: sum(gc.values()) for s, gc in subj_grade.items()}

        for subj, cnt in sorted(subj_totals.items(), key=lambda x: -x[1]):
            lines.append(f"  • {subj}  ({cnt} คาบ)")
            gc = subj_grade[subj]
            for g in grade_order:
                if g in gc:
                    lines.append(f"      {g:<6} {gc[g]} คาบ")
        lines.append('')

    return '\n'.join(lines)


def main():
    out_path = sys.argv[1] if len(sys.argv) > 1 else 'teacher_analysis_output.txt'

    # Try to attach to an already-running Excel; only start a new one if none exists.
    started_excel = False
    try:
        excel = win32.GetActiveObject('Excel.Application')
    except Exception:
        excel = win32.Dispatch('Excel.Application')
        started_excel = True

    excel.DisplayAlerts = False

    # Reuse the workbook if the user already has it open; otherwise open it ourselves.
    target = os.path.normcase(os.path.abspath(EXCEL_PATH))
    opened_wb = None
    wb = None
    for w in excel.Workbooks:
        if os.path.normcase(os.path.abspath(w.FullName)) == target:
            wb = w
            break
    if wb is None:
        opened_wb = excel.Workbooks.Open(EXCEL_PATH, ReadOnly=True)
        wb = opened_wb

    try:
        tab_counts, records = analyze(wb)
        output = format_output(tab_counts, records)
    finally:
        # Only close what we opened; never Quit Excel if user had it running.
        if opened_wb is not None:
            opened_wb.Close(False)
        if started_excel:
            excel.Quit()

    with open(out_path, 'w', encoding='utf-8') as f:
        f.write(output)

    print(f"Written to: {out_path}")


if __name__ == '__main__':
    main()
