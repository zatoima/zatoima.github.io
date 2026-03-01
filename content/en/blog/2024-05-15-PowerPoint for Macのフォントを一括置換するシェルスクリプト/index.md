---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "Shell Script to Bulk Replace Fonts in PowerPoint for Mac"
subtitle: ""
summary: " "
tags: ["Mac"]
categories: ["Mac"]
url: Mac-pptx-font-replace
date: 2024-05-15
featured: false
draft: false

# Featured image
# To use, add an image named `featured.jpg/png` to your pages folder.
# Focal points: Smart, Center, TopLeft, Top, TopRight, Left, Right, BottomLeft, Bottom, BottomRight.
image:
  caption: ""
  focal_point: ""
  preview_only: fals
---

## Introduction

Font replacement in PowerPoint for Mac via the GUI often doesn't work reliably. Here are two methods for bulk font replacement. Fonts inside tables may not change, but most other text should be replaced.

## Font Replacement via Shell Script

The first method uses a shell script to replace fonts. The script performs the following operations:

1. Creates a temporary directory and copies the .pptx file there
2. Extracts the .pptx file
3. Deletes note text
4. Replaces font information in the slide XML files
5. Re-archives the modified files into a .pptx file
6. Copies the modified .pptx file back to the original location

Using this script, you can bulk replace fonts in all .pptx files in the current directory.

```sh
#!/bin/bash

set -eu

TMP_DIR="$(mktemp -d)"
echo "Created temporary directory: $TMP_DIR"
trap 'rm -rf $TMP_DIR' EXIT

for PPTX_FILE in *.pptx; do
    if [ -e "$PPTX_FILE" ]; then
        echo "Processing $PPTX_FILE..."

        cp "$PPTX_FILE" "$TMP_DIR"
        echo "Copied $PPTX_FILE to temporary directory."

        pushd "$TMP_DIR"
        echo "Changed directory to temporary directory."

        unzip "$PPTX_FILE"
        echo "Unzipped $PPTX_FILE."

        rm "$PPTX_FILE"
        echo "Removed original $PPTX_FILE from temporary directory."

        # Font replacement
        find "./ppt/slides/"*.xml | xargs -I{} sed -i '' -e 's/typeface="[^"]*"/typeface="M PLUS 1p"/g' "{}"
        echo "Replaced typeface attributes with 'M PLUS 1p' in slide XML files."

        zip -0 -r "$PPTX_FILE" ./* # do not compress (-0)
        echo "Zipped modified files into $PPTX_FILE."

        popd
        echo "Returned to original directory."

        cp "$TMP_DIR/$PPTX_FILE" "$PPTX_FILE"
        echo "Copied modified $PPTX_FILE back to original location."
    else
        echo "File not found: $PPTX_FILE"
    fi
done

echo "Script execution completed."

```

## Font Replacement via Python Script

The second method uses a Python script with the `python-pptx` library to replace fonts. The script performs the following operations:

1. Searches for .pptx files in the current directory
2. Gets and displays the fonts used in each .pptx file
3. Replaces all text fonts with the new font specified by the user
4. Saves the modified .pptx file

When using the Python script, you need to install the `python-pptx` library.

```python
import os
from pptx import Presentation

def get_used_fonts(ppt_file):
    prs = Presentation(ppt_file)
    used_fonts = set()

    for slide in prs.slides:
        for shape in slide.shapes:
            if shape.has_text_frame:
                for paragraph in shape.text_frame.paragraphs:
                    for run in paragraph.runs:
                        used_fonts.add(run.font.name)

            if shape.has_table:
                for row in shape.table.rows:
                    for cell in row.cells:
                        for paragraph in cell.text_frame.paragraphs:
                            for run in paragraph.runs:
                                used_fonts.add(run.font.name)

    return used_fonts

def replace_fonts(ppt_file, new_font):
    prs = Presentation(ppt_file)

    for slide in prs.slides:
        for shape in slide.shapes:
            if shape.has_text_frame:
                for paragraph in shape.text_frame.paragraphs:
                    for run in paragraph.runs:
                        run.font.name = new_font

            if shape.has_table:
                table = shape.table

                for row in table.rows:
                    for cell in row.cells:
                        for paragraph in cell.text_frame.paragraphs:
                            for run in paragraph.runs:
                                run.font.name = new_font

    prs.save(ppt_file)

def main():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    ppt_files = [f for f in os.listdir(current_dir) if f.endswith('.pptx')]

    if not ppt_files:
        print("No PowerPoint files found in the current directory.")
        return

    print("Found PowerPoint files:")
    for ppt_file in ppt_files:
        print(ppt_file)

        used_fonts = get_used_fonts(os.path.join(current_dir, ppt_file))
        print(f"Fonts used in {ppt_file}:")
        for font in used_fonts:
            print(f"- {font}")
        print()

    new_font = input("Enter the font name to replace all fonts with (default: 'M PLUS 1p'): ")
    if not new_font:
        new_font = 'M PLUS 1p'

    print(f"\nReplacing all fonts with '{new_font}' in all PowerPoint files...")
    for ppt_file in ppt_files:
        replace_fonts(os.path.join(current_dir, ppt_file), new_font)

    print("\nFont replacement completed.")

if __name__ == '__main__':
    main()

```

## How to Run the Scripts

### Running the Shell Script

1. Place the script file (`replacefontppt.sh`) in the current directory

2. Open a terminal and navigate to the current directory

3. Run the script with the following command:

   ```sh
   ./replacefontppt.sh
   ```

### Running the Python Script

Install the library:

```sh
pip install python-pptx
```

1. Place the script file (`replacefontppt.py`) in the current directory

2. Open a terminal and navigate to the current directory

3. Run the script with the following command:

   ```python
   python replacefontppt.py
   ```
