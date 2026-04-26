import argparse
import shutil
import logging
from pathlib import Path
from datetime import datetime



FILE_TYPES = {
    "Images":    [".jpg", ".jpeg", ".png", ".gif", ".webp", ".svg", ".bmp", ".ico", ".tiff"],
    "Videos":    [".mp4", ".mov", ".avi", ".mkv", ".wmv", ".flv", ".webm"],
    "Documents": [".pdf", ".docx", ".doc", ".txt", ".md", ".xlsx", ".csv", ".pptx", ".odt"],
    "Audio":     [".mp3", ".wav", ".flac", ".aac", ".ogg", ".m4a"],
    "Code":      [".py", ".js", ".ts", ".html", ".css", ".json", ".xml", ".sh", ".c", ".cpp", ".java",'.py'],
    "Archives":  [".zip", ".tar", ".gz", ".rar", ".7z", ".bz2"],
    "Executables": [".exe", ".dmg", ".pkg", ".deb", ".AppImage"],
    "Other":     []
}


def setup_logging(folder:Path):

    log_file=folder/"organizer.log"

    logging.basicConfig(
        filename=log_file,
        level=logging.INFO,
        format="%(asctime)s-%(message)",
        datefmt="%Y-%m-%d %H:%M:%S"
    )


def get_category(extension: str) -> str:
    """
    Given the file extension, for instance '.jpg, return a category name like Image
    """

    for category, extensions in FILE_TYPES.items():

        if extension.lower() in extensions:

            return category
        return 'Other'
    


def handle_duplicate(destination: Path, filename:str) ->str:

    stem=Path(filename).stem
    suffix=Path(filename).suffix
    counter=1

    new_name=filename

    while (destination / new_name).exists():
        new_name=f'{stem}_{counter}{suffix}'

    return new_name


def organize(folder: Path, dry_run:bool=False) ->dict:
    """
    Scans the folder and moves each file intor its category
    """
    summary={} # counts how many file goes into each category
    undo_log=[] # will record moves so --undo can reverse them

    for file in folder.iterdir():
        
        # This is a logic that will skip subfolders since only files needs to be moved
        if file.is_dir():
            continue

        if file.name=="organizer_log":
            continue

        category=get_category(file.suffix)

        destination=folder / category

        if not dry_run:

            destination.mkdir(exist_ok=True)

            safe_name=handle_duplicate(destination, file.name)
            dest_file=destination/safe_name

            try:
                shutil.move(str(file), str(dest_file))

                logging.info(f'Moved: {file.name} -> {category}/{safe_name}')

                undo_log.append(f'{category}/{safe_name}|{file.name}')
            
            except PermissionError:

                print(f'Permission denied: {file.name} -skipping')
                continue

            except Exception as e:
                print(f'Error moving {file.name} -skipping')

                continue

            if safe_name != file.name:
                print(f"  Moved (renamed): {file.name} → {category}/{safe_name}")
            else:
                print(f"  Moved: {file.name} → {category}/")
        else:
            print(f' [DRY RUN] Would move:{file.name}-> {category}/')

        summary[category]= summary.get(category, 0)+1

    if not dry_run and undo_log:
        undo_file=folder/'.undo_log'

        with open(undo_file, "w") as f:
            f.write("\n".join(undo_log))

    return summary
 
def undo(folder: Path):
    """
    Reverses the last organize operation by reading the hidden .undo_log file.
 
    This solves extension challenge A from the project.
 
    The undo log format is:
        Category/filename|original_filename
    For example:
        Images/photo_1.jpg|photo.jpg
    """
    undo_file = folder / ".undo_log"
 
    if not undo_file.exists():
        print("No undo log found. Nothing to undo.")
        return
 
    print("Undoing last organize...\n")
    lines = undo_file.read_text().strip().split("\n")
 
    for line in lines:
        if "|" not in line:
            continue
 
        moved_path, original_name = line.split("|", 1)
        source = folder / moved_path        
        destination = folder / original_name 
 
        if source.exists():
            try:
                shutil.move(str(source), str(destination))
                print(f"  Restored: {moved_path} → {original_name}")
            except Exception as e:
                print(f"  Could not restore {moved_path}: {e}")
        else:
            print(f"  Not found (already moved?): {moved_path}")
 
    # Clean up empty category folders after undoing
    for category in FILE_TYPES.keys():
        cat_folder = folder / category
        if cat_folder.is_dir() and not any(cat_folder.iterdir()):
            cat_folder.rmdir()
            print(f"  Removed empty folder: {category}/")
 
    # Remove the undo log after restoring
    undo_file.unlink()
    print("\nUndo complete.")



def main():
    """
    Parse command-line arguments and call the right function.
    This is the "entry point" — the first function that runs.
    """
 
    # Create the argument parser with a helpful description
    parser = argparse.ArgumentParser(
        description="Organize files in a folder by type.",
        epilog="Example: python organizer.py ~/Downloads --dry-run"
    )
 
    # Positional argument — required, no flag needed
    # python organizer.py /path/to/folder
    parser.add_argument(
        "folder",
        help="Path to the folder you want to organize"
    )
 
    # Optional flag — --dry-run shows what WOULD happen without doing it
    # action="store_true" means: if the flag is present, set dry_run=True
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview changes without moving any files"
    )
 
    # Optional flag — --undo reverses the last run
    parser.add_argument(
        "--undo",
        action="store_true",
        help="Undo the last organize operation"
    )
 
    # Parse what the user actually typed in the terminal
    args = parser.parse_args()
 
    # Convert the string path to a Path object for easy manipulation
    folder = Path(args.folder)
 
    # Validate the folder exists
    if not folder.is_dir():
        print(f"Error: '{folder}' is not a valid directory.")
        print("Tip: make sure the path exists and you have permission to access it.")
        return
 
    # Set up the log file inside the target folder
    if not args.dry_run:
        setup_logging(folder)
 
    # ── UNDO MODE ──
    if args.undo:
        undo(folder)
        return
 
    # ── ORGANIZE MODE ──
    mode = "[DRY RUN] " if args.dry_run else ""
    print(f"\n{mode}Organizing: {folder.resolve()}\n")
 
    summary = organize(folder, dry_run=args.dry_run)
 
    # Print the summary report
    print("\n" + "─" * 40)
    print("Summary")
    print("─" * 40)
 
    if not summary:
        print("  No files found to organize.")
    else:
        for category, count in sorted(summary.items()):
            bar = "█" * count  # A tiny visual bar chart!
            print(f"  {category:<15} {count:>3} file(s)  {bar}")
 
    total = sum(summary.values())
    print("─" * 40)
    print(f"  Total: {total} file(s) processed.")
 
    if not args.dry_run and total > 0:
        print(f"\n  Log saved to: {folder / 'organizer.log'}")
        print(f"  To undo: python organizer.py {args.folder} --undo")
 
    print()
 
 
# ─────────────────────────────────────────────
# PYTHON ENTRY POINT GUARD
# This means: only run main() if this file is run directly.
# If someone imports this file as a module, main() won't run automatically.
# This is a Python best practice — always include it.
# ─────────────────────────────────────────────
 
if __name__ == "__main__":
    main()