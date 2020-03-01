from kedro.io import DataSetError


class ReadOnlyDataSet(DataSetError):
    def __init__(self):
        super().__init__("Cannot Save: This is a ReadOnly DataSet")

    pass


class WriteOnlyDataSet(DataSetError):
    def __init__(self):
        super().__init__("Cannot Load: This is a WriteOnly DataSet")
