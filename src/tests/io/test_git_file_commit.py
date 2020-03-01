class TestGitLogDataSet:
    def test_parse_git_log_output(self, raw_git_log, basic_git_file_commits):
        from kedro_code_forensics.io.git_file_commit import _parse_git_log_output

        actual = _parse_git_log_output(raw_git_log)
        expected = basic_git_file_commits

        assert actual == expected
