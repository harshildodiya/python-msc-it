from datetime import datetime


class Course:
    def __init__(self, course_code, day, start_time, end_time):
        self.course_code = course_code
        self.day = day
        self.start_time = self.validate_time(start_time)
        self.end_time = self.validate_time(end_time)

        if self.start_time >= self.end_time:
            raise ValueError("Start time must be earlier than end time.")

    @staticmethod
    def validate_time(time_str):
        try:
            return datetime.strptime(time_str, "%H:%M").time()
        except ValueError:
            raise ValueError(
                "Invalid time format. Please use HH:MM (24-hour format)."
            )

    def __str__(self):
        return (
            f"{self.course_code} | {self.day} | "
            f"{self.start_time.strftime('%H:%M')} - "
            f"{self.end_time.strftime('%H:%M')}"
        )


class Student:
    def __init__(self, student_id, student_name):
        self.student_id = student_id
        self.student_name = student_name
        self.registered_courses = []

    def add_course(self, course):
        self.registered_courses.append(course)

    def find_conflicts(self):
        conflicts = []

        for i in range(len(self.registered_courses)):
            for j in range(i + 1, len(self.registered_courses)):
                course1 = self.registered_courses[i]
                course2 = self.registered_courses[j]

                # Courses can conflict only if they are on the same day
                if course1.day.lower() == course2.day.lower():

                    # Time intervals overlap if:
                    # start1 < end2 AND start2 < end1
                    if (
                        course1.start_time < course2.end_time
                        and course2.start_time < course1.end_time
                    ):
                        conflicts.append((course1, course2))

        return conflicts

    def __str__(self):
        result = (
            f"\nStudent ID: {self.student_id}\n"
            f"Student Name: {self.student_name}\n"
            f"Total Registered Courses: {len(self.registered_courses)}\n"
        )

        result += "\nRegistered Courses:\n"
        for course in self.registered_courses:
            result += f"  {course}\n"

        return result


def get_course_details():
    """Accept course details and return a Course object."""

    while True:
        try:
            course_code = input("Enter course code: ").strip()

            if not course_code:
                raise ValueError("Course code cannot be empty.")

            day = input("Enter day of the week: ").strip()

            if not day:
                raise ValueError("Day cannot be empty.")

            start_time = input("Enter start time (HH:MM): ").strip()
            end_time = input("Enter end time (HH:MM): ").strip()

            return Course(course_code, day, start_time, end_time)

        except ValueError as e:
            print(f"Error: {e}")
            print("Please enter the course details again.\n")


def main():
    students = []

    # Accept number of students
    while True:
        try:
            n = int(input("Enter number of students: "))

            if n <= 0:
                raise ValueError("Number of students must be greater than 0.")

            break

        except ValueError as e:
            print(f"Invalid input: {e}")

    # Accept student information
    for i in range(n):
        print(f"\n{'=' * 40}")
        print(f"Enter details for Student {i + 1}")
        print("=" * 40)

        while True:
            try:
                student_id = input("Enter student ID: ").strip()
                student_name = input("Enter student name: ").strip()

                if not student_id:
                    raise ValueError("Student ID cannot be empty.")

                if not student_name:
                    raise ValueError("Student name cannot be empty.")

                student = Student(student_id, student_name)
                break

            except ValueError as e:
                print(f"Error: {e}")

        # Number of courses
        while True:
            try:
                course_count = int(
                    input("Enter number of registered courses: ")
                )

                if course_count < 0:
                    raise ValueError(
                        "Number of courses cannot be negative."
                    )

                break

            except ValueError as e:
                print(f"Invalid input: {e}")

        # Add courses
        for j in range(course_count):
            print(f"\nEnter details for Course {j + 1}:")
            course = get_course_details()
            student.add_course(course)

        students.append(student)

    # Display results
    print("\n\n" + "=" * 60)
    print("COURSE REGISTRATION CONFLICT REPORT")
    print("=" * 60)

    for student in students:
        print(student)

        conflicts = student.find_conflicts()

        if conflicts:
            print("CONFLICTING COURSE PAIRS:")

            for course1, course2 in conflicts:
                print(f"  1. {course1.course_code} <--> {course2.course_code}")
                print(f"     {course1}")
                print(f"     {course2}")
        else:
            print("No timetable conflicts found.")
            print("Student Timetable:")

            # Sort timetable by day and start time
            sorted_courses = sorted(
                student.registered_courses,
                key=lambda c: (c.day.lower(), c.start_time)
            )

            for course in sorted_courses:
                print(f"  {course}")

        print("-" * 60)

if __name__ == "__main__":
    main()