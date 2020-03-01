import csv
import subprocess
from datetime import datetime
from pathlib import PurePath
from typing import Any, Dict, List, NamedTuple, Optional, TextIO

import dateutil
from kedro.io import AbstractVersionedDataSet, DataSetError, Version

from kedro_code_forensics.io.expections import ReadOnlyDataSet


class Committer(NamedTuple):
    name: str
    email: str


class GitFileCommit(NamedTuple):
    hash: str
    date: datetime
    committer: Committer
    message: str
    filepath: str
    insertions: int
    deletions: int


def _count_lines(file_pointer: TextIO):
    return sum([1 for _ in file_pointer.readline()])


def _parse_git_log_output(raw_output: str) -> List[GitFileCommit]:
    """
    Parses a raw git log into individual commits for files

    Args:
        raw_output: The raw log output of a git log formatted with
            --format='commit:%H,%ci,%an,%ae,%s'

    Returns:
        A list of GitFileCommits that can be used for analysis.
    """
    out_commits = []

    current_commit = None

    parseable_lines = raw_output.strip().split("\n")

    def _parse_change(change: str):
        if change == "-":
            return 0
        return int(change)

    for line in parseable_lines:

        if line.strip() == "":
            continue

        if line.strip().startswith("commit:"):
            header = ["hash", "date", "author", "email", "message"]
            line = line[7:]
            reader = csv.reader([line])
            current_commit = dict(zip(header, next(reader)))
            current_commit["date"] = dateutil.parser.parse(current_commit["date"])

            current_commit["committer"] = Committer(
                current_commit["author"], current_commit["email"]
            )
            del current_commit["author"]
            del current_commit["email"]
            continue

        split_lines = line.split("\t")
        try:
            current_commit["insertions"] = _parse_change(split_lines[0])
            current_commit["deletions"] = _parse_change(split_lines[1])
            current_commit["filepath"] = split_lines[2]
        except (ValueError, IndexError):
            raise Exception(f'Can not parse line: "{line}"')

        out_commits.append(GitFileCommit(**current_commit))
    return out_commits


class GitFileCommitDataSet(AbstractVersionedDataSet):
    def __init__(
        self,
        filepath: PurePath,
        version: Optional[Version] = None,
        before: Optional[str] = None,
        after: Optional[str] = None,
        *args,
        **kwargs,
    ):
        super().__init__(filepath, version, *args, **kwargs)
        self._before = before
        self._after = after

    def _describe(self) -> Dict[str, Any]:
        return dict(filepath=self._filepath, before=self._before, after=self._after)

    def _save(self, data: Any) -> None:
        raise ReadOnlyDataSet()

    def _load(self) -> List[GitFileCommit]:
        try:
            git_command = [
                "git",
                "-C",
                self._filepath,
                "log",
                '--pretty=format:commit:%H,%cI,"%an",%ae,"%s"',
                "--numstat",  # Large stat width to capture entire file path
            ]

            if type(self._before) is datetime.date:
                git_command.append(f"--before={self._before}")
            if type(self._after) is datetime.date:
                git_command.append(f"--after={self._after}")

            raw_git_output = subprocess.check_output(git_command).decode("UTF8")
        except subprocess.CalledProcessError as e:
            raise DataSetError(e)

        return _parse_git_log_output(raw_git_output)
