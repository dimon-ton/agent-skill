---
name: phontan-schedule-reader
description: Extract and analyze school schedules from Phontan (โรงเรียนบ้านโพนแท่น) Excel files. Use this skill whenever the user wants to read, search, or analyze the school schedule — find a teacher's classes, list classes by day/time, extract student schedules, or get structured schedule data. Works with Elementary (ป.1-3), Junior High (ม.1-3), and Primary (ป.4-6) grades for any semester/year.
compatibility: Requires openpyxl library (Python)
---

## Overview

This skill reads Phontan school schedule Excel files and extracts structured schedule data. It handles multiple grade levels and tabs, automatically detects the sheet structure, and provides clean output in both tabular and JSON formats.

## What You Can Do

- **Find a teacher's schedule**: "Show me ครูปาณิสรา's classes"
- **List all classes by day**: "What classes are there on Monday?"
- **Extract specific grade schedule**: "Give me the ป.4 schedule"
- **Search for subjects**: "Find all Science classes"
- **Get full structured data**: "Extract all schedule data as JSON"

## How to Use

### Step 1: Provide the File

The skill expects an Excel file at the default location:
```
C:\Users\saich\Downloads\ตารางเรียนเทอม2 ปี 68-2 .xlsm
```

If your file is in a different location, provide the full path.

### Step 2: Specify What You Want

State your request clearly:
- Teacher name: `ครูปาณิสรา`, `ครูดวงใจ`, etc.
- Grade level: `ป.4`, `ม.1`, `ป.6`, etc.
- Day of week: `จันทร์`, `อังคาร`, `พุธ`, etc.
- Subject: `ภาษาไทย`, `คณิตศาสตร์`, etc.
- Time slot: `09.00-10.00`, `13.00-14.00`, etc.

### Step 3: Choose Output Format

- **Table** (default): Clean, formatted table easy to read
- **JSON**: Structured data for processing
- **Summary**: Key stats and patterns

## Example Requests

| Request | What it does |
|---------|-------------|
| `Find ครูปาณิสรา's schedule` | Shows all classes taught by this teacher, organized by day |
| `List Monday classes for ป.4` | Shows all ป.4 classes on Monday with subjects and teachers |
| `Extract all ป.1-3 schedule` | Returns complete elementary schedule as structured data |
| `Show classes on Wednesday 13.00-14.00` | Lists all classes in that time slot across all grades |
| `Find all Science classes` | Shows all วิทยาศาสตร์ classes across the week |

## Supported Sheets

The skill automatically detects and works with **ANY sheet in the Excel file**. It includes 20 tabs covering:

**Elementary & Junior High Schedules:**
- ป1.-3 เทอม2 ปี2566
- ม.1-3
- ม.1-3เทอม2ปี2566
- ม.1-3 เทอม 1 ปี 2565
- ตารางเรียนม.1-3 เทอม 2

**Primary Schedules:**
- ป. 4-6 เทอม2 ปี2566
- ป.4-6
- ป1-3เทอม2 ปี62

**Other Sheets:**
- ตารางสอบ ม-3 (Exam Schedule)
- รายคน (By Person)
- รายคน เทอม 2ปี2566 (By Person - Semester 2)
- สอนแทน ม.ต้น (Substitute Teachers)
- และอื่นๆ

Just mention the sheet name, grade level, or what you're looking for and the skill will find the right sheet!

## Output Formats

### Table Format (Default)
Clean, easy-to-read table showing:
- Day
- Grade
- Time Slot
- Subject
- Teacher Name

### JSON Format
Structured data with nested hierarchy:
```json
{
  "sheet": "ป. 4-6 เทอม2 ปี2566",
  "schedules": [
    {
      "day": "จันทร์",
      "grade": "ป.4",
      "classes": [
        {
          "time": "09.00-10.00",
          "subject": "ภาษาไทย",
          "teacher": "ครูกฤตชยากร"
        }
      ]
    }
  ]
}
```

### Summary Format
Key statistics:
- Total classes per teacher
- Busiest days/times
- Subject distribution
- Grade-level breakdown

## How It Works

1. Opens the Excel file using openpyxl
2. Detects the requested sheet (or uses default if not specified)
3. Parses the table structure (handles merged cells, multiple rows per time slot)
4. Extracts subjects and teacher names
5. Organizes by day/time/grade as requested
6. Outputs in your chosen format

## Reading While the User Has the File Open

openpyxl reads the **on-disk copy** of the file — it does not touch the running
Excel process and will never close the user's window. The trade-off: any unsaved
edits the user is making in Excel right now are invisible to openpyxl until they
press Ctrl+S. If the user reports stale data, ask them to save first.

If the skill ever needs to **write** to the file, do NOT use openpyxl for an
`.xlsm` containing macros, images, or shapes — openpyxl silently drops drawings
and VBA on save. Switch to win32com using the safe-attach pattern from the
`excel-vba` skill, which writes through the user's already-open workbook and
leaves their window intact.

## Handling Abnormal Tables

The skill is designed to handle:
- **Merged cells**: Subject and teacher on same or adjacent rows
- **Multiple rows per slot**: Subject in one row, teacher name in the next
- **Sparse data**: Empty cells and irregular layouts
- **Thai text**: Full support for Thai characters

## Tips

- **Teacher names**: Use Thai spelling (e.g., `ครูปาณิสรา`, not `khru panisara`)
- **Grade codes**: Use official codes (`ป.4`, `ม.1`, not `grade 4`)
- **Days**: Use Thai day names or numbers (Monday = `จันทร์` or `1`)
- **Time format**: Use `HH.MM-HH.MM` format (e.g., `09.00-10.00`)

If you're not sure of exact spelling or format, describe it and the skill will search and find it.
