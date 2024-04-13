# -*- coding: utf-8 -*-
"""
Created on Thu Apr 11 21:03:55 2024

@author: Home PC
"""

import pandas as pd
import numpy as np
import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt
from PIL import Image

# Set up the page configuration and title
st.set_page_config(layout="wide")

# Load the logo image
logo_path = "Master - Rental Logo Vector.jpg"
logo = Image.open(logo_path)

# Resize the logo
logo = logo.resize((3000, 1000))  # You can adjust the size as needed

# Create a layout for logo and title
col1, col2 = st.columns([1, 8])  # adjust the ratio as per your need

# Display the logo in the first column, aligned to the left
col1.image(logo)

# Display the title and subtitle in the second column
with col2:
    st.title('Parts Inventory Summary')
    st.subheader('April 2024 - Syed Sajjad Raza')


# Load data into a pandas dataframe
file = "C:\\Users\\Home PC\\OneDrive\\Desktop\\Pr_sorted_data.csv', encoding='ISO-8859-1"
df = pd.read_csv('Pr_sorted_data.csv')

# Create a dropdown to select the inventory part
inventory_parts = df['Inventory Part'].unique()
selected_inventory_part = st.selectbox('Select Inventory Part', np.insert(inventory_parts, 0, 'All'))

# Optional dropdown to select search name based on inventory part selected
if selected_inventory_part != 'All':
    search_names = df[df['Inventory Part'] == selected_inventory_part]['Search name'].unique()
else:
    search_names = df['Search name'].unique()
selected_search_name = st.selectbox('Select Search Name (optional)', np.insert(search_names, 0, 'All'))

# Optional dropdown to select item segment based on inventory part and search name selected
if selected_inventory_part != 'All' and selected_search_name != 'All':
    item_segments = df[(df['Inventory Part'] == selected_inventory_part) & (df['Search name'] == selected_search_name)]['Item Segment'].unique()
else:
    item_segments = df['Item Segment']. unique()
selected_item_segment = st.selectbox('Select Item Segment (optional)', np.insert(item_segments, 0, 'All'))

# Filter the dataframe based on the selected options
filtered_df = df.copy()
if selected_inventory_part != 'All':
    filtered_df = filtered_df[filtered_df['Inventory Part'] == selected_inventory_part]
if selected_search_name != 'All':
    filtered_df = filtered_df[filtered_df['Search name'] == selected_search_name]
if selected_item_segment != 'All':
    filtered_df = filtered_df[filtered_df['Item Segment'] == selected_item_segment]

# Display the filtered dataframe
st.write(f"Displaying information for Inventory Part: {selected_inventory_part}, Search Name: {selected_search_name}, Item Segment: {selected_item_segment}")
st.dataframe(filtered_df[['Description', 'Item Segment', 'Total available', 'Financial cost amount']])

# Calculate and display the total financial cost amount for the filtered parts
total_financial_cost = filtered_df['Financial cost amount'].sum()
st.write('Total Financial Cost Amount for selected filters:', total_financial_cost)

# Visualization section
st.subheader('Data Visualizations')

# Bar plot for 'Financial cost amount' by 'Item Segment'
st.write('Financial Cost Amount by Item Segment')
fig, ax = plt.subplots()
financial_bar_plot = sns.barplot(data=filtered_df, x='Item Segment', y='Financial cost amount', ax=ax, ci=None)
ax.set_xticklabels(ax.get_xticklabels(), fontsize=9, rotation=45, ha="right", wrap=True)
for container in financial_bar_plot.containers:
    ax.bar_label(container, fmt='%.2f', padding=3)
plt.tight_layout()
st.pyplot(fig)

# Bar plot for 'Total available' by 'Item Segment'
st.write('Total Available Items by Item Segment')
fig, ax = plt.subplots()
available_bar_plot = sns.barplot(data=filtered_df, x='Item Segment', y='Total available', ax=ax, ci=None)
ax.set_xticklabels(ax.get_xticklabels(), fontsize=9, rotation=45, ha="right", wrap=True)
for container in available_bar_plot.containers:
    ax.bar_label(container, fmt='%.2f', padding=3)
plt.tight_layout()
st.pyplot(fig)
