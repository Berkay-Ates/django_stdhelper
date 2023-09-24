import datetime
from django.core.mail import send_mail
from bs4 import BeautifulSoup
import requests
from .models import Users,Lessons
from django.utils import timezone
from datetime import *

subject = "std helper hesap dogrulama"
message = "https://djangostdhelper-production.up.railway.app/activateaccount/"
from_email = "helperstd@gmail.com"
recipient_list = ["alici@example.com"]

url = "http://www.beslenme.yildiz.edu.tr/yemekMenusu"


def sendMail(target: list):
    send_mail(subject, message + target[0], from_email, target)
    
def send_meal_mail(meal:str):
    users = Users.objects.all()
    active_users = users.filter(is_active=True,meal_notify=True)
    mail_receiver=[]
    for user in active_users:
        mail_receiver.append(user.mail)
    
    send_mail("yemek bilgilendirmesi", meal , from_email, mail_receiver)


def get_meal():
    response = requests.get(url=url)
    meal_res = BeautifulSoup(response.text, "html.parser")
    divs_with_class = meal_res.find_all("div", class_="card mx-1")
    results = []

    for div in divs_with_class:
        card_body_div = div.find("div", class_="card-body px-2 pt-2")
        content_div = card_body_div.find("div", class_="content")
        row_div = content_div.find_all("div", class_="row")
        col6_div = row_div[1].find_all("div", class_="col-6")
        col6_div2 = row_div[2].find_all("div", class_="col-6")

        date_div = div.find("div", class_="card-footer rounded py-1")
        date = date_div.find("span")

        if col6_div and col6_div2 and date:
            launch = col6_div[0].text
            dinner = col6_div2[0].text
            text = launch + " " + dinner + " " + date.text
            results.append(text)
        else:
            print("İlgili div bulunamadi.")

    return results

def todays_meal():
    results = get_meal()
    now = datetime.now().strftime("%d-%m-%Y")
    # now = datetime(year=2023, month=9, day=20, hour=15, minute=30).strftime("%d-%m-%Y")
    matched = None
    i = 0
    while matched is None and i < len(results):
        if now == results[i].split()[-2]:
            matched = results[i]
            print(matched)
        i = i + 1
        
    return matched


def send_user_lesson_mail():
    lessons = Lessons.objects.all()
    current_time = datetime.now().time()
    current_time_minutes = current_time.hour * 60 + current_time.minute
     
    for lesson in lessons:
        lesson_time = lesson.lesson_hour.hour * 60 + lesson.lesson_hour.minute
        if(lesson.lesson_hour.hour - 1 == current_time.hour and lesson_time >= current_time_minutes):
            user = Users.objects.get(std_id=lesson.user.std_id)
            message = lesson.lessons_name + ' dersi ' + lesson.class_room + ' sinifinda basliyor'
            send_lesson_mail(target=[user.mail],message=message,lesson_name=lesson.lessons_name)
    
    if(current_time.hour == 11 or current_time.hour == 17 or current_time.hour == 10 or current_time.hour == 16):
        send_meal_info()
     
     
def send_lesson_mail(target,message,lesson_name):
    send_mail(lesson_name,message, from_email, target)
    
            
def send_meal_info():
    meal = todays_meal()
    if(meal is not None):
        send_meal_mail(meal)
        