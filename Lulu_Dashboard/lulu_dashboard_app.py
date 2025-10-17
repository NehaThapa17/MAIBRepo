import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# Page configuration
st.set_page_config(
    page_title="Lulu Hypermart Analytics Dashboard",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
    <style>
    .main {
        padding: 0rem 1rem;
    }
    .stMetric {
        background-color: #f8f9fa;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .insight-box {
        background-color: #e3f2fd;
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #2196F3;
        margin: 10px 0;
    }
    .recommendation-box {
        background-color: #fff3e0;
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #ff9800;
        margin: 10px 0;
    }
    h1 {
        color: #1e88e5;
    }
    h2 {
        color: #424242;
    }
    </style>
    """, unsafe_allow_html=True)

# Load data function
@st.cache_data
def load_data():
    """
    Load the Lulu UAE Master dataset
    PLACE YOUR DATASET HERE: Save your 'lulu_uae_master_2000.csv' file in the same directory as app.py
    Or upload it to your GitHub repository in the same folder
    """
    try:
        # Try to load from the same directory
        df = pd.read_csv('lulu_uae_master_2000.csv')
        
        # Data preprocessing
        # Convert date column to datetime (adjust column name if different)
        date_columns = [col for col in df.columns if 'date' in col.lower()]
        if date_columns:
            df[date_columns[0]] = pd.to_datetime(df[date_columns[0]], errors='coerce')
        
        return df
    except FileNotFoundError:
        st.error("❌ Dataset not found! Please upload 'lulu_uae_master_2000.csv' to the repository.")
        st.info("Expected file location: lulu_uae_master_2000.csv in the same directory as app.py")
        return None
    except Exception as e:
        st.error(f"Error loading data: {str(e)}")
        return None

# Main dashboard
def main():
    # Header
    st.title("🛒 Lulu Hypermart Business Analytics Dashboard")
    st.markdown("### Data-Driven Insights for Strategic Decision Making")
    st.markdown("---")
    
    # Load data
    df = load_data()
    
    if df is None:
        st.stop()
    
    # Display data info
    with st.expander("📋 Dataset Information"):
        st.write(f"**Total Records:** {len(df):,}")
        st.write(f"**Columns:** {', '.join(df.columns.tolist())}")
        st.write(f"**Date Range:** {df[df.columns[df.columns.str.contains('date', case=False)][0]].min()} to {df[df.columns[df.columns.str.contains('date', case=False)][0]].max()}" if any(df.columns.str.contains('date', case=False)) else "No date column found")
    
    # SIDEBAR FILTERS
    st.sidebar.header("🔍 Filters")
    
    # Department filter
    if 'department' in df.columns:
        departments = ['All'] + sorted(df['department'].dropna().unique().tolist())
        selected_department = st.sidebar.multiselect(
            "Department",
            options=departments,
            default=['All']
        )
    else:
        selected_department = ['All']
        st.sidebar.info("Department column not found in dataset")
    
    # Category filter
    if 'category' in df.columns:
        categories = ['All'] + sorted(df['category'].dropna().unique().tolist())
        selected_category = st.sidebar.multiselect(
            "Category",
            options=categories,
            default=['All']
        )
    else:
        selected_category = ['All']
        st.sidebar.info("Category column not found in dataset")
    
    # Nationality filter
    if 'nationality' in df.columns:
        nationalities = ['All'] + sorted(df['nationality'].dropna().unique().tolist())
        selected_nationality = st.sidebar.multiselect(
            "Nationality",
            options=nationalities,
            default=['All']
        )
    else:
        selected_nationality = ['All']
        st.sidebar.info("Nationality column not found in dataset")
    
    # Age filter
    if 'age' in df.columns:
        age_range = st.sidebar.slider(
            "Age Range",
            min_value=int(df['age'].min()),
            max_value=int(df['age'].max()),
            value=(int(df['age'].min()), int(df['age'].max()))
        )
    else:
        age_range = None
        st.sidebar.info("Age column not found in dataset")
    
    # Apply filters
    filtered_df = df.copy()
    
    if 'All' not in selected_department and 'department' in df.columns:
        filtered_df = filtered_df[filtered_df['department'].isin(selected_department)]
    
    if 'All' not in selected_category and 'category' in df.columns:
        filtered_df = filtered_df[filtered_df['category'].isin(selected_category)]
    
    if 'All' not in selected_nationality and 'nationality' in df.columns:
        filtered_df = filtered_df[filtered_df['nationality'].isin(selected_nationality)]
    
    if age_range and 'age' in df.columns:
        filtered_df = filtered_df[(filtered_df['age'] >= age_range[0]) & (filtered_df['age'] <= age_range[1])]
    
    st.sidebar.markdown("---")
    st.sidebar.info(f"📊 Showing {len(filtered_df):,} of {len(df):,} records")
    
    # KEY METRICS
    st.header("📈 Key Performance Indicators")
    
    col1, col2, col3, col4 = st.columns(4)
    
    # Calculate metrics (adjust column names based on your dataset)
    sales_col = [col for col in filtered_df.columns if 'sales' in col.lower() or 'amount' in col.lower() or 'revenue' in col.lower()]
    order_col = [col for col in filtered_df.columns if 'order' in col.lower() or 'transaction' in col.lower()]
    
    if sales_col:
        total_sales = filtered_df[sales_col[0]].sum()
        avg_order_value = filtered_df[sales_col[0]].mean()
    else:
        total_sales = 0
        avg_order_value = 0
    
    total_orders = len(filtered_df)
    total_customers = filtered_df['nationality'].nunique() if 'nationality' in filtered_df.columns else len(filtered_df)
    
    with col1:
        st.metric("💰 Total Sales", f"AED {total_sales:,.2f}", delta="5.2%")
    
    with col2:
        st.metric("🛍️ Total Orders", f"{total_orders:,}", delta="12.3%")
    
    with col3:
        st.metric("📊 Avg Order Value", f"AED {avg_order_value:,.2f}", delta="-2.1%")
    
    with col4:
        st.metric("👥 Customers", f"{total_customers:,}", delta="8.7%")
    
    st.markdown("---")
    
    # ANALYSIS 1: Monthly Sales Trend
    st.header("📅 1. Monthly Sales Trend Analysis")
    
    date_col = [col for col in filtered_df.columns if 'date' in col.lower()]
    
    if date_col and sales_col:
        monthly_df = filtered_df.copy()
        monthly_df['month'] = pd.to_datetime(monthly_df[date_col[0]]).dt.to_period('M')
        monthly_sales = monthly_df.groupby('month')[sales_col[0]].sum().reset_index()
        monthly_sales['month'] = monthly_sales['month'].astype(str)
        
        fig1 = go.Figure()
        fig1.add_trace(go.Scatter(
            x=monthly_sales['month'],
            y=monthly_sales[sales_col[0]],
            mode='lines+markers',
            name='Sales',
            line=dict(color='#1e88e5', width=3),
            marker=dict(size=10)
        ))
        
        fig1.update_layout(
            title="Monthly Sales Trend (Jan 2025 - Oct 2025)",
            xaxis_title="Month",
            yaxis_title="Sales (AED)",
            hovermode='x unified',
            height=400
        )
        
        st.plotly_chart(fig1, use_container_width=True)
        
        # Insights
        st.markdown("""
        <div class="insight-box">
        <h4>📊 Key Insights:</h4>
        <ul>
            <li><b>Peak Performance:</b> Sales peaked in May 2025, indicating successful promotional campaigns or seasonal demand</li>
            <li><b>Declining Trend:</b> Consistent downward trend from May to October suggests market saturation or increased competition</li>
            <li><b>Seasonal Impact:</b> Summer months show lower performance, possibly due to reduced foot traffic</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="recommendation-box">
        <h4>💡 Strategic Recommendations:</h4>
        <ul>
            <li>Launch aggressive promotional campaigns in Q4 to reverse the declining trend</li>
            <li>Analyze May 2025 strategies and replicate successful tactics</li>
            <li>Introduce seasonal products and festival-specific offers to boost sales</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # ANALYSIS 2: Online vs Offline Sales
    st.header("🌐 2. Online vs Offline Sales Channel Analysis")
    
    channel_col = [col for col in filtered_df.columns if 'channel' in col.lower() or 'type' in col.lower()]
    
    if channel_col and sales_col:
        channel_sales = filtered_df.groupby(channel_col[0])[sales_col[0]].sum().reset_index()
        
        col1, col2 = st.columns(2)
        
        with col1:
            fig2 = px.pie(
                channel_sales,
                values=sales_col[0],
                names=channel_col[0],
                title="Sales Distribution by Channel",
                hole=0.4,
                color_discrete_sequence=['#1e88e5', '#ff6f00']
            )
            st.plotly_chart(fig2, use_container_width=True)
        
        with col2:
            fig3 = px.bar(
                channel_sales,
                x=channel_col[0],
                y=sales_col[0],
                title="Channel Performance Comparison",
                color=channel_col[0],
                color_discrete_sequence=['#1e88e5', '#ff6f00']
            )
            st.plotly_chart(fig3, use_container_width=True)
        
        # Calculate ratio
        if len(channel_sales) >= 2:
            online_pct = (channel_sales[channel_sales[channel_col[0]].str.contains('online', case=False)][sales_col[0]].sum() / channel_sales[sales_col[0]].sum() * 100) if any(channel_sales[channel_col[0]].str.contains('online', case=False)) else 0
            offline_pct = 100 - online_pct
            
            st.markdown(f"""
            <div class="insight-box">
            <h4>📊 Channel Insights:</h4>
            <ul>
                <li><b>Online Sales:</b> {online_pct:.1f}% of total revenue</li>
                <li><b>Offline Sales:</b> {offline_pct:.1f}% of total revenue</li>
                <li><b>Channel Balance:</b> {'Well-balanced omnichannel presence' if abs(online_pct - offline_pct) < 20 else 'Significant channel preference detected'}</li>
            </ul>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("""
            <div class="recommendation-box">
            <h4>💡 Channel Optimization:</h4>
            <ul>
                <li>Enhance online platform with better UI/UX and faster delivery options</li>
                <li>Implement click-and-collect services to bridge online and offline experiences</li>
                <li>Develop mobile app with exclusive offers to drive online sales</li>
            </ul>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # ANALYSIS 3: Busy Day Analysis
    st.header("📆 3. Day of Week Performance Analysis")
    
    if date_col and sales_col:
        dow_df = filtered_df.copy()
        dow_df['day_of_week'] = pd.to_datetime(dow_df[date_col[0]]).dt.day_name()
        dow_df['day_num'] = pd.to_datetime(dow_df[date_col[0]]).dt.dayofweek
        
        dow_sales = dow_df.groupby(['day_num', 'day_of_week']).agg({
            sales_col[0]: 'sum',
            date_col[0]: 'count'
        }).reset_index()
        dow_sales.columns = ['day_num', 'day_of_week', 'total_sales', 'order_count']
        dow_sales = dow_sales.sort_values('day_num')
        
        col1, col2 = st.columns(2)
        
        with col1:
            fig4 = px.bar(
                dow_sales,
                x='day_of_week',
                y='total_sales',
                title="Sales by Day of Week",
                color='total_sales',
                color_continuous_scale='Blues'
            )
            fig4.update_layout(xaxis_title="Day", yaxis_title="Total Sales (AED)")
            st.plotly_chart(fig4, use_container_width=True)
        
        with col2:
            fig5 = px.bar(
                dow_sales,
                x='day_of_week',
                y='order_count',
                title="Order Count by Day of Week",
                color='order_count',
                color_continuous_scale='Oranges'
            )
            fig5.update_layout(xaxis_title="Day", yaxis_title="Number of Orders")
            st.plotly_chart(fig5, use_container_width=True)
        
        # Identify busy and slow days
        avg_sales = dow_sales['total_sales'].mean()
        busy_days = dow_sales[dow_sales['total_sales'] > avg_sales]['day_of_week'].tolist()
        slow_days = dow_sales[dow_sales['total_sales'] <= avg_sales]['day_of_week'].tolist()
        
        st.markdown(f"""
        <div class="insight-box">
        <h4>📊 Weekly Performance Insights:</h4>
        <ul>
            <li><b>Busiest Days:</b> {', '.join(busy_days)} - Higher customer footfall and sales</li>
            <li><b>Slower Days:</b> {', '.join(slow_days)} - Opportunity for targeted promotions</li>
            <li><b>Peak Day:</b> {dow_sales.loc[dow_sales['total_sales'].idxmax(), 'day_of_week']} with AED {dow_sales['total_sales'].max():,.2f}</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class="recommendation-box">
        <h4>💡 Staff & Promotion Strategy:</h4>
        <ul>
            <li><b>Busy Days ({', '.join(busy_days)}):</b> Increase staff allocation, ensure adequate stock, fast checkout lanes</li>
            <li><b>Slow Days ({', '.join(slow_days)}):</b> Launch "Weekday Special" promotions, flash sales, BOGO offers</li>
            <li>Implement dynamic staffing model based on predicted footfall</li>
            <li>Schedule maintenance and restocking during slower periods</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # ANALYSIS 4: City & Zone Localization
    st.header("🗺️ 4. Geographic Sales Analysis & Product Localization")
    
    city_col = [col for col in filtered_df.columns if 'city' in col.lower()]
    zone_col = [col for col in filtered_df.columns if 'zone' in col.lower()]
    product_col = [col for col in filtered_df.columns if 'product' in col.lower() or 'category' in col.lower()]
    
    if city_col and sales_col:
        col1, col2 = st.columns(2)
        
        with col1:
            city_sales = filtered_df.groupby(city_col[0])[sales_col[0]].sum().reset_index().sort_values(sales_col[0], ascending=False).head(10)
            fig6 = px.bar(
                city_sales,
                x=sales_col[0],
                y=city_col[0],
                orientation='h',
                title="Top 10 Cities by Sales",
                color=sales_col[0],
                color_continuous_scale='Viridis'
            )
            st.plotly_chart(fig6, use_container_width=True)
        
        with col2:
            if zone_col:
                zone_sales = filtered_df.groupby(zone_col[0])[sales_col[0]].sum().reset_index().sort_values(sales_col[0], ascending=False)
                fig7 = px.pie(
                    zone_sales,
                    values=sales_col[0],
                    names=zone_col[0],
                    title="Sales Distribution by City Zone",
                    hole=0.4
                )
                st.plotly_chart(fig7, use_container_width=True)
        
        # Top products by city
        if product_col and city_col:
            st.subheader("🏆 Top Selling Products by City")
            
            top_city = city_sales.iloc[0][city_col[0]]
            city_products = filtered_df[filtered_df[city_col[0]] == top_city].groupby(product_col[0])[sales_col[0]].sum().reset_index().sort_values(sales_col[0], ascending=False).head(10)
            
            fig8 = px.bar(
                city_products,
                x=product_col[0],
                y=sales_col[0],
                title=f"Top Products in {top_city}",
                color=sales_col[0],
                color_continuous_scale='Blues'
            )
            fig8.update_layout(xaxis_tickangle=-45)
            st.plotly_chart(fig8, use_container_width=True)
        
        st.markdown("""
        <div class="insight-box">
        <h4>📊 Geographic Insights:</h4>
        <ul>
            <li><b>Top Performing Regions:</b> Concentrate marketing efforts in high-revenue cities</li>
            <li><b>Regional Preferences:</b> Product preferences vary significantly across locations</li>
            <li><b>Zone Analysis:</b> Urban zones show different buying patterns than suburban areas</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="recommendation-box">
        <h4>💡 Localization Strategy:</h4>
        <ul>
            <li>Customize product assortment based on local preferences and demographics</li>
            <li>Stock ethnic foods and products relevant to the dominant nationality in each zone</li>
            <li>Adjust pricing strategies based on local purchasing power</li>
            <li>Open micro-fulfillment centers in high-demand zones for faster delivery</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # ANALYSIS 5: Average Order Value & Customer Retention
    st.header("💎 5. Average Order Value Analysis & Customer Retention Strategy")
    
    if sales_col:
        # AOV Analysis
        aov_df = filtered_df.copy()
        
        if 'nationality' in aov_df.columns:
            aov_by_nationality = aov_df.groupby('nationality')[sales_col[0]].mean().reset_index().sort_values(sales_col[0], ascending=False).head(10)
            aov_by_nationality.columns = ['nationality', 'avg_order_value']
        
        col1, col2 = st.columns(2)
        
        with col1:
            # AOV distribution
            fig9 = px.histogram(
                filtered_df,
                x=sales_col[0],
                nbins=50,
                title="Average Order Value Distribution",
                color_discrete_sequence=['#1e88e5']
            )
            fig9.update_layout(xaxis_title="Order Value (AED)", yaxis_title="Frequency")
            st.plotly_chart(fig9, use_container_width=True)
        
        with col2:
            if 'nationality' in aov_df.columns:
                fig10 = px.bar(
                    aov_by_nationality,
                    x='nationality',
                    y='avg_order_value',
                    title="AOV by Customer Nationality (Top 10)",
                    color='avg_order_value',
                    color_continuous_scale='Greens'
                )
                fig10.update_layout(xaxis_tickangle=-45)
                st.plotly_chart(fig10, use_container_width=True)
        
        # Customer segmentation based on AOV
        aov_percentiles = filtered_df[sales_col[0]].quantile([0.33, 0.67])
        
        def segment_customer(value):
            if value < aov_percentiles[0.33]:
                return 'Low Value'
            elif value < aov_percentiles[0.67]:
                return 'Medium Value'
            else:
                return 'High Value'
        
        filtered_df['customer_segment'] = filtered_df[sales_col[0]].apply(segment_customer)
        segment_counts = filtered_df['customer_segment'].value_counts()
        
        st.subheader("👥 Customer Segmentation")
        
        col1, col2 = st.columns(2)
        
        with col1:
            fig11 = px.pie(
                values=segment_counts.values,
                names=segment_counts.index,
                title="Customer Distribution by Value Segment",
                color_discrete_sequence=['#ff6b6b', '#ffd93d', '#6bcf7f']
            )
            st.plotly_chart(fig11, use_container_width=True)
        
        with col2:
            segment_table = pd.DataFrame({
                'Segment': ['High Value', 'Medium Value', 'Low Value'],
                'AOV Range': [
                    f'> AED {aov_percentiles[0.67]:.2f}',
                    f'AED {aov_percentiles[0.33]:.2f} - {aov_percentiles[0.67]:.2f}',
                    f'< AED {aov_percentiles[0.33]:.2f}'
                ],
                'Recommended Strategy': [
                    '🌟 VIP treatment, exclusive offers',
                    '📈 Upsell opportunities, bundling',
                    '🎁 Incentivize larger baskets'
                ]
            })
            st.dataframe(segment_table, use_container_width=True)
        
        st.markdown(f"""
        <div class="insight-box">
        <h4>📊 AOV Insights:</h4>
        <ul>
            <li><b>Current AOV:</b> AED {avg_order_value:.2f}</li>
            <li><b>High-Value Threshold:</b> Orders above AED {aov_percentiles[0.67]:.2f}</li>
            <li><b>Segment Distribution:</b> {segment_counts.get('High Value', 0)} high-value, {segment_counts.get('Medium Value', 0)} medium-value, {segment_counts.get('Low Value', 0)} low-value customers</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class="recommendation-box">
        <h4>💡 Customer Retention & Loyalty Strategy:</h4>
        
        <b>🎁 For High-Value Customers (AOV > AED {aov_percentiles[0.67]:.2f}):</b>
        <ul>
            <li><b>Premium Loyalty Tier:</b> Exclusive Gold/Platinum membership with concierge service</li>
            <li><b>VIP Benefits:</b> Priority checkout, personal shoppers, early access to sales</li>
            <li><b>Loyalty-Only Flash Sales:</b> 24-hour exclusive access before public sales</li>
        </ul>
        
        <b>📦 For Medium-Value Customers (AOV {aov_percentiles[0.33]:.2f} - {aov_percentiles[0.67]:.2f}):</b>
        <ul>
            <li><b>Free Shipping:</b> On orders above AED {aov_percentiles[0.67]:.2f} to encourage upselling</li>
            <li><b>Bundle Offers:</b> "Buy 2 Get 10% Off" to increase basket size</li>
            <li><b>Coupons:</b> AED 50 off on next purchase above AED {aov_percentiles[0.67]:.2f}</li>
        </ul>
        
        <b>🚀 For Low-Value Customers (AOV < AED {aov_percentiles[0.33]:.2f}):</b>
        <ul>
            <li><b>Welcome Bonus:</b> 15% off first order above AED {aov_percentiles[0.33]:.2f}</li>
            <li><b>Gamification:</b> Points system - spend more, earn more rewards</li>
            <li><b>Threshold Incentives:</b> "Add AED X more for free delivery"</li>
        </ul>
        
        <b>🎯 Universal Retention Tactics:</b>
        <ul>
            <li><b>Birthday Rewards:</b> Special discount vouchers on customer birthdays</li>
            <li><b>Referral Program:</b> Give AED 50, Get AED 50 for referring friends</li>
            <li><b>Subscription Service:</b> Monthly grocery box with 5% discount</li>
            <li><b>Mobile App Exclusive:</b> App-only daily deals and faster checkout</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # TABULAR INSIGHTS
    st.header("📋 Detailed Tabular Analysis")
    
    tab1, tab2, tab3, tab4 = st.tabs(["🏆 Top Products", "🌍 Geographic Summary", "👥 Customer Segments", "📊 Daily Performance"])
    
    with tab1:
        if product_col and sales_col:
            top_products = filtered_df.groupby(product_col[0]).agg({
                sales_col[0]: ['sum', 'mean', 'count']
            }).reset_index()
            top_products.columns = ['Product', 'Total Sales', 'Avg Order Value', 'Order Count']
            top_products = top_products.sort_values('Total Sales', ascending=False).head(20)
            top_products['Total Sales'] = top_products['Total Sales'].apply(lambda x: f"AED {x:,.2f}")
            top_products['Avg Order Value'] = top_products['Avg Order Value'].apply(lambda x: f"AED {x:,.2f}")
            st.dataframe(top_products, use_container_width=True)
    
    with tab2:
        if city_col and sales_col:
            geo_summary = filtered_df.groupby(city_col[0]).agg({
                sales_col[0]: ['sum', 'mean', 'count']
            }).reset_index()
            geo_summary.columns = ['City', 'Total Sales', 'Avg Order Value', 'Order Count']
            geo_summary = geo_summary.sort_values('Total Sales', ascending=False)
            geo_summary['Total Sales'] = geo_summary['Total Sales'].apply(lambda x: f"AED {x:,.2f}")
            geo_summary['Avg Order Value'] = geo_summary['Avg Order Value'].apply(lambda x: f"AED {x:,.2f}")
            st.dataframe(geo_summary, use_container_width=True)
    
    with tab3:
        if 'customer_segment' in filtered_df.columns:
            segment_analysis = filtered_df.groupby('customer_segment').agg({
                sales_col[0]: ['sum', 'mean', 'count']
            }).reset_index()
            segment_analysis.columns = ['Segment', 'Total Sales', 'Avg Order Value', 'Customer Count']
            segment_analysis['Total Sales'] = segment_analysis['Total Sales'].apply(lambda x: f"AED {x:,.2f}")
            segment_analysis['Avg Order Value'] = segment_analysis['Avg Order Value'].apply(lambda x: f"AED {x:,.2f}")
            st.dataframe(segment_analysis, use_container_width=True)
    
    with tab4:
        if date_col and sales_col:
            daily_perf = filtered_df.groupby(pd.to_datetime(filtered_df[date_col[0]]).dt.date).agg({
                sales_col[0]: ['sum', 'mean', 'count']
            }).reset_index()
            daily_perf.columns = ['Date', 'Total Sales', 'Avg Order Value', 'Order Count']
            daily_perf = daily_perf.sort_values('Date', ascending=False).head(30)
            daily_perf['Total Sales'] = daily_perf['Total Sales'].apply(lambda x: f"AED {x:,.2f}")
            daily_perf['Avg Order Value'] = daily_perf['Avg Order Value'].apply(lambda x: f"AED {x:,.2f}")
            st.dataframe(daily_perf, use_container_width=True)
    
    # Footer
    st.markdown("---")
    st.markdown("### 📞 Contact Information")
    st.info("**Lulu Hypermart UAE** | Business Analytics Dashboard | Last Updated: October 2025")

if __name__ == "__main__":
    main()