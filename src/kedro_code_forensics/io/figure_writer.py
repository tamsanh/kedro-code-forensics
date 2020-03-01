import os
from pathlib import PurePath
from typing import Any, Dict, Optional

from kedro.contrib.io import DefaultArgumentsMixIn
from kedro.io import AbstractVersionedDataSet, Version
from plotly.graph_objs._figure import Figure

from kedro_code_forensics.io.expections import WriteOnlyDataSet


class FigureWriterDataSet(DefaultArgumentsMixIn, AbstractVersionedDataSet):
    DEFAULT_SAVE_ARGS = {}

    def __init__(
        self,
        filepath: PurePath,
        version: Optional[Version] = None,
        save_args: Optional[Dict[str, Any]] = None,
    ):
        super().__init__(
            filepath=filepath, version=version, load_args=None, save_args=save_args
        )

    def _load(self) -> Any:
        raise WriteOnlyDataSet()

    def _save(self, data: Figure) -> None:

        _, ext = os.path.splitext(self._filepath)

        if ext.lower() in [".html", ".htm"]:
            data.write_html(file=self._filepath, **self._save_args)
        else:
            data.write_image(file=self._filepath, **self._save_args)

    def _describe(self) -> Dict[str, Any]:
        return dict(filepath=self._filepath, save_args=self._save_args)
