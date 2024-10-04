import requests
from datetime import datetime
import smtplib

MY_LAT = 13.069252  # Your latitude
MY_LONG = 77.507762  # Your longitude
VISIBILITY_RANGE = 5

response = requests.get(url="http://api.open-notify.org/iss-now.json")
response.raise_for_status()
data = response.json()

iss_latitude = float(data["iss_position"]["latitude"])
iss_longitude = float(data["iss_position"]["longitude"])


# Your position is within +5 or -5 degrees of the ISS position.


# method for checking If the ISS is close to my current position
def is_in_range():
    long_dist = abs(MY_LAT - iss_latitude)
    lat_dist = abs(MY_LONG - iss_longitude)

    if long_dist <= VISIBILITY_RANGE and lat_dist <= VISIBILITY_RANGE:
        return True
    else:
        return False


parameters = {
    "lat": MY_LAT,
    "lng": MY_LONG,
    "formatted": 0,
}

response = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
response.raise_for_status()
data = response.json()
sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])

time_now = datetime.now()
current_hour = time_now.hour
MID_NIGHT = 0


# method for if it is currently dark

def is_dark():
    if (current_hour >= sunrise) and (current_hour <= sunset):
        return False
    else:
        return True


def give_distance_gap():
    return f"Your latitude: {MY_LAT}\nYour longitude: {MY_LONG}\n\nISS latitude: {iss_latitude}\nISS_longitude: {iss_longitude}"


SENDERS_MAIL = "ar5055063@gmail.com"
SENDERS_PASS = "dsvygthlfzliqmnl"


def notify(condition):
    with smtplib.SMTP(host="smtp.gmail.com", port=587) as connect:
        connect.starttls()
        connect.login(user=SENDERS_MAIL, password=SENDERS_PASS)
        if condition:
            connect.sendmail(to_addrs=SENDERS_MAIL, from_addr=SENDERS_MAIL,
                             msg="Subject:Look OverHead\n\nThe International Space Station is passing you.")


# Then email me to tell me to look up if the constraints ae satisfied.

check = is_dark() and is_in_range()
notify(check)
