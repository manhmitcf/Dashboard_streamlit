import streamlit as st
import logging
from modules.dashboard import create_dashboard
from modules.data_loader import load_data
from modules.filters import apply_filters

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    filename='app.log'
)
logger = logging.getLogger(__name__)
# App configuration
st.set_page_config(
    page_title="Dashboard Brazilian E-Commerce (Olist)",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS với glass morphism và gradient effects
st.markdown("""
<style>
    /* Main container styling */
    .main {
        padding: 0rem 1rem;
        background-color: #f8f9fa;
    }
    
    /* Glass morphism effect */
    .glass-container {
        background: rgba(255, 255, 255, 0.7);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.18);
        border-radius: 1rem;
        padding: 1.5rem;
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
    }
    
    /* Header styling with gradient */
    .main-header {
        background: linear-gradient(120deg, #1f77b4, #2ecc71);
        color: white;
        padding: 2rem;
        border-radius: 1rem;
        margin-bottom: 2rem;
        text-align: center;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        padding-top: 1rem;
        background: rgba(255, 255, 255, 0.8);
        backdrop-filter: blur(5px);
    }
    
    /* Card containers */
    .stcard {
        background: rgba(255, 255, 255, 0.7);
        backdrop-filter: blur(7px);
        padding: 1.2rem;
        border-radius: 1rem;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
        margin-bottom: 1.5rem;
        border: 1px solid rgba(255, 255, 255, 0.18);
        transition: all 0.3s ease;
    }
    
    .stcard:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15);
    }
    
    /* Metric styling */
    .metric-container {
        background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%);
        padding: 1.2rem;
        border-radius: 1rem;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.05);
        transition: all 0.3s ease;
        border: 1px solid #e9ecef;
    }
    
    .metric-container:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 20px rgba(0, 0, 0, 0.1);
    }
    
    /* Chart containers */
    .chart-container {
        background: rgba(255, 255, 255, 0.8);
        backdrop-filter: blur(10px);
        padding: 1.8rem;
        border-radius: 1rem;
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.2);
        margin-bottom: 2rem;
        border: 1px solid rgba(255, 255, 255, 0.18);
    }
    
    /* Table styling */
    .dataframe {
        font-size: 0.9rem !important;
        border-collapse: collapse;
        margin: 25px 0;
        box-shadow: 0 0 20px rgba(0, 0, 0, 0.1);
        border-radius: 0.5rem;
        overflow: hidden;
    }
    
    .dataframe thead tr {
        background-color: #1f77b4;
        color: #ffffff;
        text-align: left;
    }
    
    .dataframe th,
    .dataframe td {
        padding: 12px 15px;
    }
    
    .dataframe tbody tr {
        border-bottom: 1px solid #dddddd;
    }
    
    .dataframe tbody tr:nth-of-type(even) {
        background-color: #f8f9fa;
    }
    
    /* Custom tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 2rem;
        background: rgba(255, 255, 255, 0.6);
        padding: 0.5rem;
        border-radius: 0.5rem;
    }
    
    .stTabs [data-baseweb="tab"] {
        height: 3rem;
        white-space: pre-wrap;
        background-color: transparent;
        border-radius: 0.5rem;
        color: #0f1116;
        font-size: 1rem;
        transition: all 0.2s ease;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background-color: rgba(31, 119, 180, 0.1);
    }
    
    /* Button styling */
    .stButton>button {
        width: 100%;
        border-radius: 0.5rem;
        height: 2.8rem;
        background: linear-gradient(90deg, #1f77b4, #2ecc71);
        color: white;
        border: none;
        transition: all 0.3s ease;
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
    }
    
    /* Custom scrollbar */
    ::-webkit-scrollbar {
        width: 10px;
        height: 10px;
    }
    
    ::-webkit-scrollbar-track {
        background: #f1f1f1;
        border-radius: 5px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: #888;
        border-radius: 5px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: #555;
    }
    
    /* Footer styling */
    .footer {
        background: linear-gradient(90deg, #f0f2f6, #e9ecef);
        padding: 1.2rem;
        text-align: center;
        font-size: 0.9rem;
        margin-top: 2rem;
        border-radius: 1rem;
        box-shadow: 0 -2px 10px rgba(0, 0, 0, 0.05);
    }
    
    /* Animated progress bars */
    .progress-bar {
        height: 8px;
        background-color: #e9ecef;
        border-radius: 4px;
        overflow: hidden;
        margin: 10px 0;
    }
    
    .progress-bar-fill {
        height: 100%;
        background: linear-gradient(90deg, #1f77b4, #2ecc71);
        animation: progressAnimation 1.5s ease-in-out;
    }
    
    @keyframes progressAnimation {
        0% { width: 0%; }
        100% { width: 100%; }
    }
</style>
""", unsafe_allow_html=True)

# Header với logo và tiêu đề (glass morphism style)
st.markdown("""
    <div class="main-header glass-container">
        <h1>🛒 Dashboard E-Commerce Olist Brazil</h1>
        <p>Dashboard phân tích bộ dữ liệu thương mại điện tử công khai từ Olist</p>
        <div class="progress-bar">
            <div class="progress-bar-fill"></div>
        </div>
    </div>
""", unsafe_allow_html=True)
# Load data with error logging
with st.spinner('Đang tải dữ liệu...'):
    try:
        orders, order_items, products, customers, order_payments, order_reviews, sellers, product_category, olist_geolocation_dataset,RFM_log_scaled_df = load_data()
        logger.info("Data loaded successfully")
        data_loaded = True
    except FileNotFoundError as e:
        logger.error(f"File not found error: {str(e)}")
        st.error("⚠️ Không tìm thấy file dữ liệu. Vui lòng tải bộ dữ liệu Olist và đặt các file CSV vào thư mục hiện tại.")
        data_loaded = False
    except Exception as e:
        logger.error(f"Unexpected error during data loading: {str(e)}")
        st.error(f"⚠️ Lỗi khi tải dữ liệu: {e}")
        data_loaded = False
if data_loaded:
    try:
        # Gọi hàm để tạo các tabs và phân tích
        logger.info("Creating dashboard components")
        create_dashboard(orders, order_items, products, customers, order_payments, 
                        order_reviews, sellers, product_category, 
                        olist_geolocation_dataset, RFM_log_scaled_df)  # Thêm RFM_log_scaled_df
        logger.info("Dashboard created successfully")
    except Exception as e:
        logger.error(f"Error creating dashboard: {str(e)}")
        st.error(f"⚠️ Lỗi khi tạo dashboard: {e}")
    # Thêm phần kết luận và bộ lọc
    st.sidebar.title("Bộ lọc")

    # Bộ lọc theo khoảng thời gian
    if not orders.empty and 'order_purchase_timestamp' in orders.columns:
        try:
            logger.info("Applying time filters")
            apply_filters(orders)
            logger.info("Time filters applied successfully")
        except Exception as e:
            logger.error(f"Error applying filters: {str(e)}")
        st.sidebar.info("Chức năng lọc theo thời gian sẽ được áp dụng trong bản cập nhật tiếp theo")

    # Bộ lọc theo trạng thái đơn hàng
    if not orders.empty and 'order_status' in orders.columns:
        status_options = orders['order_status'].unique().tolist()
        selected_status = st.sidebar.multiselect(
            "Chọn trạng thái đơn hàng",
            options=status_options,
            default=status_options
        )
        
        st.sidebar.info("Chức năng lọc theo trạng thái sẽ được áp dụng trong bản cập nhật tiếp theo")

    # Thông tin về dữ liệu
    st.sidebar.header("Thông tin dữ liệu")
    st.sidebar.markdown("""
    **Bộ dữ liệu Brazilian E-Commerce Public Dataset by Olist** chứa thông tin về 100.000 đơn đặt hàng từ năm 2016 đến 2018 tại thị trường Brazil. Dữ liệu bao gồm thông tin về:

    - Đơn hàng
    - Sản phẩm
    - Khách hàng
    - Người bán
    - Đánh giá

    Dashboard này được tạo để phân tích và trực quan hóa xu hướng bán hàng, hành vi khách hàng và hiệu suất sản phẩm.
    """)

    # Thêm footer với glass morphism
    st.markdown("""
        <div class="footer glass-container">
            © 2025 Phân tích dữ liệu E-Commerce Olist Brazil | Powered by Streamlit
        </div>
    """, unsafe_allow_html=True)
else:
    # Hiển thị hướng dẫn tải dữ liệu
    st.header("Hướng dẫn tải dữ liệu")
    st.markdown("""
    Để sử dụng dashboard này, bạn cần tải bộ dữ liệu Brazilian E-Commerce Public Dataset by Olist từ Kaggle:

    1. Truy cập [Kaggle](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce)
    2. Tải bộ dữ liệu xuống và giải nén
    3. Đặt các file CSV vào cùng thư mục với ứng dụng Streamlit này
    4. Khởi động lại ứng dụng

    Các file cần thiết:
    - olist_orders_dataset.csv
    - olist_order_items_dataset.csv
    - olist_products_dataset.csv
    - olist_customers_dataset.csv
    - olist_order_payments_dataset.csv
    - olist_order_reviews_dataset.csv
    - olist_sellers_dataset.csv
    - product_category_name_translation.csv
    """)

    # Tạo một demo nhỏ để hiển thị khi không có dữ liệu
    st.header("Xem trước dashboard")
    st.image("https://via.placeholder.com/800x400?text=Dashboard+Preview", use_column_width=True)
