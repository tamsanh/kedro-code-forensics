class TestClocFile:
    def test_parse_cloc_files(self, basic_cloc_data):
        from kedro_code_forensics.io.cloc_file import _parse_cloc_files, ClocFile

        actual = _parse_cloc_files("./", basic_cloc_data)
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
