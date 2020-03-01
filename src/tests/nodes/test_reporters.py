from kedro_code_forensics.nodes.reporters import _extract_path


class TestReporters:
    def test_extract_path(self):
        filepath = "dir1/dir2/dir3/file1"
        actual = _extract_path(filepath)
        expected = ["dir1", "dir2", "dir3", "file1"]
        assert actual == expected
