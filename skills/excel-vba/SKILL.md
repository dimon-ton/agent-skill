---
name: excel-vba
description: Read, edit, add, delete, and run VBA macro code inside Excel .xlsm files using win32com (pywin32). Trigger when user wants to read VBA code, edit or rewrite a VBA module, add a new macro, delete VBA code, or run an existing macro in an Excel file. Also trigger on phrases like "read VBA", "edit macro", "run macro", "add VBA code", "modify VBA", "write VBA to excel", "excel macro python", "win32com VBA".
---

# excel-vba: Read, Edit & Run Excel VBA via win32com

## When to Use

Use this skill when the user wants to:
- **Read** VBA source code from an Excel module
- **Edit / rewrite** an existing VBA module
- **Add** new VBA code or a new module to a workbook
- **Delete** VBA modules or lines
- **Run** an existing macro from Python
- **Export / import** VBA modules to/from `.bas` files

> Windows only — requires Microsoft Excel installed and pywin32.

## Prerequisites

```bash
pip install pywin32
```

Also required — enable programmatic VBA access in Excel:
- Excel → File → Options → Trust Center → Trust Center Settings
- → Macro Settings → check **"Trust access to the VBA project object model"**

Or set via registry (once, run as admin):
```python
import winreg
key = winreg.OpenKey(winreg.HKEY_CURRENT_USER,
    r"Software\Microsoft\Office\16.0\Excel\Security", 0, winreg.KEY_SET_VALUE)
winreg.SetValueEx(key, "AccessVBOM", 0, winreg.REG_DWORD, 1)
winreg.CloseKey(key)
```

## Object Model Overview

```
Excel.Application
└── Workbooks(n)  ← wb
    └── VBProject
        └── VBComponents  ← collection of all modules
            └── VBComponent  ← one module (e.g. "Module1")
                └── CodeModule  ← the actual VBA source code
```

### VBComponent Type Constants
| Value | Type |
|-------|------|
| 1 | Standard module (Sub/Function) |
| 2 | Class module |
| 3 | UserForm |
| 100 | Sheet / ThisWorkbook (document module) |

## Core Boilerplate — Open & Close Excel

**CRITICAL: Never close the user's already-open workbook or quit their Excel.**

If the user has the file open in the foreground (the common case), the script must
attach to their running Excel and reuse their workbook handle. Calling `Quit()` or
`Close()` on the user's session shuts down ALL Excel instances, loses unsaved work,
and is exactly what the user reported as broken. Use the safe attach pattern:

```python
import os
import win32com.client

def open_excel_safe(filepath):
    """Attach to running Excel + workbook if possible; only start what's needed.

    Returns: (xl, wb, started_xl, opened_wb)
        started_xl: True if WE started Excel (so WE may Quit at the end)
        opened_wb:  the workbook object WE opened (so WE may Close at the end);
                    None means the workbook was already open by the user — do NOT close it
    """
    started_xl = False
    try:
        xl = win32com.client.GetActiveObject("Excel.Application")
    except Exception:
        xl = win32com.client.Dispatch("Excel.Application")
        started_xl = True
    xl.DisplayAlerts = False

    target = os.path.normcase(os.path.abspath(filepath))
    wb = None
    for w in xl.Workbooks:
        if os.path.normcase(os.path.abspath(w.FullName)) == target:
            wb = w  # user's instance — DO NOT close at the end
            break

    opened_wb = None
    if wb is None:
        opened_wb = xl.Workbooks.Open(os.path.abspath(filepath))
        wb = opened_wb

    return xl, wb, started_xl, opened_wb


def close_excel_safe(xl, wb, started_xl, opened_wb, save=True):
    """Save edits via wb.Save() (always safe). Only close/quit what WE created."""
    if save:
        wb.Save()  # safe on either user's or our workbook — refreshes their window
    if opened_wb is not None:
        opened_wb.Close(SaveChanges=False)  # we already saved above if needed
    if started_xl:
        xl.Quit()
```

**Real-time visibility benefit:** when the script edits cells on the user's open
workbook, every `Cells(r,c).Value = ...` is visible in their window immediately —
no refresh, no reopen. `wb.Save()` just persists to disk; the window stays open.

**Legacy pattern — only use when no user session exists** (headless automation,
unit tests, batch jobs). Calling `Quit()` here is fine because no one is watching:

```python
def open_excel_headless(filepath):
    xl = win32com.client.Dispatch("Excel.Application")
    xl.Visible = False
    xl.DisplayAlerts = False
    wb = xl.Workbooks.Open(os.path.abspath(filepath))
    return xl, wb

def close_excel_headless(xl, wb, save=True):
    if save:
        wb.Save()
    wb.Close(SaveChanges=save)
    xl.Quit()
```

## 1. Read VBA Module Code

```python
def read_vba_module(wb, module_name):
    """Return source code of a named VBA module as a string."""
    cm = wb.VBProject.VBComponents(module_name).CodeModule
    count = cm.CountOfLines
    if count == 0:
        return ""
    return cm.Lines(1, count)

# Usage
xl, wb, started_xl, opened_wb = open_excel_safe("file.xlsm")
code = read_vba_module(wb, "Module1")
print(code)
close_excel_safe(xl, wb, started_xl, opened_wb, save=False)
```

## 2. List All Modules

```python
def list_modules(wb):
    """Print all VBA component names and types."""
    type_names = {1: "Module", 2: "Class", 3: "UserForm", 100: "Document"}
    for comp in wb.VBProject.VBComponents:
        t = type_names.get(comp.Type, f"Unknown({comp.Type})")
        cm = comp.CodeModule
        lines = cm.CountOfLines
        print(f"  {comp.Name:30s}  [{t}]  {lines} lines")

xl, wb, started_xl, opened_wb = open_excel_safe("file.xlsm")
list_modules(wb)
close_excel_safe(xl, wb, started_xl, opened_wb, save=False)
```

## 3. Edit (Overwrite) a Module

```python
def write_vba_module(wb, module_name, new_code):
    """Replace entire content of an existing module with new_code.
    
    IMPORTANT: strips Attribute lines — they are .bas file metadata,
    not valid VBA code body. AddFromString rejects them with Syntax error.
    """
    # Strip Attribute header lines (Attribute VB_Name = "..." etc.)
    lines = new_code.splitlines()
    clean_code = '\n'.join(ln for ln in lines if not ln.startswith('Attribute'))

    cm = wb.VBProject.VBComponents(module_name).CodeModule
    count = cm.CountOfLines
    if count > 0:
        cm.DeleteLines(1, count)   # MUST clear first — AddFromString appends, not replaces
    cm.AddFromString(clean_code)

# Usage
new_code = """
Sub HelloWorld()
    Debug.Print "Hello from Python"   ' never use MsgBox in automated macros
End Sub
"""
xl, wb, started_xl, opened_wb = open_excel_safe("file.xlsm")
write_vba_module(wb, "Module1", new_code.strip())
close_excel_safe(xl, wb, started_xl, opened_wb, save=True)
```

## 4. Add a New Module

```python
def add_vba_module(wb, module_name, code):
    """Create a new standard module and insert code."""
    comp = wb.VBProject.VBComponents.Add(1)  # 1 = standard module
    comp.Name = module_name
    comp.CodeModule.AddFromString(code.strip())

# Usage
xl, wb, started_xl, opened_wb = open_excel_safe("file.xlsm")
add_vba_module(wb, "MyNewModule", """
Sub Greet()
    MsgBox "New module added by Python"
End Sub
""")
close_excel_safe(xl, wb, started_xl, opened_wb, save=True)
```

## 5. Delete a Module

```python
def delete_vba_module(wb, module_name):
    """Remove a module entirely. Document modules (type 100) cannot be deleted."""
    comp = wb.VBProject.VBComponents(module_name)
    if comp.Type == 100:
        raise ValueError(f"Cannot delete document module: {module_name}")
    wb.VBProject.VBComponents.Remove(comp)

xl, wb, started_xl, opened_wb = open_excel_safe("file.xlsm")
delete_vba_module(wb, "OldModule")
close_excel_safe(xl, wb, started_xl, opened_wb, save=True)
```

## 6. Insert / Delete Specific Lines

```python
def insert_lines(wb, module_name, at_line, lines):
    """Insert lines at a specific position (1-based).
    
    CRITICAL: InsertLines takes ONE logical VBA line per call.
    Do NOT pass a multi-line string — embedded newlines cause syntax errors.
    """
    cm = wb.VBProject.VBComponents(module_name).CodeModule
    for i, line in enumerate(lines):
        cm.InsertLines(at_line + i, line)   # one call per line

def delete_lines(wb, module_name, start_line, count):
    """Delete `count` lines starting at `start_line` (1-based)."""
    cm = wb.VBProject.VBComponents(module_name).CodeModule
    cm.DeleteLines(start_line, count)
```

## 7. Run an Existing Macro

**Thai / non-ASCII filename warning:** `xl.Application.Run("Filename.xlsm!Module.Macro")`
fails when the workbook filename contains Thai characters — COM marshaling corrupts the
filename portion. Use the bare macro name only; Excel resolves it against the active workbook:

```python
ws.Activate()
xl.Application.Run("MacroName")          # correct for Thai filenames
# xl.Application.Run(f"{wb.Name}!Module.Macro")  # DO NOT use — corrupts Thai name
```

**โรงเรียนอนุบาลเมืองพนมไพร project rule:** After editing any teacher cell in the schedule,
always run `ChangeCellColor` on all 3 schedule sheets (indexes 9, 10, 12) to keep
teacher-group colors in sync:

```python
for sheet_idx in [9, 10, 12]:
    ws = wb.Worksheets(sheet_idx)
    ws.Activate()
    xl.Application.Run("ChangeCellColor")
wb.Save()
```

```python
def run_macro(xl, wb, macro_name):
    """Run a macro by name. Format: 'MacroName' or 'Module1.MacroName'.
    
    Return values: use sentinel cell pattern — never MsgBox.
    DisplayAlerts=False does NOT suppress MsgBox; it only suppresses
    Excel system dialogs (save/overwrite prompts).
    
    If workbook filename has non-ASCII chars (Thai etc.), use bare macro name only —
    do NOT include the workbook name prefix (see note above).
    """
    wb_name = wb.Name
    xl.Application.Run(f"{wb_name}!{macro_name}")

def run_macro_with_result(xl, wb, macro_name, result_sheet_name, result_row=1, result_col=700):
    """Run a macro and read back its result from a sentinel cell.
    
    VBA side must write:  ThisWorkbook.Worksheets("ScratchSheet").Cells(1, 700).Value = result
    """
    # Clear sentinel before run
    ws = wb.Worksheets(result_sheet_name)
    ws.Cells(result_row, result_col).Value = None

    xl.Application.Run(f"{wb.Name}!{macro_name}")

    result = ws.Cells(result_row, result_col).Value
    ws.Cells(result_row, result_col).Value = None  # clean up
    return result

# Usage
xl, wb, started_xl, opened_wb = open_excel_safe("file.xlsm")
run_macro(xl, wb, "Module1.HelloWorld")
close_excel_safe(xl, wb, started_xl, opened_wb, save=True)
```

## 8. Export / Import Module Files

```python
def export_module(wb, module_name, output_path):
    """Export a VBA module to a .bas file."""
    comp = wb.VBProject.VBComponents(module_name)
    comp.Export(os.path.abspath(output_path))

def import_module(wb, bas_file_path):
    """Import a .bas file as a new module."""
    wb.VBProject.VBComponents.Import(os.path.abspath(bas_file_path))

# Usage
xl, wb, started_xl, opened_wb = open_excel_safe("file.xlsm")
export_module(wb, "Module1", "Module1.bas")
import_module(wb, "NewModule.bas")
close_excel_safe(xl, wb, started_xl, opened_wb, save=True)
```

## 9. Attach to an Already-Running Excel Instance

`open_excel_safe()` above is the canonical way to do this — it handles both the
no-Excel-running and Excel-already-running cases, and tracks ownership so you
never accidentally close the user's session.

Quick minimal form (when you only want the attach logic, not the full helper):

```python
import os
import win32com.client

try:
    xl = win32com.client.GetActiveObject('Excel.Application')
except Exception:
    xl = win32com.client.Dispatch('Excel.Application')

target = os.path.normcase(os.path.abspath(r'C:\path\to\MyFile.xlsm'))
wb = next((w for w in xl.Workbooks
           if os.path.normcase(os.path.abspath(w.FullName)) == target), None)
if wb is None:
    wb = xl.Workbooks.Open(target)
```

Why iterate `xl.Workbooks` instead of `xl.Workbooks("MyFile.xlsm")` by name?
The string lookup matches the **display name** only and is case-sensitive in some
Excel versions; full-path normalization is the only reliable identity check.

## 10. Isolated Test Subprocess Pattern

When running multiple VBA tests in separate subprocesses, Excel lingers in the process list for 1–3 seconds after `xl.Quit()`. The next test's `Workbooks.Open` collides with the dying instance.

```python
import subprocess, time

def wait_for_excel_exit(timeout=8):
    """Poll until EXCEL.EXE is gone from the process list."""
    deadline = time.time() + timeout
    while time.time() < deadline:
        r = subprocess.run(
            ['tasklist', '/FI', 'IMAGENAME eq EXCEL.EXE'],
            capture_output=True, text=True
        )
        if 'EXCEL.EXE' not in r.stdout:
            return True
        time.sleep(0.5)
    return False  # timed out

def run_test_subprocess(script_path, timeout=35):
    """Run a test script in isolation; capture output without COM pipe hang."""
    # subprocess.run(capture_output=True) HANGS — COM keeps stdout pipe open
    # Use Popen + communicate instead:
    proc = subprocess.Popen(
        ['python', script_path],
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
    )
    try:
        out, err = proc.communicate(timeout=timeout)
    except subprocess.TimeoutExpired:
        proc.kill()
        subprocess.run(['taskkill', '/F', '/IM', 'EXCEL.EXE'], capture_output=True)
        out, err = proc.communicate()
    wait_for_excel_exit()   # always wait before next test
    return out, err
```

## Full Example — Read, Edit, Run (preserves user's open file)

```python
import os
import win32com.client

filepath = r"C:\Users\saich\Downloads\MyFile.xlsm"

# Attach to user's Excel + workbook if open; only spin up our own if not.
started_xl = False
try:
    xl = win32com.client.GetActiveObject("Excel.Application")
except Exception:
    xl = win32com.client.Dispatch("Excel.Application")
    started_xl = True
xl.DisplayAlerts = False

target = os.path.normcase(os.path.abspath(filepath))
opened_wb = None
wb = next((w for w in xl.Workbooks
           if os.path.normcase(os.path.abspath(w.FullName)) == target), None)
if wb is None:
    opened_wb = xl.Workbooks.Open(target)
    wb = opened_wb

try:
    # 1. Read existing code
    cm = wb.VBProject.VBComponents("Module1").CodeModule
    print(cm.Lines(1, cm.CountOfLines))

    # 2. Overwrite with new code — visible immediately in user's VBA editor
    new_code = 'Sub Hello()\n    Debug.Print "Edited by Python"\nEnd Sub'
    cm.DeleteLines(1, cm.CountOfLines)
    cm.AddFromString(new_code)

    # 3. Save (persists to disk; user's window stays open) and run
    wb.Save()
    xl.Application.Run(f"{wb.Name}!Module1.Hello")
finally:
    # Only clean up what WE created — never touch the user's session.
    if opened_wb is not None:
        opened_wb.Close(SaveChanges=False)
    if started_xl:
        xl.Quit()
```

## Decision Guide

| Task | Method |
|------|--------|
| Read module source | `CodeModule.Lines(1, CountOfLines)` |
| List all modules | iterate `VBProject.VBComponents` |
| Overwrite module | `DeleteLines` + `AddFromString` |
| Add new module | `VBComponents.Add(1)` + `AddFromString` |
| Delete a module | `VBComponents.Remove(comp)` |
| Insert at specific line | `CodeModule.InsertLines(line, code)` |
| Run a macro | `Application.Run("workbook!Module.Sub")` |
| Export to .bas file | `comp.Export(path)` |
| Import from .bas file | `VBComponents.Import(path)` |

## Graphics / Images Safety Rule

**Never let openpyxl, pandas, or xlwings save a `.xlsm` file that contains images or shapes.**
These libraries silently drop all drawings when re-saving — this is a documented limitation ("best try, no guarantee").

| Tool | Read xlsm | Edit VBA | Save xlsm safely with graphics |
|------|-----------|----------|---------------------------------|
| **win32com** | ✅ | ✅ full | ✅ yes — use this |
| openpyxl | ✅ | ❌ | ⚠️ drops images/shapes |
| pandas ExcelWriter | ✅ | ❌ | ⚠️ drops images/shapes |
| xlwings | ✅ | run only | ⚠️ partial |

**Checklist before saving a graphics-containing xlsm:**
1. Only use `wb.Save()` (not `wb.SaveAs`) — `SaveAs` can change format and drop drawings
2. Strip `Attribute` lines before `AddFromString` — a broken VBA state triggers Excel "repair" on reopen, which strips drawings
3. Always `DeleteLines(1, n)` before `AddFromString` — partially-written modules cause the same repair
4. Call `wb.Save()` immediately after VBProject edits — don't leave the workbook open in a dirty VBA state
5. Add `Application.ScreenUpdating = True` in a `Cleanup:` label in every VBA Sub — a stuck `False` makes shapes invisible on screen even though they exist in the file

```vba
Sub SafeMacro()
    On Error GoTo Cleanup
    Application.ScreenUpdating = False
    ' ... your code ...
Cleanup:
    Application.ScreenUpdating = True   ' always restores, even on error
End Sub
```

## Common Errors & Fixes

| Symptom | Cause | Fix |
|---------|-------|-----|
| `-2147352567` / permission denied | VBA project access not enabled | Enable "Trust access to VBA project object model" in Trust Center |
| `AttributeError: VBProject` | File not open as xlsm with macros | Open with `Workbooks.Open()`, not openpyxl |
| `KeyError: Module1` | Module name doesn't exist | Use `list_modules()` first to check names |
| `win32com.client.pywintypes.com_error` | Excel not installed or COM not registered | Must have full Excel install, not just viewer |
| `Cannot delete document module` | Trying to delete Sheet/ThisWorkbook (type 100) | Clear code instead: `DeleteLines(1, CountOfLines)` |
| **Compile error: Syntax error** on `Attribute VB_Name` line | `.bas` header passed to `AddFromString` | Strip lines starting with `Attribute` before `AddFromString` |
| **Compile error** calling `Module.Function` from another module | Function declared `Private` | Change to `Public Function` |
| Script hangs forever after `Application.Run` | `MsgBox` in macro — not suppressed by `DisplayAlerts` | Remove `MsgBox`; use sentinel cell (see §7) |
| `subprocess.run` timeout never fires | COM pipe stays open while Excel is alive | Use `Popen` + `communicate(timeout=N)` (see §10) |
| `Workbooks.Open` returns `None` or wrong instance | Previous Excel process still exiting | Poll for EXCEL.EXE to disappear (see §10) |
| Module doubled, duplicate Sub declarations | `AddFromString` on non-empty module | `DeleteLines(1, CountOfLines)` before `AddFromString` |
| Graphics / images gone after script runs | openpyxl / pandas saved the xlsm | Use win32com exclusively; see Graphics Safety Rule |
| Shapes invisible, file size unchanged | `ScreenUpdating = False` left on after crash | Close + reopen file; add `Cleanup:` label to every VBA Sub |
| Graphics stripped on file reopen | VBProject edit left module in bad state → repair | Follow the 5-point checklist above |
| User's Excel window closes mid-session | Script called `xl.Quit()` or `wb.Close()` on the user's workbook | Use `open_excel_safe` / `close_excel_safe` — only Quit/Close what the script itself opened |
| Edits don't appear in user's open window | Script opened a second copy of the file via `Workbooks.Open` instead of attaching | Iterate `xl.Workbooks` and match by normalized `FullName` before opening |

## Important Notes

- Always use **absolute paths** with `os.path.abspath()` — relative paths fail silently
- `xl.DisplayAlerts = False` suppresses **Excel system dialogs only** — it does NOT suppress `MsgBox`
- Document modules (Sheet1, ThisWorkbook) **cannot be removed** — only their code can be cleared
- `AddFromString` **appends** to existing content — always `DeleteLines(1, n)` first to replace
- Reference sheets by **name** not index: `wb.Worksheets("SheetName")` not `wb.Worksheets(3)` — index changes if sheets are reordered
- `win32com.client.gencache.EnsureDispatch` generates early-binding — faster but requires gen_py cache; `Dispatch` is safer for scripts
- Functions called from another module or from Python-injected test code must be `Public`, not `Private`
