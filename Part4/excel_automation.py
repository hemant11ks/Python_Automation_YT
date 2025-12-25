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
7. Creates Excel charts (Bar chart + Pie chart)
8. Saves final professional Excel file

INPUT  FILE : sales_data.xlsx
OUTPUT FILE : Final_Excel_Report.xlsx
===================================================================
"""

# ============================================================
# IMPORT REQUIRED LIBRARIES
# ============================================================

# pandas is used to read Excel and work with tabular data
import pandas as pd

# openpyxl is used to format Excel files and create charts
from openpyxl import load_workbook

# PatternFill is used to apply background colors to Excel cells
from openpyxl.styles import PatternFill

# Chart-related classes from openpyxl
from openpyxl.chart import BarChart, PieChart, Reference


# ============================================================
# FILE CONFIGURATION
# ============================================================

# Name of input Excel file
INPUT_FILE = "sales_data.xlsx"

# Name of output Excel file
OUTPUT_FILE = "Final_Excel_Report.xlsx"


# ============================================================
# STEP 1: READ EXCEL FILE
# ============================================================

# Read Excel file into a pandas DataFrame
# Think of DataFrame as an Excel table inside Python
df = pd.read_excel(INPUT_FILE)

print("Excel file loaded successfully")


# ============================================================
# STEP 2: DATA CLEANING
# ============================================================

# dropna() removes rows where ANY column is empty
# inplace=True means modify original DataFrame
df.dropna(inplace=True)

print("Missing rows removed")


# ============================================================
# STEP 3: ADD CALCULATED COLUMN
# ============================================================

# Create a new column "Total Amount"
# Formula used: Quantity * Price
df["Total Amount"] = df["Quantity"] * df["Price"]

print("Total Amount column created")


# ============================================================
# STEP 4: ADD STATUS COLUMN (BUSINESS LOGIC)
# ============================================================

def sales_status(amount):
    """
    This function decides sales category
    based on the Total Amount.
    """
    if amount >= 100000:
        return "High"
    elif amount >= 50000:
        return "Medium"
    else:
        return "Low"


# apply() runs the function on each value of Total Amount
df["Sales Status"] = df["Total Amount"].apply(sales_status)

print("Sales Status column added")


# ============================================================
# STEP 5: CREATE SUMMARY REPORT
# ============================================================

# Create a separate DataFrame for management summary
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
        len(df),                                     # Total rows
        (df["Sales Status"] == "High").sum(),        # High count
        (df["Sales Status"] == "Medium").sum(),      # Medium count
        (df["Sales Status"] == "Low").sum()          # Low count
    ]
})

print("Summary report generated")


# ============================================================
# STEP 6: WRITE DATA TO EXCEL
# ============================================================

# ExcelWriter allows writing multiple sheets in one Excel file
with pd.ExcelWriter(OUTPUT_FILE, engine="openpyxl") as writer:

    # Write sales data to first sheet
    df.to_excel(
        writer,
        sheet_name="Sales Data",
        index=False
    )

    # Write summary data to second sheet
    summary_df.to_excel(
        writer,
        sheet_name="Summary",
        index=False
    )

print("Data written to Excel file")


# ============================================================
# STEP 7: APPLY CONDITIONAL FORMATTING
# ============================================================

# Load Excel file again to apply formatting
wb = load_workbook(OUTPUT_FILE)

# Select the "Sales Data" sheet
ws = wb["Sales Data"]

# Define background colors using HEX color codes

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

# Loop through data rows (skip header row)
for row in range(2, ws.max_row + 1):

    # Column F contains Sales Status
    status_cell = ws[f"F{row}"]

    # Apply color based on cell value
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

# Create a new worksheet to hold charts
chart_sheet = wb.create_sheet(title="Charts")


# ------------------------------------------------------------
# BAR CHART: PRODUCT vs TOTAL AMOUNT
# ------------------------------------------------------------

# Create an empty BarChart object
bar_chart = BarChart()

# Set chart title
bar_chart.title = "Product Wise Total Sales"

# Set X-axis and Y-axis titles
bar_chart.x_axis.title = "Product"
bar_chart.y_axis.title = "Total Amount"

# Select numeric data (Total Amount column = Column E)
data = Reference(
    ws,                 # Sales Data sheet
    min_col=5,          # Column E
    min_row=1,          # Include header
    max_row=ws.max_row  # Till last data row
)

# Select category labels (Product column = Column B)
categories = Reference(
    ws,                 # Sales Data sheet
    min_col=2,          # Column B
    min_row=2,          # Skip header
    max_row=ws.max_row
)

# Attach numeric data to chart
bar_chart.add_data(data, titles_from_data=True)

# Attach category labels to chart
bar_chart.set_categories(categories)

# Place bar chart at cell A1 in Charts sheet
chart_sheet.add_chart(bar_chart, "A1")


# ------------------------------------------------------------
# PIE CHART: SALES STATUS DISTRIBUTION
# ------------------------------------------------------------

# Create an empty PieChart object
pie_chart = PieChart()

# Set pie chart title
pie_chart.title = "Sales Status Distribution"

# Select labels (High / Medium / Low) from Summary sheet
labels = Reference(
    wb["Summary"],      # Summary sheet
    min_col=1,          # Metric column
    min_row=4,          # High
    max_row=6           # Low
)

# Select numeric values from Summary sheet
data = Reference(
    wb["Summary"],      # Summary sheet
    min_col=2,          # Value column
    min_row=4,
    max_row=6
)

# Attach numeric data to pie chart
pie_chart.add_data(data, titles_from_data=False)

# Attach labels to pie chart
pie_chart.set_categories(labels)

# Place pie chart below bar chart
chart_sheet.add_chart(pie_chart, "A20")


# ============================================================
# FINAL SAVE
# ============================================================

# Save Excel file with all formatting and charts
wb.save(OUTPUT_FILE)

print("Charts created successfully")
print("Excel Automation Completed Successfully")
