# ==============================
# Data Science Internship - Task 1
# ==============================

# ------------------------------
# Task 1: User Login Check
# ------------------------------

def task1_user_login_check():
    username = "admin"
    password = "1234"
    print("\n--- Task 1: User Login Check ---")

    if username == "admin" and password == "1234":
        print("Login Successful")
    else:
        print("Invalid Credentials")


# ------------------------------
# Task 2: Pass / Fail Analyzer
# ------------------------------

def task2_pass_fail_analyzer():
    marks = [45, 78, 90, 33, 60]
    pass_count = 0
    fail_count = 0
    print("\n--- Task 2: Pass / Fail Analyzer ---")

    for mark in marks:
        if mark >= 50:
            pass_count += 1
        else:
            fail_count += 1

    print("Total Pass Students:", pass_count)
    print("Total Fail Students:", fail_count)


# ------------------------------
# Task 3: Simple Data Cleaner
# ------------------------------

def task3_simple_data_cleaner():
    names = [" Alice ", "bob", " CHARLIE "]
    cleaned_names = []
    print("\n--- Task 3: Simple Data Cleaner ---")

    for name in names:
        cleaned = name.strip().lower()
        cleaned_names.append(cleaned)

    print("Cleaned Names:", cleaned_names)


# ------------------------------
# Task 4: Message Length Analyzer
# ------------------------------

def task4_message_length_analyzer():
    messages = ["Hi", "Welcome to the platform", "OK"]
    print("\n--- Task 4: Message Length Analyzer ---")

    for message in messages:
        length = len(message)
        print("Message:", message)
        print("Length:", length)

        if length > 10:
            print("⚠ Long Message")

        print()


# ------------------------------
# Task 5: Error Message Detector
# ------------------------------

def task5_error_message_detector():
    logs = ["INFO", "ERROR", "WARNING", "ERROR"]
    error_count = logs.count("ERROR")
    print("\n--- Task 5: Error Message Detector ---")
    print("Total ERROR entries:", error_count)


def main():
    task1_user_login_check()
    task2_pass_fail_analyzer()
    task3_simple_data_cleaner()
    task4_message_length_analyzer()
    task5_error_message_detector()


if __name__ == "__main__":
    main()
