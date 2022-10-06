import dataclasses
import datetime
import json
from functools import lru_cache
import sys
import os


def getroot_dir():
    return os.path.dirname(os.path.realpath(__file__))


@lru_cache(maxsize=1)
def load_config():
    """
    Loads the config, and creates it if it doesn't exist
    """
    changed = False
    with open(f"{getroot_dir()}/config.json", "r") as config_file:
        input_file = config_file.read()
        if input_file == "":
            input_file = "{}"

        config_file = json.loads(input_file)

        if "base" not in config_file:
            config_file['base'] = "BASE_URL"
            changed = True
        if "identity" not in config_file:
            config_file['identity'] = "IDENTITY"
            changed = True
        if "auth" not in config_file:
            config_file['auth'] = "AUTH"
            changed = True

    if changed:
        with open("config.json", "w") as new_config:
            json.dump(config_file, new_config)
    return config_file


@lru_cache(maxsize=1)
def load_view_options():
    """
    Loads the view options
    """
    return json.loads(open(f"{getroot_dir()}/view_options.json", "r").read())


def datetime_conversion(timeobj: str) -> datetime.datetime:
    """
    Takes in a string of format "2022-10-06T09:00:00+00:00" and returns a datetime object
    """
    return datetime.datetime.strptime(timeobj, "%Y-%m-%dT%H:%M:%S%z")


@dataclasses.dataclass
class TimetableType:
    identity: str
    full_name: str


class Lesson:
    def __init__(self, name: str, location: str, lesson_type: str, start_time: str, end_time: str):
        self.name = name.split("_")[0]
        self.location = location
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


HEADERS = {
    "Authorization": load_config()['auth'],
    "Content-Type": "application/json; charset=utf-8",
    "credentials": "include",
    "Referer": load_config()['base'] + "/",
    "Origin": load_config()['base'] + "/",
}

TimetableType = {
    "PoS": TimetableType("241e4d36-93f2-4938-9e15-d4536fe3b2eb", "Programmes of Study"),
    "Mod": TimetableType("d334dcdb-6362-408b-b3e2-4dcd061d5654", "Modules"),
    "Loc": TimetableType("1e042cb1-547d-41d4-ae93-a1f2c3d34538", "Location"),
}