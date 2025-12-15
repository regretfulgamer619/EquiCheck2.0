import streamlit as st
import pandas as pd

st.set_page_config(page_title="EquiCheck", layout="wide")

st.markdown(
    """
    <h1 style='text-align: center;'> EquiCheck 2.0 </h1>

    <h6 style='text-align: center;'> Stock hoarder </h6> 

    """,
    unsafe_allow_html=True)

file1 = st.file_uploader("Upload excel sheet 1", type="xlsx")
file2 = st.file_uploader("Upload excel sheet 2", type="xlsx")
file3 = st.file_uploader("Upload excel sheet 3", type="xlsx")
file4 = st.file_uploader("Upload excel sheet 4", type="xlsx")
file5 = st.file_uploader("Upload excel sheet 5", type="xlsx")
file6 = st.file_uploader("Upload excel sheet 6", type="xlsx")

def file_cleaner(file):
    data=pd.read_excel(file,header=None)
    for i, row in data.iterrows():
        if "Scrip Name" in row.values and "Total Holding" in row.values:
            index=i
            break
    else :
        raise ValueError("No such column names found")
    data.columns= data.iloc[index]
    data = data.drop(index=range(index + 1)).reset_index(drop=True)
    data = data[:-2]
    cleaned_data= data[["ScripCode","Scrip Name","Total Holding"]].copy()
    cleaned_data["ScripCode"] = cleaned_data["ScripCode"].astype(str).str.strip()
    cleaned_data["Scrip Name"] = cleaned_data["Scrip Name"].astype(str).str.strip()
    cleaned_data["Total Holding"] = pd.to_numeric(cleaned_data["Total Holding"], errors="coerce").fillna(0)

    return cleaned_data

if file1 and file2 and file3 and file4 and file5 and file6:
    try:
        df1 = file_cleaner(file1)
        df2 = file_cleaner(file2)
        df3 = file_cleaner(file3)
        df4 = file_cleaner(file4)
        df5 = file_cleaner(file5)
        df6 = file_cleaner(file6)

        combined = pd.concat([df1, df2, df3, df4, df5, df6],ignore_index=True)
        total_holdings = (combined.groupby(["ScripCode", "Scrip Name"], as_index=False)["Total Holding"].sum().sort_values(by="Total Holding", ascending=False) )
        st.success("Total holdings from all files")
        st.dataframe(total_holdings) 
    
    except Exception as e:
        st.error(f"Error processing files: {e}")
