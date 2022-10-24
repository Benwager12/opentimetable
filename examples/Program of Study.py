import general
import timetable

item_name = input("Enter your chosen program of study: ")  # .S/Software Engineering Year 2
pos: general.TimetableType = general.get_timetable_types()['Programmes of Study']

print(f"Searching for: \"{item_name}\" as a \"{pos.english_name}\" timetable.")

identity = timetable.get_identity_search(pos, item_name)

if len(identity) == 0:
    print("No results found")
    exit()
if len(identity) > 1:
    print("Multiple results found, please narrow your search")
    exit()

subject_identity = identity[0]

print(f"Match found: {subject_identity}\n")

timetable_data = timetable.get_timetable(pos, [subject_identity[1]])

lessons = timetable.timetable_lessons(timetable_data)

for lesson in lessons:
    print(repr(lesson))
