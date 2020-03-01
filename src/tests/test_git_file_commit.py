from datetime import datetime

from dateutil.tz import tzoffset


class TestGitLogDataSet:
    def test_parse_git_log_output(self):

        raw_output = """\
commit:bbdf70341bf44365b8fb0c83689ebe030ce76e5b,2020-02-19T07:39:20+01:00,Stanislas Michalak,stanislas-m@users.noreply.github.com,"Enable CI tests for PRs (#1907)"

 .github/workflows/tests.yml | 2 +-
 1 file changed, 1 insertion(+), 1 deletion(-)
commit:35808378f71edd89accde12c4e75d8ed8b37e91d,2020-02-06T13:40:21-05:00,Mark Bates,mark@markbates.com,"v0.15.5 (#1897)"

 Makefile                                                                  |    1 +
 runtime/version.go                                                        |    2 +-
 34 files changed, 2350 insertions(+), 1786 deletions(-)
"""  # noqa: 501

        from kedro_code_forensics.io.git_file_commit import (
            _parse_git_log_output,
            GitFileCommit,
        )

        actual = _parse_git_log_output(raw_output)
        expected = [
            GitFileCommit(
                "bbdf70341bf44365b8fb0c83689ebe030ce76e5b",
                datetime(2020, 2, 19, 7, 39, 20, 0, tzinfo=tzoffset(None, 3600)),
                "Stanislas Michalak",
                "stanislas-m@users.noreply.github.com",
                "Enable CI tests for PRs (#1907)",
                ".github/workflows/tests.yml",
                2,
            ),
            GitFileCommit(
                "35808378f71edd89accde12c4e75d8ed8b37e91d",
                datetime(2020, 2, 6, 13, 40, 21, 0, tzinfo=tzoffset(None, -18000)),
                "Mark Bates",
                "mark@markbates.com",
                "v0.15.5 (#1897)",
                "Makefile",
                1,
            ),
            GitFileCommit(
                "35808378f71edd89accde12c4e75d8ed8b37e91d",
                datetime(2020, 2, 6, 13, 40, 21, 0, tzinfo=tzoffset(None, -18000)),
                "Mark Bates",
                "mark@markbates.com",
                "v0.15.5 (#1897)",
                "runtime/version.go",
                2,
            ),
        ]

        assert actual == expected
