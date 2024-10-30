from logging import exception
from time import perf_counter

import pandas as pd
import re
import json


pattern_1 = r"^[A-Z][a-z]{2} \d{4}"
pattern_2 = r"^QTR [1-4] \d{4}"


# def validate_columns(column_list, ):


class AnthemClaims:

    def __init__(self, excel_path, table1_pattern, table2_pattern):
        self.file_path = excel_path
        self.raw_data_df = pd.read_excel(self.file_path, index_col=None, header=None)
        self.table1_coordinates = self.extract_table_coordinates(table1_pattern)
        self.table2_coordinates = self.extract_table_coordinates(table2_pattern)
        self.table1_df, self.header1_df, self.table1_columns, self.parent_column_map1 = self.extract_data_into_dfs('table1')
        self.table2_df, self.header2_df, self.table1_columns, self.parent_column_map2 = self.extract_data_into_dfs('table2')
        self.table1_dict = self.df_into_dict(self.table1_df, self.table1_columns, self.parent_column_map1)
        self.export_dict_to_json(self.table1_dict, 'table1')

    def extract_table_coordinates(self, table_pattern):

        # Divide Entire Excel into 4 parts i.e header_1, table_1, header_2, table_2
        # Identify the division points to divide the excel into 4 parts
        for index, row in self.raw_data_df.iterrows():
            if not pd.isna(row[0]):
                pattern_match = bool(re.match(table_pattern, row[0]))
                if pattern_match:
                    x = index
                    for sub_index, sub_row in self.raw_data_df[x:].iterrows():
                        if not pd.isna(sub_row[0]):
                            end_pattern_match = bool(re.match(table_pattern, sub_row[0]))
                            if not end_pattern_match:
                                y = sub_index-1
                                return [x, y]

    def extract_data_into_dfs(self, table_type):

        # Divide table into header and table dfs
        if table_type == 'table1':
            table = self.raw_data_df.iloc[self.table1_coordinates[0]: self.table1_coordinates[1] + 2].dropna(
                how='all').dropna(axis=1, how='all').reset_index(drop=True)
            header = self.raw_data_df[:self.table1_coordinates[0]].dropna(
                how='all').dropna(axis=1, how='all').reset_index(drop=True)
        elif table_type == 'table2':
            table = self.raw_data_df.iloc[self.table2_coordinates[0]: self.table2_coordinates[1] + 1].dropna(
                how='all').dropna(axis=1, how='all').reset_index(drop=True)
            header = self.raw_data_df[ self.table1_coordinates[1] + 4:self.table2_coordinates[0]].dropna(
                how='all').dropna(axis=1, how='all').reset_index(drop=True)
        else:
            raise exception(f"table type not supported, {table_type}")

        # extract child columns from header df
        new_columns = []
        for column in header.iloc[-1].tolist():
            if not pd.isna(column):
                new_columns.append(column.replace("\n", ""))
        table.columns = new_columns

        # Extract parent column coordinates
        parent_column_map = {}
        parent_column_raw_list = header.iloc[-2].to_list()[0:len(new_columns)]
        for index, column in enumerate(parent_column_raw_list):
            if not pd.isna(column):
                end_index = len(parent_column_raw_list) - 1
                for sub_index, sub_column in enumerate(parent_column_raw_list[index + 1:]):
                    if not pd.isna(sub_column):
                        end_index = sub_index + 1
                        break
                parent_column_map[column] = [index, end_index]

        return table, header, new_columns, parent_column_map

    def df_into_dict(self, table_df, columns, parent_column_map):
        final_dict = {}
        for index, row in table_df.iterrows():
            parent_column_dict = {}
            for parent_column, value in parent_column_map.items():
                child_column_dict = {}
                for i in range(value[0], value[1], 1):
                    child_column_dict[columns[i]] = row[columns[i]]
                parent_column_dict[parent_column] = child_column_dict
            final_dict[row[columns[0]]] = parent_column_dict

        return final_dict

    def export_dict_to_json(self, dict_obj, table_type):
        file_name = self.file_path.split('.')[0]
        json_file_path = f"{file_name}_{table_type}.json"
        with open(json_file_path, 'w') as json_file:
            json.dump(dict_obj, json_file, indent=4)


anthem_claim_obj = AnthemClaims('Anthem Claims.xlsx', pattern_1, pattern_2)
