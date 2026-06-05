import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Page Config
st.set_page_config(
    page_title="TATA Motors Dashboard",
    page_icon="🚗",
    layout="wide"
)

# Load Data
@st.cache_data
def load_data():
    df = pd.read_csv('TATA_car_sales_cleaned.csv')
    df['total_revenue'] = df['units_sold'] * df['average_sale_price']
    bins = [18, 30, 45, 60, 75]
    labels = ['18-30', '31-45', '46-60', '60+']
    df['age_group'] = pd.cut(df['customer_age'], bins=bins, labels=labels)
    return df

df = load_data()

# Sidebar
st.sidebar.image('TATA_motors_logo.png', width=200)
st.sidebar.title("Navigation")
page = st.sidebar.radio(
    "Go to",
    [" Home", " Revenue Analysis", " Customer Insights", " Competitor Conquest", " Discount & Operations"]
)

# Sidebar Filters
st.sidebar.markdown("---")
st.sidebar.subheader(" Filters")
selected_year = st.sidebar.multiselect("Select Year", sorted(df['year'].unique()), default=sorted(df['year'].unique()))
selected_region = st.sidebar.multiselect("Select Region", df['region'].unique(), default=df['region'].unique())
selected_country = st.sidebar.multiselect("Select Country", df['country'].unique(), default=df['country'].unique())

# Filter Data
df_filtered = df[
    (df['year'].isin(selected_year)) &
    (df['region'].isin(selected_region)) &
    (df['country'].isin(selected_country))
]

# ============================================================
# HOME PAGE
# ============================================================
if page == " Home":
    st.title(" TATA Motors Sales Intelligence Dashboard")
    st.markdown("### Global Sales Performance | 2015-2024 | 7 Countries | 250K Records")
    st.markdown("---")

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Records", f"{len(df_filtered):,}")
    with col2:
        st.metric("Countries", df_filtered['country'].nunique())
    with col3:
        st.metric("Car Models", df_filtered['car_model'].nunique())
    with col4:
        st.metric("Years", f"{df_filtered['year'].min()} - {df_filtered['year'].max()}")

# ============================================================
# REVENUE ANALYSIS PAGE
# ============================================================
elif page == " Revenue Analysis":
    st.title(" Revenue Analysis")
    st.markdown("---")

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Revenue", f"${df_filtered['total_revenue'].sum()/1e9:.2f}B")
    with col2:
        st.metric("Total Units Sold", f"{df_filtered['units_sold'].sum():,}")
    with col3:
        st.metric("Avg Sale Price", f"${df_filtered['average_sale_price'].mean():,.0f}")

    st.markdown("---")

    # Year wise Revenue
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Year-wise Revenue Trend")
        yearly = df_filtered.groupby('year')['total_revenue'].sum() / 1e9
        fig, ax = plt.subplots(figsize=(8, 4))
        ax.plot(yearly.index, yearly.values, marker='o', color='steelblue', linewidth=2)
        ax.set_xlabel('Year')
        ax.set_ylabel('Revenue (Billions)')
        for x, y in zip(yearly.index, yearly.values):
            ax.text(x, y + 0.005, f'{y:.2f}B', ha='center', fontsize=8)
        plt.tight_layout()
        st.pyplot(fig)

    with col2:
        st.subheader("Top 5 Car Models by Units Sold")
        top5 = df_filtered.groupby('car_model')['units_sold'].sum().sort_values(ascending=False).head(5)
        fig, ax = plt.subplots(figsize=(8, 4))
        ax.bar(top5.index, top5.values, color='steelblue')
        ax.set_xlabel('Car Model')
        ax.set_ylabel('')
        ax.set_yticks([])
        for x, y in zip(top5.index, top5.values):
            ax.text(x, y + 10000, f'{y/1e7:.2f}Cr', ha='center', fontsize=8)
        plt.tight_layout()
        st.pyplot(fig)

    # Region wise Revenue
    st.subheader("Region-wise Revenue")
    region_rev = df_filtered.groupby('region')['total_revenue'].sum() / 1e9
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.bar(region_rev.index, region_rev.values, color='steelblue')
    ax.set_yticks([])
    for x, y in zip(region_rev.index, region_rev.values):
        ax.text(x, y + 0.005, f'{y:.2f}B', ha='center', fontsize=9)
    plt.tight_layout()
    st.pyplot(fig)

# ============================================================
# CUSTOMER INSIGHTS PAGE
# ============================================================
elif page == " Customer Insights":
    st.title(" Customer Insights")
    st.markdown("---")

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Age Group vs Income Group")
        age_income = df_filtered.groupby(['age_group', 'customer_income_group'])['units_sold'].sum().unstack()
        fig, ax = plt.subplots(figsize=(8, 5))
        sns.heatmap(age_income, annot=True, fmt=',', cmap='Blues', ax=ax)
        plt.tight_layout()
        st.pyplot(fig)

    with col2:
        st.subheader("Test Drive vs Units Sold")
        test = df_filtered.groupby('test_drive')['units_sold'].sum()
        fig, ax = plt.subplots(figsize=(6, 4))
        ax.bar(['No Test Drive', 'Test Drive'], test.values, color=['steelblue', 'orange'])
        ax.set_yticks([])
        for x, y in zip(['No Test Drive', 'Test Drive'], test.values):
            ax.text(x, y + 50000, f'{y/1e7:.2f}Cr', ha='center', fontsize=9)
        plt.tight_layout()
        st.pyplot(fig)

# ============================================================
# COMPETITOR CONQUEST PAGE
# ============================================================
elif page == " Competitor Conquest":
    st.title(" Competitor Conquest Analysis")
    st.markdown("---")

    st.subheader("Previous Brand Migration")
    conquest = df_filtered[df_filtered['previous_car_brand'] != 'Unknown'].groupby('previous_car_brand')['units_sold'].sum().sort_values(ascending=False).head(8)
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.bar(conquest.index, conquest.values, color='steelblue')
    ax.set_yticks([])
    for x, y in zip(conquest.index, conquest.values):
        ax.text(x, y + 100000, f'{y/1e7:.2f}Cr', ha='center', fontsize=8)
    plt.tight_layout()
    st.pyplot(fig)

# ============================================================
# DISCOUNT & OPERATIONS PAGE
# ============================================================
elif page == " Discount & Operations":
    st.title(" Discount & Operations Analysis")
    st.markdown("---")

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Discount Leakage Analysis")
        discount = df_filtered.groupby('discount_reason')['dealer_discount_pct'].mean().sort_values(ascending=False)
        colors = ['crimson' if x == 'No Discount' else 'steelblue' for x in discount.index]
        fig, ax = plt.subplots(figsize=(8, 4))
        ax.bar(discount.index, discount.values, color=colors)
        ax.set_yticks([])
        for x, y in zip(discount.index, discount.values):
            ax.text(x, y + 0.05, f'{y:.2f}%', ha='center', fontsize=9)
        plt.tight_layout()
        st.pyplot(fig)

    with col2:
        st.subheader("Delivery Time vs Customer Rating")
        delivery = df_filtered.groupby('delivery_time_days')['customer_rating'].mean().reset_index()
        fig, ax = plt.subplots(figsize=(8, 4))
        ax.scatter(delivery['delivery_time_days'], delivery['customer_rating'], color='steelblue', alpha=0.6)
        ax.set_xlabel('Delivery Time (Days)')
        ax.set_ylabel('Avg Customer Rating')
        plt.tight_layout()
        st.pyplot(fig)