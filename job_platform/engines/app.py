#!/usr/bin/python3
"""starts the web application"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, User, JobApplication
from email_utils import send_weekly_report
import xlsxwriter
from os import getenv
from routes import *

DATABASE_URL = "sqlite:///./test.db"  # Example using SQLite. Adjust accordingly.

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    Base.metadata.create_all(bind=engine)

def user_list(main_workbook):
    session = SessionLocal()
    users = session.query(User).all()
    email_users = {'Not Enough Weeks': [], 'Warning': [], 'Good': [], 'Recommendation': []}
    for user in users:
        message = make_message(user, main_workbook)
        email_users[message['standing']].append(message)
    session.close()
    return email_users

def make_message(user, main_workbook):
    name = user.name.replace(' ', '')
    workbook = xlsxwriter.Workbook(name + '.xlsx')

    worksheet = workbook.add_worksheet()
    main_worksheet = main_workbook.add_worksheet(name)

    date_range = weekly_stats.generate_week_range(datetime.date.today())
    dates = {'start_date': date_range[0], 'end_date': date_range[1]}
    applied_jobs = user.get_jobs_applied(**dates)
    applied_stats = user.get_jobs_applied_stats(datetime.date.today())
    applied_jobs = applied_jobs['applied'] + applied_jobs['screening'] + applied_jobs['offerStage'] + applied_jobs['archived']
    three_week_total = applied_stats['three_week_total']
    message = ['{} Weekly Report\n'.format(user.name)]
    message.append('Number Applied this Week: {}\n\n'.format(len(applied_jobs)))

    message.append('All Time Total: {}\n'.format(applied_stats['total_applications']))
    message.append('Avg Over {} Week(s): {}\n\n'.format(applied_stats['num_weeks'], applied_stats['avg_applications']))
    message.append('Total in Last 3 Weeks: {}\n'.format(three_week_total))

    three_week_avg = three_week_total / 3
    if applied_stats['num_weeks'] < 3:
        standing = 'Not Enough Weeks'
    elif three_week_avg >= 15:
        standing = 'Recommendation'
    elif three_week_avg >= 5:
        standing = 'Good'
    else:
        standing = 'Warning'

    message.append('Avg Over Last 3 Weeks: {:.2f}\n'.format(three_week_avg))
    message.append('Standing: {}\n\n'.format(standing))

    main_worksheet.write('A1', 'STUDENT FIRST and LAST NAME')
    main_worksheet.write('A2', user.name)
    main_worksheet.write('B1', 'DATE')
    main_worksheet.write('B2', str(datetime.date.today()))
    main_worksheet.write('C1', 'COHORT')

    worksheet.write('A1', 'STUDENT FIRST and LAST NAME')
    worksheet.write('A2', user.name)
    worksheet.write('B1', 'DATE')
    worksheet.write('B2', str(datetime.date.today()))
    worksheet.write('C1', 'COHORT')

    main_worksheet.write('A4', 'Date of Application')
    main_worksheet.write('B4', 'Company Name')
    main_worksheet.write('C4', 'URL to Job Post')
    main_worksheet.write('D4', 'Job Title')
    main_worksheet.write('E4', 'Address')
    main_worksheet.write('F4', 'Additional Notes')
    main_worksheet.write('G4', 'Current Status')
    main_worksheet.write('H4', 'Interview Progress')
    worksheet.write('A4', 'Date of Application')
    worksheet.write('B4', 'Company Name')
    worksheet.write('C4', 'URL to Job Post')
    worksheet.write('D4', 'Job Title')
    worksheet.write('E4', 'Address')
    worksheet.write('F4', 'Additional Notes')
    worksheet.write('G4', 'Current Status')
    worksheet.write('H4', 'Interview Progress')

    for index, job in enumerate(applied_jobs):
        date = str(job.get('date_applied')).ljust(30)
        company = job.get('company').ljust(40)
        title = job.get('job_title').ljust(40)
        message.append(''.join([date, company, title, '\n']))
        row = str(index + 5)
        worksheet.write('A' + row, str(job['date_applied']))
        worksheet.write('B' + row, job['company'])
        worksheet.write('C' + row, job['url'])
        worksheet.write('D' + row, job['job_title'])
        worksheet.write('E' + row, job['location'])
        worksheet.write('F' + row, job['notes'])
        worksheet.write('G' + row, job['status'])
        worksheet.write('H' + row, job['interview_progress'])

        main_worksheet.write('A' + row, job['date_applied'])
        main_worksheet.write('B' + row, job['company'])
        main_worksheet.write('C' + row, job['url'])
        main_worksheet.write('D' + row, job['job_title'])
        main_worksheet.write('E' + row, job['location'])
        main_worksheet.write('F' + row, job['notes'])
        main_worksheet.write('G' + row, job['status'])
        main_worksheet.write('H' + row, job['interview_progress'])

    workbook.close()

    return {
        'name' : user.name,
        'standing' : standing,
        'email' : user.email if user.email else 'jobodysseynotifications@gmail.com',
        'message' : ''.join(message),
        'excel': name + '.xlsx'
    }

def email_standing(users, standing, total_report, email_address, email_pwd):
    total_report.append('--------------------------------------------------\n')
    total_report.append('Students with {} Standing\n'.format(standing))
    total_report.append('--------------------------------------------------\n')
    for user in users:
        try:
            send_email(user['email'], email_address, email_pwd, user['message'], user['excel'])
        except Exception as e:
            pass
        total_report.append(user['message'])

def main():
    email_address = getenv('JO_EMAIL')
    email_pwd = getenv('JO_EMAIL_PWD')

    main_workbook_name = 'StudentSummaries' + '.xlsx'
    main_workbook = xlsxwriter.Workbook(main_workbook_name)

    total_report = []

    users = user_list(main_workbook)
    for standing in users.keys():
        email_standing(users[standing], standing, total_report, email_address, email_pwd)

    main_workbook.close()
    send_email('sf-students-hr@holbertonschool.com', email_address, email_pwd, '\n\n'.join(total_report), main_workbook_name)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
