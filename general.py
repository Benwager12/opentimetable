import datetime
import json
import re
from functools import lru_cache
import os

import requests
from bs4 import BeautifulSoup


@lru_cache(maxsize=1)
def getroot_dir():
    return os.path.dirname(os.path.realpath(__file__))


@lru_cache(maxsize=1)
def get_view_options():
    res_url = f"{load_base()}/broker/api/ViewOptions"
    res = requests.get(res_url, headers=HEADERS)
    return json.loads(res.text)


@lru_cache(maxsize=1)
def load_base():
    try:
        return open(os.path.join(getroot_dir(), "base.txt"), "r").read()
    except FileNotFoundError:
        print("Base file not found, please make a base.txt file in the same directory as this script")
        exit()


def datetime_conversion(timeobj: str) -> datetime.datetime:
    """
    Takes in a string of format "2022-10-06T09:00:00+00:00" and returns a datetime object
    """
    return datetime.datetime.strptime(timeobj, "%Y-%m-%dT%H:%M:%S%z")


@lru_cache(maxsize=1)
def get_category_type_options():
    res_url = f"{load_base()}/broker/api/categoryTypeOptions"
    res = requests.get(res_url, headers=HEADERS)

    return json.loads(res.text)


class TimetableType:
    def __init__(self, category_data: json):
        self.full_name = category_data['Name']
        self.category_id = category_data['CategoryTypeId']
        # Remove this if you're in a university that doesn't put the attribute name in Welsh
        language_split = self.full_name.split(" / ")
        self.english_name = language_split[0]
        self.welsh_name = language_split[1]
        self.filter_identity = category_data['DefaultFilter'][0]['Identity']

    def __str__(self):
        return f"{self.english_name} ({self.category_id})"


class Lesson:
    def __init__(self, name: str, location: str, lesson_type: str, start_time: str, end_time: str):
        self.name = name.split("_")[0]
        self.location = location.split(" (")[0]
        self.lesson_type = lesson_type
        self.start_time = datetime_conversion(start_time)
        self.end_time = datetime_conversion(end_time)

    def length(self) -> int:
        """
        Returns the length of the lesson in minutes
        :return: Length of time in minutes
        """
        return int((self.end_time - self.start_time).total_seconds() / 60)

    def __repr__(self):
        return f"Lesson[name={self.name}, location={self.location}, lesson_type={self.lesson_type}, " \
               f"start_time={self.start_time}, end_time={self.end_time}, length={self.length()}]"

    def __str__(self):
        return f"{self.name} is at {self.location}, it is a {self.lesson_type} lesson, it lasts for " \
               f"{self.length()} minutes"


@lru_cache(maxsize=1)
def get_global_auth():
    res_one = requests.get(load_base())
    soup = BeautifulSoup(res_one.text, 'html.parser')
    main_script = soup.findAll('script')[-1]

    res_two = requests.get(f"{load_base()}/{main_script['src']}")
    auth = re.search(r"apiAuthentication:\"(basic .{10})\"", res_two.text).group(1)
    return auth


def get_timetable_types():
    data = get_category_type_options()
    arr = [TimetableType(x) for x in data]
    return {x.english_name: x for x in arr}


HEADERS = {
    "Authorization": get_global_auth(),
    "Content-Type": "application/json; charset=utf-8",
    "credentials": "include",
    "Referer": load_base() + "/",
    "Origin": load_base() + "/",
}
