def get_grade_point(marks):
    if marks >= 90:
        return 10
    elif marks >= 80:
        return 9
    elif marks >= 70:
        return 8
    elif marks >= 60:
        return 7
    elif marks >= 55:
        return 6
    elif marks >= 50:
        return 5.5
    elif marks > 40:
        return 5
    elif marks == 40:
        return 4
    else:
        return 0


def get_practical_gp(marks):
    if marks >= 45:
        return 10
    elif marks >= 39:
        return 9
    elif marks >= 35:
        return 8
    elif marks >= 30:
        return 7
    elif marks >= 25:
        return 6
    elif marks >= 22:
        return 5
    else:
        return 0


def main():
    while True:

        print("\n=== GPA Calculator ===")
        print("1. Calculate SGPA")
        print("2. Calculate CGPA")
        print("3. Exit")

        choice = input("Enter your choice (1, 2 or 3): ")

        # ---------------- SGPA ----------------
        if choice == "1":
            try:
                n_theory = int(input("Enter number of theory subjects: "))
                n_practical = int(input("Enter number of practical subjects: "))
                if n_theory <= 0:
                    print("Number of subjects must be greater than 0.")
                    continue
            except ValueError:
                print("Invalid input! Please enter a valid number.")
                continue

            total_weighted_gp = 0
            total_credits = 0

            for i in range(1, n_theory + 1):
                while True:
                    try:
                        marks = float(input(f"Enter marks for subject {i}: "))
                        if marks < 0 or marks > 100:
                            print("Enter marks between 0 and 100.")
                            continue

                        credit = float(input(f"Enter credit for subject {i}: "))
                        gp = get_grade_point(marks)

                        total_weighted_gp += gp * credit
                        total_credits += credit
                        break

                    except ValueError:
                        print("Invalid input!")

            print("\n--- Practical Subjects ---")

            for i in range(1, n_practical + 1):
                while True:
                    try:
                        marks = float(input(f"Enter practical marks for subject {i}: "))
                        if marks < 0 or marks > 50:
                            print("Enter marks between 0 and 50.")
                            continue

                        credit = float(input(f"Enter credit for practical subject {i}: "))
                        gp = get_practical_gp(marks)

                        total_weighted_gp += gp * credit
                        total_credits += credit
                        break

                    except ValueError:
                        print("Invalid input!")

            if total_credits > 0:
                sgpa = total_weighted_gp / total_credits
                print(f"\nFinal SGPA: {round(sgpa, 2)}")

        # ---------------- CGPA ----------------
        elif choice == "2":
            try:
                n_sem = int(input("Enter number of semesters: "))
                if n_sem <= 0:
                    print("Invalid number of semesters.")
                    continue
            except ValueError:
                print("Invalid input!")
                continue

            total_sgpa_weighted = 0
            total_sem_credits = 0

            for i in range(1, n_sem + 1):
                try:
                    sgpa_input = float(input(f"Enter SGPA for semester {i}: "))
                    credits = float(input(f"Enter credits for semester {i}: "))

                    total_sgpa_weighted += sgpa_input * credits
                    total_sem_credits += credits

                except ValueError:
                    print("Invalid input! Skipping...")

            if total_sem_credits > 0:
                cgpa = total_sgpa_weighted / total_sem_credits
                print(f"\nFinal CGPA: {round(cgpa, 2)}")

        elif choice == "3":
            print("Exiting program. Thank you!")
            break

        else:
            print("Invalid choice! Try again.")


if __name__ == "__main__":
    main()