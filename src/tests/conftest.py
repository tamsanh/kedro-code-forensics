from datetime import datetime

import pytest
from dateutil.tz import tzoffset

from kedro_code_forensics.io.git_file_commit import Committer, GitFileCommit


@pytest.fixture
def raw_git_log():
    raw_output = """\
commit:46dae90e5219c14e12f805ac5e34eea037b24dca,2020-03-01T18:14:49+08:00,"Tam Nguyen",Tam_Nguyen@McKinsey.com,"Testing"
1\t3\tsrc/kedro_code_forensics/io/git_file_commit.py
6\t4\tsrc/kedro_code_forensics/run.py

commit:4381639de273ed226a5ef861a4ee2f7cd1ff25e7,2020-03-01T18:14:50+08:00,"Tam Nguyen",Tam_Nguyen@McKinsey.com,"Testing Again"
6\t4\tsrc/kedro_code_forensics/run.py

commit:79c6a2a0e4a8f57fd81dd8f50531ec9a9f24bedb,2020-03-01T19:14:58+08:00,"Tam Nguyen",Tam_Nguyen@McKinsey.com,"Last Test"
75\t0\tsrc/kedro_code_forensics/run.py
"""  # noqa: 501
    return raw_output


@pytest.fixture
def basic_git_file_commits():
    return [
        GitFileCommit(
            "46dae90e5219c14e12f805ac5e34eea037b24dca",
            datetime(2020, 3, 1, 18, 14, 49, 0, tzinfo=tzoffset(None, 28800)),
            Committer("Tam Nguyen", "Tam_Nguyen@McKinsey.com",),
            "Testing",
            "src/kedro_code_forensics/io/git_file_commit.py",
            1,
            3,
        ),
        GitFileCommit(
            "46dae90e5219c14e12f805ac5e34eea037b24dca",
            datetime(2020, 3, 1, 18, 14, 49, 0, tzinfo=tzoffset(None, 28800)),
            Committer("Tam Nguyen", "Tam_Nguyen@McKinsey.com",),
            "Testing",
            "src/kedro_code_forensics/run.py",
            6,
            4,
        ),
        GitFileCommit(
            "4381639de273ed226a5ef861a4ee2f7cd1ff25e7",
            datetime(2020, 3, 1, 18, 14, 50, 0, tzinfo=tzoffset(None, 28800)),
            Committer("Tam Nguyen", "Tam_Nguyen@McKinsey.com",),
            "Testing Again",
            "src/kedro_code_forensics/run.py",
            6,
            4,
        ),
        GitFileCommit(
            "79c6a2a0e4a8f57fd81dd8f50531ec9a9f24bedb",
            datetime(2020, 3, 1, 19, 14, 58, 0, tzinfo=tzoffset(None, 28800)),
            Committer("Tam Nguyen", "Tam_Nguyen@McKinsey.com",),
            "Last Test",
            "src/kedro_code_forensics/run.py",
            75,
            0,
        ),
    ]


@pytest.fixture
def basic_cloc_data():
    return {
        "header": {
            "cloc_url": "github.com/AlDanial/cloc",
            "cloc_version": "1.84",
            "elapsed_seconds": 0.03460693359375,
            "n_files": 28,
            "n_lines": 1870,
            "files_per_second": 809.086419753086,
            "lines_per_second": 54035.4144620811,
        },
        "./kedro_cli.py": {
            "blank": 101,
            "comment": 88,
            "code": 435,
            "language": "Python",
        },
        "./README.md": {"blank": 50, "comment": 0, "code": 87, "language": "Markdown"},
        "./docs/source/conf.py": {
            "blank": 46,
            "comment": 126,
            "code": 85,
            "language": "Python",
        },
        "./.idea/workspace.xml": {
            "blank": 0,
            "comment": 0,
            "code": 79,
            "language": "XML",
        },
        "./src/kedro_code_forensics/io/git_file_commit.py": {
            "blank": 23,
            "comment": 9,
            "code": 61,
            "language": "Python",
        },
        "./conf/base/logging.yml": {
            "blank": 9,
            "comment": 0,
            "code": 57,
            "language": "YAML",
        },
        "./src/kedro_code_forensics/io/cloc_file.py": {
            "blank": 17,
            "comment": 1,
            "code": 51,
            "language": "Python",
        },
        "./.ipython/profile_default/startup/00-kedro-init.py": {
            "blank": 12,
            "comment": 3,
            "code": 43,
            "language": "Python",
        },
    }
