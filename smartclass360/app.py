import streamlit as st
import plotly.graph_objects as go
import pandas as pd

# ----------🎓 OOP Classes ----------
class Student:
    def __init__(self, name: str, roll_no: int, grades: dict):
        self.name = name
        self.roll_no = roll_no
        self.grades = grades

    def calculate_average(self):
        return sum(self.grades.values()) / len(self.grades) if self.grades else 0

    def performance_remark(self):
        avg = self.calculate_average()
        if avg >= 85:
            return "🌟 Outstanding"
        elif avg >= 70:
            return "✅ Good"
        elif avg >= 50:
            return "⚠️ Needs Improvement"
        else:
            return "❌ Poor"

class StudentDatabase:
    def __init__(self):
        self.students = []

    def add_student(self, student: Student):
        if not self.get_student(student.roll_no):
            self.students.append(student)
            return True
        return False  # duplicate

    def get_student(self, roll_no: int):
        return next((s for s in self.students if s.roll_no == roll_no), None)

    def get_all_students(self):
        return self.students

    def reset(self):
        self.students = []

# ----------🌐 Streamlit UI ----------
st.set_page_config(page_title="SmartClass360", layout="centered", page_icon="🎓")
st.title("📊 SmartClass360 – AI-Powered Student Performance Dashboard")

if 'db' not in st.session_state:
    st.session_state.db = StudentDatabase()

db = st.session_state.db

# ----------👨‍💻 Add Student ----------
st.sidebar.header("👨‍💻 Add New Student")
name = st.sidebar.text_input("Full Name")
roll = st.sidebar.number_input("Roll No", min_value=1, step=1)

st.sidebar.subheader("💡 Subjects: Python, TypeScript, Next.js")
grades = {
    "Python": st.sidebar.slider("Python", 0, 100, 70),
    "TypeScript": st.sidebar.slider("TypeScript", 0, 100, 75),
    "Next.js": st.sidebar.slider("Next.js", 0, 100, 80),
}

if st.sidebar.button("➕ Add Student"):
    student = Student(name, roll, grades)
    added = db.add_student(student)
    if added:
        st.sidebar.success(f"{name} added successfully! 🎉")
    else:
        st.sidebar.error("Roll number already exists! ❌")

# ----------🔍 Search ----------
st.subheader("🔍 Search Student by Roll No")
search_roll = st.number_input("Enter Roll Number", min_value=1, step=1, key="search")

if st.button("🔎 Search"):
    student = db.get_student(search_roll)
    if student:
        st.success("🎉 Student Found")
        st.markdown(f"**👤 Name:** {student.name}")
        st.markdown(f"**🆔 Roll No:** {student.roll_no}")
        st.markdown(f"**📚 Grades:** {student.grades}")
        st.markdown(f"**📊 Average:** `{student.calculate_average():.2f}`")
        st.markdown(f"**📝 Remark:** {student.performance_remark()}")

        # ----------📈 Plotly Chart ----------
        st.subheader("📈 Visual Grade Distribution")

        subjects = list(student.grades.keys())
        scores = list(student.grades.values())

        fig = go.Figure(data=[
            go.Bar(
                x=subjects,
                y=scores,
                marker_color=["#4caf50", "#2196f3", "#ff9800"],
                text=[f"{s}%" for s in scores],
                textposition="auto"
            )
        ])

        fig.update_layout(
            title="📘 Subjects vs Grades",
            yaxis=dict(range=[0, 100], title="Marks"),
            xaxis_title="Subjects",
            height=400
        )

        st.plotly_chart(fig, use_container_width=True)

    else:
        st.warning("Student not found ❗")

# ----------📋 All Students Table ----------
st.subheader("🗂️ All Students Summary")

all_students = db.get_all_students()
if all_students:
    # Create DataFrame for All Students
    df = pd.DataFrame([{
        "Name": s.name,
        "Roll No": s.roll_no,
        "Python": s.grades["Python"],
        "TypeScript": s.grades["TypeScript"],
        "Next.js": s.grades["Next.js"],
        "Avg": s.calculate_average(),
        "Remark": s.performance_remark()
    } for s in all_students])

    st.dataframe(df, use_container_width=True)

    # ----------📊 Plotly Chart for All Students ----------
    st.subheader("📊 All Students Average Grade")

    student_names = [s.name for s in all_students]
    avg_grades = [s.calculate_average() for s in all_students]

    fig_all_students = go.Figure(data=[
        go.Bar(
            x=student_names,
            y=avg_grades,
            marker_color="#4caf50",
            text=[f"{avg:.2f}" for avg in avg_grades],
            textposition="auto"
        )
    ])

    fig_all_students.update_layout(
        title="📊 Student Names vs Average Grade",
        yaxis=dict(range=[0, 100], title="Average Marks"),
        xaxis_title="Students",
        height=500
    )

    st.plotly_chart(fig_all_students, use_container_width=True)

else:
    st.info("No students added yet.")

# ----------⚠️ Reset ----------
if st.button("🔄 Reset Student Data"):
    db.reset()
    st.success("Student database reset!")

# ----------👋 Footer ----------
st.markdown("---")
st.markdown("🚀 *Made by Tayyaba | Built using Python, Streamlit & OOP ✨*")
