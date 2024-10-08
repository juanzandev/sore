import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

if 'spending_data' not in st.session_state:
    st.session_state['spending_data'] = pd.DataFrame(
        columns=['Date', 'Category', 'Amount', 'Description'])

st.title('Spending Tracker App')

st.header('Add a New Expense')
date = st.date_input('Date')
category = st.selectbox(
    'Category', ['Food', 'Transportation', 'Utilities', 'Entertainment', 'Others'])
amount = st.number_input('Amount', min_value=0.01, format='%0.2f')
description = st.text_input('Description')

if st.button('Add Expense'):
    new_expense = {'Date': pd.to_datetime(
        date), 'Category': category, 'Amount': amount, 'Description': description}
    st.session_state['spending_data'] = pd.concat(
        [st.session_state['spending_data'], pd.DataFrame([new_expense])], ignore_index=True)
    st.success('Expense added successfully!')

st.header('Spending Records')
st.dataframe(st.session_state['spending_data'])

st.header('Summary')
if not st.session_state['spending_data'].empty:
    total_spent = st.session_state['spending_data']['Amount'].sum()
    st.write(f'Total Spent: ${total_spent:.2f}')

    spending_by_category = st.session_state['spending_data'].groupby('Category')[
        'Amount'].sum()
    st.write('Spending by Category:')
    st.bar_chart(spending_by_category)
else:
    st.write('No spending records yet.')

st.header('Filter Records by Date')
start_date = st.date_input('Start Date', value=pd.to_datetime('2023-01-01'))
end_date = st.date_input('End Date', value=pd.to_datetime('2023-12-31'))

# Convert datetime.date to pd.Timestamp
start_date = pd.Timestamp(start_date)
end_date = pd.Timestamp(end_date)

filtered_data = st.session_state['spending_data'][
    (st.session_state['spending_data']['Date'] >= start_date) &
    (st.session_state['spending_data']['Date'] <= end_date)
]

st.write('Filtered Records:')
if not filtered_data.empty:
    st.write(filtered_data)
else:
    st.write('No records found for the selected date range.')
