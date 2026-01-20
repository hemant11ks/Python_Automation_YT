# =========================================================
# PYTHON SCRIPT: SEND EXCEL DATA VIA EMAIL WITH ATTACHMENT
# =========================================================
# This script demonstrates:
# 1. Reading data from an Excel file
# 2. Filtering data using business rules
# 3. Converting Excel data to HTML for email
# 4. Sending HTML email using SMTP
# 5. Attaching Excel file in the email
# =========================================================


# ---------------------------------------------------------
# 1️⃣ IMPORT REQUIRED MODULES
# ---------------------------------------------------------

import smtplib
# smtplib:
# This module is used to connect Python with an email server
# (SMTP server) and send emails programmatically.

import pandas as pd
# pandas:
# Used to read Excel files and manipulate tabular data
# (very common in real-world automation).

import os
# os:
# Used to securely read environment variables
# like email and password from .env file.

from email.message import EmailMessage
# EmailMessage:
# Helps create professional emails with subject,
# HTML content, and attachments.

from pathlib import Path
# Path:
# Used to safely extract the filename from file path
# while attaching files.

from dotenv import load_dotenv
# load_dotenv:
# Loads environment variables from a .env file.


# ---------------------------------------------------------
# 2️⃣ LOAD EMAIL CREDENTIALS SECURELY
# ---------------------------------------------------------

# Load variables from .env file into environment
load_dotenv()

# Read email credentials
SENDER_EMAIL = os.getenv("SENDER_EMAIL")
SENDER_PASSWORD = os.getenv("SENDER_PASSWORD")

# If credentials are missing, stop execution immediately
if not SENDER_EMAIL or not SENDER_PASSWORD:
    raise ValueError("SENDER_EMAIL or SENDER_PASSWORD not found")


# ---------------------------------------------------------
# 3️⃣ SMTP SERVER CONFIGURATION
# ---------------------------------------------------------

# Gmail SMTP server details
SMTP_SERVER = "smtp.gmail.com"

# Port 587 is used for TLS (secure email sending)
SMTP_PORT = 587


# ---------------------------------------------------------
# 4️⃣ EXCEL FILE CONFIGURATION
# ---------------------------------------------------------

# Excel file name
EXCEL_FILE = "data.xlsx"

# Sheet name inside Excel
SHEET_NAME = "Attendance"

# Business rule:
# Minimum working hours required per day
MIN_WORK_HOURS = 8


# ---------------------------------------------------------
# 5️⃣ READ & FILTER EXCEL DATA
# ---------------------------------------------------------

def read_excel_data():
    """
    PURPOSE:
    -----------------------------------------------
    Reads attendance data from Excel file and
    returns employees who worked less than
    required minimum hours.
    """

    # Read Excel sheet into pandas DataFrame
    df = pd.read_excel(EXCEL_FILE, sheet_name=SHEET_NAME)

    # Filter employees who worked less than minimum hours
    short_hours_df = df[df["Total Hours"] < MIN_WORK_HOURS]

    # Return filtered data
    return short_hours_df


# ---------------------------------------------------------
# 6️⃣ CONVERT DATAFRAME TO HTML TABLE
# ---------------------------------------------------------

def dataframe_to_html(df):
    """
    PURPOSE:
    -----------------------------------------------
    Converts pandas DataFrame into an HTML table
    so it can be embedded directly inside email body.
    """

    def highlight_hours(value):
        """
        This function is applied to each value
        in 'Total Hours' column.

        If hours < required minimum,
        the value will appear in RED color.
        """
        if value < MIN_WORK_HOURS:
            return "color:red;font-weight:bold;"
        return ""

    # Apply styling to DataFrame
    styled_df = df.style.map(
        highlight_hours,
        subset=["Total Hours"]
    )

    # Convert styled DataFrame into HTML
    return styled_df.to_html(index=False)


# ---------------------------------------------------------
# 7️⃣ SEND EMAIL WITH HTML BODY & ATTACHMENT
# ---------------------------------------------------------

def send_email(to, cc, subject, html_body, attachment):
    """
    PURPOSE:
    -----------------------------------------------
    Sends an email with:
    - HTML content
    - Excel attachment
    """

    # Create EmailMessage object
    msg = EmailMessage()

    # ---------------- EMAIL HEADERS ----------------
    msg["From"] = SENDER_EMAIL
    msg["To"] = ", ".join(to)
    msg["Cc"] = ", ".join(cc)
    msg["Subject"] = subject

    # Plain text fallback (important for email clients)
    msg.set_content(
        "This email contains HTML content. "
        "Please view it in a supported email client."
    )

    # Add HTML version of email body
    msg.add_alternative(html_body, subtype="html")

    # ---------------- ATTACHMENT LOGIC ----------------
    # Open Excel file in binary mode
    with open(attachment, "rb") as file:
        msg.add_attachment(
            file.read(),                      # File content as bytes
            maintype="application",           # Generic file type
            subtype="octet-stream",           # Works for any file
            filename=Path(attachment).name    # Extract filename
        )

    # Combine all recipients
    recipients = to + cc

    # ---------------- SMTP CONNECTION ----------------
    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls()                     # Secure connection
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.send_message(msg, to_addrs=recipients)

    print("✅ Email sent successfully with attachment")


# ---------------------------------------------------------
# 8️⃣ MAIN EXECUTION FLOW
# ---------------------------------------------------------

if __name__ == "__main__":

    # Step 1: Read Excel data
    short_hours_df = read_excel_data()

    # If no employee has short hours, stop program
    if short_hours_df.empty:
        print("No employees found with short working hours")
        exit()

    # Step 2: Convert Excel data into HTML table
    html_table = dataframe_to_html(short_hours_df)

    # Step 3: Create HTML email body
    html_body = f"""
    <html>
    <body>
        <h2 style="color:red;">Attendance Alert</h2>
        <p>Employees who worked less than {MIN_WORK_HOURS} hours:</p>
        {html_table}
    </body>
    </html>
    """

    # Step 4: Send email WITH Excel attachment
    send_email(
        to=["example@gmail.com"],
        cc=[],
        subject="Attendance Report",
        html_body=html_body,
        attachment=EXCEL_FILE
    )
