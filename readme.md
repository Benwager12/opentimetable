# Swansea University OpenTimetable Analyser

---

This is a tool that I have made that will call into the OpenTimetable API and return the data in a format.
As of right now it is able to look up a Program of Study and return the timetable that associates from it for the current week.

--- 

## Setup
### Installation
Clone this repo, in there, run a terminal with the following.

```batch
python3 -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```
If you are on Linux or Mac, you will need to use `python` instead of `python3` and `source venv/bin/activate` instead of `venv\Scripts\activate`

### Configuration
You will need to create a file called `base.txt` in the root of the project. This file will contain the following.

```
https://opentimetable.{your university.ac}/
```

---

## Usage
The only demo that the program possesses currently that you don't have to interact with code is `Program of Study.py`, more will be added in the future as more functionality is added.
With this program you need to be particularly exact with the name of the program of study, as I don't have a quick option to choose between multiple search results.

---

## Todo
* Add more demos
* Add the ability to grab multiple modules
* See different weeks
* Grab data and cache it in a file
* Make website for hosting the Timetable data
* Implement a rule based system for labs.