from io import BytesIO
import pandas as pd


def dataframe_to_excel_bytes(dataframe, sheet_name):
    excel_buffer = BytesIO()

    with pd.ExcelWriter(excel_buffer, engine="openpyxl") as writer:
        dataframe.to_excel(
            writer,
            index=False,
            sheet_name=sheet_name
        )

    return excel_buffer.getvalue()