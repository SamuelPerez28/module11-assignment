# module11-assignment.py
# Module 11 Assignment: Data Visualization with Matplotlib
# SunCoast Retail Visual Analysis

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Welcome message
print("=" * 60)
print("SUNCOAST RETAIL VISUAL ANALYSIS")
print("=" * 60)

# ----- USE THE FOLLOWING CODE TO CREATE SAMPLE DATA (DO NOT MODIFY) -----
# Create a seed for reproducibility
np.random.seed(42)

# Generate dates for 8 quarters (Q1 2022 - Q4 2023)
quarters = pd.date_range(start='2022-01-01', periods=8, freq='Q')
quarter_labels = ['Q1 2022', 'Q2 2022', 'Q3 2022', 'Q4 2022',
                  'Q1 2023', 'Q2 2023', 'Q3 2023', 'Q4 2023']

# Store locations
locations = ['Tampa', 'Miami', 'Orlando', 'Jacksonville']

# Product categories
categories = ['Electronics', 'Clothing', 'Home Goods', 'Sporting Goods', 'Beauty']

# Generate quarterly sales data for each location and category
quarterly_data = []

for quarter_idx, quarter in enumerate(quarters):
    for location in locations:
        for category in categories:
            # Base sales with seasonal pattern (Q4 higher, Q1 lower)
            base_sales = np.random.normal(loc=100000, scale=20000)
            seasonal_factor = 1.0
            if quarter.quarter == 4:  # Q4 (holiday boost)
                seasonal_factor = 1.3
            elif quarter.quarter == 1:  # Q1 (post-holiday dip)
                seasonal_factor = 0.8

            # Location effect
            location_factor = {
                'Tampa': 1.0,
                'Miami': 1.2,
                'Orlando': 0.9,
                'Jacksonville': 0.8
            }[location]

            # Category effect
            category_factor = {
                'Electronics': 1.5,
                'Clothing': 1.0,
                'Home Goods': 0.8,
                'Sporting Goods': 0.7,
                'Beauty': 0.9
            }[category]

            # Growth trend over time (5% per year, quarterly compounded)
            growth_factor = (1 + 0.05/4) ** quarter_idx

            # Calculate sales with some randomness
            sales = base_sales * seasonal_factor * location_factor * category_factor * growth_factor
            sales = sales * np.random.normal(loc=1.0, scale=0.1)  # Add noise

            # Advertising spend (correlated with sales but with diminishing returns)
            ad_spend = (sales ** 0.7) * 0.05 * np.random.normal(loc=1.0, scale=0.2)

            # Record
            quarterly_data.append({
                'Quarter': quarter,
                'QuarterLabel': quarter_labels[quarter_idx],
                'Location': location,
                'Category': category,
                'Sales': round(sales, 2),
                'AdSpend': round(ad_spend, 2),
                'Year': quarter.year
            })

# Create customer data
customer_data = []
total_customers = 2000

# Age distribution parameters for each location
age_params = {
    'Tampa': (45, 15),      # Older demographic
    'Miami': (35, 12),      # Younger demographic
    'Orlando': (38, 14),    # Mixed demographic
    'Jacksonville': (42, 13)  # Middle-aged demographic
}

for location in locations:
    # Generate ages based on location demographics
    mean_age, std_age = age_params[location]
    customer_count = int(total_customers * {
        'Tampa': 0.3,
        'Miami': 0.35,
        'Orlando': 0.2,
        'Jacksonville': 0.15
    }[location])

    ages = np.random.normal(loc=mean_age, scale=std_age, size=customer_count)
    ages = np.clip(ages, 18, 80).astype(int)  # Ensure ages are between 18-80

    # Generate purchase amounts
    for age in ages:
        # Younger and older customers spend differently across categories
        if age < 30:
            category_preference = np.random.choice(categories, p=[0.3, 0.3, 0.1, 0.2, 0.1])
        elif age < 50:
            category_preference = np.random.choice(categories, p=[0.25, 0.2, 0.25, 0.15, 0.15])
        else:
            category_preference = np.random.choice(categories, p=[0.15, 0.1, 0.35, 0.1, 0.3])

        # Purchase amount based on age and category
        base_amount = np.random.gamma(shape=5, scale=20)

        # Product tier (budget, mid-range, premium)
        price_tier = np.random.choice(['Budget', 'Mid-range', 'Premium'],
                                      p=[0.3, 0.5, 0.2])

        tier_factor = {'Budget': 0.7, 'Mid-range': 1.0, 'Premium': 1.8}[price_tier]

        purchase_amount = base_amount * tier_factor

        customer_data.append({
            'Location': location,
            'Age': age,
            'Category': category_preference,
            'PurchaseAmount': round(purchase_amount, 2),
            'PriceTier': price_tier
        })

# Create DataFrames
sales_df = pd.DataFrame(quarterly_data)
customer_df = pd.DataFrame(customer_data)

# Add some calculated columns
sales_df['Quarter_Num'] = sales_df['Quarter'].dt.quarter
sales_df['SalesPerDollarSpent'] = sales_df['Sales'] / sales_df['AdSpend']

# Print data info
print("\nSales Data Sample:")
print(sales_df.head())
print("\nCustomer Data Sample:")
print(customer_df.head())
print("\nDataFrames created successfully. Ready for visualization!")
# ----- END OF DATA CREATION -----


# TODO 1: Time Series Visualization - Sales Trends
# 1.1 Create a line chart showing overall quarterly sales trends
# REQUIRED: Function must create and return a matplotlib figure
def plot_quarterly_sales_trend():
    """
    Create a line chart showing total sales for each quarter.
    REQUIRED: Return the figure object
    """
    fig, ax = plt.subplots(figsize=(10, 5))

    total_sales = sales_df.groupby("QuarterLabel")["Sales"].sum()
    ax.plot(total_sales.index, total_sales.values, marker='o', linewidth=2)

    ax.set_title("Total Quarterly Sales Trend")
    ax.set_xlabel("Quarter")
    ax.set_ylabel("Total Sales ($)")
    ax.grid(True)

    return fig


# 1.2 Create a multi-line chart comparing sales trends across locations
# REQUIRED: Function must create and return a matplotlib figure
def plot_location_sales_comparison():
    """
    Create a multi-line chart comparing quarterly sales across different locations.
    REQUIRED: Return the figure object
    """
    fig, ax = plt.subplots(figsize=(10, 5))

    for loc in locations:
        loc_sales = (sales_df[sales_df["Location"] == loc]
                     .groupby("QuarterLabel")["Sales"].sum())
        ax.plot(loc_sales.index, loc_sales.values, marker='o', label=loc)

    ax.set_title("Quarterly Sales Comparison by Location")
    ax.set_xlabel("Quarter")
    ax.set_ylabel("Sales ($)")
    ax.legend(title="Location")
    ax.grid(True)

    return fig


# TODO 2: Categorical Comparison - Product Performance by Location
# 2.1 Create a grouped bar chart comparing category performance by location
# REQUIRED: Function must create and return a matplotlib figure
def plot_category_performance_by_location():
    """
    Create a grouped bar chart showing how each product category performs in different locations.
    Focus on the most recent quarter.
    REQUIRED: Return the figure object
    """
    fig, ax = plt.subplots(figsize=(10, 6))

    latest_quarter = sales_df["QuarterLabel"].iloc[-1]
    latest_data = sales_df[sales_df["QuarterLabel"] == latest_quarter]

    pivot = latest_data.pivot_table(values="Sales",
                                    index="Category",
                                    columns="Location",
                                    aggfunc="sum")

    pivot.plot(kind="bar", ax=ax)
    ax.set_title(f"Category Performance by Location ({latest_quarter})")
    ax.set_xlabel("Category")
    ax.set_ylabel("Sales ($)")
    ax.legend(title="Location")

    return fig


# 2.2 Create a stacked bar chart showing the composition of sales in each location
# REQUIRED: Function must create and return a matplotlib figure
def plot_sales_composition_by_location():
    """
    Create a stacked bar chart showing the composition of sales across categories for each location.
    REQUIRED: Return the figure object
    """
    fig, ax = plt.subplots(figsize=(10, 6))

    pivot = sales_df.pivot_table(values="Sales",
                                 index="Location",
                                 columns="Category",
                                 aggfunc="sum")

    pivot_percent = pivot.div(pivot.sum(axis=1), axis=0)

    pivot_percent.plot(kind="bar", stacked=True, ax=ax)
    ax.set_title("Sales Composition by Category for Each Location")
    ax.set_xlabel("Location")
    ax.set_ylabel("Percentage of Sales")

    return fig


# TODO 3: Relationship Analysis - Advertising and Sales
# 3.1 Create a scatter plot to examine the relationship between ad spend and sales
# REQUIRED: Function must create and return a matplotlib figure
def plot_ad_spend_vs_sales():
    """
    Create a scatter plot to visualize the relationship between advertising spend and sales.
    REQUIRED: Return the figure object
    """
    fig, ax = plt.subplots(figsize=(8, 6))

    ax.scatter(sales_df["AdSpend"], sales_df["Sales"], alpha=0.6)

    # Best-fit line
    m, b = np.polyfit(sales_df["AdSpend"], sales_df["Sales"], 1)
    ax.plot(sales_df["AdSpend"], m * sales_df["AdSpend"] + b, color='red')

    ax.set_title("Ad Spend vs Sales")
    ax.set_xlabel("Advertising Spend ($)")
    ax.set_ylabel("Sales ($)")

    return fig


# 3.2 Create a line chart showing sales per dollar spent on advertising over time
# REQUIRED: Function must create and return a matplotlib figure
def plot_ad_efficiency_over_time():
    """
    Create a line chart showing how efficient advertising spend has been over time.
    REQUIRED: Return the figure object
    """
    fig, ax = plt.subplots(figsize=(10, 5))

    efficiency = sales_df.groupby("QuarterLabel")["SalesPerDollarSpent"].mean()

    ax.plot(efficiency.index, efficiency.values, marker='o')
    ax.set_title("Advertising Efficiency Over Time")
    ax.set_xlabel("Quarter")
    ax.set_ylabel("Sales per Dollar Spent")

    return fig


# TODO 4: Distribution Analysis - Customer Demographics
# 4.1 Create histograms of customer age distribution
# REQUIRED: Function must create and return a matplotlib figure with subplots
def plot_customer_age_distribution():
    """
    Create histograms showing the age distribution of customers, both overall and by location.
    REQUIRED: Return the figure object
    """
    # 3x2 grid: 1 overall + 4 locations + 1 extra (hidden)
    fig, axes = plt.subplots(3, 2, figsize=(12, 12))
    axes = axes.flatten()

    # Overall distribution
    overall = customer_df["Age"]
    axes[0].hist(overall, bins=20, color='skyblue')
    axes[0].axvline(overall.mean(), color='red', linestyle='--', label='Mean')
    axes[0].axvline(overall.median(), color='green', linestyle='--', label='Median')
    axes[0].set_title("Overall Age Distribution")
    axes[0].set_xlabel("Age")
    axes[0].set_ylabel("Frequency")
    axes[0].legend()

    # One subplot per location
    for i, loc in enumerate(locations, start=1):
        ages = customer_df[customer_df["Location"] == loc]["Age"]
        axes[i].hist(ages, bins=20)
        axes[i].axvline(ages.mean(), color='red', linestyle='--')
        axes[i].axvline(ages.median(), color='green', linestyle='--')
        axes[i].set_title(f"Age Distribution - {loc}")
        axes[i].set_xlabel("Age")
        axes[i].set_ylabel("Frequency")

    # Hide any unused subplot
    for j in range(len(locations) + 1, len(axes)):
        axes[j].axis('off')

    return fig


# 4.2 Create box plots comparing purchase amounts by age groups
# REQUIRED: Function must create and return a matplotlib figure
def plot_purchase_by_age_group():
    """
    Create box plots showing purchase amounts across different age groups.
    REQUIRED: Return the figure object
    """
    fig, ax = plt.subplots(figsize=(10, 6))

    bins = [18, 30, 45, 60, 80]
    labels = ["18-30", "31-45", "46-60", "61+"]

    customer_df["AgeGroup"] = pd.cut(customer_df["Age"], bins=bins, labels=labels, right=True)

    data = [customer_df[customer_df["AgeGroup"] == group]["PurchaseAmount"] for group in labels]

    ax.boxplot(data, labels=labels)
    ax.set_title("Purchase Amount by Age Group")
    ax.set_xlabel("Age Group")
    ax.set_ylabel("Purchase Amount ($)")

    return fig


# TODO 5: Sales Distribution - Pricing Tiers
# 5.1 Create a histogram of purchase amounts
# REQUIRED: Function must create and return a matplotlib figure
def plot_purchase_amount_distribution():
    """
    Create a histogram showing the distribution of purchase amounts.
    REQUIRED: Return the figure object
    """
    fig, ax = plt.subplots(figsize=(8, 5))

    ax.hist(customer_df["PurchaseAmount"], bins=30, color='purple', alpha=0.7)
    ax.set_title("Distribution of Purchase Amounts")
    ax.set_xlabel("Purchase Amount ($)")
    ax.set_ylabel("Frequency")

    return fig


# 5.2 Create a pie chart showing sales breakdown by price tier
# REQUIRED: Function must create and return a matplotlib figure
def plot_sales_by_price_tier():
    """
    Create a pie chart showing the breakdown of sales by price tier.
    REQUIRED: Return the figure object
    """
    fig, ax = plt.subplots(figsize=(7, 7))

    tier_sales = customer_df.groupby("PriceTier")["PurchaseAmount"].sum()
    explode = [0.1 if x == tier_sales.max() else 0 for x in tier_sales]

    ax.pie(tier_sales, labels=tier_sales.index, autopct='%1.1f%%', explode=explode)
    ax.set_title("Sales by Price Tier")

    return fig


# TODO 6: Market Share Analysis
# 6.1 Create a pie chart showing sales breakdown by category
# REQUIRED: Function must create and return a matplotlib figure
def plot_category_market_share():
    """
    Create a pie chart showing the market share of each product category.
    REQUIRED: Return the figure object
    """
    fig, ax = plt.subplots(figsize=(7, 7))

    category_sales = sales_df.groupby("Category")["Sales"].sum()
    explode = [0.1 if x == category_sales.max() else 0 for x in category_sales]

    ax.pie(category_sales, labels=category_sales.index, autopct='%1.1f%%', explode=explode)
    ax.set_title("Market Share by Product Category")

    return fig


# 6.2 Create a pie chart showing sales breakdown by location
# REQUIRED: Function must create and return a matplotlib figure
def plot_location_sales_distribution():
    """
    Create a pie chart showing the distribution of sales across different store locations.
    REQUIRED: Return the figure object
    """
    fig, ax = plt.subplots(figsize=(7, 7))

    location_sales = sales_df.groupby("Location")["Sales"].sum()

    ax.pie(location_sales, labels=location_sales.index, autopct='%1.1f%%')
    ax.set_title("Sales Distribution by Location")

    return fig


# TODO 7: Comprehensive Dashboard
# REQUIRED: Function must create and return a matplotlib figure with at least 4 subplots
def create_business_dashboard():
    """
    Create a comprehensive dashboard with multiple subplots highlighting key business insights.
    REQUIRED: Return the figure object with at least 4 subplots
    """
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))

    # Subplot 1: Quarterly sales trend
    total_sales = sales_df.groupby("QuarterLabel")["Sales"].sum()
    axes[0, 0].plot(total_sales.index, total_sales.values, marker='o')
    axes[0, 0].set_title("Quarterly Sales Trend")
    axes[0, 0].set_xlabel("Quarter")
    axes[0, 0].set_ylabel("Sales ($)")
    axes[0, 0].tick_params(axis='x', rotation=45)

    # Subplot 2: Sales by price tier
    tier_sales = customer_df.groupby("PriceTier")["PurchaseAmount"].sum()
    axes[0, 1].pie(tier_sales, labels=tier_sales.index, autopct='%1.1f%%')
    axes[0, 1].set_title("Sales by Price Tier")

    # Subplot 3: Category market share
    category_sales = sales_df.groupby("Category")["Sales"].sum()
    axes[1, 0].bar(category_sales.index, category_sales.values)
    axes[1, 0].set_title("Category Market Share")
    axes[1, 0].set_xlabel("Category")
    axes[1, 0].set_ylabel("Sales ($)")
    axes[1, 0].tick_params(axis='x', rotation=45)

    # Subplot 4: Ad efficiency over time
    efficiency = sales_df.groupby("QuarterLabel")["SalesPerDollarSpent"].mean()
    axes[1, 1].plot(efficiency.index, efficiency.values, marker='o')
    axes[1, 1].set_title("Ad Efficiency Over Time")
    axes[1, 1].set_xlabel("Quarter")
    axes[1, 1].set_ylabel("Sales per Dollar Spent")
    axes[1, 1].tick_params(axis='x', rotation=45)

    fig.suptitle("SunCoast Retail Business Dashboard", fontsize=16)

    fig.tight_layout(rect=[0, 0.03, 1, 0.95])

    return fig


# Main function to execute all visualizations
# REQUIRED: Do not modify this function name
def main():
    print("\n" + "=" * 60)
    print("SUNCOAST RETAIL VISUAL ANALYSIS RESULTS")
    print("=" * 60)

    # Time Series Analysis
    fig1 = plot_quarterly_sales_trend()
    fig2 = plot_location_sales_comparison()

    # Categorical Comparison
    fig3 = plot_category_performance_by_location()
    fig4 = plot_sales_composition_by_location()

    # Relationship Analysis
    fig5 = plot_ad_spend_vs_sales()
    fig6 = plot_ad_efficiency_over_time()

    # Distribution Analysis
    fig7 = plot_customer_age_distribution()
    fig8 = plot_purchase_by_age_group()

    # Sales Distribution
    fig9 = plot_purchase_amount_distribution()
    fig10 = plot_sales_by_price_tier()

    # Market Share Analysis
    fig11 = plot_category_market_share()
    fig12 = plot_location_sales_distribution()

    # Comprehensive Dashboard
    fig13 = create_business_dashboard()

    # REQUIRED: Add business insights summary
    print("\nKEY BUSINESS INSIGHTS:")
    print("- Sales show clear seasonal patterns, with Q4 consistently outperforming other quarters.")
    print("- Miami emerges as a top-performing location, especially in high-value categories like Electronics and Beauty.")
    print("- Advertising spend is positively correlated with sales, but efficiency fluctuates by quarter.")
    print("- Age distributions differ by location, which likely drives different category preferences and spending levels.")
    print("- Premium-tier purchases, while fewer, contribute a disproportionately large share of total revenue.")
    print("- Electronics dominate overall category market share, suggesting continued strategic focus is warranted.")

    # Display all figures
    plt.show()


# Run the main function
if __name__ == "__main__":
    main()
