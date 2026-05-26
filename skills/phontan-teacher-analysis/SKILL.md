---
name: phontan-teacher-analysis
description: >
  Analyzes teacher workload for โรงเรียนอนุบาลเมืองพนมไพร from the schedule Excel file.
  Use this skill whenever the user asks about teacher workload, how many periods each teacher teaches,
  which subjects each teacher teaches, or anything related to teacher schedule analysis.
  Trigger phrases: "analyze teacher", "teacher workload", "วิเคราะห์ครู", "ภาระงานครู",
  "วิชาที่ครูสอน", "ครูสอนกี่คาบ", "show teacher analysis", "how many periods".
  Always run this skill proactively when the user says "analyze again" in context of teachers/schedule.
---

# Teacher Workload Analysis — โรงเรียนอนุบาลเมืองพนมไพร

## What this skill does

Reads the school schedule from the Excel file and produces:
1. A summary table: each teacher × schedule group (ป.1-3, ป.4-6, ม.1-3) × total periods/week
2. Per-teacher detail: subjects taught, broken down by grade and period count

## Excel file details

- Path: `C:\Users\saich\Documents\excel-vba-schedule\ตารางเรียนเทอม1 ปี 69-1 - execution.xlsm`
- Sheet 9 (1-based): ป.1-3 — grades ป.1, ป.2, ป.3
- Sheet 10 (1-based): ป.4-6 — grades ป.4, ป.5, ป.6
- Sheet 12 (1-based): ม.1-3 — grades ม.1, ม.2, ม.3

## Running the analysis

Use the bundled script at `scripts/analyze_teachers.py`:

```powershell
$outFile = "C:\Users\saich\Documents\excel-vba-schedule\teacher_analysis_output.txt"
python "C:\Users\saich\.claude\skills\phontan-teacher-analysis\scripts\analyze_teachers.py" $outFile
```

Then read the output file and display it to the user:

```
Read $outFile and show the full contents
```

## After editing teacher cells — always run ChangeCellColor

**Any time a teacher name is changed in a schedule cell** (on any of the 3 schedule sheets),
run `ChangeCellColor` on all 3 sheets so teacher-group coloring stays in sync.
The macro reads RGB values from the `colorTeacher` sheet and recolors every teacher cell.

```python
for sheet_idx in [9, 10, 12]:
    ws = wb.Worksheets(sheet_idx)
    ws.Activate()          # ChangeCellColor runs on ActiveSheet
    xl.Application.Run("ChangeCellColor")   # bare name — Thai filename, no workbook prefix
wb.Save()
```

Run this immediately after `wb.Save()` for the cell edits, before opening Excel for the user.

## After analysis — always open Excel

After every analysis run, open the Excel file so the user can review it:

```powershell
Start-Process "C:\Users\saich\Documents\excel-vba-schedule\ตารางเรียนเทอม1 ปี 69-1 - execution.xlsm"
```

## Output format

**Summary table** (sorted by total periods descending):
```
ครู                  ป.1-3    ป.4-6    ม.1-3     รวม
-------------------------------------------------------
ครูXXX                   8        6        4      18
...
รวมทั้งหมด               XX       XX       XX     XXX
```

**Per-teacher detail** (subject → grade breakdown):
```
ครูXXX  (รวม 18 คาบ/สัปดาห์)
  • คณิตศาสตร์  (10 คาบ)
      ป.4    4 คาบ
      ป.5    3 คาบ
      ป.6    3 คาบ
  • วิทยาศาสตร์  (5 คาบ)
      ป.4    2 คาบ
      ป.5    3 คาบ
```

Note: subject names from ม.1-3 are stripped of trailing digits (ภาษาไทย2 → ภาษาไทย)
so same subject across ม.1/ม.2/ม.3 rolls up under one entry.

## Key implementation notes

- Uses `win32com` with safe-attach: reuses the user's running Excel instance and open workbook if present; never calls `Quit()` or `Close()` on the user's session
- `merge_val()` handles merged cells by reading from the top-left cell of the merge area
- Only names starting with `ครู` are counted as teachers; activity entries are excluded
- The SKIP set excludes shared activity blocks (lunch, scouts, prayers, etc.)
- Period columns: 3=09-10, 4=10-11, 5=11-12, 7=13-14, 8=14-15, 9=15-16 (col 6 = lunch, skipped)
- Day base rows: จันทร์=3, อังคาร=9, พุธ=15, พฤหัสบดี=21, ศุกร์=27
- For each day+grade: subject row = base + grade_index*2, teacher row = base + grade_index*2 + 1

## Troubleshooting

- **Thai text garbled in terminal**: The script writes UTF-8 to a file; always use the Read tool to display it, not terminal output
- **Wrong sheet**: Confirm via VBA constants `SHEET_IDX_P1_3=9`, `SHEET_IDX_P4_6=10`, `SHEET_IDX_M1_3=12`
- **Excel already open**: The script attaches to the running Excel instance and reuses the user's workbook if open — no second copy, no closing the user's window
