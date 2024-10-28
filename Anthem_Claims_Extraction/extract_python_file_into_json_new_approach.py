import pandas as pd
import re
import json


class AnthemExcelTable:

    def __init__(self, table_df, columns):
        self.table = table_df
        self.columns = columns

