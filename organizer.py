import os
import shutil
import argparse
from pathlib import Path
from datetime import datetime

FILE_TYPE_MAP = {
    "Images":     [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".svg", ".webp"],
    "Videos":     [".mp4", ".mov", ".avi", ".mkv", ".wmv", ".flv"],
    "Audio":      [".mp3", ".wav", ".aac", ".flac", ".ogg", ".m4a"],
    "Documents":  [".pdf", ".doc", ".docx", ".txt", ".md", ".pptx", ".xlsx", ".csv"],
    "Code":       [".py", ".js", ".ts", ".html", ".css", ".java", ".cpp", ".c", ".json", ".yaml", ".yml"],
    "Archives":   [".zip", ".tar", ".gz", ".rar", ".7z"],
    "Others":     [],
}


def get_file_type(extension: str) -> str:
    for category, extensions in FILE_TYPE_MAP.items():
        if extension.lower() in extensions:
            return category
    return "Others"


def get_date_folder(file_path: Path) -> str:
    modified_time = file_path.stat().st_mtime
    date = datetime.fromtimestamp(modified_time)
    return date.strftime("%Y-%m")


def organize_by_type(source_dir: Path, dry_run: bool = False) -> list[dict]:
    moves = []
    for file_path in source_dir.iterdir():
        if file_path.is_dir():
            continue
        category = get_file_type(file_path.suffix)
        destination = source_dir / category / file_path.name
        moves.append({"from": file_path, "to": destination, "category": category})

    if not dry_run:
        for move in moves:
            move["to"].parent.mkdir(parents=True, exist_ok=True)
            shutil.move(str(move["from"]), str(move["to"]))

    return moves


def organize_by_date(source_dir: Path, dry_run: bool = False) -> list[dict]:
    moves = []
    for file_path in source_dir.iterdir():
        if file_path.is_dir():
            continue
        month_folder = get_date_folder(file_path)
        destination = source_dir / month_folder / file_path.name
        moves.append({"from": file_path, "to": destination, "category": month_folder})

    if not dry_run:
        for move in moves:
            move["to"].parent.mkdir(parents=True, exist_ok=True)
            shutil.move(str(move["from"]), str(move["to"]))

    return moves


def print_results(moves: list[dict], dry_run: bool) -> None:
    if not moves:
        print("No files found to organize.")
        return

    label = "[DRY RUN] " if dry_run else ""
    print(f"\n{label}Organizing {len(moves)} file(s):\n")
    for move in moves:
        print(f"  {move['from'].name}")
        print(f"    → {move['category']}/\n")

    if dry_run:
        print("Dry run complete. No files were moved.")
    else:
        print(f"Done! Moved {len(moves)} file(s).")


def main():
    parser = argparse.ArgumentParser(
        description="Organize files in a folder by type or date.",
        formatter_class=argparse.RawTextHelpFormatter,
    )
    parser.add_argument(
        "folder",
        help="Path to the folder you want to organize",
    )
    parser.add_argument(
        "--by",
        choices=["type", "date"],
        default="type",
        help="How to organize files:\n  type  = sort into Images, Videos, Documents, etc. (default)\n  date  = sort into YYYY-MM folders by last modified date",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview what would happen without moving any files",
    )

    args = parser.parse_args()
    source_dir = Path(args.folder).resolve()

    if not source_dir.exists():
        print(f"Error: Folder '{source_dir}' does not exist.")
        return
    if not source_dir.is_dir():
        print(f"Error: '{source_dir}' is not a folder.")
        return

    print(f"Target folder: {source_dir}")
    print(f"Mode: {'by ' + args.by}")

    if args.by == "type":
        moves = organize_by_type(source_dir, dry_run=args.dry_run)
    else:
        moves = organize_by_date(source_dir, dry_run=args.dry_run)

    print_results(moves, dry_run=args.dry_run)


if __name__ == "__main__":
    main()
