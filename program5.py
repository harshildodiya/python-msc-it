stud = int(input("Enter Number of Students (Minimum 3): "))

subject=["python","linux","java","computer networking","data structure"]

if stud < 3:
    print("Please enter at least 3 students.")

else:
    students = []

   
    for i in range(stud):
        print(f"\n- Student {i + 1} -")

        roll = int(input("Roll No: "))
        name = input("Name: ")

        marks = []

        for sub in subject:
            mark = int(input(f"Enter " +sub+ " Marks:"))
            marks.append(mark)

        total = sum(marks)
        percentage = total / 5

        # Grade
        if percentage >= 90:
            grade = "A+"
        elif percentage >= 80:
            grade = "A"
        elif percentage >= 70:
            grade = "B"
        elif percentage >= 60:
            grade = "C"
        elif percentage >= 50:
             grade = "D"    
        else:
            grade = "F"

        student = {
            "roll": roll,
            "name": name,
            "total": total,
            "percentage": percentage,
            "grade": grade
        }

        students.append(student)

    students.sort(key=lambda student: student["total"], reverse=True)

    print("\n= Rank List =")

    rank = 1

    for i, student in enumerate(students):

        if i > 0 and student["total"] != students[i - 1]["total"]:
            rank = i + 1

        print(f"\nRank : {rank}")
        print(f"Roll Number : {student['roll']}")
        print(f"Name : {student['name']}")
        print(f"Total : {student['total']}")
        print(f"Percentage : {student['percentage']:.2f}%")
        print(f"Grade : {student['grade']}")