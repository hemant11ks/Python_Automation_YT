"""
===================================================================
Python Excel Automation Script (Single Script – End to End)
===================================================================

This script will automatically:
1. Read Excel data
2. Clean missing values
3. Calculate total sales
4. Add business status logic
5. Generate a summary report
6. Apply conditional formatting
7. Create Excel charts
8. Save a final professional Excel file

Input  : sales_data.xlsx
Output : Final_Excel_Report.xlsx
===================================================================
"""

# ============================================================
# IMPORT REQUIRED LIBRARIES
# ============================================================

import pandas as pd
from openpyxl import load_workbook
from openpyxl.styles import PatternFill
from openpyxl.chart import BarChart, PieChart, Reference


# ============================================================
# FILE CONFIGURATION
# ============================================================

INPUT_FILE = "sales_data.xlsx"
OUTPUT_FILE = "Final_Excel_Report.xlsx"


# ============================================================
# STEP 1: READ EXCEL FILE
# ============================================================

df = pd.read_excel(INPUT_FILE)
print("📥 Excel file loaded successfully")


# ============================================================
# STEP 2: DATA CLEANING
# ============================================================

df.dropna(inplace=True)
print("🧹 Missing rows removed")


# ============================================================
# STEP 3: ADD CALCULATED COLUMN
# ============================================================

df["Total Amount"] = df["Quantity"] * df["Price"]
print("🧮 Total Amount column created")


# ============================================================
# STEP 4: ADD STATUS COLUMN (BUSINESS LOGIC)
# ============================================================

def sales_status(amount):
    if amount >= 100000:
        return "High"
    elif amount >= 50000:
        return "Medium"
    else:
        return "Low"

df["Sales Status"] = df["Total Amount"].apply(sales_status)
print("🏷 Sales Status column added")


# ============================================================
# STEP 5: CREATE SUMMARY REPORT
# ============================================================

summary_df = pd.DataFrame({
    "Metric": [
        "Total Revenue",
        "Total Orders",
        "High Sales Orders",
        "Medium Sales Orders",
        "Low Sales Orders"
    ],
    "Value": [
        df["Total Amount"].sum(),
        len(df),
        (df["Sales Status"] == "High").sum(),
        (df["Sales Status"] == "Medium").sum(),
        (df["Sales Status"] == "Low").sum()
    ]
})

print("📊 Summary report generated")


# ============================================================
# STEP 6: WRITE DATA TO EXCEL
# ============================================================

with pd.ExcelWriter(OUTPUT_FILE, engine="openpyxl") as writer:
    df.to_excel(writer, sheet_name="Sales Data", index=False)
    summary_df.to_excel(writer, sheet_name="Summary", index=False)

print("💾 Data written to Excel")


# ============================================================
# STEP 7: APPLY CONDITIONAL FORMATTING
# ============================================================

wb = load_workbook(OUTPUT_FILE)
ws = wb["Sales Data"]

high_fill = PatternFill(start_color="C6EFCE", end_color="C6EFCE", fill_type="solid")
medium_fill = PatternFill(start_color="FFEB9C", end_color="FFEB9C", fill_type="solid")
low_fill = PatternFill(start_color="FFC7CE", end_color="FFC7CE", fill_type="solid")

for row in range(2, ws.max_row + 1):
    status_cell = ws[f"F{row}"]

    if status_cell.value == "High":
        status_cell.fill = high_fill
    elif status_cell.value == "Medium":
        status_cell.fill = medium_fill
    elif status_cell.value == "Low":
        status_cell.fill = low_fill

print("🎨 Conditional formatting applied")


# ============================================================
# STEP 8: CREATE EXCEL CHARTS
# ============================================================

# -------------------------------
# Create Chart Sheet
# -------------------------------
chart_sheet = wb.create_sheet(title="Charts")

# -------------------------------
# BAR CHART: Product vs Total Amount
# -------------------------------

bar_chart = BarChart()
bar_chart.title = "Product Wise Total Sales"
bar_chart.x_axis.title = "Product"
bar_chart.y_axis.title = "Total Amount"

data = Reference(ws, min_col=5, min_row=1, max_row=ws.max_row)
categories = Reference(ws, min_col=2, min_row=2, max_row=ws.max_row)

bar_chart.add_data(data, titles_from_data=True)
bar_chart.set_categories(categories)

chart_sheet.add_chart(bar_chart, "A1")

# -------------------------------
# PIE CHART: Sales Status Distribution
# -------------------------------

pie_chart = PieChart()
pie_chart.title = "Sales Status Distribution"

labels = Reference(wb["Summary"], min_col=1, min_row=4, max_row=6)
data = Reference(wb["Summary"], min_col=2, min_row=4, max_row=6)

pie_chart.add_data(data, titles_from_data=False)
pie_chart.set_categories(labels)

chart_sheet.add_chart(pie_chart, "A20")

# Save final Excel file
wb.save(OUTPUT_FILE)

print("📊 Charts created successfully")
print("✅ Excel Automation Completed Successfully")
