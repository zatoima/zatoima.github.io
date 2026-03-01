---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "Shell Script to Bulk Delete Notes from PowerPoint for Mac"
subtitle: ""
summary: " "
tags: ["Mac"]
categories: ["Mac"]
url: mac-pptx-delete-note
date: 2024-04-26
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

PowerPoint presentation files (*.pptx) allow you to add notes to each slide. However, PowerPoint for Mac does not have a built-in feature to bulk delete these notes. This article automates note deletion using a shell script.

## Shell Script Explanation

This shell script (`delete_note.sh`) performs the following operations:

1. Creates a temporary directory and stores its path in the `TMP_DIR` variable.

2. For each pptx file in the current directory, it performs the following:

   1. Copies the `.pptx` file to the temporary directory.
   2. Extracts the `.pptx` file in the temporary directory.
   3. For each `.xml` file in the `./ppt/notesSlides/` directory, clears the content of `<a:t>` tags.
   4. Re-archives the extracted files into a `.pptx` file.
   5. Copies the generated `.pptx` file back to the original directory.

3. Deletes the temporary directory.

## Shell Script

```shell
#!/bin/bash

set -eu

TMP_DIR="$(mktemp -d)"
trap 'rm -rf $TMP_DIR' EXIT

for PPTX_FILE in *.pptx; do
    if [ -e "$PPTX_FILE" ]; then
        echo "Processing $PPTX_FILE..."

        cp "$PPTX_FILE" "$TMP_DIR"
        pushd "$TMP_DIR"

        unzip "$PPTX_FILE"
        rm "$PPTX_FILE"
        find "./ppt/notesSlides/"*.xml | xargs -I{} sed -i '' -e 's/<a:t>[^<]*<\/a:t>/<a:t><\/a:t>/g' "{}"
        zip -0 -r "$PPTX_FILE" ./* # do not compress (-0)

        popd

        cp "$TMP_DIR/$PPTX_FILE" "$PPTX_FILE"
    fi
done

```

## Background: PPTX File Structure

A PPTX file is actually a collection of XML files. Specifically, it has the following structure:

- `_rels/`: Directory containing XML files that define relationships.
- `docProps/`: Directory containing XML files that define document properties.
- `pptx` Directory containing XML files that make up the presentation body.
  - `slides/`: Directory containing XML files with information for each slide.
  - `slideMasters/`: Directory containing XML files with slide master information.
  - `notesMasters/`: Directory containing XML files with notes master information.
  - `notesSlides/`: Directory containing XML files with notes information for each slide.
  - `theme/`: Directory containing XML files with theme information.
- `_rels/`: Directory containing XML files that define relationships.
- `[Content_Types].xml`: XML file that defines content types.

These XML files are compressed into a PPTX file. In other words, to edit a PPTX file, you need to extract it, modify the XML files, and re-compress it. Not knowing this structure can leave you stuck when managing PowerPoint for Mac.
