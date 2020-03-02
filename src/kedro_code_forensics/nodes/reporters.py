import os
from typing import List

from kedro_code_forensics.io.bubble_packer import BubblePack
from kedro_code_forensics.nodes.transformations import HotSpotData


def _extract_path(filepath: str):
    split_path = []
    frontier = filepath
    while frontier != "":
        basename = os.path.basename(frontier)
        split_path.append(basename)
        frontier = os.path.dirname(frontier)
    return list(reversed(split_path))


def report_hot_spots_bubble_pack(hot_spots: List[HotSpotData]) -> List[BubblePack]:
    """
    Takes a list of HotSpotData and transforms
    them into BubblePack tuples in preparation for
    being written to disk by the BubblePackerDataSet

    :param hot_spots: List[HostSpotData]
    :return: List[BubblePack]
    """
    out_bubble_packs: List[BubblePack] = []

    for hot_spot in hot_spots:
        out_bubble_packs.append(
            BubblePack(
                path=_extract_path(hot_spot.filepath),
                size=hot_spot.lines,
                value=hot_spot.rating,
            )
        )

    return out_bubble_packs
