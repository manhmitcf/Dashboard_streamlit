# Các bộ lọc
import streamlit as st
import pandas as pd
def apply_filters(orders):
    # Bộ lọc theo khoảng thời gian
    min_date = orders['order_purchase_timestamp'].min().date()
    max_date = orders['order_purchase_timestamp'].max().date()
    
    date_range = st.sidebar.date_input(
        "Chọn khoảng thời gian",
        [min_date, max_date],
        min_value=min_date,
        max_value=max_date
    )
    
    filtered_orders = orders[(orders['order_purchase_timestamp'] >= pd.to_datetime(date_range[0])) & 
                             (orders['order_purchase_timestamp'] <= pd.to_datetime(date_range[1]))]
    return filtered_orders
