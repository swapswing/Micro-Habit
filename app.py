import streamlit as st
import json
from pathlib import Path
from datetime import date, timedelta

st.set_page_config(
    page_title="Micro Habits",
    page_icon="🌱",
    layout="centered",
)

DATA_FILE = Path(__file__).with_name("habits_data.json")

PRESETS = [
    {"id": "move", "label": "Move more", "action": "Put on one shoe."},
    {"id": "read", "label": "Read more", "action": "Read one word."},
    {"id": "eat", "label": "Eat well", "action": "Eat one bite of something green."},
    {"id": "water", "label": "Drink water", "action": "Take one sip of water."},
    {"id": "meditate", "label": "Meditate", "action": "Take one slow breath."},
    {"id": "write", "label": "Write", "action": "Write one word."},
    {"id": "tidy", "label": "Tidy up", "action": "Put one thing back in place."},
    {"id": "stretch", "label": "Stretch", "action": "Touch your toes, once."},
]

STARTER_IDS = ["move", "read", "eat", "water"]
STARTER_STREAKS = {"move": 12, "read": 5, "eat": 8, "water": 21}


def suggest_micro(goal_raw: str) -> str:
    goal = goal_raw.strip()
    g = goal.lower()

    if not goal:
        return ""

    if any(word in g for word in ["guitar", "piano", "violin", "instrument"]):
        return "Pick it up and hold it for 10 seconds."

    if any(word in g for word in ["sleep", "bed"]):
        return "Turn off one light, 10 minutes early."

    if any(word in g for word in ["save", "budget", "money"]):
        return "Move one coin into savings."

    if any(word in g for word in ["code", "programming", "coding"]):
        return "Open the editor and write one line."

    if any(word in g for word in ["clean", "declutter", "organize", "organise"]):
        return "Put one thing back in its place."

    if any(word in g for word in ["write", "journal", "blog"]):
        return "Write one sentence."

    if any(word in g for word in ["spanish", "french", "language", "vocab"]):
        return "Learn one new word."

    return f'Do the smallest possible version of "{goal}" — for 10 seconds.'


def default_habits():
    habits = []

    for preset_id in STARTER_IDS:
        preset = next(p for p in PRESETS if p["id"] == preset_id)

        habits.append(
            {
                **preset,
                "streak": STARTER_STREAKS.get(preset_id, 0),
                "completed": False,
                "last_completed": None,
            }
        )

    return habits


def load_data():
    if DATA_FILE.exists():
        try:
            data = json.loads(DATA_FILE.read_text(encoding="utf-8"))
            habits = data.get("habits", default_habits())
            last_open = data.get("last_open_date")

            # Reset completion status when a new day starts.
            if last_open != str(date.today()):
                for habit in habits:
                    habit["completed"] = False

            return habits

        except Exception:
            return default_habits()

    return default_habits()


def save_data():
    data = {
        "habits": st.session_state.habits,
        "last_open_date": str(date.today()),
    }

    DATA_FILE.write_text(
        json.dumps(data, indent=2),
        encoding="utf-8",
    )


def update_streak(habit):
    today = date.today()
    last_completed = habit.get("last_completed")

    last_date = None

    if last_completed:
        try:
            last_date = date.fromisoformat(last_completed)
        except ValueError:
            last_date = None

    # Do not increase twice on the same day.
    if last_date == today:
        return

    # Continue streak if completed yesterday.
    if last_date == today - timedelta(days=1):
        habit["streak"] = habit.get("streak", 0) + 1

    # First completion.
    elif last_date is None:
        habit["streak"] = max(habit.get("streak", 0), 0) + 1

    # Missed one or more days.
    else:
        habit["streak"] = 1

    habit["last_completed"] = str(today)


# --------------------------
# SESSION STATE
# --------------------------

if "habits" not in st.session_state:
    st.session_state.habits = load_data()

if "current_id" not in st.session_state:
    st.session_state.current_id = (
        st.session_state.habits[0]["id"]
        if st.session_state.habits
        else None
    )

if "view" not in st.session_state:
    st.session_state.view = "focus"

if "suggested_micro" not in st.session_state:
    st.session_state.suggested_micro = ""


# --------------------------
# CSS
# --------------------------

st.markdown(
    """
    <style>

    /* Main page background */
    .stApp {
        background: #1B241D;
    }

    /* Hide Streamlit header/footer */
    header[data-testid="stHeader"] {
        background: transparent;
    }

    footer {
        visibility: hidden;
    }

    /* Main app card */
    .block-container {
        max-width: 430px;
        background: #EEF0E3;
        border-radius: 30px;
        padding: 28px 28px 34px 28px !important;
        margin-top: 28px;
        margin-bottom: 28px;
        box-shadow: 0 25px 55px rgba(0, 0, 0, 0.35);
        min-height: 650px;
    }

    /* General text */
    .block-container,
    .block-container p,
    .block-container span,
    .block-container label {
        color: #202B22;
    }

    /* Progress text */
    .progress-text {
        font-size: 13px;
        color: #647163;
        margin-top: 4px;
        margin-bottom: 8px;
    }

    /* Habit label */
    .habit-label {
        font-size: 14px;
        color: #647163;
        text-align: center;
        margin-top: 45px;
        margin-bottom: 12px;
    }

    /* Large micro-habit text */
    .habit-action {
        font-family: Georgia, serif;
        font-size: 34px;
        line-height: 1.2;
        font-weight: 500;
        text-align: center;
        color: #202B22;
        margin: 10px auto 30px auto;
        max-width: 320px;
    }

    /* Streak */
    .streak {
        text-align: center;
        color: #647163;
        margin-top: 18px;
        margin-bottom: 12px;
        font-size: 14px;
    }

    /* Completed page */
    .done-title {
        text-align: center;
        font-family: Georgia, serif;
        font-size: 30px;
        font-weight: 500;
        color: #202B22;
        padding-top: 65px;
        margin-bottom: 8px;
    }

    .done-subtitle {
        text-align: center;
        color: #647163;
        font-size: 14px;
        margin-bottom: 28px;
    }

    /* Preset cards */
    .micro-card {
        padding: 12px 14px;
        background: #F6F7EF;
        border-radius: 14px;
        border: 1px solid #D8DECB;
        margin-bottom: 8px;
        color: #202B22;
    }

    .micro-card small {
        color: #8A9587;
    }

    /* Streamlit buttons */
    div.stButton > button {
        border-radius: 14px;
        min-height: 44px;
        font-weight: 600;
    }

    div.stButton > button[kind="primary"] {
        background: #4B7857;
        border-color: #4B7857;
    }

    div.stButton > button[kind="primary"]:hover {
        background: #3F694B;
        border-color: #3F694B;
    }

    /* Input controls */
    div[data-baseweb="input"] input,
    textarea {
        border-radius: 12px !important;
    }

    /* Progress bar */
    div[data-testid="stProgress"] > div > div > div {
        background-color: #4B7857;
    }

    /* Expander */
    details {
        background: #F6F7EF;
        border-radius: 14px;
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# --------------------------
# APP LOGIC
# --------------------------

habits = st.session_state.habits
done_count = sum(1 for h in habits if h.get("completed"))
total = len(habits)

top_left, top_right = st.columns([2, 1])

with top_left:
    st.markdown(
        f'<div class="progress-text">{done_count} of {total} today</div>',
        unsafe_allow_html=True,
    )

with top_right:
    if st.button("＋ Add habit", use_container_width=True):
        st.session_state.view = "add"
        st.rerun()

if total > 0:
    st.progress(done_count / total)
else:
    st.progress(0)


# --------------------------
# ADD HABIT VIEW
# --------------------------

if st.session_state.view == "add":

    st.markdown("### Add a habit")

    if st.button("← Back"):
        st.session_state.view = "focus"
        st.rerun()

    st.caption("Pick one")

    added_ids = {h["id"] for h in st.session_state.habits}

    for preset in PRESETS:

        col1, col2 = st.columns([3, 1])

        with col1:
            st.markdown(
                f"""
                <div class="micro-card">
                    <b>{preset["label"]}</b><br>
                    <small>{preset["action"]}</small>
                </div>
                """,
                unsafe_allow_html=True,
            )

        with col2:

            if preset["id"] in added_ids:

                st.button(
                    "Added",
                    key=f"added_{preset['id']}",
                    disabled=True,
                    use_container_width=True,
                )

            else:

                if st.button(
                    "Add",
                    key=f"add_{preset['id']}",
                    use_container_width=True,
                ):

                    st.session_state.habits.append(
                        {
                            **preset,
                            "streak": 0,
                            "completed": False,
                            "last_completed": None,
                        }
                    )

                    st.session_state.current_id = preset["id"]

                    save_data()

                    st.session_state.view = "focus"

                    st.rerun()

    st.divider()

    st.caption("Or build your own")

    goal = st.text_input(
        "What do you want to get better at?",
        placeholder="e.g. learn Spanish",
    )

    if st.button(
        "Suggest a micro-habit",
        disabled=not goal.strip(),
        use_container_width=True,
    ):
        st.session_state.suggested_micro = suggest_micro(goal)

    if st.session_state.suggested_micro:

        micro = st.text_area(
            "Your micro-habit",
            value=st.session_state.suggested_micro,
            height=90,
        )

        if st.button(
            "Add custom habit",
            type="primary",
            use_container_width=True,
        ):

            if micro.strip():

                custom_id = f"custom-{len(st.session_state.habits) + 1}-{date.today()}"

                st.session_state.habits.append(
                    {
                        "id": custom_id,
                        "label": goal.strip() or "Your habit",
                        "action": micro.strip(),
                        "streak": 0,
                        "completed": False,
                        "last_completed": None,
                    }
                )

                st.session_state.current_id = custom_id
                st.session_state.suggested_micro = ""

                save_data()

                st.session_state.view = "focus"

                st.rerun()


# --------------------------
# ALL DONE VIEW
# --------------------------

elif total > 0 and done_count == total:

    st.markdown(
        '<div class="done-title">That’s today, done. 🌱</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        f'<div class="done-subtitle">'
        f'You showed up for {total} {"thing" if total == 1 else "things"} today.'
        f'</div>',
        unsafe_allow_html=True,
    )

    for habit in habits:
        st.markdown(
            f"✅ **{habit['label']}** &nbsp;&nbsp; "
            f"{habit.get('streak', 0)}-day streak"
        )

    st.write("")

    if st.button(
        "Add another habit",
        use_container_width=True,
    ):
        st.session_state.view = "add"
        st.rerun()


# --------------------------
# FOCUS VIEW
# --------------------------

else:

    if habits:

        current = next(
            (
                h
                for h in habits
                if h["id"] == st.session_state.current_id
            ),
            habits[0],
        )

        habit_names = [h["label"] for h in habits]

        current_index = habits.index(current)

        selected_label = st.selectbox(
            "Today's habits",
            habit_names,
            index=current_index,
            label_visibility="collapsed",
        )

        selected = next(
            h
            for h in habits
            if h["label"] == selected_label
        )

        st.session_state.current_id = selected["id"]

        st.markdown(
            f'<div class="habit-label">{selected["label"]}</div>',
            unsafe_allow_html=True,
        )

        st.markdown(
            f'<div class="habit-action">{selected["action"]}</div>',
            unsafe_allow_html=True,
        )

        if selected.get("completed"):

            st.success("✓ Done for today")

        else:

            if st.button(
                "🌱 Mark as done",
                type="primary",
                use_container_width=True,
            ):

                update_streak(selected)

                selected["completed"] = True

                save_data()

                next_habit = next(
                    (
                        h
                        for h in habits
                        if not h.get("completed")
                    ),
                    None,
                )

                if next_habit:
                    st.session_state.current_id = next_habit["id"]

                st.rerun()

        streak = selected.get("streak", 0)

        if streak > 0:
            streak_text = f"{streak}-day streak"
        else:
            streak_text = "Day 1 — every streak starts here"

        st.markdown(
            f'<div class="streak">{streak_text}</div>',
            unsafe_allow_html=True,
        )

        st.divider()

        with st.expander("Manage this habit"):

            new_label = st.text_input(
                "Habit name",
                value=selected["label"],
                key=f"label_{selected['id']}",
            )

            new_action = st.text_input(
                "Micro action",
                value=selected["action"],
                key=f"action_{selected['id']}",
            )

            edit_col, delete_col = st.columns(2)

            with edit_col:

                if st.button(
                    "Save changes",
                    key=f"save_{selected['id']}",
                    use_container_width=True,
                ):

                    selected["label"] = (
                        new_label.strip()
                        or selected["label"]
                    )

                    selected["action"] = (
                        new_action.strip()
                        or selected["action"]
                    )

                    save_data()

                    st.rerun()

            with delete_col:

                if st.button(
                    "Delete habit",
                    key=f"delete_{selected['id']}",
                    use_container_width=True,
                ):

                    st.session_state.habits = [
                        h
                        for h in st.session_state.habits
                        if h["id"] != selected["id"]
                    ]

                    st.session_state.current_id = (
                        st.session_state.habits[0]["id"]
                        if st.session_state.habits
                        else None
                    )

                    save_data()

                    st.rerun()

    else:

        st.markdown(
            '<div class="done-title">No habits yet.</div>',
            unsafe_allow_html=True,
        )

        st.markdown(
            '<div class="done-subtitle">'
            'Add your first micro-habit to begin.'
            '</div>',
            unsafe_allow_html=True,
        )

        if st.button(
            "＋ Add your first habit",
            type="primary",
            use_container_width=True,
        ):
            st.session_state.view = "add"
            st.rerun()
