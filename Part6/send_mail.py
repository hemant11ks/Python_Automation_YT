# ---------------------------------------------------------
# IMPORT REQUIRED MODULES
# ---------------------------------------------------------

import smtplib
import pandas as pd
import os
from email.message import EmailMessage
from pathlib import Path
from dotenv import load_dotenv


# ---------------------------------------------------------
# 1️⃣ LOAD EMAIL CREDENTIALS SECURELY
# ---------------------------------------------------------

load_dotenv()

SENDER_EMAIL = os.getenv("SENDER_EMAIL")
SENDER_PASSWORD = os.getenv("SENDER_PASSWORD")

if not SENDER_EMAIL or not SENDER_PASSWORD:
    raise ValueError("Email credentials missing in .env file")


# ---------------------------------------------------------
# 2️⃣ SMTP CONFIGURATION (GMAIL)
# ---------------------------------------------------------

SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587


# ---------------------------------------------------------
# 3️⃣ EXCEL CONFIGURATION
# ---------------------------------------------------------

EXCEL_FILE = "data.xlsx"
SHEET_NAME = "Attendance"
MIN_WORK_HOURS = 8


# ---------------------------------------------------------
# 4️⃣ READ & FILTER EXCEL DATA
# ---------------------------------------------------------

def read_excel_data():
    """
    Reads Excel file and returns employees
    who worked less than minimum hours
    """
    df = pd.read_excel(EXCEL_FILE, sheet_name=SHEET_NAME)

    # Filter employees with less working hours
    short_hours_df = df[df["Total Hours"] < MIN_WORK_HOURS]

    return short_hours_df


# ---------------------------------------------------------
# 5️⃣ CONVERT DATAFRAME TO EMAIL-SAFE HTML
# ---------------------------------------------------------

def dataframe_to_html(df):
    """
    Converts DataFrame to EMAIL-SAFE HTML table
    using inline CSS (works in Gmail/Outlook)
    """

    html = """
    <table border="1" cellpadding="6" cellspacing="0"
           style="border-collapse:collapse;font-family:Arial;">
    """

    # Table header
    html += "<tr>"
    for col in df.columns:
        html += f"""
        <th style="background:#f2f2f2;font-weight:bold;">
            {col}
        </th>
        """
    html += "</tr>"

    # Table rows
    for _, row in df.iterrows():
        html += "<tr>"
        for col in df.columns:
            value = row[col]

            # Highlight Total Hours < MIN_WORK_HOURS
            if col == "Total Hours" and value < MIN_WORK_HOURS:
                html += f"""
                <td style="color:red;font-weight:bold;text-align:center;">
                    {value}
                </td>
                """
            else:
                html += f"""
                <td style="text-align:center;">
                    {value}
                </td>
                """
        html += "</tr>"

    html += "</table>"
    return html


# ---------------------------------------------------------
# 6️⃣ SEND EMAIL WITH ATTACHMENT
# ---------------------------------------------------------

def send_email(to, cc, subject, html_body, attachment):
    """
    Sends HTML email with Excel attachment
    """

    msg = EmailMessage()
    msg["From"] = SENDER_EMAIL
    msg["To"] = ", ".join(to)
    msg["Cc"] = ", ".join(cc)
    msg["Subject"] = subject

    # Plain text fallback
    msg.set_content("Please view this email in HTML format.")

    # HTML body
    msg.add_alternative(html_body, subtype="html")

    # Attach Excel file
    with open(attachment, "rb") as file:
        msg.add_attachment(
            file.read(),
            maintype="application",
            subtype="octet-stream",
            filename=Path(attachment).name
        )

    # Combine TO + CC for SMTP delivery
    recipients = to + cc

    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.send_message(msg, to_addrs=recipients)


# ---------------------------------------------------------
# 7️⃣ MAIN EXECUTION
# ---------------------------------------------------------

if __name__ == "__main__":

    short_hours_df = read_excel_data()

    if short_hours_df.empty:
        print("No employees with short hours.")
        exit()

    html_table = dataframe_to_html(short_hours_df)

    html_body = f"""
    <html>
    <body>
        <h2 style="color:red;">🚨 Attendance Alert</h2>
        <p>Employees who worked less than <b>{MIN_WORK_HOURS}</b> hours:</p>
        {html_table}
    </body>
    </html>
    """

    send_email(
        to=["ksingh1617@gmail.com"],
        cc=["ksingh1617@gmail.com"],
        subject="Attendance Report",
        html_body=html_body,
        attachment=EXCEL_FILE
    )

    print("✅ Email sent successfully.")
