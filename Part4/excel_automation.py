"""
===================================================================
Python Excel Automation Script (Single Script – End to End)
===================================================================

WHAT THIS SCRIPT DOES:
---------------------
1. Reads Excel data
2. Removes rows with missing values
3. Calculates total sales amount
4. Adds business status (High / Medium / Low)
5. Creates a summary sheet
6. Applies conditional formatting (colors)
7. Creates Excel charts (Bar + Pie)
8. Saves final professional Excel file

INPUT  FILE : sales_data.xlsx
OUTPUT FILE : Final_Excel_Report.xlsx
===================================================================
"""

# ============================================================
# IMPORT REQUIRED LIBRARIES
# ============================================================

# pandas is used for reading and processing Excel data
import pandas as pd

# load_workbook is used to reopen Excel for formatting and charts
from openpyxl import load_workbook

# PatternFill is used to apply background colors to Excel cells
from openpyxl.styles import PatternFill

# Chart-related classes from openpyxl
from openpyxl.chart import BarChart, PieChart, Reference


# ============================================================
# FILE CONFIGURATION
# ============================================================

# Input Excel file name
INPUT_FILE = "sales_data.xlsx"

# Output Excel file name
OUTPUT_FILE = "Final_Excel_Report.xlsx"


# ============================================================
# STEP 1: READ EXCEL FILE
# ============================================================

# Read Excel file into pandas DataFrame
# DataFrame = Excel table inside Python
df = pd.read_excel(INPUT_FILE)

print("Excel file loaded successfully")


# ============================================================
# STEP 2: DATA CLEANING
# ============================================================

# Remove rows that contain empty values
# inplace=True modifies the original DataFrame
df.dropna(inplace=True)

print("Missing rows removed")


# ============================================================
# STEP 3: ADD CALCULATED COLUMN
# ============================================================

# Create new column "Total Amount"
# Formula: Quantity * Price
df["Total Amount"] = df["Quantity"] * df["Price"]

print("Total Amount column created")


# ============================================================
# STEP 4: ADD STATUS COLUMN (BUSINESS LOGIC)
# ============================================================

def sales_status(amount):
    """
    Decide sales category based on Total Amount.

    Rules:
    - >= 100000 -> High
    - >= 50000  -> Medium
    - < 50000   -> Low
    """
    if amount >= 100000:
        return "High"
    elif amount >= 50000:
        return "Medium"
    else:
        return "Low"


# Apply business logic to each row
df["Sales Status"] = df["Total Amount"].apply(sales_status)

print("Sales Status column added")


# ============================================================
# STEP 5: CREATE SUMMARY REPORT
# ============================================================

# Create a separate DataFrame for summary
summary_df = pd.DataFrame({
    "Metric": [
        "Total Revenue",
        "Total Orders",
        "High Sales Orders",
        "Medium Sales Orders",
        "Low Sales Orders"
    ],
    "Value": [
        df["Total Amount"].sum(),                    # Sum of sales
        len(df),                                     # Number of orders
        (df["Sales Status"] == "High").sum(),        # High count
        (df["Sales Status"] == "Medium").sum(),      # Medium count
        (df["Sales Status"] == "Low").sum()          # Low count
    ]
})

print("Summary report generated")


# ============================================================
# STEP 6: WRITE DATA TO EXCEL
# ============================================================

# ExcelWriter allows multiple sheets in one Excel file
with pd.ExcelWriter(OUTPUT_FILE, engine="openpyxl") as writer:

    # Write main sales data
    df.to_excel(
        writer,
        sheet_name="Sales Data",
        index=False
    )

    # Write summary data
    summary_df.to_excel(
        writer,
        sheet_name="Summary",
        index=False
    )

print("Data written to Excel file")


# ============================================================
# STEP 7: APPLY CONDITIONAL FORMATTING
# ============================================================

# Load the Excel file again for formatting
wb = load_workbook(OUTPUT_FILE)

# Select Sales Data sheet
ws = wb["Sales Data"]

# Define background color styles using HEX color codes

# Green color for High sales
high_fill = PatternFill(
    start_color="C6EFCE",
    end_color="C6EFCE",
    fill_type="solid"
)

# Yellow color for Medium sales
medium_fill = PatternFill(
    start_color="FFEB9C",
    end_color="FFEB9C",
    fill_type="solid"
)

# Red color for Low sales
low_fill = PatternFill(
    start_color="FFC7CE",
    end_color="FFC7CE",
    fill_type="solid"
)

# Loop through each data row (skip header row)
for row in range(2, ws.max_row + 1):

    # Column F contains "Sales Status"
    status_cell = ws[f"F{row}"]

    # Apply color based on status value
    if status_cell.value == "High":
        status_cell.fill = high_fill
    elif status_cell.value == "Medium":
        status_cell.fill = medium_fill
    elif status_cell.value == "Low":
        status_cell.fill = low_fill

print("Conditional formatting applied")


# ============================================================
# STEP 8: CREATE EXCEL CHARTS
# ============================================================

# Create a new sheet named "Charts"
chart_sheet = wb.create_sheet(title="Charts")


# -------------------------------
# BAR CHART: Product vs Total Amount
# -------------------------------

bar_chart = BarChart()
bar_chart.title = "Product Wise Total Sales"
bar_chart.x_axis.title = "Product"
bar_chart.y_axis.title = "Total Amount"

# Data for bar chart (Total Amount column - Column E)
data = Reference(
    ws,
    min_col=5,
    min_row=1,
    max_row=ws.max_row
)

# Categories for bar chart (Product column - Column B)
categories = Reference(
    ws,
    min_col=2,
    min_row=2,
    max_row=ws.max_row
)

bar_chart.add_data(data, titles_from_data=True)
bar_chart.set_categories(categories)

chart_sheet.add_chart(bar_chart, "A1")


# -------------------------------
# PIE CHART: Sales Status Distribution
# -------------------------------

pie_chart = PieChart()
pie_chart.title = "Sales Status Distribution"

# Labels (High, Medium, Low)
labels = Reference(
    wb["Summary"],
    min_col=1,
    min_row=4,
    max_row=6
)

# Values for pie chart
data = Reference(
    wb["Summary"],
    min_col=2,
    min_row=4,
    max_row=6
)

pie_chart.add_data(data, titles_from_data=False)
pie_chart.set_categories(labels)

chart_sheet.add_chart(pie_chart, "A20")


# ============================================================
# FINAL SAVE
# ============================================================

# Save the Excel file with all formatting and charts
wb.save(OUTPUT_FILE)

print("Charts created successfully")
print("Excel Automation Completed Successfully")
