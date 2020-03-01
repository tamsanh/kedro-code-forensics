import pytest


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


class TestClocFile:
    def test_parse_cloc_files(self, basic_cloc_data):
        from kedro_code_forensics.io.cloc_file import _parse_cloc_files, ClocFile

        actual = _parse_cloc_files(basic_cloc_data)
        expected = [
            ClocFile("kedro_cli.py", 101, 88, 435, "Python"),
            ClocFile("README.md", 50, 0, 87, "Markdown"),
            ClocFile("docs/source/conf.py", 46, 126, 85, "Python"),
            ClocFile(".idea/workspace.xml", 0, 0, 79, "XML"),
            ClocFile(
                "src/kedro_code_forensics/io/git_file_commit.py", 23, 9, 61, "Python"
            ),
            ClocFile("conf/base/logging.yml", 9, 0, 57, "YAML"),
            ClocFile("src/kedro_code_forensics/io/cloc_file.py", 17, 1, 51, "Python"),
            ClocFile(
                ".ipython/profile_default/startup/00-kedro-init.py", 12, 3, 43, "Python"
            ),
        ]

        assert actual == expected
