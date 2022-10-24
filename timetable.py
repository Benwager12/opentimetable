import json
import requests

import general
from general import HEADERS, load_base, Lesson


def get_identity_search(timetabletype: general.TimetableType, subject_query: str) -> tuple[str, str] or None:
    """
    Gets the subject's identity from a search
    """

    res_data = {
        "Identity": timetabletype.filter_identity,
        "Values": ["null"]
    }

    page_number = 1

    res_url = f"{load_base()}/broker/api/CategoryTypes/{timetabletype.category_id}" \
              f"/Categories/Filter?pageNumber=[pg]&query={subject_query}"
    res = requests.post(res_url.replace("[pg]", str(page_number)), headers=HEADERS, json=res_data)

    res_json = json.loads(res.text)
    total_pages = int(res_json['TotalPages'])

    if res.status_code != 200:
        print("Unable to get identity for subject: %s", subject_query)
        return

    results = res_json['Results']
    identities_dict = []

    while page_number < total_pages:
        page_number += 1
        res = requests.post(res_url.replace("[pg]", str(page_number)), headers=HEADERS, json=res_data)
        res_json = json.loads(res.text)
        results += res_json['Results']

    for result in results:
        identities_dict.append((result['Name'], result['Identity']))
    return identities_dict


def get_timetable(timetable_type: general.TimetableType, identities: [str]) -> list or None:
    """
    Gets the timetable for a subject based on the timetable type and given identities
    """
    res_data = {
        "ViewOptions": general.get_view_options(),
        "CategoryIdentities": identities,
    }

    res_url = f"{load_base()}/broker/api/CategoryTypes/{timetable_type.category_id}" \
              f"/categories/events/filter"
    res = requests.post(res_url, headers=HEADERS, json=res_data)

    if res.status_code != 200:
        print(f"Unable to get timetable for subject: {identities}")
        return

    return json.loads(res.text)


def timetable_lessons(timetable_data: list) -> list[Lesson]:
    """
    Gets the lessons from the timetable data
    """
    events = [event for separate_timetable in timetable_data for event in separate_timetable['CategoryEvents']]

    return [Lesson(lesson['Name'], lesson['Location'], lesson['EventType'], lesson['StartDateTime'],
            lesson['EndDateTime']) for lesson in events]
