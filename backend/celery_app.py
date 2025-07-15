# from celery import Celery

# celery = Celery(
#     'tasks',
#     broker='redis://localhost:6379/0'
# )

# celery.conf.update(
#     timezone='Asia/Kolkata',
#     enable_utc=False,
# )


# from app import app
# from application.models import User
# from mail import send_mail
# import csv


# # Tasks
# @celery.task()
# def generate_csv(data, filename='report.csv'):
#     import time
#     time.sleep(20)
#     with open(filename, mode='w', newline='') as f:
#         writer = csv.DictWriter(f, fieldnames=data[0].keys())
#         writer.writeheader()
#         writer.writerows(data)
#     send_mail('admin@parking.com', 'Here\'s your csv export', 'Download your csv here http://127.0.0.1:5000/static/admin.csv')


from celery import Celery

celery = Celery(
    'tasks',
    broker='redis://localhost:6379/0'
)

celery.conf.update(
    timezone='Asia/Kolkata',
    enable_utc=False,
)

from app import app
from application.models import User
from mail import send_mail
import csv

# Tasks
@celery.task()
def generate_csv(data, filename='/static/report.csv'):
    import time
    time.sleep(20)
    with open(filename, mode='w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=data[0].keys())
        writer.writeheader()
        writer.writerows(data)
    send_mail('admin@parking.com', 'Here\'s your csv export', 'Download your csv here http://127.0.0.1:5000/static/admin.csv')
    
    

@celery.task()
def daily_reminders():
    with app.app_context():
        users = User.query.all()
        for user in users:
            send_mail(user.email, "Visit the application!", "Hey user,\n\n Have you visited our application? if not click here http://127.0.0.1:5000")
    print('mails sent')

@celery.task()
def montly_report():
    with app.app_context():
        users = User.query.all()
        for user in users:
            # fetch user's past month's information like what he did, no of registrations reviews etc
            data = [
                {'no': 1, 'name': 'reliance'},
                {'no': 2, 'name': 'market'},
                {'no': 3, 'name': 'surya theater'}
            ]
            template = """
here is your past month activity
{% for activity in data %}
    {{ activity.no }} - {{ activity.name }}
{% endfor %}
"""
            from jinja2 import Template
            send_mail(user.email, "Here's your montly activity", Template(template).render(data=data))
    print('mails sent')


# Scheduled Tasks
from datetime import timedelta
from celery.schedules import crontab

celery.conf.beat_schedule = {
    'send_daily_reminders': {
        'task': 'celery_app.daily_reminders',
        # 'schedule': timedelta(seconds=3)
        'schedule': crontab(hour= 18, minute=7)
    },
        'send_monthly_report': {
        'task': 'celery_app.montly_report',
        'schedule': timedelta(seconds=30)
        # 'schedule': crontab(hour=15, minute=14, day_of_month=1)
    }
}