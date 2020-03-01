import pytest

from kedro_code_forensics.io.bubble_packer import (
    BubblePack,
    _aggregate_bubble_packs,
    _rec_childrenizer,
)


@pytest.fixture
def aggregated_bubble_pack_fixture():
    return {
        "dir1": {
            "dir2": {
                "dir3": {
                    "file1": {
                        "/is_leaf": True,
                        "name": "file1",
                        "size": 10,
                        "value": 10,
                    },
                    "file3": {
                        "/is_leaf": True,
                        "name": "file3",
                        "size": 10,
                        "value": 10,
                    },
                }
            },
            "dir3": {
                "file3": {"/is_leaf": True, "name": "file3", "size": 10, "value": 10}
            },
        }
    }


class TestBubblePacker:
    def test_aggregate_bubble_packs(self, aggregated_bubble_pack_fixture):
        actual = _aggregate_bubble_packs(
            [
                BubblePack(["dir1", "dir2", "dir3", "file1"], 10, 10),
                BubblePack(["dir1", "dir3", "file3"], 10, 10),
                BubblePack(["dir1", "dir2", "dir3", "file3"], 10, 10),
            ]
        )
        assert actual == aggregated_bubble_pack_fixture

    def test_childrenize_aggregate(self, aggregated_bubble_pack_fixture):
        actual = _rec_childrenizer("root", aggregated_bubble_pack_fixture)
        expected = {
            "children": [
                {
                    "children": [
                        {
                            "children": [
                                {
                                    "children": [
                                        {
                                            "/is_leaf": True,
                                            "name": "file1",
                                            "size": 10,
                                            "value": 10,
                                        },
                                        {
                                            "/is_leaf": True,
                                            "name": "file3",
                                            "size": 10,
                                            "value": 10,
                                        },
                                    ],
                                    "name": "dir3",
                                }
                            ],
                            "name": "dir2",
                        },
                        {
                            "children": [
                                {
                                    "/is_leaf": True,
                                    "name": "file3",
                                    "size": 10,
                                    "value": 10,
                                }
                            ],
                            "name": "dir3",
                        },
                    ],
                    "name": "dir1",
                }
            ],
            "name": "root",
        }
        assert actual == expected
