import shutil
from pathlib import Path

import pytest

from scripts import build_docs


def test_find_soffice_falls_back_to_windows_default(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    windows_default = Path(r"C:\Program Files\LibreOffice\program\soffice.exe")
    monkeypatch.delenv("SOFFICE", raising=False)
    monkeypatch.setattr(shutil, "which", lambda name: None)
    monkeypatch.setattr(Path, "is_file", lambda self: self == windows_default)

    assert build_docs.find_soffice() == str(windows_default)


def test_find_soffice_raises_when_not_found(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("SOFFICE", raising=False)
    monkeypatch.setattr(shutil, "which", lambda name: None)
    monkeypatch.setattr(Path, "is_file", lambda self: False)

    with pytest.raises(build_docs.BuildError, match="LibreOffice not found"):
        build_docs.find_soffice()
