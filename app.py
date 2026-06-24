import pandas as pd
import streamlit as st
from pathlib import Path
from datetime import date

TASKS_FILE = Path("tasks.csv")

TASK_COLUMNS = [
    "task_id",
    "title",
    "course_project",
    "priority",
    "status",
    "deadline",
    "created_at",
    "completed_at",
]

def create_empty_tasks_df():
    return pd.DataFrame(columns=TASK_COLUMNS)


def save_tasks(tasks_df):
    tasks_df = tasks_df.reindex(columns=TASK_COLUMNS)
    tasks_df.to_csv(TASKS_FILE, index=False)


def load_tasks():
    if not TASKS_FILE.exists() or TASKS_FILE.stat().st_size == 0:
        empty_df = create_empty_tasks_df()
        save_tasks(empty_df)
        return empty_df

    try:
        tasks_df = pd.read_csv(TASKS_FILE, dtype=str)
    except pd.errors.EmptyDataError:
        empty_df = create_empty_tasks_df()
        save_tasks(empty_df)
        return empty_df

    tasks_df = tasks_df.reindex(columns=TASK_COLUMNS)
    tasks_df = tasks_df.fillna("")

    return tasks_df

def get_next_task_id(tasks_df):
    if tasks_df.empty:
        return 1

    task_ids = pd.to_numeric(tasks_df["task_id"], errors="coerce")

    if task_ids.dropna().empty:
        return 1

    return int(task_ids.max()) + 1

def add_task_form(tasks_df):
    st.subheader("Add New Task")

    with st.form("add_task_form", clear_on_submit=True):
        title = st.text_input("Task title")
        course_project = st.text_input("Course / Project")
        priority = st.selectbox("Priority", ["Low", "Medium", "High"])
        deadline = st.date_input("Deadline")

        submitted = st.form_submit_button("Add Task")

    if submitted:
        title = title.strip()
        course_project = course_project.strip()

        if title == "":
            st.error("Task title cannot be empty.")
            return tasks_df

        new_task = {
            "task_id": get_next_task_id(tasks_df),
            "title": title,
            "course_project": course_project,
            "priority": priority,
            "status": "Pending",
            "deadline": deadline.isoformat(),
            "created_at": date.today().isoformat(),
            "completed_at": "",
        }

        updated_tasks = pd.concat(
            [tasks_df, pd.DataFrame([new_task])],
            ignore_index=True
        )

        save_tasks(updated_tasks)
        st.success("Task added and saved.")

        return updated_tasks

    return tasks_df


def display_tasks(tasks):
    st.subheader("Task List")

    if tasks.empty:
        st.info("No tasks yet. Add your first study task using the form above.")
        return

    visible_columns = [
        "task_id",
        "title",
        "course_project",
        "priority",
        "status",
        "deadline",
        "created_at",
    ]

    existing_columns = [column for column in visible_columns if column in tasks.columns]

    display_df = tasks[existing_columns].copy()

    display_df = display_df.rename(
        columns={
            "task_id": "ID",
            "title": "Task",
            "course_project": "Course / Project",
            "priority": "Priority",
            "status": "Status",
            "deadline": "Deadline",
            "created_at": "Created",
        }
    )

    st.dataframe(
        display_df,
        use_container_width=True,
        hide_index=True,
    )

    st.caption(f"Showing {len(display_df)} saved task(s).")


# Page setup
st.set_page_config(
    page_title="Study Task Tracker",
    page_icon="📚",
    layout="wide"
)

tasks = load_tasks()


# Temporary preview data for the task table.
# This will be replaced in Step 05 Display Tasks.
preview_tasks = pd.DataFrame(
    [
        {
            "title": "Review lecture notes",
            "course_project": "Machine Learning",
            "priority": "High",
            "status": "Pending",
            "deadline": "2026-06-28",
        },
        {
            "title": "Finish Streamlit layout",
            "course_project": "Project 02",
            "priority": "Medium",
            "status": "Pending",
            "deadline": "2026-06-30",
        },
        {
            "title": "Submit assignment draft",
            "course_project": "Numerical Computation",
            "priority": "Low",
            "status": "Completed",
            "deadline": "2026-06-20",
        },
    ]
)


# Sidebar
st.sidebar.title("Filters")
st.sidebar.caption("Filter controls will work after the data model and CSV logic are added.")

status_filter = st.sidebar.selectbox(
    "Status",
    ["All", "Pending", "Completed"]
)

priority_filter = st.sidebar.selectbox(
    "Priority",
    ["All", "High", "Medium", "Low"]
)

course_filter = st.sidebar.selectbox(
    "Course / Project",
    ["All", "Machine Learning", "Numerical Computation", "Project 02"]
)


# Main page header
st.title("Study Task Tracker")
st.caption("Track university tasks, deadlines, priorities, and progress.")


# Summary metrics
st.subheader("Overview")

metric_col_1, metric_col_2, metric_col_3, metric_col_4 = st.columns(4)

with metric_col_1:
    st.metric("Total Tasks", "3")

with metric_col_2:
    st.metric("Pending", "2")

with metric_col_3:
    st.metric("Completed", "1")

with metric_col_4:
    st.metric("Overdue", "0")


# Overdue warning placeholder
st.subheader("Overdue Tasks")
st.success("No overdue tasks. Real overdue logic will be added later.")


# Monthly deadline overview placeholder
st.subheader("Monthly Deadline Overview")
with st.container():
    st.info("Calendar preview will appear here after deadline logic is added.")


tasks = add_task_form(tasks)
display_tasks(tasks)


# Chart placeholder
st.subheader("Progress Preview")
st.caption("This chart is temporary. Later it will use real task status data.")

chart_data = pd.DataFrame(
    {
        "count": [2, 1]
    },
    index=["Pending", "Completed"]
)

st.bar_chart(chart_data)

with st.expander("CSV Storage Test"):
    st.write(f"Loaded {len(tasks)} tasks from tasks.csv")
    st.dataframe(tasks, use_container_width=True)