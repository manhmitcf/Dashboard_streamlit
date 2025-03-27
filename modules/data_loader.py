import pandas as pd
import streamlit as st

@st.cache_data
def load_data():
    """
    Load and preprocess all required datasets for the Olist E-commerce dashboard.
    
    This function loads multiple CSV files containing Olist e-commerce data,
    converts datetime columns to the appropriate format, and returns all datasets
    needed for the dashboard.
    
    Returns:
        tuple: Contains the following dataframes:
            - orders: Order information including timestamps and status
            - order_items: Items within each order with pricing and shipping details
            - products: Product details including dimensions and categories
            - customers: Customer information including location
            - order_payments: Payment details including methods and values
            - order_reviews: Customer reviews and satisfaction scores
            - sellers: Seller information including location
            - product_category: Product category name translations
            - olist_geolocation_dataset: Geolocation data for mapping
            
    Raises:
        FileNotFoundError: If any required CSV file is missing
        Exception: For other data loading errors
    """
    data_path = "data/"  # Path to directory containing CSV files
    orders = pd.read_csv(data_path + 'olist_orders_dataset.csv')
    order_items = pd.read_csv(data_path + 'olist_order_items_dataset.csv')
    products = pd.read_csv(data_path + 'olist_products_dataset.csv')
    customers = pd.read_csv(data_path + 'olist_customers_dataset.csv')
    order_payments = pd.read_csv(data_path + 'olist_order_payments_dataset.csv')
    order_reviews = pd.read_csv(data_path + 'olist_order_reviews_dataset.csv')
    sellers = pd.read_csv(data_path + 'olist_sellers_dataset.csv')
    product_category = pd.read_csv(data_path + 'product_category_name_translation.csv')
    olist_geolocation_dataset = pd.read_csv(data_path + 'olist_geolocation_dataset.csv')
    RFM_log_scaled_df = pd.read_csv(data_path + 'RFM_log_scaled_df.csv')

    # Đảm bảo chuyển đổi các cột thời gian thành datetime trước khi sử dụng
    datetime_columns = [
        'order_purchase_timestamp', 'order_approved_at',
        'order_delivered_carrier_date', 'order_delivered_customer_date',
        'order_estimated_delivery_date'
    ]
    
    for col in datetime_columns:
        if col in orders.columns:
            orders[col] = pd.to_datetime(orders[col], errors='coerce')
    
    return orders, order_items, products, customers, order_payments, order_reviews, sellers, product_category, olist_geolocation_dataset, RFM_log_scaled_df
