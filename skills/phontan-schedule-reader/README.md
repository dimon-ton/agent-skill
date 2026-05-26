# Phontan Schedule Reader Skill

A Claude Code skill for reading and analyzing Phontan school schedule Excel files.

## Overview

The **phontan-schedule-reader** skill extracts and analyzes school schedules from the Phontan (โรงเรียนบ้านโพนแท่น) Excel file. It works with all 20 sheets in the workbook and supports:

- **Finding teacher schedules** - See all classes taught by a specific teacher
- **Listing schedule by day** - View all classes on a specific day
- **Filtering by grade** - Get schedules for specific grade levels
- **Searching by subject** - Find all classes for a particular subject
- **Extracting full schedules** - Get structured data in table or JSON format

## Supported Sheets

Works with all actual sheets in the Excel file:

**Elementary:**
- ป1.-3 เทอม2 ปี2566

**Junior High (ม.1-3):**
- ม.1-3
- ม.1-3เทอม2ปี2566
- ม.1-3 เทอม 1 ปี 2565

**Primary (ป.4-6):**
- ป. 4-6 เทอม2 ปี2566
- ป.4-6

And many more supporting sheets (exam schedules, by-person views, substitutes, etc.)

## Files

- **SKILL.md** - Skill documentation and usage guide
- **scripts/extract_schedule.py** - Python script that handles Excel parsing
- **evals/evals.json** - Test cases for skill evaluation

## Usage

The skill is triggered when users ask to:
- Find or search for a teacher's schedule
- List classes by day, grade, or subject
- Extract or analyze schedule data
- Get information from the Phontan school schedule

## Example Prompts

```
"Find ครูปาณิสรา's schedule"
"Show all Monday classes for ป.4"
"Extract the ม.1-3 schedule"
"List all Science classes"
"Show me all sheets in the schedule file"
```

## Technical Details

- **Language:** Python 3
- **Dependencies:** openpyxl (Excel reading)
- **Thai Support:** Full support for Thai characters
- **Parsing:** Handles complex table structures with merged cells and multi-row entries

## How It Works

1. Opens the Phontan Excel file
2. Auto-detects or accepts sheet name specification
3. Parses table structure (days, grades, subjects, teachers)
4. Applies filters (by teacher, grade, day, subject)
5. Outputs in table or JSON format

## Notes

- The skill uses fuzzy matching for teacher and sheet names
- It automatically skips non-schedule sheets (metadata, lookups, etc.)
- All output supports Thai text without encoding issues
- Works with any semester/year in the Excel file
