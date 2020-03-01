import json
import subprocess
from pathlib import PurePath
from typing import Any, Dict, List, NamedTuple, Optional, Union

from kedro.io import AbstractVersionedDataSet, Version

from kedro_code_forensics.io.expections import ReadOnlyDataSet


class ClocFile(NamedTuple):
    filepath: str
    blank: int
    comment: int
    code: int
    language: str


def _parse_cloc_files(
    base_path: str, raw_cloc_data: Dict[str, Dict[str, Union[str, int]]]
):
    out_cloc_files = []

    if not base_path.endswith("/"):
        base_path += "/"

    # Drop the extra unneeded metadata
    if "header" in raw_cloc_data:
        del raw_cloc_data["header"]
    if "SUM" in raw_cloc_data:
        del raw_cloc_data["SUM"]

    for raw_file_path, file_data in raw_cloc_data.items():
        filepath = raw_file_path.replace(base_path, "")
        out_cloc_files.append(ClocFile(filepath, **file_data))

    return out_cloc_files


class ClocFileDataSet(AbstractVersionedDataSet):
    DEFAULT_EXCLUDED_DIRS = ["venv"]

    def __init__(
        self,
        filepath: PurePath,
        version: Optional[Version] = None,
        excluded_dirs: List[str] = None,
        ignore_comments: bool = False,
        *args,
        **kwargs
    ):
        super().__init__(filepath, version=version, *args, **kwargs)
        self._excluded_dirs = excluded_dirs or self.DEFAULT_EXCLUDED_DIRS
        self._ignore_comments = ignore_comments

    def _load(self) -> Any:
        excluded_dirs = []

        if len(self._excluded_dirs) > 0:
            excluded_dirs = ["--exclude-dir"] + self._excluded_dirs

        raw_json = subprocess.check_output(
            ["cloc", "--by-file", *excluded_dirs, "--json", self._filepath]
        )

        raw_cloc_data = json.loads(raw_json)

        return _parse_cloc_files(self._filepath, raw_cloc_data)

    def _save(self, data: Any) -> None:
        raise ReadOnlyDataSet()

    def _describe(self) -> Dict[str, Any]:
        return dict(
            filepath=self._filepath,
            excluded_dirs=self._excluded_dirs,
            ignore_comments=self._ignore_comments,
        )
