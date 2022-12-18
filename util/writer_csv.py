import pandas as pd

def writer(filename, dataframe):

    writer = pd.ExcelWriter(filename, engine='xlsxwriter')


    dataframe.to_excel(writer, sheet_name='Sheet1', index=False)

    worksheet = writer.sheets['Sheet1']  # pull worksheet object
    for idx, col in enumerate(dataframe):  # loop through all columns
        series = dataframe[col]
        max_len = max((
            series.astype(str).map(len).max(),  # len of largest item
            len(str(series.name))  # len of column name/header
        )) + 1  # adding a little extra space
        worksheet.set_column(idx, idx, max_len)

    writer.close()