import json
from datetime import datetime, timedelta

def load_slot_info(slot_info_file='slotinfofile.json'):
    with open(slot_info_file, 'r') as f:
        return json.load(f)

def generate_ics_test(courses, slot_info, semester_start):
    days = ['MO', 'TU', 'WE', 'TH', 'FR', 'SA', 'SU']
    semester_start_dt = datetime.combine(semester_start, datetime.min.time())
    
    print(f"Semester start date: {semester_start_dt}")

    print("\nSlot info from JSON:")
    for slot in ['L3', 'L4', 'A1', 'F1', 'D1']:
        print(f"  {slot}: {slot_info.get(slot, 'Not found')}")

    for course_name, slots in courses.items():
        print(f"\nProcessing course: {course_name}")
        for slot in slots:
            print(f"  Slot: {slot}")
            if slot in slot_info:
                for class_info in slot_info[slot]:
                    start_time = class_info[0]
                    day_index = class_info[1] - 22  # Convert 22-28 to 0-6
                    day_abbr = days[day_index]
                    
                    print(f"    Raw start time: {start_time}")
                    print(f"    Day index: {day_index} ({day_abbr})")
                    
                    start_dt = semester_start_dt + timedelta(days=day_index, hours=start_time[0], minutes=start_time[1])
                    
                    print(f"    Calculated start time: {start_dt}")
                    
                    if len(class_info) > 2:
                        end_time = class_info[2]
                        end_dt = semester_start_dt + timedelta(days=day_index, hours=end_time[0], minutes=end_time[1])
                    else:
                        end_dt = start_dt + timedelta(minutes=50)
                    
                    print(f"    Calculated end time: {end_dt}")
            else:
                print(f"    Slot {slot} not found in slot_info")

# Test the function
if __name__ == "__main__":
    slot_info = load_slot_info()
    
    # Example course data
    courses = {
        "Artificial Intelligence": ["L3", "L4"],
        "Database Management Systems": ["A1", "F1", "D1"]
    }
    
    # Example semester start date (adjust as needed)
    semester_start = datetime(2024, 7, 15).date()  # A Monday
    
    generate_ics_test(courses, slot_info, semester_start)