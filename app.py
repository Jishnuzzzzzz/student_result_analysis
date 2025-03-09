import streamlit as st
import pandas as pd
import utils
import database

# Custom CSS for DeepSeek-like UI
def load_css():
    st.markdown(
        """
        <style>
        .stApp {
            background-color: #0E1117;
            color: #FFFFFF;
        }
        .stDataFrame {
            background-color: #1F2A3C;
            color: #FFFFFF;
            font-size: 18px;
            width: 100%;
        }
        .stDataFrame th {
            font-size: 20px;
            padding: 12px;
        }
        .stDataFrame td {
            font-size: 18px;
            padding: 10px;
        }
        .stDataFrame tr:hover {
            background-color: #2C3A4D;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

# Page configuration
st.set_page_config(page_title="Student Result Analysis", layout="wide")

# Load custom CSS
load_css()

# Admin login in the main div
def admin_login():
    st.title("Admin Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if username == "admin" and password == "admin123":
            st.session_state.logged_in = True
            st.success("Logged in successfully!")
        else:
            st.error("Invalid credentials")

# Upload CSV file and create database
def upload_csv_and_create_db():
    st.subheader("📂 Upload CSV File")
    uploaded_file = st.file_uploader("Choose a CSV file", type=["csv"])
    if uploaded_file is not None:
        try:
            df = pd.read_csv(uploaded_file)
            st.session_state.df = df  # Store the DataFrame in session state
            st.success("CSV file uploaded successfully!")

            # Allow user to name the database
            db_name = st.text_input("Enter a name for the database (without extension):", "student_results")
            if st.button("Create Database"):
                if db_name:
                    database.create_database_from_csv(df, db_name + ".db")
                    st.success(f"Database '{db_name}.db' created successfully!")
                    st.session_state.db_created = True
                else:
                    st.error("Please enter a valid database name.")
        except Exception as e:
            st.error(f"Error loading CSV file: {e}")
    return None

# Dashboard for data analysis
def dashboard():
    st.title("🎓 Student Result Analysis Dashboard")

    # Check if the DataFrame is available in session state
    if "df" not in st.session_state or st.session_state.df is None:
        st.warning("Please upload a CSV file first.")
        return

    df = st.session_state.df

    # Define columns representing marks
    marks_columns = ["Graphics & Multimedia", "Computer Networks", "Internet of Things"]

    # Display options in the sidebar
    st.sidebar.title("Options")
    option = st.sidebar.selectbox(
        "Select an option",
        [
            "Highest Mark",
            "Subjectwise Analysis",
            "Fail or Pass",
            "Top 5",
            "List of Failures",
            "Subjectwise Pass or Fail",
            "Compare Marks and Attendance",
            "Report Generation"
        ]
    )

    if option == "Highest Mark":
        st.subheader("🏆 Highest Mark")
        highest_mark = df[df['Total Marks'] == df['Total Marks'].max()]
        st.write(highest_mark)

    elif option == "Subjectwise Analysis":
        st.subheader("📊 Subjectwise Analysis")
        subject = st.selectbox("Select Subject", marks_columns)
        subject_data = df[['Name', subject]]
        st.write(subject_data)

    elif option == "Fail or Pass":
        st.subheader("✅ Fail or Pass")
        for subject in marks_columns:
            df[f'{subject}_status'] = df[subject].apply(utils.calculate_pass_fail)
        st.write(df[['Name'] + marks_columns + [f'{col}_status' for col in marks_columns]])

    elif option == "Top 5":
        st.subheader("🥇 Top 5 Students")
        top_5 = utils.get_top_students(df)
        st.write(top_5)

    elif option == "List of Failures":
        st.subheader("❌ List of Failures")
        failures = utils.get_failures(df, marks_columns)
        if failures:
            for subject, students in failures.items():
                st.write(f"**{subject} Failures:**")
                if students:
                    # Convert the list of students into a DataFrame for better display
                    failures_df = pd.DataFrame(students, columns=["Name"])
                    st.dataframe(failures_df)  # Display as a table
                else:
                    st.write("No failures in this subject.")
        else:
            st.write("No failures found.")

    elif option == "Subjectwise Pass or Fail":
        st.subheader("📚 Subjectwise Pass or Fail")
        subject = st.selectbox("Select Subject", marks_columns)
        subject_data = df[['Name', subject]]
        subject_data['status'] = subject_data[subject].apply(utils.calculate_pass_fail)
        st.write(subject_data)

    elif option == "Compare Marks and Attendance":
        st.subheader("📈 Compare Marks and Attendance")
        st.scatter_chart(df, x='Attendance', y='Total Marks')

    elif option == "Report Generation":
        st.subheader("📄 Report Generation")
        report = utils.generate_report(df, marks_columns)
        st.write(report)
        st.download_button(
            label="Download Report",
            data=report.to_csv(index=False).encode('utf-8'),
            file_name='student_report.csv',
            mime='text/csv'
        )

# Main app logic
def main():
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False
    if "df" not in st.session_state:
        st.session_state.df = None
    if "db_created" not in st.session_state:
        st.session_state.db_created = False

    # Show login in the main div if not logged in
    if not st.session_state.logged_in:
        admin_login()
    else:
        # Show the sidebar only after login
        if not st.session_state.db_created:
            upload_csv_and_create_db()
        else:
            dashboard()

if __name__ == "__main__":
    main()