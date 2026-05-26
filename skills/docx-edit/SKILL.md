---
name: docx-edit
description: Edit existing .docx files while preserving original formatting using python-docx and docxedit libraries. Trigger when user wants to edit, find-replace, modify tables, or fill data in Word documents — especially SAR templates, reports, or any existing .docx that must keep its formatting. Also trigger on phrases like "edit docx", "edit word file", "fill SAR", "replace in docx", "docx table", "python-docx".
---

# docx-edit: Edit .docx Files While Preserving Formatting

## When to Use

Use this skill when the user wants to:
- Edit an existing .docx file without losing formatting
- Find and replace text in a .docx
- Fill data into table cells
- Modify existing Word documents (SAR, reports, forms, etc.)
- Do NOT use for creating new documents from scratch

## Prerequisites

```bash
pip install python-docx docxedit
```

- `python-docx` — core library for reading/writing .docx
- `docxedit` — wrapper that preserves original formatting when editing

## Core API Reference

### 1. Replace text (preserves formatting)

```python
from docx import Document
import docxedit

doc = Document("input.docx")

# Replace all occurrences
docxedit.replace_string(doc, old_string="old text", new_string="new text")

# Replace up to a specific paragraph number
docxedit.replace_string_up_to_paragraph(
    doc, old_string="old", new_string="new", paragraph_number=10
)

doc.save("output.docx")
```

### 2. Table operations

```python
# Add text to a table cell
docxedit.add_text_in_table(
    doc.tables[0], row_num=1, column_num=1, new_string="Hello"
)

# Change font size of entire table
docxedit.change_table_font_size(doc.tables[0], font_size=12)
```

### 3. Remove content

```python
# Remove lines containing specific text (+ N lines after)
docxedit.remove_lines(doc, first_line="REMOVE ME", number_of_lines=5)

# Remove a specific paragraph
docxedit.remove_paragraph(doc.paragraphs[0])
```

### 4. Search / debug

```python
# Show line number where text is found
docxedit.show_line(doc, current_text="search term")
```

## Advanced: Direct XML Manipulation

When `docxedit` is not enough (e.g., editing headers, footers, complex table merges), use direct XML manipulation. A .docx is a ZIP containing XML files.

```python
import zipfile
import shutil
import os
import re

def edit_docx_xml(input_path, output_path, replacements):
    """
    Edit docx by directly modifying the XML.
    replacements: dict of {old_text: new_text}
    Preserves ALL formatting perfectly.
    """
    temp_dir = "temp_docx_edit"
    
    with zipfile.ZipFile(input_path, "r") as z:
        z.extractall(temp_dir)
    
    xml_files = [
        "word/document.xml",
        "word/header1.xml",
        "word/header2.xml",
        "word/footer1.xml",
        "word/footer2.xml",
    ]
    
    for xml_file in xml_files:
        full_path = os.path.join(temp_dir, xml_file)
        if not os.path.exists(full_path):
            continue
        
        with open(full_path, "r", encoding="utf-8") as f:
            content = f.read()
        
        for old, new in replacements.items():
            content = content.replace(old, new)
        
        with open(full_path, "w", encoding="utf-8") as f:
            f.write(content)
    
    shutil.make_archive(output_path.replace(".docx", ""), "zip", temp_dir)
    shutil.rmtree(temp_dir)
    
    zip_path = output_path.replace(".docx", ".zip")
    if os.path.exists(output_path):
        os.remove(output_path)
    os.rename(zip_path, output_path)
```

**IMPORTANT XML caveat:** In Word XML, text is split across `<w:t>` tags by runs. A single word like "Hello" might appear as:
```xml
<w:t>Hel</w:t><w:t>lo</w:t>
```
For reliable replacements, use regex that handles split tags:

```python
import re

def replace_in_xml(content, old, new):
    pattern = re.escape(old)
    return re.sub(pattern, new, content)
```

## Advanced: python-docx Table Iteration

When you need to read/modify specific table cells:

```python
from docx import Document

doc = Document("input.docx")

for table in doc.tables:
    for row_idx, row in enumerate(table.rows):
        for col_idx, cell in enumerate(row.cells):
            text = cell.text
            if "target" in text:
                for paragraph in cell.paragraphs:
                    for run in paragraph.runs:
                        if "target" in run.text:
                            run.text = run.text.replace("target", "replacement")

doc.save("output.docx")
```

## SAR-Specific Patterns

### Fill PLC data into a table

```python
doc = Document("SAR_template.docx")

plc_data = [
    {"date": "27/06/2568", "topic": "นักเรียนไม่ส่งการบ้าน", "hours": "1"},
    {"date": "17/07/2568", "topic": "นักเรียนอ่านไม่ออก", "hours": "1"},
]

table = doc.tables[5]  # find the PLC table
for i, row_data in enumerate(plc_data):
    row = table.rows[i + 1]  # skip header
    row.cells[0].text = row_data["date"]
    row.cells[1].text = row_data["topic"]
    row.cells[2].text = row_data["hours"]

doc.save("SAR_output.docx")
```

### Replace Thai text in SAR

```python
import docxedit

doc = Document("SAR_template.docx")

docxedit.replace_string(doc, old_string="ชื่อ นางสาวXXX", new_string="ชื่อ นางสาวจรรยาภรณ์")
docxedit.replace_string(doc, old_string="นามสกุล YYY", new_string="นามสกุล ภูกลาง")

doc.save("SAR_output.docx")
```

## Decision Guide

| Task | Method |
|------|--------|
| Simple text find/replace | `docxedit.replace_string()` |
| Replace only in early paragraphs | `docxedit.replace_string_up_to_paragraph()` |
| Fill table cell | `docxedit.add_text_in_table()` |
| Change table font size | `docxedit.change_table_font_size()` |
| Read table data | `python-docx` table iteration |
| Remove paragraph/line | `docxedit.remove_lines()` or `docxedit.remove_paragraph()` |
| Edit header/footer text | Direct XML manipulation |
| Complex formatting preservation | Direct XML manipulation |
| Create new document from scratch | `python-docx` only (no docxedit needed) |

## Common Pitfalls

1. **Formatting loss**: `python-docx` paragraph.text assignment strips formatting. Always use `docxedit.replace_string()` or iterate `run.text` instead.
2. **Split runs**: Word splits text into multiple runs arbitrarily. `docxedit` handles this internally.
3. **Thai encoding**: Always use `encoding="utf-8"` when doing XML manipulation.
4. **Table cell merging**: Merged cells share the same content. Writing to one merged cell overwrites all.
5. **File locking**: Make sure the .docx is not open in Word before running the script.

## Enable Debug Logging

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```
