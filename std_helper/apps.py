from threading import Thread
from django.apps import AppConfig


class StdshelperConfig(AppConfig):
    name = 'std_helper'
    
    def ready(self):
        pass
        # from apscheduler.schedulers.background import BackgroundScheduler
        # from django_apscheduler.jobstores import DjangoJobStore, register_events
        # from .utils import send_user_lesson_mail, send_meal_info , printWorking
        
        # scheduler = BackgroundScheduler()
        # scheduler.add_jobstore(DjangoJobStore(),'default')
        # scheduler.add_job(send_user_lesson_mail, 'interval', minutes=20)
        # scheduler.add_job(send_meal_info, 'cron', hour=11, minute=20)
        # scheduler.add_job(send_meal_info, 'cron', hour=17, minute=30)
        # scheduler.add_job(printWorking, 'cron', hour=22, minute=25)
        
        # scheduler.start()
        # register_events(scheduler)