from typing import Dict, Any
import pandas as pd
import streamlit as st

def display_kpis(
    orders: pd.DataFrame,
    customers: pd.DataFrame,
    products: pd.DataFrame,
    sellers: pd.DataFrame,
    order_payments: pd.DataFrame
) -> None:
    """
    Display key performance indicators for the e-commerce dashboard.
    
    Args:
        orders (pd.DataFrame): Orders dataset
        customers (pd.DataFrame): Customers dataset
        products (pd.DataFrame): Products dataset
        sellers (pd.DataFrame): Sellers dataset
        order_payments (pd.DataFrame): Order payments dataset
    """
    # Tính tổng doanh thu
    total_revenue = order_payments['payment_value'].sum()
    
    # Tính giá trị đơn hàng trung bình
    avg_order_value = total_revenue / len(orders) if len(orders) > 0 else 0
    
    # Header với gradient
    st.markdown("""
        <div class='gradient-header'>
            <h1>📊 Chỉ số kinh doanh chính (KPIs)</h1>
            <p>Phân tích chi tiết hiệu suất kinh doanh</p>
        </div>
    """, unsafe_allow_html=True)
    
    # CSS cho các KPI cards với animations và glass morphism
    st.markdown("""
    <style>
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    @keyframes pulse {
        0% { box-shadow: 0 0 0 0 rgba(0,0,0,0.1); }
        70% { box-shadow: 0 0 0 10px rgba(0,0,0,0); }
        100% { box-shadow: 0 0 0 0 rgba(0,0,0,0); }
    }
    
    @keyframes progressFill {
        from { width: 0; }
        to { width: 100%; }
    }
    
    .gradient-header {
        background: linear-gradient(90deg, #4b6cb7 0%, #182848 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        text-align: center;
        animation: fadeIn 1s ease-out;
    }
    
    .glass-container {
        background: rgba(255, 255, 255, 0.7);
        backdrop-filter: blur(10px);
        border-radius: 15px;
        border: 1px solid rgba(255, 255, 255, 0.3);
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.2);
        padding: 1.5rem;
        margin: 0.7rem;
        text-align: center;
        animation: fadeIn 0.8s ease-out;
        transition: all 0.3s ease;
    }
    
    .glass-container:hover {
        transform: translateY(-10px);
        box-shadow: 0 15px 30px rgba(0,0,0,0.15);
        animation: pulse 2s infinite;
    }
    
    .metric-card {
        position: relative;
        overflow: hidden;
    }
    
    .progress-bar {
        height: 4px;
        background: rgba(0,0,0,0.1);
        border-radius: 2px;
        margin-top: 1rem;
        overflow: hidden;
    }
    
    .progress-bar-fill {
        height: 100%;
        background: linear-gradient(90deg, #00d2ff 0%, #3a7bd5 100%);
        animation: progressFill 1.5s ease-out forwards;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # KPIs với glass morphism - hàng 1
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"""
            <div class='glass-container metric-card'>
                <h3 style='color: #1f77b4; margin-bottom: 0.5rem;'>Tổng đơn hàng</h3>
                <h2 style='font-size: 2rem; margin: 0;'>{len(orders):,}</h2>
                <p style='color: #666; font-size: 0.9rem;'>Đơn hàng</p>
                <div class='progress-bar'>
                    <div class='progress-bar-fill'></div>
                </div>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
            <div class='glass-container metric-card'>
                <h3 style='color: #2ecc71; margin-bottom: 0.5rem;'>Doanh thu</h3>
                <h2 style='font-size: 2rem; margin: 0;'>R$ {total_revenue:,.2f}</h2>
                <p style='color: #666; font-size: 0.9rem;'>Tổng doanh thu</p>
                <div class='progress-bar'>
                    <div class='progress-bar-fill'></div>
                </div>
            </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
            <div class='glass-container metric-card'>
                <h3 style='color: #e67e22; margin-bottom: 0.5rem;'>Khách hàng</h3>
                <h2 style='font-size: 2rem; margin: 0;'>{customers['customer_unique_id'].nunique():,}</h2>
                <p style='color: #666; font-size: 0.9rem;'>Số lượng khách hàng</p>
                <div class='progress-bar'>
                    <div class='progress-bar-fill'></div>
                </div>
            </div>
        """, unsafe_allow_html=True)
    
    # KPIs với glass morphism - hàng 2
    col4, col5, col6 = st.columns(3)
    
    with col4:
        st.markdown(f"""
            <div class='glass-container metric-card'>
                <h3 style='color: #9b59b6; margin-bottom: 0.5rem;'>Sản phẩm</h3>
                <h2 style='font-size: 2rem; margin: 0;'>{products['product_id'].nunique():,}</h2>
                <p style='color: #666; font-size: 0.9rem;'>Số lượng sản phẩm</p>
                <div class='progress-bar'>
                    <div class='progress-bar-fill'></div>
                </div>
            </div>
        """, unsafe_allow_html=True)
    
    with col5:
        st.markdown(f"""
            <div class='glass-container metric-card'>
                <h3 style='color: #3498db; margin-bottom: 0.5rem;'>Người bán</h3>
                <h2 style='font-size: 2rem; margin: 0;'>{sellers['seller_id'].nunique():,}</h2>
                <p style='color: #666; font-size: 0.9rem;'>Số lượng người bán</p>
                <div class='progress-bar'>
                    <div class='progress-bar-fill'></div>
                </div>
            </div>
        """, unsafe_allow_html=True)
    
    with col6:
        st.markdown(f"""
            <div class='glass-container metric-card'>
                <h3 style='color: #e74c3c; margin-bottom: 0.5rem;'>Giá trị TB</h3>
                <h2 style='font-size: 2rem; margin: 0;'>R$ {avg_order_value:,.2f}</h2>
                <p style='color: #666; font-size: 0.9rem;'>Giá trị đơn hàng TB</p>
                <div class='progress-bar'>
                    <div class='progress-bar-fill'></div>
                </div>
            </div>
        """, unsafe_allow_html=True)
    
    # Thêm khoảng cách sau KPIs
    st.markdown("<div style='margin-top: 2rem;'></div>", unsafe_allow_html=True)
