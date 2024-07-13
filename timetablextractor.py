import re

def extract_timetable_info(timetable_data):
    courses = []
    lines = timetable_data.split('\n')
    current_course = {}
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
        
        if re.match(r'^\d+$', line):  # New course entry starts
            if current_course:
                process_course(current_course, courses)
            current_course = {}
        elif ':' in line:  # Skip header line
            continue
        elif ' - ' in line and not line.startswith('('):  # Course code and name
            parts = line.split(' - ')
            current_course['code'] = parts[0]
            current_course['name'] = parts[1]
        elif line.startswith('('):  # Course type (Theory/Lab/Project)
            current_course['type'] = line
        elif re.match(r'^([A-Z]+\d+(\+[A-Z]+\d+)*)\s*-', line):  # Slot information (single or multiple)
            current_course['slot'] = line.split(' - ')[0]
        elif re.match(r'^[A-Z]+\d+$', line):  # Venue
            current_course['venue'] = line

    if current_course:
        process_course(current_course, courses)
    
    return courses

def process_course(course, courses):
    if 'code' in course and 'name' in course and 'slot' in course and 'venue' in course:
        if course['venue'] != "NIL":
            # Remove trailing '-', then trim whitespace
            # slots = course['slot'].rstrip('-').strip()
            slots = course['slot'].replace('+', ' ').rstrip(' -').strip()
            courses.append(f"{course['name']} - {course['venue']} : {slots}")

def extract_timetable(timetable_text):
    try:
        extracted_courses = extract_timetable_info(timetable_text)
        if len(extracted_courses) == 0:
            return None, "Warning: No courses were extracted. Check if the input format matches the expected format."
        return extracted_courses, None
    except Exception as e:
        return None, f"An error occurred: {str(e)}"

# This block is optional and can be used for any initialization if needed
if __name__ == "__main__":
    pass  # No operation performed