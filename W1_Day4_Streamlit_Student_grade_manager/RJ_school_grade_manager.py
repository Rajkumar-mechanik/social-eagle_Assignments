import streamlit as st
import io
import xlwt


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="RJ International School",
    page_icon="🎓",
    layout="wide"
)


# ============================================================
# CUSTOM LIGHT THEME
# ============================================================

st.markdown(
    """
    <style>

    /* Main application background */
    .stApp {
        background: linear-gradient(
            135deg,
            #f4f9ff 0%,
            #eaf4ff 50%,
            #ffffff 100%
        );
    }

    /* Main content width */
    .block-container {
        max-width: 1200px;
        padding-top: 2rem;
        padding-bottom: 3rem;
    }

    /* School title */
    .school-title {
        font-size: 42px;
        font-weight: 900;
        text-align: center;
        color: #174ea6;
        margin-bottom: 5px;
    }

    /* School subtitle */
    .school-subtitle {
        font-size: 28px;
        font-weight: 800;
        text-align: center;
        color: #1f2937;
        margin-bottom: 30px;
    }

    /* Section heading */
    .section-heading {
        font-size: 24px;
        font-weight: 800;
        color: #174ea6;
        margin-top: 20px;
        margin-bottom: 10px;
    }

    /* Table title */
    .table-title {
        font-size: 26px;
        font-weight: 800;
        color: #174ea6;
        background-color: #ffffff;
        padding: 15px 20px;
        border-left: 6px solid #2563eb;
        border-radius: 10px;
        margin-top: 25px;
        margin-bottom: 15px;
    }

    /* Buttons */
    .stButton > button {
        border-radius: 8px;
        font-weight: 700;
        min-height: 42px;
    }

    /* Download button */
    .stDownloadButton > button {
        border-radius: 8px;
        font-weight: 700;
        min-height: 42px;
    }

    /* Footer */
    .footer {
        text-align: center;
        color: #64748b;
        font-size: 14px;
        margin-top: 40px;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# SESSION STATE
# ============================================================

if "students" not in st.session_state:
    st.session_state.students = []

if "selected_class" not in st.session_state:
    st.session_state.selected_class = None

if "selected_section" not in st.session_state:
    st.session_state.selected_section = None


# ============================================================
# GRADE CALCULATION
# ============================================================

def calculate_grade(mark):

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


# ============================================================
# CREATE XLS FILE
# ============================================================

def create_xls_file(students, class_number, section):

    # --------------------------------------------------------
    # Create workbook and worksheet
    # --------------------------------------------------------

    workbook = xlwt.Workbook()

    worksheet = workbook.add_sheet(
        f"Class {class_number}-{section}"
    )


    # ========================================================
    # TITLE STYLE
    # ========================================================

    title_font = xlwt.Font()

    title_font.bold = True

    title_font.height = 320


    title_alignment = xlwt.Alignment()

    title_alignment.horz = xlwt.Alignment.HORZ_CENTER

    title_alignment.vert = xlwt.Alignment.VERT_CENTER


    title_style = xlwt.XFStyle()

    title_style.font = title_font

    title_style.alignment = title_alignment


    # ========================================================
    # HEADER STYLE
    # ========================================================

    header_font = xlwt.Font()

    header_font.bold = True


    header_alignment = xlwt.Alignment()

    header_alignment.horz = xlwt.Alignment.HORZ_CENTER

    header_alignment.vert = xlwt.Alignment.VERT_CENTER


    header_style = xlwt.XFStyle()

    header_style.font = header_font

    header_style.alignment = header_alignment


    # ========================================================
    # NORMAL CELL STYLE
    # ========================================================

    cell_alignment = xlwt.Alignment()

    cell_alignment.horz = xlwt.Alignment.HORZ_CENTER

    cell_alignment.vert = xlwt.Alignment.VERT_CENTER


    cell_style = xlwt.XFStyle()

    cell_style.alignment = cell_alignment


    # ========================================================
    # EXCEL TITLE
    # ========================================================

    worksheet.write_merge(
        0,
        0,
        0,
        3,
        (
            f"RJ International School - "
            f"Class {class_number} - Section {section}"
        ),
        title_style
    )


    # ========================================================
    # COLUMN HEADERS
    # ========================================================

    headers = [
        "No.",
        "Student Name",
        "Mark",
        "Grade"
    ]


    for column, header in enumerate(headers):

        worksheet.write(
            2,
            column,
            header,
            header_style
        )


    # ========================================================
    # STUDENT DATA
    # ========================================================

    for row, student in enumerate(
        students,
        start=3
    ):

        # Student number
        worksheet.write(
            row,
            0,
            row - 2,
            cell_style
        )


        # Student name
        worksheet.write(
            row,
            1,
            student["Name"],
            cell_style
        )


        # Mark
        worksheet.write(
            row,
            2,
            student["Mark"],
            cell_style
        )


        # Grade
        worksheet.write(
            row,
            3,
            student["Grade"],
            cell_style
        )


    # ========================================================
    # COLUMN WIDTHS
    # ========================================================

    worksheet.col(0).width = 2000

    worksheet.col(1).width = 8000

    worksheet.col(2).width = 4000

    worksheet.col(3).width = 4000


    # ========================================================
    # SAVE FILE TO MEMORY
    # ========================================================

    output = io.BytesIO()

    workbook.save(output)

    output.seek(0)

    return output

# ============================================================
# SCHOOL HEADER
# ============================================================

st.markdown(
    '<div class="school-title">🎓 RJ INTERNATIONAL SCHOOL</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="school-subtitle">Student Grade Management System</div>',
    unsafe_allow_html=True
)


# ============================================================
# CLASS AND SECTION
# ============================================================

st.markdown(
    '<div class="section-heading">📚 Select Class & Section</div>',
    unsafe_allow_html=True
)


class_col, section_col, button_col = st.columns(
    [2, 2, 1]
)


with class_col:

    selected_class = st.selectbox(
        "Class",
        list(range(1, 13)),
        format_func=lambda x: f"Class {x}"
    )


with section_col:

    selected_section = st.selectbox(
        "Section",
        ["A", "B", "C", "D"]
    )


with button_col:

    st.write("")

    if st.button(
        "➕ Add Class",
        use_container_width=True
    ):

        st.session_state.selected_class = selected_class

        st.session_state.selected_section = selected_section

        st.success(
            f"Class {selected_class} - "
            f"Section {selected_section} selected."
        )


# ============================================================
# SHOW STUDENT AREA AFTER CLASS IS ADDED
# ============================================================

if (
    st.session_state.selected_class is not None
    and
    st.session_state.selected_section is not None
):

    current_class = st.session_state.selected_class

    current_section = st.session_state.selected_section


    # ========================================================
    # STUDENT INPUT
    # ========================================================

    st.markdown(
        '<div class="section-heading">👨‍🎓 Student Details</div>',
        unsafe_allow_html=True
    )


    name_col, mark_col, add_col = st.columns(
        [3, 2, 1]
    )


    with name_col:

        student_name = st.text_input(
            "Student Name",
            placeholder="Enter student name"
        )


    with mark_col:

        student_mark = st.number_input(
            "Mark",
            min_value=0,
            max_value=100,
            value=0,
            step=1
        )


    with add_col:

        st.write("")

        add_student = st.button(
            "➕ Add Student",
            use_container_width=True
        )


    # ========================================================
    # ADD STUDENT
    # ========================================================

    if add_student:

        clean_name = student_name.strip()


        # ----------------------------------------------------
        # Validate Student Name
        # ----------------------------------------------------

        if not clean_name:

            st.error(
                "Please enter the student name."
            )


        # ----------------------------------------------------
        # Add Student
        # ----------------------------------------------------

        else:

            grade = calculate_grade(
                student_mark
            )


            student = {
                "Class": current_class,
                "Section": current_section,
                "Name": clean_name,
                "Mark": student_mark,
                "Grade": grade
            }


            st.session_state.students.append(
                student
            )


            st.success(
                f"{clean_name} added successfully "
                f"with Grade {grade}."
            )


    # ========================================================
    # FILTER STUDENTS FOR CURRENT CLASS & SECTION
    # ========================================================

    current_students = [

        student

        for student in st.session_state.students

        if (
            student["Class"] == current_class
            and
            student["Section"] == current_section
        )
    ]


    # ========================================================
    # TABLE TITLE
    # ========================================================

    st.markdown(
        f"""
        <div class="table-title">
            📋 Class {current_class} - Section {current_section}
            Student Grade List
        </div>
        """,
        unsafe_allow_html=True
    )


    # ========================================================
    # STUDENT TABLE
    # ========================================================

    if current_students:

        # ----------------------------------------------------
        # Create table data
        # ----------------------------------------------------

        table_data = []


        for number, student in enumerate(
            current_students,
            start=1
        ):

            table_data.append(
                {
                    "No.": number,
                    "Student Name": student["Name"],
                    "Mark": student["Mark"],
                    "Grade": student["Grade"]
                }
            )


        # ----------------------------------------------------
        # Display Student Table
        # ----------------------------------------------------

        st.table(table_data)


        # ====================================================
        # EXPORT TO XLS
        # ====================================================

        xls_file = create_xls_file(
            current_students,
            current_class,
            current_section
        )


        st.download_button(
            label="📥 Export to XLS",
            data=xls_file,
            file_name=(
                f"Class_{current_class}_"
                f"Section_{current_section}_"
                f"Student_Grades.xls"
            ),
            mime="application/vnd.ms-excel",
            use_container_width=True
        )


        # ====================================================
        # CLASS SUMMARY
        # ====================================================

        st.markdown(
            '<div class="section-heading">📊 Class Summary</div>',
            unsafe_allow_html=True
        )


        total_students = len(
            current_students
        )


        total_marks = sum(
            student["Mark"]
            for student in current_students
        )


        average_mark = (
            total_marks / total_students
        )


        highest_mark = max(
            student["Mark"]
            for student in current_students
        )


        summary_col1, summary_col2, summary_col3 = st.columns(3)


        with summary_col1:

            st.metric(
                "👨‍🎓 Total Students",
                total_students
            )


        with summary_col2:

            st.metric(
                "📈 Average Mark",
                f"{average_mark:.2f}"
            )


        with summary_col3:

            st.metric(
                "🏆 Highest Mark",
                highest_mark
            )


        # ====================================================
        # REMOVE STUDENT
        # ====================================================

        st.markdown(
            '<div class="section-heading">🗑️ Remove Student</div>',
            unsafe_allow_html=True
        )


        student_options = [

            student["Name"]

            for student in current_students
        ]


        selected_student = st.selectbox(
            "Select Student",
            student_options
        )


        if st.button(
            "🗑️ Remove Selected Student"
        ):

            st.session_state.students = [

                student

                for student in st.session_state.students

                if not (
                    student["Class"] == current_class
                    and
                    student["Section"] == current_section
                    and
                    student["Name"] == selected_student
                )
            ]


            st.success(
                f"{selected_student} removed successfully."
            )


            st.rerun()


    else:

        st.info(
            f"No students added yet for "
            f"Class {current_class} - "
            f"Section {current_section}."
        )


# ============================================================
# WELCOME MESSAGE
# ============================================================

else:

    st.info(
        "👋 Select a Class and Section, then click "
        "'Add Class' to start entering student details."
    )


# ============================================================
# GRADE SCALE
# ============================================================

st.markdown(
    '<div class="section-heading">🏆 Grade Scale</div>',
    unsafe_allow_html=True
)


grade_col1, grade_col2, grade_col3, grade_col4, grade_col5 = st.columns(5)


with grade_col1:

    st.metric(
        "A",
        "90 - 100"
    )


with grade_col2:

    st.metric(
        "B",
        "80 - 89"
    )


with grade_col3:

    st.metric(
        "C",
        "70 - 79"
    )


with grade_col4:

    st.metric(
        "D",
        "60 - 69"
    )


with grade_col5:

    st.metric(
        "E",
        "Below 60"
    )


# ============================================================
# FOOTER
# ============================================================

st.markdown(
    """
    <div class="footer">
        © 2026 RJ International School
        <br>
        Student Grade Management System
    </div>
    """,
    unsafe_allow_html=True
)
