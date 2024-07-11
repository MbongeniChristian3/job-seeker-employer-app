#!/usr/bin/env python3
"""
holds a function which allows user to send emails
"""

import datetime
from application.models import database, weekly_stats
from os import getenv
import xlsxwriter
from email_utils import send_weekly_report

def user_list(main_workbook):
    # ... (Your existing user_list function code)

def make_message(user, main_workbook):
    # ... (Your existing make_message function code)

def email_standing(users, standing, total_report, email_address, email_pwd):
    """
    Sends emails to users based on their standing.

    Args:
        users: List of user messages.
        standing: User standing category.
        total_report: List to collect all report messages.
        email_address: Sender email address.
        email_pwd: Sender email password.
    """
    total_report.append('--------------------------------------------------\n')
    total_report.append(f'Students with {standing} Standing\n')
    total_report.append('--------------------------------------------------\n')
    for user in users:
        try:
            send_weekly_report(user['email'], email_address, email_pwd, user['message'], user['excel'])
            total_report.append(user['message'])
        except Exception as e:
            print(f"Failed to send email to {user['email']}: {e}")

def main():
    email_address = getenv('EMAIL_')
    email_pwd = getenv('EMAIL_PWD')

    main_workbook_name = 'StudentSummaries.xlsx'
    main_workbook = xlsxwriter.Workbook(main_workbook_name)

    total_report = []
    users = user_list(main_workbook)
    for standing in users.keys():
        email_standing(users[standing], standing, total_report, email_address, email_pwd)

    main_workbook.close()
    send_weekly_report('sf-students-hr@holbertonschool.com', email_address, email_pwd, '\n\n'.join(total_report), main_workbook_name)

if __name__ == '__main__':
    main()
