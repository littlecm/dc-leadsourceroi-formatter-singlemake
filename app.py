import streamlit as st
import pandas as pd
from io import StringIO

# Function to process data from the first CSV
def transform_data(data, date, dealership_name):
    headers = ['Date', 'Dealership', 'Lead Source', 'Type', 'Total Leads (Including Dupes)', 'Good Leads', 
               'Bad Leads', 'Duplicates', 'Sold in Timeframe', 'Sold from Leads', 'Attempted Contact', 
               'Actual Contact (Engaged)']
    
    output_data = []
    source = ''
    
    for i in range(len(data)):
        if i % 4 == 0:
            source = data.iloc[i, 0]
        elif data.iloc[i, 0] in ['New', 'Used', 'Unknown']:
            new_row = [date, dealership_name, source] + data.iloc[i, :].tolist()
            output_data.append(new_row)
    
    output_df = pd.DataFrame(output_data, columns=headers)
    return output_df

# Function to process data from the second CSV
def transform_data_part2(data, date, dealership_name):
    headers = ['Date', 'Dealership', 'Lead Source', 'Type', 'Appts Set', 'Appts Scheduled', 
               'Appts Confirmed', 'Appts Shown', 'Total Visits', 'Initial Visit', 'Be Back Visits', 
               'Total Front Gross', 'Total Back Gross', 'Total Gross']
    
    output_data = []
    source = ''
    
    for i in range(len(data)):
        if i % 4 == 0:
            source = data.iloc[i, 0]
        elif data.iloc[i, 0] in ['New', 'Used', 'Unknown']:
            new_row = [date, dealership_name, source] + data.iloc[i, :].tolist()
            output_data.append(new_row)
    
    output_df = pd.DataFrame(output_data, columns=headers)
    return output_df

# Function to merge the processed data
def merge_data(data1, data2):
    merged_data = []
    for i in range(len(data1)):
        combined_row = data1.iloc[i, :4].tolist() + data1.iloc[i, 4:].tolist() + data2.iloc[i, 4:].tolist()
        merged_data.append(combined_row)
    
    return pd.DataFrame(merged_data, columns=data1.columns.tolist() + data2.columns[4:].tolist())

# Function to reorder columns
def reorder_columns(data):
    headers = ['Lead Source', 'Type', 'Vehicle Make', 'Total Leads (Including Dupes)', 'Good Leads', 
               'Active Leads', 'Lost Leads', 'Bad Leads', 'Duplicates', 'Bad Other Leads', 
               'Customers Influenced', 'Sold in Timeframe', 'Sold from Leads', 'Avg Days to Sale', 
               'Attempted Contact', 'Actual Contact (Engaged)', 'Internet Avg Attempts to Contact', 
               'Appts Set', 'Appts Scheduled', 'Appts Confirmed', 'Appts Shown', 'Avg Days to Appt Set', 
               'Total Visits', 'Initial Visit', 'Be Back Visits', 'Avg Days to Initial Visit', 
               'Avg Days Initial Visit to Be Back', 'Total Front Gross', 'Total Back Gross', 'Total Gross']
    
    reordered_data = data[headers].copy()
    return reordered_data

# Streamlit UI
st.title("Lead Source ROI Processor")

# File uploader for the first CSV
uploaded_file1 = st.file_uploader("Upload Lead Source ROI CSV", type=["csv"])
uploaded_file2 = st.file_uploader("Upload Lead Source ROI Part 2 CSV", type=["csv"])

# Get user inputs
date = st.text_input("Enter Date (e.g., 08/29/2024):")
dealership_name = st.text_input("Enter Dealership Name:")

if uploaded_file1 and uploaded_file2 and date and dealership_name:
    # Load the CSVs into Pandas DataFrames
    data1 = pd.read_csv(uploaded_file1)
    data2 = pd.read_csv(uploaded_file2)
    
    # Process the data
    output1 = transform_data(data1, date, dealership_name)
    output2 = transform_data_part2(data2, date, dealership_name)
    merged_output = merge_data(output1, output2)
    final_output = reorder_columns(merged_output)
    
    # Allow user to download the final CSV
    csv = final_output.to_csv(index=False)
    st.download_button(label="Download Final CSV", data=csv, file_name="final_output.csv", mime="text/csv")

    st.write("Final Processed Data:")
    st.dataframe(final_output)
else:
    st.write("Please upload both CSV files and fill in all required fields.")
