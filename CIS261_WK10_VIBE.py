"""Student Grade Calculator.

This program manages student records, calculates averages and letter grades,
prints class statistics, and saves records to a pipe-delimited text file.
"""

from __future__ import annotations

DATA_FILE = "student_grades.txt"


def calculate_average(test1: float, test2: float, test3: float) -> float:
    """Calculate the average of three scores."""
    return (test1 + test2 + test3) / 3


def calculate_grade(average: float) -> str:
    """Return the letter grade based on the numeric average."""
    if average >= 90:
        return "A"
    if average >= 80:
        return "B"
    if average >= 70:
        return "C"
    if average >= 60:
        return "D"
    return "F"


def create_student_record(name: str, student_id: str, test1: float, test2: float, test3: float) -> dict:
    """Create a student dictionary with average and grade included."""
    raw_average = calculate_average(test1, test2, test3)
    rounded_average = round(raw_average, 2)
    grade = calculate_grade(rounded_average)
    return {
        "name": name,
        "id": student_id,
        "test1": float(test1),
        "test2": float(test2),
        "test3": float(test3),
        "average": rounded_average,
        "grade": grade,
    }


def load_students(filename: str = DATA_FILE) -> list[dict]:
    """Load student records from a pipe-delimited file."""
    students: list[dict] = []
    try:
        with open(filename, "r", encoding="utf-8") as file:
            for line_number, line in enumerate(file, start=1):
                data = line.strip()
                if not data:
                    continue
                parts = data.split("|")
                if len(parts) != 7:
                    print(f"Warning: skipping invalid record on line {line_number}.")
                    continue
                try:
                    name, student_id, test1, test2, test3, average, grade = parts
                    student_record = {
                        "name": name,
                        "id": student_id,
                        "test1": float(test1),
                        "test2": float(test2),
                        "test3": float(test3),
                        "average": float(average),
                        "grade": grade,
                    }
                    students.append(student_record)
                except ValueError:
                    print(f"Warning: skipping malformed record on line {line_number}.")
    except FileNotFoundError:
        print("No saved records found. Starting with an empty list.")
    except OSError as exc:
        print(f"Error loading student records: {exc}")

    print(f"Loaded {len(students)} student record(s).")
    return students


def save_students(students: list[dict], filename: str = DATA_FILE) -> None:
    """Save all student records to the grade file."""
    try:
        with open(filename, "w", encoding="utf-8") as file:
            for student in students:
                file.write(
                    f"{student['name']}|{student['id']}|{student['test1']:.2f}|"
                    f"{student['test2']:.2f}|{student['test3']:.2f}|{student['average']:.2f}|"
                    f"{student['grade']}\n"
                )
        print(f"Student records saved to {filename}.")
    except OSError as exc:
        print(f"Error saving student records: {exc}")


def prompt_for_float(prompt: str) -> float:
    """Get a valid float score from the user."""
    while True:
        value = input(prompt).strip()
        try:
            score = float(value)
            if 0 <= score <= 100:
                return score
            print("Please enter a score between 0 and 100.")
        except ValueError:
            print("Invalid input. Please enter a numeric score.")


def add_student(students: list[dict]) -> None:
    """Prompt the user for a student record and add it to the list."""
    name = input("Enter student name: ").strip()
    while not name:
        print("Name cannot be blank.")
        name = input("Enter student name: ").strip()

    student_id = input("Enter student ID: ").strip()
    while not student_id:
        print("Student ID cannot be blank.")
        student_id = input("Enter student ID: ").strip()

    test1 = prompt_for_float("Enter Test 1 score: ")
    test2 = prompt_for_float("Enter Test 2 score: ")
    test3 = prompt_for_float("Enter Test 3 score: ")

    student = create_student_record(name, student_id, test1, test2, test3)
    students.append(student)
    save_students(students)
    print(f"Student {name} was added successfully.")


def display_students(students: list[dict]) -> None:
    """Display all student records in a formatted table."""
    if not students:
        print("No student records to display.")
        return

    print("\nStudent Records")
    print("-" * 110)
    print(f"{'Name':<15} {'ID':<12} {'Test 1':>8} {'Test 2':>8} {'Test 3':>8} {'Average':>10} {'Grade':>6}")
    print("-" * 110)
    for student in students:
        print(
            f"{student['name']:<15} {student['id']:<12} {student['test1']:>8.2f} {student['test2']:>8.2f} "
            f"{student['test3']:>8.2f} {student['average']:>10.2f} {student['grade']:>6}"
        )
    print("-" * 110)


def calculate_class_statistics(students: list[dict]) -> dict:
    """Calculate the highest average, lowest average, and class average."""
    if not students:
        return {"highest": 0.0, "lowest": 0.0, "class_average": 0.0}

    averages = [student["average"] for student in students]
    highest_average = max(averages)
    lowest_average = min(averages)
    class_average = round(sum(averages) / len(averages), 2)
    return {
        "highest": highest_average,
        "lowest": lowest_average,
        "class_average": class_average,
    }


def display_class_statistics(students: list[dict]) -> None:
    """Display class statistics."""
    if not students:
        print("No student records available for class statistics.")
        return

    stats = calculate_class_statistics(students)
    print("\nClass Statistics")
    print("-" * 40)
    print(f"Highest Average: {stats['highest']:.2f}")
    print(f"Lowest Average:  {stats['lowest']:.2f}")
    print(f"Class Average:   {stats['class_average']:.2f}")
    print("-" * 40)


def search_student(students: list[dict]) -> None:
    """Search for a student by name in a case-insensitive manner."""
    query = input("Enter a student name to search: ").strip()
    if not query:
        print("Search name cannot be blank.")
        return

    matches = [student for student in students if query.lower() in student["name"].lower()]
    if not matches:
        print(f"No student found matching '{query}'.")
        return

    print("\nSearch Results")
    print("-" * 110)
    print(f"{'Name':<15} {'ID':<12} {'Test 1':>8} {'Test 2':>8} {'Test 3':>8} {'Average':>10} {'Grade':>6}")
    print("-" * 110)
    for student in matches:
        print(
            f"{student['name']:<15} {student['id']:<12} {student['test1']:>8.2f} {student['test2']:>8.2f} "
            f"{student['test3']:>8.2f} {student['average']:>10.2f} {student['grade']:>6}"
        )
    print("-" * 110)


def print_menu() -> None:
    """Print the main menu."""
    print("\nStudent Grade Calculator")
    print("1. Add Student")
    print("2. Display All Students")
    print("3. Search for Student")
    print("4. Class Statistics")
    print("5. Save Records")
    print("ESC. Exit")


def main() -> None:
    """Run the main program loop."""
    students = load_students()
    print("\nWelcome to the Student Grade Calculator.")

    while True:
        print_menu()
        choice = input("Choose an option: ").strip()

        if choice.lower() == "esc":
            print("Exiting program. Goodbye!")
            save_students(students)
            break

        if choice == "1":
            add_student(students)
        elif choice == "2":
            display_students(students)
        elif choice == "3":
            search_student(students)
        elif choice == "4":
            display_class_statistics(students)
        elif choice == "5":
            save_students(students)
        else:
            print("Invalid option. Please choose 1, 2, 3, 4, 5, or ESC.")


if __name__ == "__main__":
    main()

