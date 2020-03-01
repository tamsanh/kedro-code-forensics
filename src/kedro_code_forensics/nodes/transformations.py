from typing import Dict, List, NamedTuple

import pandas as pd

from kedro_code_forensics.io.cloc_file import ClocFile
from kedro_code_forensics.io.git_file_commit import Committer, GitFileCommit


class GitRevision(NamedTuple):
    filepath: str
    revisions: int
    insertions: int
    deletions: int


def generate_git_revisions(
    git_file_commits: List[GitFileCommit],
) -> Dict[str, GitRevision]:
    df = pd.DataFrame(git_file_commits)
    df["revisions"] = 1
    raw_revisions = (
        df[["filepath", "revisions", "insertions", "deletions"]]
        .groupby("filepath")
        .sum()
    )
    revisions = {}
    for filepath, raw_revision in raw_revisions.iterrows():
        revisions[filepath] = GitRevision(
            filepath,
            raw_revision["revisions"],
            raw_revision["insertions"],
            raw_revision["deletions"],
        )
    return revisions


class HotSpotData(NamedTuple):
    filepath: str
    revisions: int
    lines: int
    # The less revisions and the less complex, the better
    # The higher this number is, the worst it gets
    rating: int


def generate_hot_spots(
    git_revisions: Dict[str, GitRevision], cloc_files: List[ClocFile]
) -> List[HotSpotData]:
    hot_spot_data: List[HotSpotData] = []

    for cloc_file in cloc_files:
        git_revision = git_revisions.get(cloc_file.filepath)
        if git_revision is None:
            continue
        hot_spot_data.append(
            HotSpotData(
                cloc_file.filepath,
                git_revision.revisions,
                cloc_file.code,
                rating=cloc_file.code * git_revision.revisions,
            )
        )

    return hot_spot_data


class FileKnowledge(NamedTuple):
    filepath: str
    lines: int
    committer: Committer
    committed_lines: int
