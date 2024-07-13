import streamlit as st
from datetime import datetime
from timetablextractor import extract_timetable
from icsgenerator import create_ics_file

def main():
    st.title("VIT Timetable to ICS Converter")

    name = st.text_input("Enter your name:")
    st.text("None of your data is stored. Your name will be used as the name for the generated file.")

    # Timetable input
    st.header("Step 1: Input Your Timetable")
    timetable_text = st.text_area("Paste your timetable here:", height=300)

    # Date input
    st.header("Step 2: Set Semester Dates")
    col1, col2 = st.columns(2)
    with col1:
        start_date = st.date_input("Semester Start Date", datetime(2024, 7, 15))
    with col2:
        end_date = st.date_input("Semester End Date", datetime(2024, 11, 22))

    if 'extracted_courses' not in st.session_state:
        st.session_state.extracted_courses = None
    if 'additional_courses' not in st.session_state:
        st.session_state.additional_courses = []

    if st.button("Extract Courses"):
        if timetable_text:
            # Extract timetable
            extracted_courses, error = extract_timetable(timetable_text)
            if error:
                st.error(error)
            else:
                st.session_state.extracted_courses = extracted_courses
                st.success(f"Successfully extracted {len(extracted_courses)} courses.")
        else:
            st.warning("Please provide your timetable.")

    if st.session_state.extracted_courses is not None:
        st.header("Step 3: Verify and Edit Courses")
        st.write("Please verify the extracted courses and their slots. You can make changes if needed.")
        
        updated_courses = []
        for i, course in enumerate(st.session_state.extracted_courses):
            course_info, slots = course.split(' : ')
            col1, col2 = st.columns(2)
            with col1:
                updated_course_info = st.text_input(f"Course {i+1}", value=course_info, key=f"course_{i}")
            with col2:
                updated_slots = st.text_input(f"Slots for Course {i+1}", value=slots, key=f"slots_{i}")
            updated_courses.append(f"{updated_course_info} : {updated_slots}")

        # Add new courses
        st.subheader("Add Additional Courses")
        new_course_info = st.text_input("New Course Name and Venue (e.g., 'Course Name - Venue')")
        new_course_slots = st.text_input("New Course Slots (space-separated)")
        if st.button("Add Course"):
            if new_course_info and new_course_slots:
                new_course = f"{new_course_info} : {new_course_slots}"
                st.session_state.additional_courses.append(new_course)
                st.success(f"Added new course: {new_course}")
            else:
                st.warning("Please provide both course information and slots.")

        # Display additional courses
        if st.session_state.additional_courses:
            st.subheader("Additional Courses")
            for i, course in enumerate(st.session_state.additional_courses):
                course_info, slots = course.split(' : ')
                col1, col2 = st.columns(2)
                with col1:
                    updated_course_info = st.text_input(f"Additional Course {i+1}", value=course_info, key=f"add_course_{i}")
                with col2:
                    updated_slots = st.text_input(f"Slots for Additional Course {i+1}", value=slots, key=f"add_slots_{i}")
                updated_courses.append(f"{updated_course_info} : {updated_slots}")

        if st.button("Generate ICS File"):
            if start_date and end_date:
                # Convert updated courses to the format expected by create_ics_file
                courses_dict = {}
                for course in updated_courses:
                    course_info, slots = course.split(' : ')
                    courses_dict[course_info] = slots.split()

                # Generate ICS file
                ics_content, error = create_ics_file(courses_dict, start_date, end_date)
                if error:
                    st.error(error)
                else:
                    st.success("ICS file generated successfully!")
                    st.download_button(
                        label="Download ICS File",
                        data=ics_content,
                        file_name=f"{name} - timetable.ics",
                        mime="text/calendar"
                    )
            else:
                st.warning("Please select valid semester dates.")

if __name__ == "__main__":
    main()