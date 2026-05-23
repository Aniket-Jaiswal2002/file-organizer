# File Organizer CLI

A command-line tool that automatically sorts files in any folder — by file type or by date. No more messy Downloads folders.

## Features

- Sort files into categories: Images, Videos, Documents, Code, Audio, Archives, and more
- Sort files by last-modified month (`YYYY-MM` folders)
- `--dry-run` flag to preview changes before moving anything
- Clean terminal output showing exactly what moved where

## Usage

```bash
# Sort by file type (default)
python organizer.py /path/to/your/folder

# Sort by date (last modified)
python organizer.py /path/to/your/folder --by date

# Preview without moving files
python organizer.py /path/to/your/folder --dry-run
```

### Example output

```
Target folder: /Users/you/Downloads
Mode: by type

Organizing 4 file(s):

  resume.pdf
    → Documents/

  vacation.jpg
    → Images/

  script.py
    → Code/

  archive.zip
    → Archives/

Done! Moved 4 file(s).
```

## Installation

```bash
# Clone the repo
git clone https://github.com/Aniket-Jaiswal2002/file-organizer.git
cd file-organizer

# Install dependencies
pip install -r requirements.txt
```

## Running tests

```bash
pytest tests/
```

## File type categories

| Category  | Extensions |
|-----------|-----------|
| Images    | jpg, jpeg, png, gif, bmp, svg, webp |
| Videos    | mp4, mov, avi, mkv, wmv, flv |
| Audio     | mp3, wav, aac, flac, ogg, m4a |
| Documents | pdf, doc, docx, txt, md, pptx, xlsx, csv |
| Code      | py, js, ts, html, css, java, cpp, json, yaml |
| Archives  | zip, tar, gz, rar, 7z |
| Others    | anything else |

## Tech stack

- Python 3.10+
- Standard library only (`os`, `shutil`, `pathlib`, `argparse`, `datetime`)
- `pytest` for testing
