import general
import timetable

item_name = input("Enter your chosen program of study: ")  # .S/Software Engineering Year 2
timetable_type = "PoS"

print(f"Searching for: \"{item_name}\" as a \"{general.TimetableType[timetable_type].full_name}\" timetable.")

identity = timetable.get_identity_search(item_name)

if len(identity) == 0:
    print("No results found")
if len(identity) > 1:
    print("Multiple results found, please narrow your search")

subject_identity = identity[0]

print(f"Match found: {subject_identity}\n")

timetable_data = timetable.get_timetable(timetable_type, [subject_identity[1]])

lessons = timetable.timetable_lessons(timetable_data)

for lesson in lessons:
    print(lesson)
