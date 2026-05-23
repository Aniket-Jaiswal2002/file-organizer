import pytest
from pathlib import Path
from organizer import get_file_type, organize_by_type, organize_by_date


def test_get_file_type_image():
    assert get_file_type(".jpg") == "Images"
    assert get_file_type(".PNG") == "Images"


def test_get_file_type_document():
    assert get_file_type(".pdf") == "Documents"
    assert get_file_type(".docx") == "Documents"


def test_get_file_type_code():
    assert get_file_type(".py") == "Code"
    assert get_file_type(".js") == "Code"


def test_get_file_type_unknown():
    assert get_file_type(".xyz") == "Others"
    assert get_file_type("") == "Others"


def test_organize_by_type_dry_run(tmp_path):
    (tmp_path / "photo.jpg").write_text("fake image")
    (tmp_path / "notes.txt").write_text("some text")
    (tmp_path / "script.py").write_text("print('hello')")

    moves = organize_by_type(tmp_path, dry_run=True)

    assert len(moves) == 3
    categories = {m["category"] for m in moves}
    assert "Images" in categories
    assert "Documents" in categories
    assert "Code" in categories

    # dry run: no folders should have been created
    assert not (tmp_path / "Images").exists()
    assert not (tmp_path / "Documents").exists()


def test_organize_by_type_actually_moves(tmp_path):
    (tmp_path / "photo.jpg").write_text("fake image")
    (tmp_path / "notes.pdf").write_text("fake pdf")

    organize_by_type(tmp_path, dry_run=False)

    assert (tmp_path / "Images" / "photo.jpg").exists()
    assert (tmp_path / "Documents" / "notes.pdf").exists()
    assert not (tmp_path / "photo.jpg").exists()


def test_organize_by_date_dry_run(tmp_path):
    (tmp_path / "file.txt").write_text("hello")

    moves = organize_by_date(tmp_path, dry_run=True)

    assert len(moves) == 1
    assert not (tmp_path / moves[0]["category"]).exists()


def test_empty_folder(tmp_path):
    moves = organize_by_type(tmp_path, dry_run=True)
    assert moves == []
