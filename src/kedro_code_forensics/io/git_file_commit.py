import csv
import subprocess
from datetime import datetime
from typing import Any, Dict, List, NamedTuple, TextIO

import dateutil
from kedro.io import AbstractVersionedDataSet, DataSetError


class GitFileCommit(NamedTuple):
    hash: str
    date: datetime
    author: str
    email: str
    message: str
    filepath: str
    change_count: str


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

    for line in parseable_lines:

        if line.strip() == "":
            continue

        if line.startswith("commit:"):
            header = ["hash", "date", "author", "email", "message"]
            line = line[7:]
            reader = csv.reader([line])
            current_commit = dict(zip(header, next(reader)))
            current_commit["date"] = dateutil.parser.parse(current_commit["date"])
            continue

        if all([x in line for x in ["changed", "insertion", "deletion"]]):
            # Ignore stat summary line
            continue

        # Grab the change count
        split_line = line.strip().split("|")
        last_segment = split_line[-1]
        change_count, _ = last_segment.strip().split(" ")
        current_commit["change_count"] = int(change_count)

        # Grab the file path
        filepath = "|".join(split_line[:-1])
        current_commit["filepath"] = filepath.strip()

        out_commits.append(GitFileCommit(**current_commit))
    return out_commits


class GitFileCommitDataSet(AbstractVersionedDataSet):
    def _describe(self) -> Dict[str, Any]:
        return dict(
            filepath=self._filepath,
        )

    def _save(self, data: Any) -> None:
        raise DataSetError("This is a read-only dataset.")

    def _load(self) -> List[GitFileCommit]:
        try:
            raw_git_output = subprocess.check_output(
                [
                    "git",
                    "-C",
                    self._filepath,
                    "log",
                    '--format=\'commit:%H,%cI,"%an",%ae,"%s"\'',
                    "--stat=9999999",  # Large stat width to capture entire file path
                ]
            )
        except subprocess.CalledProcessError as e:
            raise DataSetError(e)

        return _parse_git_log_output(raw_git_output)
