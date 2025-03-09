import pandas as pd

def calculate_pass_fail(marks, total_marks=100):
    """
    Determines if a student has passed or failed based on marks.

    Args:
        marks (int): Marks obtained by the student.
        total_marks (int): Total marks for the subject (default is 100).

    Returns:
        str: 'Pass' if marks >= 33% of total_marks, otherwise 'Fail'.
    """
    pass_mark = 0.33 * total_marks  # 33% of total marks
    return 'Pass' if marks >= pass_mark else 'Fail'

def get_top_students(df, n=5):
    """
    Returns the top N students based on total marks.

    Args:
        df (pd.DataFrame): DataFrame containing student data.
        n (int): Number of top students to return.

    Returns:
        pd.DataFrame: DataFrame of the top N students.
    """
    try:
        # Get the top N students based on Total Marks
        top_students = df.nlargest(n, 'Total Marks')
        return top_students
    except KeyError:
        print("Error: 'Total Marks' column not found in DataFrame.")
        return pd.DataFrame()

def get_failures(df, marks_columns):
    """
    Identifies students who failed in each subject (marks < 33% of total marks).

    Args:
        df (pd.DataFrame): DataFrame containing student data.
        marks_columns (list): List of columns representing marks.

    Returns:
        dict: A dictionary where keys are subject names and values are lists of failing students.
    """
    try:
        failures = {}
        for subject in marks_columns:
            pass_mark = 0.33 * 100  # Assuming each subject is out of 100
            failing_students = df[df[subject] < pass_mark]['Name'].tolist()
            failures[subject] = failing_students
        return failures
    except KeyError:
        print("Error: Required columns not found in DataFrame.")
        return {}
def generate_report(df, marks_columns):
    """
    Generates a report with average marks and attendance for each student.

    Args:
        df (pd.DataFrame): DataFrame containing student data.
        marks_columns (list): List of columns representing marks.

    Returns:
        pd.DataFrame: Report DataFrame with columns: Name, Average Marks, Average Attendance.
    """
    try:
        # Calculate average marks and attendance
        report = df.groupby('Name').agg(
            Average_Marks=('Total Marks', 'mean'),
            Average_Attendance=('Attendance', 'mean')
        ).reset_index()
        return report
    except KeyError:
        print("Error: Required columns not found in DataFrame.")
        return pd.DataFrame()