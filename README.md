# File Organizer CLI

A command-line tool written in Python that automatically sorts files in any folder into subfolders by type — images, videos, documents, code, and more.

Built as part of my CS self-study journey. 

---

## Features

- Sorts 35+ file types into 8 smart categories
- `--dry-run` flag to safely preview changes before moving anything
- `--undo` flag to instantly reverse the last operation
- Duplicate file handling — never overwrites existing files
- Automatic log file with timestamps saved to `organizer.log`
- Zero dependencies — uses Python standard library only

---

## Demo

```bash
$ python organizer.py ~/Downloads --dry-run

[DRY RUN] Organizing: /home/user/Downloads

  [DRY RUN] Would move: photo.jpg        → Images/
  [DRY RUN] Would move: report.pdf       → Documents/
  [DRY RUN] Would move: song.mp3         → Audio/
  [DRY RUN] Would move: project.zip      → Archives/
  [DRY RUN] Would move: script.py        → Code/

────────────────────────────────────────
Summary
────────────────────────────────────────
  Archives          1 file(s)  █
  Audio             1 file(s)  █
  Code              1 file(s)  █
  Documents         1 file(s)  █
  Images            1 file(s)  █
────────────────────────────────────────
  Total: 5 file(s) processed.
```

---

## Installation

No installation required. Just clone and run.

```bash
git clone https://github.com/loickemajou/file-organizer.git
cd file-organizer
```

Requires Python 3.6+

---

## Usage

```bash
# Organize a folder (moves files for real)
python organizer.py /path/to/folder

# Preview changes without moving anything
python organizer.py /path/to/folder --dry-run

# Undo the last organize operation
python organizer.py /path/to/folder --undo

# See all options
python organizer.py --help
```

---

## File categories

| Category | Extensions |
|---|---|
| Images | .jpg .jpeg .png .gif .webp .svg .bmp .ico .tiff |
| Videos | .mp4 .mov .avi .mkv .wmv .flv .webm |
| Documents | .pdf .docx .doc .txt .md .xlsx .csv .pptx |
| Audio | .mp3 .wav .flac .aac .ogg .m4a |
| Code | .py .js .ts .html .css .json .xml .sh .c .cpp .java |
| Archives | .zip .tar .gz .rar .7z .bz2 |
| Executables | .exe .dmg .pkg .deb |
| Other | Anything not matched above |

---


---

## Project structure

```
file-organizer/
├── organizer.py      # Main script — all logic lives here
├── README.md         # You are here
└── .gitignore        # Excludes logs, cache, undo files
```

---



