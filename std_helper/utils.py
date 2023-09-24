import datetime
import time
from django.core.mail import send_mail
from bs4 import BeautifulSoup
import requests
import schedule
from datetime import datetime

subject = "std helper hesap dogrulama"
message = "https://djangostdhelper-production.up.railway.app/activateaccount/"
from_email = "helperstd@gmail.com"
recipient_list = ["alici@example.com"]

url = "http://www.beslenme.yildiz.edu.tr/yemekMenusu"


def sendMail(target: list):
    send_mail(subject, message + target[0], from_email, target)


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


def scheduled_meal_mail():
    results = get_meal()
    now = datetime.now().strftime("%d-%m-%Y")
    matched = None
    i = 0
    while matched is None and i < len(results):
        print(results[i].split()[-2])
        if now == results[i].split()[-2]:
            matched = results[i]
        i = i + 1

    if matched is not None:
        schedule.every().day.at("21:23").do(send_mail)

    # while True:
    #     schedule.run_pending()  # Planlanmış işleri kontrol et ve çalıştır
    #     time.sleep(1)  # İşlemleri kontrol etmek için bir aralık ekleyebilirsiniz
