import requests
from datetime import datetime
import smtplib as Reminder

# Geo location of UET taxila

MY_LATITUDE = 33.765011
MY_LONGITUDE = 72.821388

API_PARAMETERS = {
    "lat":MY_LATITUDE,
    "lng":MY_LONGITUDE,
    "formatted":0,
    
}

MY_TIME = datetime.now()


SUNRISE_API_KEY = "https://api.sunrise-sunset.org/json"

# SUNRISE_API_KEY_INLINE_PARAMS = "https://api.sunrise-sunset.org/json?lat=33.765011&lng=72.821388&formatted=0"

# we can use SUNRISE_API_KEY with params       
# --------------- or    
# just   use SUNRISE_API_KEY_INLINE_PARAMS


response = requests.get(SUNRISE_API_KEY,params=API_PARAMETERS)
response.raise_for_status()

data = response.json()["results"]

sunrise = data["sunrise"].split('T')[1].split(":")
sunset = data["sunset"].split('T')[1].split(":")

sunrise_hr = int(sunrise[0])
sunrise_min = int(sunrise[1])
sunset_hr = int(sunset[0])
sunset_min = int(sunset[1])







# NOW taking hold of ISS Location

ISS_API = "http://api.open-notify.org/iss-now.json"

iss_response = requests.get(ISS_API)["iss_position"]

iss_lat = float(iss_response["latitude"])
iss_lon = float(iss_response["longitude"])



# NOW checking if its dark and satellite is in range So generate a message

HOST = "smtp.gmail.com"
MY_mail = "testingsmtpprotocol@gmail.com"
MY_mail_pass = "vjip xfhm jcfy mkur"
activity_detected_message = """Subject: Satellite above you\n\n
        International Space satellite is just going to pass from your
        area.
            So, take a cup of tea and move to the roof to watch the satellite in the sky.
           
        Thanks you.
        Regards: Auto mail generator"""

if (MY_TIME.hour >=sunset_hr and MY_TIME.minute >=sunset_min) and (MY_TIME.hour <sunrise_hr and MY_TIME.minute <sunrise_min):
    if (MY_LATITUDE-0.5<=iss_lat<=MY_LATITUDE+0.5) and (MY_LONGITUDE-0.5<=iss_lon<=MY_LONGITUDE+0.5) :
        with Reminder.SMTP(HOST) as remainder:
            remainder.starttls()
            remainder.login(user=MY_mail,password=MY_mail_pass)
            remainder.send_message(from_addr=MY_mail,
                                to_addrs=MY_mail,
                                msg=activity_detected_message)

