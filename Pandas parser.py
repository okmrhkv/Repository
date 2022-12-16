import pandas as pd
import numpy as np
import os

pd.options.mode.chained_assignment = None
listdir = os.chdir(r'D:\Users\phoen\PycharmProjects\dataParsing\excel_parser\dict')

all_files = [x for x in os.listdir('.')]


for file in all_files:
    df = pd.read_excel(file, sheet_name='Список законопроектов', header=None, index_col=None)
    df_p1 = df.iloc[0:3,:]
    df_p2 = df.iloc[3:, :]
    df_p2.columns = df_p2.iloc[0]
    df_p2['Партия'] = df_p1.iloc[0, 0]
    df_p2['Стадия прохождения проектов'] = df_p1.iloc[1, 0]
    df_p2['Данные на дату'] = df_p1.iloc[2, 0]
    df_p2 = df_p2.drop(3)
    new_df = pd.DataFrame()
    for i, row in df_p2.iterrows():
        new_row = row.copy()
        items = row['СПЗИ'].replace(';',',').split(',')
        for item in items:
            new_row['СПЗИ']= item.strip()
            new_df = new_df.append(new_row)
            new_df['имя файла']=file
    with pd.ExcelWriter(r'D:\Users\phoen\PycharmProjects\dataParsing\excel_parser\output\outputfinal.xlsx',
            mode='a', if_sheet_exists= 'new') as writer:
        new_df.to_excel(writer, sheet_name='Sheet_name_10')








