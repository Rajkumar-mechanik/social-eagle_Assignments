students = []


def get_grade(mark):
    if mark >= 90:
        return "A"
    elif mark >= 80:
        return "B"
    elif mark >= 70:
        return "C"
    elif mark >= 60:
        return "D"
    else:
        return "E"


def add_student():
    # Validate student name
    while True:
        name = input("Enter student name: ").strip()
        if name:
            break
        print("Name cannot be empty. Please enter a valid name.")

    # Validate student mark
    while True:
        raw_mark = input("Enter mark (0-100): ").strip()
        try:
            mark = float(raw_mark)
            if mark < 0 or mark > 100:
                print("Invalid mark. Marks must be between 0 and 100.")
                continue
            # Store whole numbers cleanly as integers
            if mark.is_integer():
                mark = int(mark)
            break
        except ValueError:
            print("Invalid input. Please enter a valid numerical mark.")

    grade = get_grade(mark)
    students.append({"name": name, "mark": mark, "grade": grade})
    print(f"Added {name} with a mark of {mark} (Grade: {grade}).")


def show_results():
    if not students:
        print("\nNo student records found. Add at least one student first.")
        return

    # Print table header
    print(f"\n{'Name':<12} {'Mark':>4}   {'Grade':>5}")

    total_marks = 0
    highest = students[0]["mark"]
    lowest = students[0]["mark"]

    for s in students:
        mark = s["mark"]
        total_marks += mark

        if mark > highest:
            highest = mark
        if mark < lowest:
            lowest = mark

        print(f"{s['name']:<12} {mark:>4}   {s['grade']:>5}")

    average = total_marks / len(students)
    print(f"Average: {average:.1f}   Highest: {highest}   Lowest: {lowest}")


def main():
    """Menu loop to manage student records."""
    while True:
        print("\n=== Student Grade Manager ===")
        print("1. Add Student")
        print("2. Show Results")
        print("3. Quit")

        choice = input("Select an option (1-3): ").strip()

        if choice == "1":
            add_student()
        elif choice == "2":
            show_results()
        elif choice == "3":
            print("Exiting program. Goodbye!")
            break
        else:
            print("Invalid selection. Please enter 1, 2, or 3.")


if __name__ == "__main__":
    main()
