import streamlit as st
import pandas as pd
import os
import tempfile
import base64

def fill_order_sheet(order_sheet, stock_sheets):
    # Read the CSV files
    order_df = pd.read_csv(order_sheet)

    for stock_sheet in stock_sheets:
        stock_df = pd.read_csv(stock_sheet)

        # Match columns and rows
        common_columns = list(set(order_df.columns).intersection(stock_df.columns))
        common_rows = list(order_df.index.intersection(stock_df.index))

        # Fill in the order sheet
        order_df.loc[common_rows, common_columns] = stock_df.loc[common_rows, common_columns]

    return order_df

def main():
    st.title("Order Sheet Filler")
    st.write("Upload your CSV files.")

    order_file = st.file_uploader("Upload the Order Sheet CSV file", type="csv")
    stock_files = st.file_uploader("Upload the Stock Sheet CSV files", type="csv", accept_multiple_files=True)

    if order_file is not None and stock_files:
        filled_order_df = fill_order_sheet(order_file, stock_files)

        st.subheader("Newly Filled-in Order Sheet")
        st.write(filled_order_df)

        st.subheader("Download")
        download_options = ["CSV", "Excel"]
        download_format = st.selectbox("Select the download format", download_options)

        if st.button("Download"):
            if download_format == "CSV":
                csv = filled_order_df.to_csv(index=False)
                b64 = base64.b64encode(csv.encode()).decode()
                st.download_button(label="Download CSV", data=b64, file_name="filled_order_sheet.csv", mime="text/csv")
            elif download_format == "Excel":
                with tempfile.NamedTemporaryFile(delete=False, suffix=".xlsx") as tmp:
                    filled_order_df.to_excel(tmp.name, index=False)
                    tmp.seek(0)
                    st.download_button(
                        label="Download Excel",
                        data=tmp.read(),
                        file_name="filled_order_sheet.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                    )
                os.unlink(tmp.name)  # Delete the temporary file

if __name__ == "__main__":
    main()
