import pandas as pd
import re
import json

def regex_month_pattern_match(date_str):
    pattern = r"^[A-Z][a-z]{2} \d{4}"
    return bool(re.match(pattern, date_str)) if not pd.isna(date_str) else False

def regex_quarter_pattern_match(date_str):
    pattern = r"^QTR [1-4] \d{4}"
    return bool(re.match(pattern, date_str)) if not pd.isna(date_str) else False

file_name = "Anthem Claims.xlsx"
df = pd.read_excel(file_name, index_col=None, header=None)

header1_table1_seperator = 0
table1_header2_seperator = 0
header2_table2_seperator = 0
table_2_end_index = 0
end_index_found = False




for index, row in df.iterrows():
    if regex_month_pattern_match(row[0]):
        header1_table1_seperator = index if not header1_table1_seperator else header1_table1_seperator
    if header1_table1_seperator and not header2_table2_seperator:
        if not pd.isna(row[0]) and "Report Run Date:" in row[0]:
            table1_header2_seperator = index
    if header1_table1_seperator and table1_header2_seperator:
        if regex_quarter_pattern_match(row[0]):
            header2_table2_seperator = index if not header2_table2_seperator else header2_table2_seperator
    if header2_table2_seperator and not end_index_found:
        if not regex_quarter_pattern_match(row[0]):
            table_2_end_index = index
            end_index_found = True



print(header1_table1_seperator, table1_header2_seperator, header2_table2_seperator, table_2_end_index)
header_1_df_test = df.iloc[0:header1_table1_seperator]
print(header_1_df_test)

header_1_df = df.iloc[0:header1_table1_seperator].dropna(how='all').dropna(axis=1, how='all').reset_index(drop=True)
print(header_1_df)

table_1_df = df.iloc[header1_table1_seperator:table1_header2_seperator].dropna(how='all').dropna(axis=1, how='all').reset_index(drop=True)
header_2_df = df.iloc[table1_header2_seperator + 1:header2_table2_seperator].dropna(how='all').dropna(axis=1, how='all').reset_index(drop=True)
table_2_df = df.iloc[header2_table2_seperator:table_2_end_index].dropna(how='all').dropna(axis=1, how='all').reset_index(drop=True)





# print(header_2_df)

table_1_columns = [column.replace("\n", "") for column in header_1_df.iloc[-1].tolist()]
table_2_columns = [column.replace("\n", "") for column in header_2_df.iloc[-1].tolist()]

table_1_df.columns = table_1_columns
table_2_df.columns = table_2_columns


print(table_1_df)
# print(table_2_df)


parent_columns_table_1 = {}
parent_column_list = header_1_df.iloc[4].to_list()
print(parent_column_list)
for index, column in enumerate(parent_column_list):
    if not pd.isna(column):
        start_index = index
        end_index = len(parent_column_list) - 1
        for sub_index, sub_column in enumerate(parent_column_list[start_index+1:]):
            if not pd.isna(sub_column):
                end_index = sub_index + 2
                break
        parent_columns_table_1[column] = {'start_index': start_index, 'end_index': end_index}

print(parent_columns_table_1)
# print(table_1_df)


table_1_data_dict ={}

def get_parent_column_name(index, look_up_dict):
    for column in look_up_dict.keys():
        if look_up_dict[column]['start_index'] <= index <= look_up_dict[column]['end_index']:
            return column

# temp_dict = {}
# for index, row in table_1_df.iterrows():
#     # temp_dict[row[table_1_columns[0]]] =
#     temp_parent_column_dict = {}
#     for sub_index, column in enumerate(table_1_columns):
#         temp_child_column_dict = {column: row[column]}
#         if sub_index != 0:
#             temp_parent_column_dict[get_parent_column_name(sub_index, parent_columns_table_1)] = temp_child_column_dict
#
#     temp_dict[row[table_1_columns[0]]] = temp_parent_column_dict

temp_dict = {}

for index, row in table_1_df.iterrows():
    parent_column_dict = {}
    for parent_column in parent_columns_table_1.keys():
        temp_column_dict = {}
        print(f"{parent_column}: {parent_columns_table_1.get(parent_column)['start_index']}, "
              f"{parent_columns_table_1.get(parent_column)['end_index']}")
        for i in range(parent_columns_table_1.get(parent_column)['start_index'],
                       parent_columns_table_1.get(parent_column)['end_index']+1, 1):
            print(i)
            temp_column_dict[table_1_columns[i]] = row[table_1_columns[i]]
        parent_column_dict[parent_column] = temp_column_dict
    temp_dict[row[table_1_columns[0]]] = parent_column_dict


json_file_path = 'output.json'
with open(json_file_path, 'w') as json_file:
    json.dump(temp_dict, json_file, indent=4)
