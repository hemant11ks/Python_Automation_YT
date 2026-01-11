"""
Enterprise HR Attendance Automation

Features:
- Attendance alert (< 8 hrs)
- Auto-mail employee (uses Email column from Excel)
- Monthly summary report
- HTML color highlighting
- Exception handling
- Logging to file + console
"""

import smtplib
import pandas as pd
import os
import logging
import re
from email.message import EmailMessage
from pathlib import Path
from dotenv import load_dotenv

# ==============================
# LOGGING CONFIG (FILE + CONSOLE)
# ==============================
logger = logging.getLogger()
logger.setLevel(logging.INFO)

formatter = logging.Formatter(
    "%(asctime)s - %(levelname)s - %(message)s"
)

# File handler
file_handler = logging.FileHandler("attendance.log")
file_handler.setFormatter(formatter)

# Console handler
console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)

logger.addHandler(file_handler)
logger.addHandler(console_handler)

# ==============================
# LOAD ENV VARIABLES
# ==============================
load_dotenv()

SENDER_EMAIL = os.getenv("SENDER_EMAIL")
SENDER_PASSWORD = os.getenv("SENDER_PASSWORD")

if not SENDER_EMAIL or not SENDER_PASSWORD:
    raise ValueError("❌ SENDER_EMAIL or SENDER_PASSWORD missing in .env file")

# ==============================
# EMAIL CONFIG
# ==============================
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

HR_EMAILS = ["hemantkumarsingh455@gmail.com"]
MANAGER_EMAILS = ["hemantkumarsingh455@gmail.com"]

# ==============================
# FILE CONFIG
# ==============================
EXCEL_FILE = "data.xlsx"
SHEET_NAME = "Attendance"
MONTHLY_REPORT = "monthly_summary.xlsx"

REQUIRED_COLUMNS = {
    "Employee ID", "Name", "Email",
    "Date", "Check-in", "Check-out", "Total Hours"
}

MIN_WORK_HOURS = 8

# ==============================
# EMAIL VALIDATION
# ==============================
def is_valid_email(email):
    pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    return isinstance(email, str) and re.match(pattern, email)

def validate_email_list(email_list, label):
    for email in email_list:
        if not is_valid_email(email):
            raise ValueError(f"❌ Invalid {label} email detected: {email}")

# ==============================
# READ ATTENDANCE
# ==============================
def read_attendance():
    try:
        df = pd.read_excel(EXCEL_FILE, sheet_name=SHEET_NAME)

        missing_cols = REQUIRED_COLUMNS - set(df.columns)
        if missing_cols:
            raise ValueError(f"❌ Missing columns in Excel: {missing_cols}")

        # 🔥 CRITICAL: Clean email column
        df["Email"] = (
            df["Email"]
            .astype(str)
            .str.strip()
            .str.replace(r"\s+", "", regex=True)
            .str.lower()
        )

        logging.info("✅ Attendance file read and cleaned successfully")
        return df

    except Exception as e:
        logging.error(f"❌ Failed to read Excel: {e}")
        raise

# ==============================
# FILTER SHORT HOURS
# ==============================
def get_short_hours(df):
    return df[df["Total Hours"] < MIN_WORK_HOURS]

# ==============================
# HTML TABLE WITH COLOR
# ==============================
def html_table_with_highlight(df):
    def color_hours(val):
        return "color:red;font-weight:bold;" if val < MIN_WORK_HOURS else ""

    styled_df = df.style.applymap(color_hours, subset=["Total Hours"])
    return styled_df.to_html(index=False)

# ==============================
# SEND EMAIL FUNCTION
# ==============================
def send_email(to, cc, subject, html_body, attachment=None):
    try:
        msg = EmailMessage()
        msg["From"] = SENDER_EMAIL
        msg["To"] = ", ".join(to)
        msg["Cc"] = ", ".join(cc)
        msg["Subject"] = subject

        msg.set_content("Please view this email in HTML format.")
        msg.add_alternative(html_body, subtype="html")

        recipients = to + cc

        if attachment:
            with open(attachment, "rb") as f:
                msg.add_attachment(
                    f.read(),
                    maintype="application",
                    subtype="octet-stream",
                    filename=Path(attachment).name
                )

        logging.info(f"📤 Sending email to: {recipients}")

        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.send_message(msg, to_addrs=recipients)

        logging.info("✅ Email sent successfully")

    except Exception as e:
        logging.error(f"❌ Email sending failed: {e}")

# ==============================
# AUTO MAIL TO EMPLOYEE
# ==============================
def send_employee_mail(row):
    email = row["Email"]

    if not is_valid_email(email):
        logging.warning(f"⚠️ Skipping invalid employee email: {email}")
        return

    html = f"""
    <html>
    <body>
        <h3 style="color:red;">Attendance Alert</h3>
        <p>Hello <b>{row['Name']}</b>,</p>

        <p>Your working hours on <b>{row['Date']}</b> were
        <b style="color:red;">{row['Total Hours']} hrs</b>.</p>

        <p>Please ensure a minimum of <b>{MIN_WORK_HOURS} working hours</b>.</p>

        <br>
        Regards,<br>
        HR Automation System 🤖
    </body>
    </html>
    """

    logging.info(f"📧 Preparing employee email for {email}")

    send_email(
        to=[email],
        cc=[],
        subject="[Daily] Attendance Warning",
        html_body=html
    )

# ==============================
# MONTHLY SUMMARY REPORT
# ==============================
def generate_monthly_summary(df):
    try:
        summary = df.groupby("Name")["Total Hours"].mean().reset_index()
        summary.rename(columns={"Total Hours": "Avg Monthly Hours"}, inplace=True)
        summary.to_excel(MONTHLY_REPORT, index=False)
        logging.info("📊 Monthly summary report generated")

    except Exception as e:
        logging.error(f"❌ Monthly summary failed: {e}")

# ==============================
# MAIN AUTOMATION
# ==============================
def run_automation():
    try:
        logging.info("🚀 Attendance Automation Started")

        # Validate HR & Manager emails
        validate_email_list(HR_EMAILS, "HR")
        validate_email_list(MANAGER_EMAILS, "Manager")

        df = read_attendance()
        short_df = get_short_hours(df)

        if short_df.empty:
            logging.info("✅ No short-hour employees found")
            return

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

        send_email(
            to=HR_EMAILS,
            cc=MANAGER_EMAILS,
            subject="Attendance Alert Report",
            html_body=hr_html,
            attachment=EXCEL_FILE
        )

        # Employee emails
        for _, row in short_df.iterrows():
            send_employee_mail(row)

        # Monthly summary
        generate_monthly_summary(df)

        logging.info("🎉 Attendance Automation Completed Successfully")

    except Exception as e:
        logging.critical(f"🔥 Automation failed: {e}")

# ==============================
# EXECUTION
# ==============================
if __name__ == "__main__":
    run_automation()
