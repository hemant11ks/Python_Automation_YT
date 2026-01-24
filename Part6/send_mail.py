# ---------------------------------------------------------
# IMPORT REQUIRED MODULES
# ---------------------------------------------------------

# smtplib is used to connect to an SMTP server (like Gmail)
# and send emails programmatically
import smtplib

# pandas is used to read and process Excel files easily
import pandas as pd

# os is used to access environment variables securely
import os

# EmailMessage helps us create a full email
# (subject, body, attachments, etc.)
from email.message import EmailMessage

# Path helps in handling file paths safely
from pathlib import Path

# load_dotenv loads variables from a .env file
# This avoids hardcoding sensitive data like passwords
from dotenv import load_dotenv


# ---------------------------------------------------------
# 1️⃣ LOAD EMAIL CREDENTIALS SECURELY
# ---------------------------------------------------------

# Load all variables from .env file into environment
load_dotenv()

# Read sender email ID from environment variable
SENDER_EMAIL = os.getenv("SENDER_EMAIL")

# Read sender email App Password from environment variable
SENDER_PASSWORD = os.getenv("SENDER_PASSWORD")

# If email or password is missing, stop the program
# This avoids sending email with invalid credentials
if not SENDER_EMAIL or not SENDER_PASSWORD:
    raise ValueError("Email credentials missing in .env file")


# ---------------------------------------------------------
# 2️⃣ SMTP CONFIGURATION (GMAIL)
# ---------------------------------------------------------

# Gmail SMTP server address
SMTP_SERVER = "smtp.gmail.com"

# Port 587 is used for secure TLS connection
SMTP_PORT = 587


# ---------------------------------------------------------
# 3️⃣ EXCEL CONFIGURATION
# ---------------------------------------------------------

# Name of the Excel file containing attendance data
EXCEL_FILE = "data.xlsx"

# Sheet name inside the Excel file
SHEET_NAME = "Attendance"

# Minimum required working hours
# Anyone below this will be highlighted in email
MIN_WORK_HOURS = 8


# ---------------------------------------------------------
# 4️⃣ READ & FILTER EXCEL DATA
# ---------------------------------------------------------

def read_excel_data():
    """
    Reads Excel file and returns only employees
    who worked less than minimum required hours
    """

    # Read Excel file into a pandas DataFrame
    df = pd.read_excel(EXCEL_FILE, sheet_name=SHEET_NAME)

    # Filter rows where Total Hours < MIN_WORK_HOURS
    # This creates a new DataFrame with only short-hour employees
    short_hours_df = df[df["Total Hours"] < MIN_WORK_HOURS]

    # Return the filtered DataFrame
    return short_hours_df


# ---------------------------------------------------------
# 5️⃣ CONVERT DATAFRAME TO EMAIL-SAFE HTML
# ---------------------------------------------------------

def dataframe_to_html(df):
    """
    Converts DataFrame to EMAIL-SAFE HTML table.
    Uses INLINE CSS because Gmail/Outlook
    do NOT support <style> tags properly.
    """

    # Start HTML table with borders and font styling
    html = """
    <table border="1" cellpadding="6" cellspacing="0"
           style="border-collapse:collapse;font-family:Arial;">
    """

    # -----------------------------
    # CREATE TABLE HEADER
    # -----------------------------
    html += "<tr>"

    # Loop through each column name
    for col in df.columns:
        html += f"""
        <th style="background:#f2f2f2;font-weight:bold;">
            {col}
        </th>
        """

    html += "</tr>"

    # -----------------------------
    # CREATE TABLE ROWS
    # -----------------------------
    for _, row in df.iterrows():

        # Start a new table row
        html += "<tr>"

        # Loop through each column in the row
        for col in df.columns:
            value = row[col]

            # If column is "Total Hours" AND value is less than minimum
            # then highlight it in RED color
            if col == "Total Hours" and value < MIN_WORK_HOURS:
                html += f"""
                <td style="color:red;font-weight:bold;text-align:center;">
                    {value}
                </td>
                """
            else:
                # Normal cell without highlight
                html += f"""
                <td style="text-align:center;">
                    {value}
                </td>
                """

        # Close table row
        html += "</tr>"

    # Close table tag
    html += "</table>"

    # Return final HTML string
    return html


# ---------------------------------------------------------
# 6️⃣ SEND EMAIL WITH ATTACHMENT
# ---------------------------------------------------------

def send_email(to, cc, subject, html_body, attachment):
    """
    Sends an HTML email with Excel attachment
    """

    # Create EmailMessage object
    msg = EmailMessage()

    # Set sender email
    msg["From"] = SENDER_EMAIL

    # Set TO recipients (visible to receiver)
    msg["To"] = ", ".join(to)

    # Set CC recipients (visible to receiver)
    msg["Cc"] = ", ".join(cc)

    # Set email subject
    msg["Subject"] = subject

    # Plain text fallback
    # Shown if email client does not support HTML
    msg.set_content("Please view this email in HTML format.")

    # Add HTML version of email body
    msg.add_alternative(html_body, subtype="html")

    # -----------------------------
    # ATTACH EXCEL FILE
    # -----------------------------
    with open(attachment, "rb") as file:
        msg.add_attachment(
            file.read(),                     # File data
            maintype="application",          # File type
            subtype="octet-stream",          # Generic binary
            filename=Path(attachment).name  # Attachment name
        )

    # Combine TO and CC recipients
    # SMTP server uses this list to deliver email
    recipients = to + cc

    # -----------------------------
    # SMTP CONNECTION & SEND
    # -----------------------------
    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:

        # Start TLS encryption for security
        server.starttls()

        # Login using Gmail App Password
        server.login(SENDER_EMAIL, SENDER_PASSWORD)

        # Send email to all recipients
        server.send_message(msg, to_addrs=recipients)


# ---------------------------------------------------------
# 7️⃣ MAIN EXECUTION (PROGRAM ENTRY POINT)
# ---------------------------------------------------------

if __name__ == "__main__":

    # Step 1: Read and filter Excel attendance data
    short_hours_df = read_excel_data()

    # If no employee has short hours, stop execution
    if short_hours_df.empty:
        print("No employees with short hours.")
        exit()

    # Step 2: Convert DataFrame to HTML table
    html_table = dataframe_to_html(short_hours_df)

    # Step 3: Create complete HTML email body
    html_body = f"""
    <html>
    <body>
        <h2 style="color:red;">🚨 Attendance Alert</h2>
        <p>Employees who worked less than <b>{MIN_WORK_HOURS}</b> hours:</p>
        {html_table}
    </body>
    </html>
    """

    # Step 4: Send email with attachment
    send_email(
        to=["ksingh1617@gmail.com"],
        cc=["ksingh1617@gmail.com"],
        subject="Attendance Report",
        html_body=html_body,
        attachment=EXCEL_FILE
    )

    # Confirmation message
    print("✅ Email sent successfully.")
