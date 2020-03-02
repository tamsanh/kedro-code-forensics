from typing import Dict, List, NamedTuple

import pandas as pd

from kedro_code_forensics.io.cloc_file import ClocFile
from kedro_code_forensics.io.git_file_commit import GitFileCommit


class GitRevisionAggregate(NamedTuple):
    """
    An aggregate of the revision data for a file.
        filepath: The path to the file in question
        revisions: The count of the number of commits to this file
        insertions: The sum of the insertions for this file over all commits
        deletions: The sum of the deletions for this file over all commits
    """

    filepath: str
    revisions: int
    insertions: int
    deletions: int


def generate_git_revision_aggregates(
    git_file_commits: List[GitFileCommit],
) -> Dict[str, GitRevisionAggregate]:
    """
    Aggregates per-file commit data, returning the sum of
    all insertions, deletions, and count of number of commits
    (revisions) that this particular file has gone through,
    returning the data in the form of a dictionary with
    the filepath as key and the GitRevisionAggregate as a value
    :param git_file_commits: List[GitFileCommit]
    :return: Dict[filepath, GitRevisionAggregate]
    """
    df = pd.DataFrame(git_file_commits)
    df["revisions"] = 1
    raw_revisions = (
        df[["filepath", "revisions", "insertions", "deletions"]]
        .groupby("filepath")
        .sum()
    )
    revisions = {}
    for filepath, raw_revision in raw_revisions.iterrows():
        revisions[filepath] = GitRevisionAggregate(
            filepath,
            raw_revision["revisions"],
            raw_revision["insertions"],
            raw_revision["deletions"],
        )
    return revisions


class HotSpotData(NamedTuple):
    """
    A tuple containing the calculations used to identify hotspots.
        filepath: THe filepath in question for the hotpsot analysis
        revisions: The number of revisions to a file
        lines: The number of lines for a file that acts as a proxy for complexity
        rating: The lines multiplied by the complexity
    """

    filepath: str
    revisions: int
    lines: int
    # The less revisions and the less complex, the better
    # The higher this number is, the worst it gets
    rating: int


def generate_hot_spots(
    git_revisions: Dict[str, GitRevisionAggregate], cloc_files: List[ClocFile]
) -> List[HotSpotData]:
    """
    Generates hotspot data by taking the revision aggregates and cloc_files,
    aggregating on the filepath, and applying simple calculations on to them to
    generate a simple rating for a hotspot

    :param git_revisions: Dict[str, GitRevisionAggregate] keyed by filepath
    :param cloc_files: List[ClocFile]
    :return: List[HotSpotData[
    """
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
