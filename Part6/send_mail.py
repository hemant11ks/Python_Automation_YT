"""
===========================================================
ENTERPRISE HR ATTENDANCE AUTOMATION SYSTEM (PYTHON)
===========================================================

WHAT THIS SCRIPT DOES:
-----------------------------------------------------------
1. Reads attendance data from an Excel file
2. Identifies employees working less than minimum hours
3. Sends alert email to HR & Managers
4. Sends warning email to each employee
5. Generates a monthly summary Excel report
6. Logs every important step (file + console)

THIS IS A REAL-WORLD, PRODUCTION-STYLE SCRIPT
-----------------------------------------------------------
"""

# =========================================================
# 1️⃣ IMPORT REQUIRED PYTHON MODULES
# =========================================================

import smtplib
# smtplib → Used to connect to SMTP server and send emails

import pandas as pd
# pandas → Used for reading Excel files and data manipulation

import os
# os → Used to read environment variables securely

import logging
# logging → Used instead of print() for professional logging

import re
# re → Used for regex-based email validation

from email.message import EmailMessage
# EmailMessage → Helps create structured email messages (HTML + attachment)

from pathlib import Path
# Path → Safely extracts file names for attachments

from dotenv import load_dotenv
# load_dotenv → Loads sensitive data from .env file

# =========================================================
# 2️⃣ LOGGING CONFIGURATION (FILE + CONSOLE)
# =========================================================

# Create root logger
logger = logging.getLogger()

# Set minimum log level
# INFO → logs info, warnings, errors, critical messages
logger.setLevel(logging.INFO)

# Define common log format
formatter = logging.Formatter(
    "%(asctime)s - %(levelname)s - %(message)s"
)

# -------- FILE LOGGING --------
# Logs will be saved in attendance.log
file_handler = logging.FileHandler("attendance.log", encoding="utf-8")
file_handler.setFormatter(formatter)

# -------- CONSOLE LOGGING --------
# Logs will also be shown in terminal
console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)

# Attach handlers to logger
logger.addHandler(file_handler)
logger.addHandler(console_handler)

# =========================================================
# 3️⃣ LOAD ENVIRONMENT VARIABLES (.env FILE)
# =========================================================

# Load .env file into environment
load_dotenv()

# Read email credentials securely
SENDER_EMAIL = os.getenv("SENDER_EMAIL")
SENDER_PASSWORD = os.getenv("SENDER_PASSWORD")

# Fail fast if credentials are missing
if not SENDER_EMAIL or not SENDER_PASSWORD:
    raise ValueError("SENDER_EMAIL or SENDER_PASSWORD missing in .env file")

# =========================================================
# 4️⃣ EMAIL CONFIGURATION
# =========================================================

# Gmail SMTP configuration
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587  # TLS port

# HR & Manager email lists
# These receive the consolidated attendance report
HR_EMAILS = ["hemantkumarsingh455@gmail.com"]
MANAGER_EMAILS = ["hemantkumarsingh455@gmail.com"]

# =========================================================
# 5️⃣ FILE & BUSINESS RULE CONFIGURATION
# =========================================================

# Excel input file
EXCEL_FILE = "data.xlsx"

# Sheet name inside Excel
SHEET_NAME = "Attendance"

# Monthly summary output file
MONTHLY_REPORT = "monthly_summary.xlsx"

# Required columns in Excel file
REQUIRED_COLUMNS = {
    "Employee ID", "Name", "Email",
    "Date", "Check-in", "Check-out", "Total Hours"
}

# Minimum required working hours per day
MIN_WORK_HOURS = 8

# =========================================================
# 6️⃣ EMAIL VALIDATION LOGIC
# =========================================================

def is_valid_email(email):
    """
    PURPOSE:
    --------------------------------------------------------
    Validates a single email address using regex

    RETURNS:
    --------------------------------------------------------
    True  → if email format is valid
    False → if email is invalid
    """

    # Regex pattern defining a valid email structure
    pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"

    # Check:
    # 1. email must be string
    # 2. email must match regex pattern
    return isinstance(email, str) and re.match(pattern, email)

def validate_email_list(email_list, label):
    """
    PURPOSE:
    --------------------------------------------------------
    Validates a list of email addresses (HR / Manager)

    FAIL-FAST PRINCIPLE:
    --------------------------------------------------------
    If even ONE email is invalid → stop program immediately
    """

    for email in email_list:
        if not is_valid_email(email):
            raise ValueError(f"Invalid {label} email detected: {email}")

# =========================================================
# 7️⃣ READ & CLEAN ATTENDANCE EXCEL FILE
# =========================================================

def read_attendance():
    """
    PURPOSE:
    --------------------------------------------------------
    Reads attendance data from Excel and cleans it
    """

    try:
        # Read Excel sheet into pandas DataFrame
        df = pd.read_excel(EXCEL_FILE, sheet_name=SHEET_NAME)

        # Ensure required columns exist
        missing_cols = REQUIRED_COLUMNS - set(df.columns)
        if missing_cols:
            raise ValueError(f"Missing columns in Excel: {missing_cols}")

        # Clean Email column to avoid delivery issues
        df["Email"] = (
            df["Email"]
            .astype(str)                 # Convert to string
            .str.strip()                 # Remove leading/trailing spaces
            .str.replace(r"\s+", "", regex=True)  # Remove internal spaces
            .str.lower()                 # Convert to lowercase
        )

        logging.info("Attendance file loaded and cleaned successfully")
        return df

    except Exception as e:
        logging.error(f"Failed to read Excel file: {e}")
        raise

# =========================================================
# 8️⃣ FILTER EMPLOYEES WITH SHORT HOURS
# =========================================================

def get_short_hours(df):
    """
    PURPOSE:
    --------------------------------------------------------
    Returns employees working less than minimum hours
    """

    return df[df["Total Hours"] < MIN_WORK_HOURS]

# =========================================================
# 9️⃣ CREATE HTML TABLE WITH COLOR HIGHLIGHTING
# =========================================================

def html_table_with_highlight(df):
    """
    PURPOSE:
    --------------------------------------------------------
    Converts DataFrame to HTML table
    Highlights short working hours in RED
    """

    def color_hours(value):
        # Apply red color if hours < required minimum
        if value < MIN_WORK_HOURS:
            return "color:red;font-weight:bold;"
        return ""

    # Apply styling safely (future-proof)
    styled_df = df.style.map(color_hours, subset=["Total Hours"])

    # Convert styled table to HTML
    return styled_df.to_html(index=False)

# =========================================================
# 🔟 SEND EMAIL FUNCTION (GENERIC)
# =========================================================

def send_email(to, cc, subject, html_body, attachment=None):
    """
    PURPOSE:
    --------------------------------------------------------
    Sends HTML email with optional attachment
    """

    try:
        # Create email object
        msg = EmailMessage()
        msg["From"] = SENDER_EMAIL
        msg["To"] = ", ".join(to)
        msg["Cc"] = ", ".join(cc)
        msg["Subject"] = subject

        # Plain text fallback
        msg.set_content("Please view this email in HTML format.")

        # HTML email content
        msg.add_alternative(html_body, subtype="html")

        # All recipients
        recipients = to + cc

        # Attach file if provided
        if attachment:
            with open(attachment, "rb") as f:
                msg.add_attachment(
                    f.read(),
                    maintype="application",
                    subtype="octet-stream",
                    filename=Path(attachment).name
                )

        logging.info(f"Sending email to {recipients}")

        # Connect to SMTP server securely
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()  # Secure connection
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.send_message(msg, to_addrs=recipients)

        logging.info("Email sent successfully")

    except Exception as e:
        logging.error(f"Email sending failed: {e}")

# =========================================================
# 1️⃣1️⃣ SEND WARNING EMAIL TO EMPLOYEE
# =========================================================

def send_employee_mail(row):
    """
    PURPOSE:
    --------------------------------------------------------
    Sends personalized warning email to employee
    """

    email = row["Email"]

    # Skip invalid employee emails
    if not is_valid_email(email):
        logging.warning(f"Skipping invalid employee email: {email}")
        return

    # HTML email body
    html = f"""
    <html>
    <body>
        <h3 style="color:red;">Attendance Alert</h3>
        <p>Hello <b>{row['Name']}</b>,</p>

        <p>Your working hours on <b>{row['Date']}</b> were
        <b style="color:red;">{row['Total Hours']} hrs</b>.</p>

        <p>Please ensure a minimum of <b>{MIN_WORK_HOURS} hours</b>.</p>

        <br>
        Regards,<br>
        HR Automation System
    </body>
    </html>
    """

    send_email(
        to=[email],
        cc=[],
        subject="[Daily] Attendance Warning",
        html_body=html
    )

# =========================================================
# 1️⃣2️⃣ MONTHLY SUMMARY REPORT
# =========================================================

def generate_monthly_summary(df):
    """
    PURPOSE:
    --------------------------------------------------------
    Generates average monthly working hours per employee
    """

    try:
        summary = df.groupby("Name")["Total Hours"].mean().reset_index()
        summary.rename(columns={"Total Hours": "Avg Monthly Hours"}, inplace=True)
        summary.to_excel(MONTHLY_REPORT, index=False)

        logging.info("Monthly summary report generated")

    except Exception as e:
        logging.error(f"Monthly summary generation failed: {e}")

# =========================================================
# 1️⃣3️⃣ MAIN AUTOMATION CONTROLLER
# =========================================================

def run_automation():
    """
    PURPOSE:
    --------------------------------------------------------
    Controls the entire automation flow
    """

    try:
        logging.info("Automation Started")

        # Validate HR & Manager emails
        validate_email_list(HR_EMAILS, "HR")
        validate_email_list(MANAGER_EMAILS, "Manager")

        # Read attendance data
        df = read_attendance()

        # Filter short-hour employees
        short_df = get_short_hours(df)

        if short_df.empty:
            logging.info("No short-hour employees found")
            return

        # Create HTML report for HR
        html_table = html_table_with_highlight(short_df)

        hr_html = f"""
        <html>
        <body>
            <h2 style="color:red;">Attendance Alert</h2>
            <p>Employees with less than {MIN_WORK_HOURS} hours:</p>
            {html_table}
        </body>
        </html>
        """

        # Send consolidated email to HR & Managers
        send_email(
            to=HR_EMAILS,
            cc=MANAGER_EMAILS,
            subject="Attendance Alert Report",
            html_body=hr_html,
            attachment=EXCEL_FILE
        )

        # Send individual warning emails
        for _, row in short_df.iterrows():
            send_employee_mail(row)

        # Generate monthly summary
        generate_monthly_summary(df)

        logging.info("Automation Completed Successfully")

    except Exception as e:
        logging.critical(f"Automation failed: {e}")

# =========================================================
# 1️⃣4️⃣ SCRIPT ENTRY POINT
# =========================================================

if __name__ == "__main__":
    run_automation()
