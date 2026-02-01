# Installation Guide

## Windows
1. Download `mondrian-grid-generator.zip` from Releases
2. Extract the ZIP file
3. Copy `mondriangrid.inx` and `mondriangrid.py` to:

%APPDATA%\inkscape\extensions\
text

4. Restart Inkscape
5. Find it under: **Extensions → Render → Mondrian Grid Generator**

## Linux
```bash
# Download and extract
unzip mondrian-grid-generator.zip

# Copy to extensions directory
cp extension/mondriangrid.* ~/.config/inkscape/extensions/

# Restart Inkscape

macOS

    Download and extract the ZIP

    Copy files to:
    text

    ~/Library/Application Support/inkscape/extensions/

    Restart Inkscape

Verification

After installation, restart Inkscape and verify:

    Menu appears: Extensions → Render → Mondrian Grid Generator

    Dialog opens with all parameters

    Click "Apply" to generate a test composition

Troubleshooting

If the extension doesn't appear:

    Check file permissions

    Ensure files are directly in the extensions folder (not in subfolders)

    Check Inkscape's extension error log:

        Windows: %APPDATA%\inkscape\extension-errors.log

        Linux: ~/.config/inkscape/extension-errors.log

        macOS: ~/Library/Application Support/inkscape/extension-errors.log