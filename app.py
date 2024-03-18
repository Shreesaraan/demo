# import streamlit as st
# import pandas as pd
#
# # Function to process the uploaded file and generate the output
# def process_data(file):
#     df = pd.read_excel(file)
#     df['in/out time'] = pd.to_datetime(df['in/out time'], errors='coerce')
#     return df
#
# # Main function to run the Streamlit app
# def main():
#     st.title('Employee Data Analysis')
#
#     # File uploader for uploading the input Excel file
#     uploaded_file = st.file_uploader("Upload Excel file", type=['xlsx'])
#
#     if uploaded_file is not None:
#         # Process the uploaded file
#         df = process_data(uploaded_file)
#
#         # Display the raw data
#         st.subheader("Raw Data")
#         st.write(df)
#
#         # Filters
#         employee_ids = df['employee_id'].unique()
#         vendors = df['vendor_name'].unique()
#         dates = pd.to_datetime(df['account_date']).dt.date.unique()
#
#         # Multi-select filters for employee_id and vendor
#         selected_employee_ids = st.multiselect("Select Employee IDs", employee_ids)
#         selected_vendors = st.multiselect("Select Vendors", vendors)
#
#         # Date range filter
#         date_range = st.date_input("Select Date Range", (dates.min(), dates.max()))
#
#         # Filter the data based on selected filters
#         filtered_df = df[
#             (df['employee_id'].isin(selected_employee_ids)) &
#             (df['vendor_name'].isin(selected_vendors)) &
#             (pd.to_datetime(df['account_date']).dt.date >= date_range[0]) &
#             (pd.to_datetime(df['account_date']).dt.date <= date_range[1])
#         ]
#
#         # Display the filtered data
#         st.subheader("Filtered Data")
#         st.write(filtered_df)
#
# # Run the Streamlit app
# if __name__ == "__main__":
#     main()

import streamlit as st
import pandas as pd
import plotly.express as px
from functools import lru_cache

# Load the dataset
@lru_cache(maxsize=None)
def load_data():
    # Load your dataset here (e.g., using pd.read_csv())
    # Replace 'path_to_your_dataset.csv' with the actual path to your dataset
    df = pd.read_excel(r"C:\Users\admin\Downloads\sample.xlsx")
    print("Dataset loaded successfully")
    return df

df = load_data()

if df.empty:
    st.error("Error: Dataset is empty. Please check the data loading.")

else:
    # Convert 'date' column to datetime format
    df['date'] = pd.to_datetime(df['date'])

    # Sidebar filters
    st.sidebar.header("Filters")

    min_date = df['date'].min() if not df.empty else None
    max_date = df['date'].max() if not df.empty else None
    date_filter = st.sidebar.date_input("Select Date", min_value=min_date, max_value=max_date)

    if 'vendor code' in df.columns:
        vendor_code_filter = st.sidebar.selectbox("Select Vendor Code", df['vendor code'].unique())
    else:
        vendor_code_filter = None
    if 'department' in df.columns:
        department_filter = st.sidebar.selectbox("Select Department", df['department'].unique())
    else:
        department_filter = None

    # Apply filters
    filtered_df = df[(df['date'] == date_filter)]
    if vendor_code_filter:
        filtered_df = filtered_df[filtered_df['vendor code'] == vendor_code_filter]
    if department_filter:
        filtered_df = filtered_df[filtered_df['department'] == department_filter]

    # Display total employees, vendors, and departments
    total_employees = filtered_df['employee id'].nunique()
    total_vendors = filtered_df['vendor code'].nunique()
    total_departments = filtered_df['department'].nunique()

    st.write(f"Total Employees: {total_employees}")
    st.write(f"Total Vendors: {total_vendors}")
    st.write(f"Total Departments: {total_departments}")

    # Pie chart of vendors
    vendor_counts = filtered_df['vendor name'].value_counts()
    fig = px.pie(values=vendor_counts.values, names=vendor_counts.index, title='Vendors')
    st.plotly_chart(fig)

    # On clicking each vendor, display another pie chart of departments
    selected_vendor = st.selectbox("Select Vendor to View Departments", vendor_counts.index)
    departments_for_vendor = filtered_df[filtered_df['vendor name'] == selected_vendor]['department'].value_counts()
    fig_dept = px.pie(values=departments_for_vendor.values, names=departments_for_vendor.index, title=f'Departments for {selected_vendor}')
    st.plotly_chart(fig_dept)
