from __future__ import annotations

from pathlib import Path
from typing import Union

def check_file_exist(create: bool = True, _file: Union[str, Path] = None) -> bool:
    """Check if a file exists.

    If create = True, create file/dirs if not exist.
    """
    if not _file:
        raise ValueError("Missing a file name/path")

    if not isinstance(_file, Path):
        _file = Path(_file)

    if not _file.exists():
        if create:
            if not _file.parent.exists():
                try:
                    _file.parent.mkdir(exist_ok=True, parents=True)
                except Exception as exc:
                    _except: Exception = Exception(
                        f"Unhandled exception creating directory: {_file}. Details: {exc}"
                    )

                    print(_except)

                    return False

            try:
                with open(_file, "a") as f:
                    f.close()

                return True

            except Exception as exc:
                _except: Exception = Exception(
                    f"Unhandled exception creating file: {_file}. Details: {exc}"
                )

                print(_except)

                return False

    return True
