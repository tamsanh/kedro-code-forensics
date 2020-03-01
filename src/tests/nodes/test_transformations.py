from kedro_code_forensics.io.cloc_file import ClocFile
from kedro_code_forensics.nodes.transformations import (
    GitRevision,
    HotSpotData,
    generate_git_revisions,
    generate_hot_spots,
)


class TestTransformations:
    def test_generate_git_revisions(self, basic_git_file_commits):
        actual = generate_git_revisions(basic_git_file_commits)
        expected = {
            "src/kedro_code_forensics/io/git_file_commit.py": GitRevision(
                filepath="src/kedro_code_forensics/io/git_file_commit.py",
                revisions=1,
                insertions=1,
                deletions=3,
            ),
            "src/kedro_code_forensics/run.py": GitRevision(
                filepath="src/kedro_code_forensics/run.py",
                revisions=3,
                insertions=87,
                deletions=8,
            ),
        }

        assert actual == expected

        actual = generate_git_revisions(basic_git_file_commits + basic_git_file_commits)
        expected = {
            "src/kedro_code_forensics/io/git_file_commit.py": GitRevision(
                filepath="src/kedro_code_forensics/io/git_file_commit.py",
                revisions=2,
                insertions=2,
                deletions=6,
            ),
            "src/kedro_code_forensics/run.py": GitRevision(
                filepath="src/kedro_code_forensics/run.py",
                revisions=6,
                insertions=174,
                deletions=16,
            ),
        }

        assert actual == expected

    def test_generate_hot_spot_data(self):
        simple_revisions = [("file1", 2, 2, 3), ("file2", 3, 4, 5), ("file3", 4, 8, 8)]
        git_revisions = {
            filepath: GitRevision(filepath, revisions, insertions, deletions)
            for filepath, revisions, insertions, deletions in simple_revisions
        }
        cloc_files = [
            ClocFile("file1", 2, 2, 3, "Python"),
            ClocFile("file2", 2, 2, 3, "Python"),
            ClocFile("file3", 2, 2, 3, "Python"),
        ]
        actual = generate_hot_spots(git_revisions, cloc_files)
        expected = [
            HotSpotData(filepath="file1", revisions=2, lines=3, rating=6),
            HotSpotData(filepath="file2", revisions=3, lines=3, rating=9),
            HotSpotData(filepath="file3", revisions=4, lines=3, rating=12),
        ]
        assert actual == expected
