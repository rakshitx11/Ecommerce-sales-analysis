import pandas as pd
import matplotlib.pyplot as plt
import os

# PROJECT SETUP
DATA_FILE = os.path.join(
    os.path.dirname(__file__),
    "data",
    "data.csv"
)
OUTPUT_FOLDER = "visualizations"

os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# LOAD DATA
def load_data():
    df = pd.read_csv(DATA_FILE)
    print("Data loaded successfully!")
    print("Number of rows:", len(df))
    print("Number of columns:", len(df.columns))
    return df


# DATA CLEANING
def clean_data(df):
    print(" \n========== DATA CLEANING ==========")
    # Check missing values
    print("\nMissing values:")
    print(df.isnull().sum())
    # Remove duplicate rows
    df = df.drop_duplicates()
    # Convert Date column
    df["Date"] = pd.to_datetime(df["Date"])

    # Convert numerical 
    df["Quantity"] = pd.to_numeric(df["Quantity"])
    df["Price"] = pd.to_numeric(df["Price"])
    df["Total_Sales"] = pd.to_numeric(df["Total_Sales"])

    # Remove rows with missing important values
    df = df.dropna(
        subset=[
            "Date",
            "Product",
            "Quantity",
            "Price",
            "Customer_ID",
            "Region",
            "Total_Sales"
        ]
    )

    # Remove invalid numerical values
    df = df[
        (df["Quantity"] > 0) &
        (df["Price"] >= 0) &
        (df["Total_Sales"] >= 0)
    ]

    print("\nData cleaning completed!")
    print("Final number of rows:", len(df))
    return df


# DATA EXPLORATION
def explore_data(df):
    print("\n========== DATA EXPLORATION ==========")
    print("\nFirst 5 rows:")
    print(df.head())

    print("\nDataset information:")
    df.info()

    print("\nStatistical summary:")
    print(df.describe())

    print("\nProducts:")
    print(df["Product"].unique())

    print("\nRegions:")
    print(df["Region"].unique())


# BASIC SALES ANALYSIS
def analyze_data(df):
    print("\n========== SALES ANALYSIS ==========")

    # Total sales
    total_sales = df["Total_Sales"].sum()

    # Average sale
    average_sales = df["Total_Sales"].mean()

    # Total quantity sold
    total_quantity = df["Quantity"].sum()

    # Sales by product
    product_sales = df.groupby("Product")["Total_Sales"].sum()

    # Quantity sold by product
    product_quantity = df.groupby("Product")["Quantity"].sum()

    # Sales by region
    region_sales = df.groupby("Region")["Total_Sales"].sum()

    # Best product by revenue
    best_product = product_sales.idxmax()
    best_product_sales = product_sales.max()

    # Product with highest quantity sold
    highest_quantity_product = product_quantity.idxmax()
    highest_quantity = product_quantity.max()

    # Best region
    best_region = region_sales.idxmax()
    best_region_sales = region_sales.max()

    # Unique customers
    unique_customers = df["Customer_ID"].nunique()


    # Display results
    print("\nTotal Sales: ₹", round(total_sales, 2))
    print("Average Sale: ₹", round(average_sales, 2))
    print("Total Quantity Sold:", total_quantity)
    print("Unique Customers:", unique_customers)

    print("\nBest Product by Revenue:", best_product)
    print("Revenue:", round(best_product_sales, 2))

    print("\nBest Product by Quantity Sold:", highest_quantity_product)
    print("Quantity Sold:", highest_quantity)

    print("\nBest Performing Region:", best_region)
    print("Regional Sales:", round(best_region_sales, 2))

    print("\nSales by Product:")
    print(product_sales.sort_values(ascending=False))

    print("\nSales by Region:")
    print(region_sales.sort_values(ascending=False))

    return (
        total_sales,
        average_sales,
        total_quantity,
        unique_customers,
        product_sales,
        product_quantity,
        region_sales,
        best_product,
        best_product_sales,
        highest_quantity_product,
        highest_quantity,
        best_region,
        best_region_sales
    )


# BAR CHART - SALES BY PRODUCT
def create_product_chart(product_sales):
    plt.figure(figsize=(9, 6))
    product_sales.sort_values(ascending=False).plot(kind="bar")
    plt.title("Total Sales by Product")
    plt.xlabel("Product")
    plt.ylabel("Total Sales (₹)")

    plt.xticks(rotation=0)
    plt.tight_layout()

    file_path = os.path.join(
        OUTPUT_FOLDER,
        "sales_by_product.png"
    )

    plt.savefig(file_path)
    plt.show()
    plt.close()
    print("\nProduct chart saved!")


# LINE CHART - MONTHLY SALES
def create_monthly_chart(df):
    monthly_sales = (
        df.groupby(df["Date"].dt.to_period("M"))["Total_Sales"]
        .sum()
    )
    # Convert month into string
    monthly_sales.index = monthly_sales.index.astype(str)
    plt.figure(figsize=(10, 6))
    plt.plot(
        monthly_sales.index,
        monthly_sales.values,
        marker="o"
    )

    plt.title("Monthly Sales Trend")
    plt.xlabel("Month")
    plt.ylabel("Total Sales (₹)")

    plt.xticks(rotation=45)
    plt.grid(True)

    plt.tight_layout()

    file_path = os.path.join(
        OUTPUT_FOLDER,
        "monthly_sales.png"
    )

    plt.savefig(file_path)
    plt.show()
    plt.close()
    print("Monthly sales chart saved!")

    return monthly_sales


# PIE CHART - SALES BY REGION
def create_region_chart(region_sales):
    plt.figure(figsize=(8, 8))
    plt.pie(
        region_sales.values,
        labels=region_sales.index,
        autopct="%1.1f%%",
        startangle=90
    )
    plt.title("Sales Distribution by Region")
    plt.tight_layout()
    file_path = os.path.join(
        OUTPUT_FOLDER,
        "sales_by_region.png"
    )

    plt.savefig(file_path)
    plt.show()
    plt.close()
    print("Region chart saved!")


# GENERATE KEY INSIGHTS
def generate_insights(
    total_sales,
    unique_customers,
    best_product,
    best_product_sales,
    highest_quantity_product,
    highest_quantity,
    best_region,
    best_region_sales,
    monthly_sales
):
    print("\n========== KEY INSIGHTS ==========")
    # Highest sales month
    best_month = monthly_sales.idxmax()
    best_month_sales = monthly_sales.max()

    # Lowest sales month
    lowest_month = monthly_sales.idxmin()
    lowest_month_sales = monthly_sales.min()

    # Percentage of total sales
    product_percentage = (
        best_product_sales / total_sales
    ) * 100

    region_percentage = (
        best_region_sales / total_sales
    ) * 100

    print(
        "1. Total revenue generated was ₹",
        round(total_sales, 2)
    )
    print(
        "2.", best_product,
        "generated the highest revenue of ₹",
        round(best_product_sales, 2),
        "which is",
        round(product_percentage, 1),
        "% of total sales."
    )
    print(
        "3.", highest_quantity_product,
        "had the highest quantity sold:",
        highest_quantity,
        "units."
    )
    print(
        "4.", best_region,
        "generated the highest regional sales of ₹",
        round(best_region_sales, 2),
        "which is",
        round(region_percentage, 1),
        "% of total sales."
    )
    print(
        "5.", best_month,
        "was the highest-sales month with ₹",
        round(best_month_sales, 2)
    )
    print(
        "6.", lowest_month,
        "was the lowest-sales month with ₹",
        round(lowest_month_sales, 2)
    )
    print(
        "7. The dataset contains",
        unique_customers,
        "unique customers."
    )

# MAIN PROGRAM
def main():
    print("====================================")
    print("     E-COMMERCE SALES ANALYSIS      ")
    print("====================================")
    df = load_data()
    df = clean_data(df)
    explore_data(df)
    results = analyze_data(df)

    # Take values from analysis
    total_sales = results[0]
    average_sales = results[1]
    total_quantity = results[2]
    unique_customers = results[3]
    product_sales = results[4]
    highest_quantity_product = results[9]
    highest_quantity = results[10]
    best_product = results[7]
    best_product_sales = results[8]
    region_sales = results[6]
    best_region = results[11]
    best_region_sales = results[12]

    # Create visualizations
    print("\n========== CREATING VISUALIZATIONS ==========")
    create_product_chart(product_sales)
    monthly_sales = create_monthly_chart(df)
    create_region_chart(region_sales)

    # Generate insights
    generate_insights(
        total_sales,
        unique_customers,
        best_product,
        best_product_sales,
        highest_quantity_product,
        highest_quantity,
        best_region,
        best_region_sales,
        monthly_sales
    )

    print("\n====================================")
    print("PROJECT COMPLETED SUCCESSFULLY!")
    print("====================================")
    print(
        "\nCharts are saved inside the 'visualizations' folder."
    )

main()
