import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from modules.kpis import display_kpis


def create_dashboard(orders, order_items, products, customers, order_payments, order_reviews, sellers, product_category, olist_geolocation_dataset, RFM_log_scaled_df=None):
    # Tạo tabs để phân chia các nhóm phân tích
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["Tổng quan", "Phân tích bán hàng", "Phân tích khách hàng", "Phân tích sản phẩm", "Bản đồ phân bố"])
    
    with tab1:
        st.header("Tổng quan về dữ liệu")
        
        display_kpis(orders, customers, products, sellers, order_payments)
        st.subheader("Phân tích đơn hàng và doanh thu theo khoảng thời gian")
        
        # Chuẩn bị dữ liệu
        orders['date'] = orders['order_purchase_timestamp'].dt.date
        daily_orders = orders.groupby('date').size().reset_index(name='count')
        daily_orders['date'] = pd.to_datetime(daily_orders['date'])
        
        payment_values = order_payments.groupby('order_id')['payment_value'].sum().reset_index()
        orders_with_payment = orders.merge(payment_values, on='order_id', how='left')
        orders_with_payment['date'] = orders_with_payment['order_purchase_timestamp'].dt.date
        daily_revenue = orders_with_payment.groupby('date')['payment_value'].sum().reset_index()
        daily_revenue['date'] = pd.to_datetime(daily_revenue['date'])
        
        # Tạo date picker
        min_date = daily_orders['date'].min().date()
        max_date = daily_orders['date'].max().date()
        
        col1, col2 = st.columns(2)
        with col1:
            start_date = st.date_input("Từ ngày", min_date, min_value=min_date, max_value=max_date)
        with col2:
            end_date = st.date_input("Đến ngày", max_date, min_value=min_date, max_value=max_date)
        
        # Lọc dữ liệu
        filtered_data = daily_orders[(daily_orders['date'] >= pd.to_datetime(start_date)) & 
                                   (daily_orders['date'] <= pd.to_datetime(end_date))]
        filtered_revenue = daily_revenue[(daily_revenue['date'] >= pd.to_datetime(start_date)) & 
                                       (daily_revenue['date'] <= pd.to_datetime(end_date))]
        
        # Tạo biểu đồ kết hợp
        fig = go.Figure()
        
        # Thêm dữ liệu doanh thu và số lượng đơn hàng
        fig.add_trace(
            go.Scatter(
                x=filtered_revenue['date'],
                y=filtered_revenue['payment_value'],
                mode='lines',
                name='Doanh thu',
                line=dict(color='#19D3F3', width=2)
            )
        )
        
        fig.add_trace(
            go.Scatter(
                x=filtered_data['date'],
                y=filtered_data['count'],
                mode='lines',
                name='Số đơn hàng',
                line=dict(color='#FF9800', width=2),
                yaxis='y2'
            )
        )
        
        # Cấu hình layout
        fig.update_layout(
            title=f"So sánh doanh thu và số lượng đơn hàng từ {start_date} đến {end_date}",
            xaxis=dict(
                title='Ngày',
                rangeselector=dict(
                    buttons=list([
                        dict(count=7, label="7 ngày", step="day", stepmode="backward"),
                        dict(count=1, label="1 tháng", step="month", stepmode="backward"),
                        dict(count=3, label="3 tháng", step="month", stepmode="backward"),
                        dict(count=6, label="6 tháng", step="month", stepmode="backward"),
                        dict(step="all", label="Tất cả")
                    ])
                ),
                rangeslider=dict(visible=True),
                type="date"
            ),
            yaxis=dict(
                title=dict(text='Doanh thu (R$)', font=dict(color='#19D3F3')),
                tickfont=dict(color='#19D3F3')
            ),
            yaxis2=dict(
                title=dict(text='Số đơn hàng', font=dict(color='#FF9800')),
                tickfont=dict(color='#FF9800'),
                anchor='x',
                overlaying='y',
                side='right'
            ),
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            )
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Phân tích theo giờ trong ngày
        st.subheader("Phân tích đơn hàng theo giờ trong ngày")
        
        orders['hour'] = orders['order_purchase_timestamp'].dt.hour
        hourly_orders = orders.groupby('hour').size().reset_index(name='count')
        
        hour_range = st.slider("Chọn khoảng giờ", 0, 23, (0, 23), 1)
        
        filtered_hours = hourly_orders[(hourly_orders['hour'] >= hour_range[0]) & 
                                     (hourly_orders['hour'] <= hour_range[1])]
        
        fig = px.bar(
            filtered_hours,
            x='hour',
            y='count',
            title=f"Số lượng đơn hàng theo giờ (từ {hour_range[0]}h đến {hour_range[1]}h)",
            labels={'hour': 'Giờ trong ngày', 'count': 'Số đơn hàng'},
            color='count',
            color_continuous_scale=px.colors.sequential.Viridis
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with tab2:
        pass
        st.header("Phân tích bán hàng")

        ### 1. Phân tích doanh thu theo tháng
        st.subheader("Doanh thu theo tháng")
        
        # Tính tổng giá trị đơn hàng
        payment_values = order_payments.groupby('order_id')['payment_value'].sum().reset_index()
        merged_data = orders.merge(payment_values, on='order_id', how='left')
        
        # Tạo dữ liệu doanh thu theo tháng
        merged_data['month_year'] = merged_data['order_purchase_timestamp'].dt.strftime('%Y-%m')
        monthly_revenue = merged_data.groupby('month_year')['payment_value'].sum().reset_index()
        monthly_revenue['month_year'] = pd.to_datetime(monthly_revenue['month_year'] + '-01')
        monthly_revenue = monthly_revenue.sort_values('month_year')
        
        # Vẽ biểu đồ doanh thu theo tháng
        fig = px.line(
            monthly_revenue,
            x='month_year',
            y='payment_value',
            title="Doanh thu theo tháng",
            labels={'month_year': 'Tháng', 'payment_value': 'Doanh thu (R$)'}
        )
        st.plotly_chart(fig, use_container_width=True)
        
        ### 2. Phân tích phương thức thanh toán
        st.subheader("Phương thức thanh toán")
        
        # Phân tích số lượng đơn hàng theo phương thức thanh toán
        payment_types = order_payments['payment_type'].value_counts().reset_index()
        payment_types.columns = ['payment_type', 'count']
        
        # Vẽ biểu đồ phương thức thanh toán
        fig = px.bar(
            payment_types,
            x='payment_type',
            y='count',
            title="Số lượng đơn hàng theo phương thức thanh toán",
            labels={'payment_type': 'Phương thức thanh toán', 'count': 'Số lượng'},
            color='payment_type'
        )
        st.plotly_chart(fig, use_container_width=True)
        
        ### 5. Phân tích thời gian giao hàng
        st.subheader("Thời gian giao hàng trung bình")
        
        # Tính thời gian giao hàng
        merged_data['delivery_time'] = (merged_data['order_delivered_customer_date'] - merged_data['order_purchase_timestamp']).dt.days
        
        # Thời gian giao hàng trung bình theo trạng thái đơn hàng
        avg_delivery_time = merged_data.groupby('order_status')['delivery_time'].mean().reset_index()
        
        # Vẽ biểu đồ thời gian giao hàng
        fig = px.bar(
            avg_delivery_time,
            x='order_status',
            y='delivery_time',
            title="Thời gian giao hàng trung bình theo trạng thái đơn hàng",
            labels={'order_status': 'Trạng thái đơn hàng', 'delivery_time': 'Thời gian giao hàng (ngày)'},
            color='delivery_time',
            color_continuous_scale=px.colors.sequential.Viridis
        )
        st.plotly_chart(fig, use_container_width=True)
        ### 7. Phân tích tỷ lệ huỷ đơn hàng
        st.subheader("Tỷ lệ trạng thái đơn hàng")
        
        # Tính số lượng và tỷ lệ huỷ đơn hàng
        order_status_counts = merged_data['order_status'].value_counts(normalize=True).reset_index()
        order_status_counts.columns = ['order_status', 'percentage']
        order_status_counts['percentage'] *= 100  # Đổi thành %
        
        # Vẽ biểu đồ tỷ lệ trạng thái đơn hàng
        fig = px.pie(
            order_status_counts,
            names='order_status',
            values='percentage',
            title="Tỷ lệ trạng thái đơn hàng",
            color='order_status',
            color_discrete_sequence=px.colors.sequential.RdBu
        )
        st.plotly_chart(fig, use_container_width=True)

    
    with tab3:
        st.header("Phân tích khách hàng")
        
        # Phân tích đánh giá khách hàng
        st.subheader("Đánh giá của khách hàng")
        review_scores = order_reviews['review_score'].value_counts().sort_index().reset_index()
        review_scores.columns = ['review_score', 'count']
        
        fig = px.bar(
            review_scores,
            x='review_score',
            y='count',
            title="Phân bố điểm đánh giá của khách hàng",
            labels={'review_score': 'Điểm đánh giá', 'count': 'Số lượng'},
            color='review_score',
            color_continuous_scale=px.colors.sequential.RdBu
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Phân tích thời gian giao hàng và ảnh hưởng đến đánh giá
        st.subheader("Thời gian giao hàng và ảnh hưởng đến đánh giá")
        
        # Tính thời gian giao hàng (ngày)
        delivery_time = orders.copy()
    # Trong phần phân tích thời gian giao hàng
        if 'order_delivered_customer_date' in delivery_time.columns and 'order_purchase_timestamp' in delivery_time.columns:
            delivery_time['delivery_time'] = (delivery_time['order_delivered_customer_date'] - 
                                            delivery_time['order_purchase_timestamp']).dt.total_seconds() / (24*60*60)
            
        # Chỉ lấy đơn hàng đã giao thành công
        delivery_time = delivery_time[delivery_time['order_status'] == 'delivered']
        
        # Kết hợp với đánh giá
        delivery_review = delivery_time.merge(order_reviews[['order_id', 'review_score']], on='order_id', how='left')
        delivery_review = delivery_review.dropna(subset=['delivery_time', 'review_score'])
        
        # Tạo nhóm thời gian giao hàng
        bins = [0, 5, 10, 15, 20, 30, 100]
        labels = ['0-5 ngày', '6-10 ngày', '11-15 ngày', '16-20 ngày', '21-30 ngày', '>30 ngày']
        delivery_review['delivery_time_group'] = pd.cut(delivery_review['delivery_time'], bins=bins, labels=labels)
        
        # Tính điểm đánh giá trung bình cho mỗi nhóm
        delivery_score = delivery_review.groupby('delivery_time_group')['review_score'].mean().reset_index()
        
        fig = px.bar(
            delivery_score,
            x='delivery_time_group',
            y='review_score',
            title="Điểm đánh giá trung bình theo thời gian giao hàng",
            labels={'delivery_time_group': 'Thời gian giao hàng', 'review_score': 'Điểm đánh giá TB'},
            color='review_score',
            color_continuous_scale=px.colors.sequential.Viridis
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Phân tích RFM 
        if RFM_log_scaled_df is not None:
            st.subheader("Phân tích RFM")
            # Tạo biểu đồ 3D
            fig = px.scatter_3d(
                RFM_log_scaled_df,
                x='recency',  
                y='frequency',
                z='monetary',
                color='Cluster',
                title='RFM Clusters in 3D',
                labels={'recency': 'Recency', 'frequency': 'Frequency', 'monetary': 'Monetary'}
            )

            # Tùy chỉnh biểu đồ
            fig.update_traces(marker=dict(size=5))  # Điều chỉnh kích thước điểm
            fig.update_layout(scene=dict(
                xaxis_title='Recency',
                yaxis_title='Frequency',
                zaxis_title='Monetary'
            ))

            # Hiển thị biểu đồ trong Streamlit
            st.subheader("Phân tích RFM - Clusters Visualization")
            st.plotly_chart(fig, use_container_width=True)
    with tab4:
        st.header("Phân tích sản phẩm")
        
        # Thêm tên danh mục tiếng Anh
        merged_products = products.merge(product_category, 
                                         left_on='product_category_name', 
                                         right_on='product_category_name', 
                                         how='left')
        
        # Top 10 danh mục sản phẩm bán chạy nhất
        st.subheader("Top 10 danh mục sản phẩm bán chạy nhất")
        
        # Kết hợp dữ liệu để tìm danh mục phổ biến nhất
        product_order = order_items.merge(merged_products, on='product_id', how='left')
        category_counts = product_order['product_category_name_english'].value_counts().reset_index()
        category_counts.columns = ['category', 'count']
        category_counts = category_counts.head(10)  # Lấy top 10
        
        fig = px.bar(
            category_counts,
            x='count',
            y='category',
            title="Top 10 danh mục sản phẩm bán chạy nhất",
            labels={'count': 'Số lượng bán', 'category': 'Danh mục'},
            orientation='h',
            color='count',
            color_continuous_scale=px.colors.sequential.Blues
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Phân tích giá sản phẩm theo danh mục
        st.subheader("Giá trung bình theo danh mục sản phẩm")
        
        # Tính giá trung bình cho mỗi danh mục
        category_price = product_order.groupby('product_category_name_english')['price'].mean().reset_index()
        category_price = category_price.sort_values('price', ascending=False).head(10)  # Top 10 danh mục đắt nhất
        
        fig = px.bar(
            category_price,
            x='price',
            y='product_category_name_english',
            title="Top 10 danh mục sản phẩm có giá trung bình cao nhất",
            labels={'price': 'Giá trung bình (R$)', 'product_category_name_english': 'Danh mục'},
            orientation='h',
            color='price',
            color_continuous_scale=px.colors.sequential.Reds
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Phân tích kích thước sản phẩm
        st.subheader("Phân tích trọng lượng sản phẩm theo danh mục")
        
        # Lọc bỏ các giá trị bất thường
        weight_analysis = merged_products[merged_products['product_weight_g'] > 0]
        weight_analysis = weight_analysis[weight_analysis['product_weight_g'] < 30000]  # Loại bỏ các sản phẩm quá nặng
        
        # Tính trọng lượng trung bình cho mỗi danh mục
        category_weight = weight_analysis.groupby('product_category_name_english')['product_weight_g'].mean().reset_index()
        category_weight = category_weight.sort_values('product_weight_g', ascending=False).head(10)
        
        fig = px.bar(
            category_weight,
            x='product_weight_g',
            y='product_category_name_english',
            title="Top 10 danh mục sản phẩm nặng nhất",
            labels={'product_weight_g': 'Trọng lượng TB (g)', 'product_category_name_english': 'Danh mục'},
            orientation='h',
            color='product_weight_g',
            color_continuous_scale=px.colors.sequential.Greens
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with tab5:
        st.header("Bản đồ phân bố khách hàng và người bán")
        
        # Chuẩn bị dữ liệu khách hàng theo tiểu bang
        customer_states = customers['customer_state'].value_counts().reset_index()
        customer_states.columns = ['state', 'customer_count']
        
        # Chuẩn bị dữ liệu người bán theo tiểu bang
        seller_states = sellers['seller_state'].value_counts().reset_index()
        seller_states.columns = ['state', 'seller_count']
        
        # Kết hợp dữ liệu khách hàng và người bán
        combined_states = customer_states.merge(seller_states, on='state', how='outer').fillna(0)
        
        # Tạo cột tỷ lệ khách hàng/người bán
        combined_states['customer_seller_ratio'] = combined_states['customer_count'] / combined_states['seller_count'].replace(0, 0.1)
        
        # Tạo tabs con trong tab bản đồ
        map_tab1, map_tab2, map_tab3, map_tab4, map_tab5 = st.tabs(["Khách hàng (Choropleth)", "Người bán (Choropleth)", "So sánh", "Tỷ lệ", "Bản đồ chi tiết"])
        
        with map_tab1:
            st.subheader("Phân bố khách hàng theo tiểu bang")
            
            fig = px.choropleth(
                customer_states,
                locations='state',
                color='customer_count',
                title="Số lượng khách hàng theo tiểu bang",
                labels={'customer_count': 'Số khách hàng', 'state': 'Tiểu bang'},
                color_continuous_scale=px.colors.sequential.Plasma,
                scope="south america"
            )
            fig.update_geos(
                visible=False,
                projection_type="mercator",
                lataxis_range=[-33.7, 5.2],
                lonaxis_range=[-73.9, -34.7]
            )
            st.plotly_chart(fig, use_container_width=True)
            
            # Hiển thị bảng dữ liệu
            st.dataframe(customer_states.sort_values('customer_count', ascending=False))
        
        with map_tab2:
            st.subheader("Phân bố người bán theo tiểu bang")
            
            fig = px.choropleth(
                seller_states,
                locations='state',
                color='seller_count',
                title="Số lượng người bán theo tiểu bang",
                labels={'seller_count': 'Số người bán', 'state': 'Tiểu bang'},
                color_continuous_scale=px.colors.sequential.Viridis,
                scope="south america"
            )
            fig.update_geos(
                visible=False,
                projection_type="mercator",
                lataxis_range=[-33.7, 5.2],
                lonaxis_range=[-73.9, -34.7]
            )
            st.plotly_chart(fig, use_container_width=True)
            
            # Hiển thị bảng dữ liệu
            st.dataframe(seller_states.sort_values('seller_count', ascending=False))
        
        with map_tab3:
            st.subheader("So sánh phân bố khách hàng và người bán")
            
            # Tạo biểu đồ cột so sánh
            top_states = combined_states.sort_values('customer_count', ascending=False).head(10)
            
            fig = px.bar(
                top_states,
                x='state',
                y=['customer_count', 'seller_count'],
                title="So sánh số lượng khách hàng và người bán tại 10 tiểu bang hàng đầu",
                labels={'state': 'Tiểu bang', 'value': 'Số lượng', 'variable': 'Loại'},
                barmode='group',
                color_discrete_map={'customer_count': '#636EFA', 'seller_count': '#00CC96'}
            )
            fig.update_layout(legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            ))
            st.plotly_chart(fig, use_container_width=True)
            
            # Hiển thị bảng dữ liệu
            st.dataframe(combined_states[['state', 'customer_count', 'seller_count']].sort_values('customer_count', ascending=False))
        
        with map_tab4:
            st.subheader("Tỷ lệ khách hàng/người bán theo tiểu bang")
            
            fig = px.choropleth(
                combined_states,
                locations='state',
                color='customer_seller_ratio',
                title="Tỷ lệ khách hàng/người bán theo tiểu bang",
                labels={'customer_seller_ratio': 'Tỷ lệ KH/NB', 'state': 'Tiểu bang'},
                color_continuous_scale=px.colors.sequential.RdBu,
                scope="south america"
            )
            fig.update_geos(
                visible=False,
                projection_type="mercator",
                lataxis_range=[-33.7, 5.2],
                lonaxis_range=[-73.9, -34.7]
            )
            st.plotly_chart(fig, use_container_width=True)
            
            # Hiển thị bảng dữ liệu với tỷ lệ
            ratio_df = combined_states[['state', 'customer_count', 'seller_count', 'customer_seller_ratio']]
            ratio_df = ratio_df.sort_values('customer_seller_ratio', ascending=False)
            st.dataframe(ratio_df)
            
            # Phân tích tỷ lệ
            st.write("""
            ### Phân tích tỷ lệ khách hàng/người bán
            
            - **Tỷ lệ cao**: Tiểu bang có nhiều khách hàng nhưng ít người bán - cơ hội kinh doanh tiềm năng
            - **Tỷ lệ thấp**: Tiểu bang có nhiều người bán so với số lượng khách hàng - thị trường cạnh tranh cao
            """)
        
        with map_tab5:
            st.subheader("Bản đồ chi tiết phân bố khách hàng và người bán")
            
            # Xử lý dữ liệu địa lý
            # Lấy tọa độ trung bình cho mỗi tiểu bang từ dữ liệu geolocation
            geo_data = olist_geolocation_dataset.copy()
            
            # Tính tọa độ trung bình cho mỗi tiểu bang
            state_locations = geo_data.groupby('geolocation_state')[['geolocation_lat', 'geolocation_lng']].mean().reset_index()
            
            # Kết hợp với dữ liệu khách hàng và người bán
            customer_geo = customer_states.merge(state_locations, left_on='state', right_on='geolocation_state', how='left')
            seller_geo = seller_states.merge(state_locations, left_on='state', right_on='geolocation_state', how='left')
            
            # Tạo bản đồ với Plotly
            fig = go.Figure()
            
            # Thêm đường viền Brazil
            fig.add_trace(go.Scattergeo(
                lon=state_locations['geolocation_lng'],
                lat=state_locations['geolocation_lat'],
                mode='lines',
                line=dict(width=1, color='gray'),
                name='Brazil'
            ))
            
            # Thêm điểm khách hàng
            fig.add_trace(go.Scattergeo(
                lon=customer_geo['geolocation_lng'],
                lat=customer_geo['geolocation_lat'],
                text=customer_geo['state'] + '<br>Số khách hàng: ' + customer_geo['customer_count'].astype(str),
                mode='markers',
                marker=dict(
                    size=customer_geo['customer_count'] / customer_geo['customer_count'].max() * 50,
                    color='blue',
                    opacity=0.7,
                    line=dict(width=1, color='white')
                ),
                name='Khách hàng'
            ))
            
            # Thêm điểm người bán
            fig.add_trace(go.Scattergeo(
                lon=seller_geo['geolocation_lng'],
                lat=seller_geo['geolocation_lat'],
                text=seller_geo['state'] + '<br>Số người bán: ' + seller_geo['seller_count'].astype(str),
                mode='markers',
                marker=dict(
                    size=seller_geo['seller_count'] / seller_geo['seller_count'].max() * 50,
                    color='green',
                    opacity=0.7,
                    line=dict(width=1, color='white')
                ),
                name='Người bán'
            ))
            
            # Cấu hình bản đồ
            fig.update_geos(
                visible=True,
                resolution=50,
                scope='south america',
                showcountries=True,
                countrycolor='gray',
                showcoastlines=True,
                coastlinecolor='gray',
                showland=True,
                landcolor='lightgray',
                showocean=True,
                oceancolor='aliceblue',
                projection_type='mercator',
                lataxis_range=[-33.7, 5.2],
                lonaxis_range=[-73.9, -34.7]
            )
            
            fig.update_layout(
                title='Phân bố khách hàng và người bán trên bản đồ Brazil',
                height=700,
                legend=dict(
                    orientation="h",
                    yanchor="bottom",
                    y=1.02,
                    xanchor="right",
                    x=1
                )
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Thêm bộ lọc để hiển thị chỉ khách hàng hoặc người bán
            st.subheader("Lọc hiển thị trên bản đồ")
            display_option = st.radio(
                "Hiển thị:",
                ("Cả khách hàng và người bán", "Chỉ khách hàng", "Chỉ người bán")
            )
            
            if display_option != "Cả khách hàng và người bán":
                fig = go.Figure()
                
                # Thêm đường viền Brazil
                fig.add_trace(go.Scattergeo(
                    lon=state_locations['geolocation_lng'],
                    lat=state_locations['geolocation_lat'],
                    mode='lines',
                    line=dict(width=1, color='gray'),
                    name='Brazil'
                ))
                
                if display_option == "Chỉ khách hàng":
                    # Thêm điểm khách hàng
                    fig.add_trace(go.Scattergeo(
                        lon=customer_geo['geolocation_lng'],
                        lat=customer_geo['geolocation_lat'],
                        text=customer_geo['state'] + '<br>Số khách hàng: ' + customer_geo['customer_count'].astype(str),
                        mode='markers',
                        marker=dict(
                            size=customer_geo['customer_count'] / customer_geo['customer_count'].max() * 50,
                            color='blue',
                            opacity=0.7,
                            line=dict(width=1, color='white')
                        ),
                        name='Khách hàng'
                    ))
                    title = 'Phân bố khách hàng trên bản đồ Brazil'
                else:
                    # Thêm điểm người bán
                    fig.add_trace(go.Scattergeo(
                        lon=seller_geo['geolocation_lng'],
                        lat=seller_geo['geolocation_lat'],
                        text=seller_geo['state'] + '<br>Số người bán: ' + seller_geo['seller_count'].astype(str),
                        mode='markers',
                        marker=dict(
                            size=seller_geo['seller_count'] / seller_geo['seller_count'].max() * 50,
                            color='green',
                            opacity=0.7,
                            line=dict(width=1, color='white')
                        ),
                        name='Người bán'
                    ))
                    title = 'Phân bố người bán trên bản đồ Brazil'
                
                # Cấu hình bản đồ
                fig.update_geos(
                    visible=True,
                    resolution=50,
                    scope='south america',
                    showcountries=True,
                    countrycolor='gray',
                    showcoastlines=True,
                    coastlinecolor='gray',
                    showland=True,
                    landcolor='lightgray',
                    showocean=True,
                    oceancolor='aliceblue',
                    projection_type='mercator',
                    lataxis_range=[-33.7, 5.2],
                    lonaxis_range=[-73.9, -34.7]
                )
                
                fig.update_layout(
                    title=title,
                    height=700
                )
                
                st.plotly_chart(fig, use_container_width=True)
            
            # Thêm phân tích mật độ khách hàng theo thành phố
            st.subheader("Phân tích mật độ khách hàng theo thành phố")
            
            # Lấy top 20 thành phố có nhiều khách hàng nhất
            customer_cities = customers['customer_city'].value_counts().reset_index()
            customer_cities.columns = ['city', 'customer_count']
            top_cities = customer_cities.head(20)
            
            fig = px.bar(
                top_cities,
                x='customer_count',
                y='city',
                title="Top 20 thành phố có nhiều khách hàng nhất",
                labels={'customer_count': 'Số khách hàng', 'city': 'Thành phố'},
                orientation='h',
                color='customer_count',
                color_continuous_scale=px.colors.sequential.Plasma
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Hiển thị bảng dữ liệu
            st.dataframe(top_cities)
            
            # Thêm bản đồ nhiệt (heatmap) nếu có đủ dữ liệu
            st.subheader("Bản đồ nhiệt phân bố khách hàng")
            st.write("Bản đồ nhiệt hiển thị mật độ khách hàng trên toàn Brazil")
            
            # Kết hợp dữ liệu khách hàng với tọa độ
            # Lấy mẫu ngẫu nhiên từ dữ liệu địa lý để tạo bản đồ nhiệt (để tránh quá tải)
            if len(geo_data) > 1000:
                geo_sample = geo_data.sample(1000, random_state=42)
            else:
                geo_sample = geo_data
                
            # Tạo bản đồ nhiệt
            fig = go.Figure()
            
            fig.add_trace(go.Densitymapbox(
                lat=geo_sample['geolocation_lat'],
                lon=geo_sample['geolocation_lng'],
                z=[1] * len(geo_sample),  # Tạo danh sách các giá trị 1 có cùng độ dài với dữ liệu
                radius=10,
                colorscale='Viridis',
                showscale=False,
                name='Mật độ khách hàng'
            ))
            
            fig.update_layout(
                title='Bản đồ nhiệt phân bố khách hàng',
                mapbox=dict(
                    style='carto-positron',
                    center=dict(lat=-15.0, lon=-55.0),
                    zoom=3
                ),
                height=700
            )
            
            st.plotly_chart(fig, use_container_width=True)
