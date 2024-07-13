import json
from datetime import datetime, timedelta

def load_slot_info(slot_info_file='slotinfofile.json'):
    with open(slot_info_file, 'r') as f:
        return json.load(f)

def create_ics_event(summary, start_time, end_time, day_of_week, semester_end):
    ics_event = f"""BEGIN:VEVENT
SUMMARY:{summary}
DTSTART:{start_time.strftime('%Y%m%dT%H%M%S')}
DTEND:{end_time.strftime('%Y%m%dT%H%M%S')}
RRULE:FREQ=WEEKLY;BYDAY={day_of_week};UNTIL={semester_end.strftime('%Y%m%dT235959Z')}
END:VEVENT
"""
    return ics_event

def generate_ics(courses, slot_info, semester_start, semester_end):
    ics_content = "BEGIN:VCALENDAR\nVERSION:2.0\nPRODID:-//Your Organization//EN\n"
    days = ['MO', 'TU', 'WE', 'TH', 'FR', 'SA', 'SU']

    # Convert semester_start to datetime if it's not already
    if isinstance(semester_start, datetime):
        semester_start_dt = semester_start
    else:
        semester_start_dt = datetime.combine(semester_start, datetime.min.time())

    for course_with_venue, slots in courses.items():
        course_name, venue = course_with_venue.rsplit(' - ', 1)
        
        if isinstance(slots, str):
            slots = slots.split()
        
        for slot in slots:
            if slot in slot_info:
                for class_info in slot_info[slot]:
                    start_time = class_info[0]
                    day_index = class_info[1] - 22  # Convert 22-28 to 0-6
                    day_abbr = days[day_index]
                    
                    start_dt = semester_start_dt + timedelta(days=day_index, hours=start_time[0], minutes=start_time[1])
                    
                    if len(class_info) > 2:
                        end_time = class_info[2]
                        end_dt = semester_start_dt + timedelta(days=day_index, hours=end_time[0], minutes=end_time[1])
                    else:
                        end_dt = start_dt + timedelta(minutes=50)
                    
                    event_name = f"{course_name} - {venue}"
                    ics_content += create_ics_event(event_name, start_dt, end_dt, day_abbr, semester_end)
            else:
                print(f"Warning: Slot {slot} not found in slot_info")

    ics_content += "END:VCALENDAR"
    return ics_content

def create_ics_file(courses, semester_start, semester_end, slot_info_file='slotinfofile.json'):
    try:
        slot_info = load_slot_info(slot_info_file)
        ics_content = generate_ics(courses, slot_info, semester_start, semester_end)
        return ics_content, None
    except Exception as e:
        return None, f"An error occurred: {str(e)}"

# This block is optional and can be used for any initialization if needed
if __name__ == "__main__":
    pass