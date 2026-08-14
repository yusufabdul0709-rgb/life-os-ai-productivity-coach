import os
import requests
import pandas as pd
import streamlit as st

from dotenv import load_dotenv
from google import genai


# ============================================================
# CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Life-OS",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

load_dotenv()


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
    <style>

    .main {
        background-color: #0e1117;
    }

    .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
    }

    .hero {
        padding: 1.5rem;
        border-radius: 20px;
        background: linear-gradient(
            135deg,
            #161b22,
            #202938
        );
        border: 1px solid #30363d;
        margin-bottom: 25px;
    }

    .hero h1 {
        font-size: 42px;
        margin-bottom: 5px;
    }

    .hero p {
        color: #9da7b3;
        font-size: 17px;
    }

    .section-title {
        font-size: 24px;
        font-weight: 700;
        margin-top: 25px;
        margin-bottom: 15px;
    }

    .coach-card {
        padding: 25px;
        border-radius: 18px;
        background-color: #161b22;
        border: 1px solid #30363d;
        line-height: 1.7;
    }

    .footer {
        text-align: center;
        color: #777;
        margin-top: 50px;
        padding: 20px;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# LOAD DATA
# ============================================================

@st.cache_data
def load_data():

    df = pd.read_csv("screentime.csv")

    df["Date"] = pd.to_datetime(df["Date"])

    return df


df = load_data()


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def format_time(minutes):

    hours = int(minutes // 60)
    mins = int(minutes % 60)

    if hours > 0:
        return f"{hours}h {mins}m"

    return f"{mins}m"


def get_day_summary(day_df):

    category_summary = (
        day_df
        .groupby("Category")["Minutes_Used"]
        .sum()
        .sort_values(ascending=False)
    )

    app_summary = (
        day_df
        .groupby("App_Name")["Minutes_Used"]
        .sum()
        .sort_values(ascending=False)
    )

    return category_summary, app_summary


def create_ai_data_bridge(day_df):

    category_summary = (
        day_df
        .groupby("Category")["Minutes_Used"]
        .sum()
        .sort_values(ascending=False)
    )

    app_summary = (
        day_df
        .groupby("App_Name")["Minutes_Used"]
        .sum()
        .sort_values(ascending=False)
    )

    total_minutes = int(day_df["Minutes_Used"].sum())

    bridge_data = pd.DataFrame({
        "Category": category_summary.index,
        "Minutes": category_summary.values
    })

    app_data = pd.DataFrame({
        "App": app_summary.index,
        "Minutes": app_summary.values
    })

    summary_string = f"""
DATE:
{day_df["Date"].iloc[0].strftime("%Y-%m-%d")}

TOTAL SCREEN TIME:
{total_minutes} minutes ({format_time(total_minutes)})

CATEGORY BREAKDOWN:
{bridge_data.to_string(index=False)}

APP BREAKDOWN:
{app_data.to_string(index=False)}
"""

    return summary_string


def get_severity(total_minutes, goal_minutes):

    percentage = total_minutes / goal_minutes

    if percentage <= 0.8:
        return "good"

    elif percentage <= 1:
        return "normal"

    elif percentage <= 1.5:
        return "warning"

    else:
        return "critical"


# ============================================================
# GEMINI AI
# ============================================================

def get_gemini_client():

    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:

        try:
            api_key = st.secrets["GEMINI_API_KEY"]

        except Exception:
            return None

    return genai.Client(api_key=api_key)


def generate_coaching(summary_string, goal_minutes):

    client = get_gemini_client()

    if client is None:

        return (
            "⚠️ Gemini API key not configured. "
            "Add GEMINI_API_KEY to your .env file."
        )

    prompt = f"""
You are LIFE-OS, a brutally honest but fair productivity,
health and lifestyle coach.

Your job is NOT to simply tell the user to "use their phone less."

Analyze their actual screen-time behavior and give specific,
real-world actions that can replace unhealthy digital behavior.

Here is the user's daily screen-time data:

{summary_string}

The user's maximum daily screen-time goal is:

{goal_minutes} minutes.

Follow these rules:

1. Be brutally honest but never insulting.
2. Identify the biggest source of wasted time.
3. Separate productive screen time from entertainment/social media.
4. Look for unhealthy patterns.
5. Explain what the user could have accomplished with that time.
6. Suggest physical and real-world replacements.
7. Give at least 3 specific replacement activities.
8. Make the suggestions realistic for a college student.
9. Include one immediate action for tonight.
10. Include one action for tomorrow.
11. Do not give generic advice such as "reduce phone usage."
12. Use the actual categories and applications from the data.
13. If coding/education usage is high, acknowledge it as productive.
14. If entertainment/social media dominates, explicitly point that out.
15. Do not shame the user.
16. Keep the response structured and concise.

Use this structure:

## 🧠 Brutal Truth

## 📊 What Your Data Says

## 🔥 Biggest Problem

## 🌱 What You Could Have Done Instead

Give 3-5 concrete alternatives.

## 🎯 Tomorrow's Rules

Give 3 practical rules.

## ⚡ One Action Tonight

Give exactly one immediate action.

Your response should feel like a personalized coach
who actually studied the user's data.
"""

    try:

        response = client.models.generate_content(
            model="gemini-3.6-flash",
            contents=prompt
        )

        return response.text

    except Exception as e:

        return f"Gemini API error: {str(e)}"


# ============================================================
# GUILT-TRIP AVATAR
# ============================================================

def create_avatar_prompt(total_minutes, goal_minutes, category_summary):

    top_category = category_summary.index[0]

    if total_minutes > goal_minutes * 1.5:

        return (
            "A cinematic digital illustration of a tired college student "
            "sitting on a couch late at night, staring at a glowing "
            "smartphone, surrounded by clocks showing lost time, "
            "dark moody atmosphere, realistic concept art, "
            "symbolizing excessive screen time and digital burnout"
        )

    elif total_minutes > goal_minutes:

        return (
            "A cinematic illustration of a college student distracted "
            "by a glowing smartphone while a notebook and running shoes "
            "sit untouched nearby, symbolic of missed opportunities, "
            "realistic digital art"
        )

    else:

        return (
            "A cinematic inspirational illustration of a focused college "
            "student putting a smartphone aside and working on a laptop "
            "with books, running shoes and a water bottle nearby, "
            "bright productive atmosphere, realistic digital art"
        )


def generate_avatar(prompt):

    encoded_prompt = requests.utils.quote(prompt)

    image_url = (
        "https://image.pollinations.ai/prompt/"
        + encoded_prompt
    )

    try:

        response = requests.get(
            image_url,
            timeout=30
        )

        if response.status_code == 200:

            return image_url

    except Exception:
        pass

    return None


# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.title("⚙️ Life-OS Controls")

st.sidebar.markdown(
    "Control your daily screen-time analysis."
)

available_dates = sorted(
    df["Date"].dt.strftime("%Y-%m-%d").unique()
)

selected_date = st.sidebar.selectbox(
    "📅 Select a Day",
    available_dates,
    index=len(available_dates) - 1
)

daily_goal_hours = st.sidebar.slider(
    "🎯 Daily Screen-Time Goal",
    min_value=1.0,
    max_value=12.0,
    value=4.0,
    step=0.5
)

goal_minutes = int(daily_goal_hours * 60)

st.sidebar.divider()

st.sidebar.info(
    f"Your daily goal is "
    f"**{format_time(goal_minutes)}**."
)


# ============================================================
# FILTER SELECTED DAY
# ============================================================

selected_datetime = pd.to_datetime(selected_date)

day_df = df[
    df["Date"] == selected_datetime
].copy()


total_minutes = int(
    day_df["Minutes_Used"].sum()
)

category_summary, app_summary = get_day_summary(
    day_df
)


most_used_app = app_summary.index[0]

most_used_app_minutes = int(
    app_summary.iloc[0]
)


delta_minutes = total_minutes - goal_minutes

severity = get_severity(
    total_minutes,
    goal_minutes
)


# ============================================================
# HERO SECTION
# ============================================================

st.markdown(
    """
    <div class="hero">

        🧠 LIFE-OS

       
        Your personal screen-time command center.
        Data-driven self-awareness powered by Gemini.
       

    </div>
    """,
    unsafe_allow_html=True
)


st.caption(
    f"Analyzing: {selected_date}"
)


# ============================================================
# KPI ROW
# ============================================================

col1, col2, col3, col4 = st.columns(4)


with col1:

    st.metric(
        "📱 Screen Time",
        format_time(total_minutes)
    )


with col2:

    st.metric(
        "🔥 Most Used App",
        most_used_app,
        format_time(most_used_app_minutes)
    )


with col3:

    st.metric(
        "🎯 Daily Goal",
        format_time(goal_minutes)
    )


with col4:

    if delta_minutes > 0:

        delta_text = (
            f"{format_time(abs(delta_minutes))} over goal"
        )

    else:

        delta_text = (
            f"{format_time(abs(delta_minutes))} under goal"
        )

    st.metric(
        "📊 Goal Difference",
        format_time(abs(delta_minutes)),
        delta_text,
        delta_color="inverse"
    )


# ============================================================
# STATUS MESSAGE
# ============================================================

if severity == "good":

    st.success(
        "🟢 Excellent. Your screen time is comfortably "
        "within your target."
    )

elif severity == "normal":

    st.info(
        "🔵 You're within your target, but there is "
        "still room to improve."
    )

elif severity == "warning":

    st.warning(
        "🟠 You're above your daily target. "
        "Your digital habits need attention."
    )

else:

    st.error(
        "🔴 Critical screen-time day. "
        "Your phone is taking a significant part of your day."
    )


# ============================================================
# 14-DAY TREND
# ============================================================

st.markdown(
    '<div class="section-title">📈 14-Day Screen Time Trend</div>',
    unsafe_allow_html=True
)


daily_usage = (
    df.groupby("Date")["Minutes_Used"]
    .sum()
    .reset_index()
)

daily_usage["Date"] = daily_usage["Date"].dt.strftime(
    "%b %d"
)

daily_usage = daily_usage.set_index("Date")


st.line_chart(
    daily_usage["Minutes_Used"],
    height=350
)


# ============================================================
# CATEGORY + APP VISUALIZATION
# ============================================================

left, right = st.columns(2)


with left:

    st.markdown(
        '<div class="section-title">📊 Category Breakdown</div>',
        unsafe_allow_html=True
    )

    category_chart = category_summary.reset_index()

    category_chart.columns = [
        "Category",
        "Minutes"
    ]

    st.bar_chart(
        category_chart.set_index("Category"),
        height=350
    )


with right:

    st.markdown(
        '<div class="section-title">📱 App Usage</div>',
        unsafe_allow_html=True
    )

    app_chart = app_summary.reset_index()

    app_chart.columns = [
        "App",
        "Minutes"
    ]

    st.bar_chart(
        app_chart.set_index("App"),
        height=350
    )


# ============================================================
# AI DATA BRIDGE
# ============================================================

st.markdown(
    '<div class="section-title">🤖 AI Life Coach</div>',
    unsafe_allow_html=True
)


ai_summary = create_ai_data_bridge(
    day_df
)


with st.expander("🔍 View Data Sent to AI"):

    st.code(
        ai_summary,
        language="text"
    )


# ============================================================
# AI BUTTON
# ============================================================

if st.button(
    "🧠 Analyze My Day",
    type="primary",
    use_container_width=True
):

    with st.spinner(
        "Gemini is analyzing your digital life..."
    ):

        coaching = generate_coaching(
            ai_summary,
            goal_minutes
        )

    if severity == "critical":

        st.error("🚨 Brutal Mode Activated")

    elif severity == "warning":

        st.warning("⚠️ Your habits need attention")

    else:

        st.info("🧠 Here's what your data says")

    st.markdown(
        f"""
        <div class="coach-card">

        {coaching}

        </div>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# GUILT-TRIP AVATAR
# ============================================================

st.markdown(
    '<div class="section-title">🎭 Your Day as an Avatar</div>',
    unsafe_allow_html=True
)


avatar_prompt = create_avatar_prompt(
    total_minutes,
    goal_minutes,
    category_summary
)


with st.expander("🎨 View Avatar Prompt"):

    st.write(avatar_prompt)


if st.button(
    "🎭 Generate My Day's Avatar",
    use_container_width=True
):

    with st.spinner(
        "Generating your digital alter ego..."
    ):

        avatar_url = generate_avatar(
            avatar_prompt
        )

    if avatar_url:

        st.image(
            avatar_url,
            caption="Your Life-OS daily avatar"
        )

    else:

        st.warning(
            "Unable to generate the avatar right now."
        )


# ============================================================
# RAW DATA
# ============================================================

with st.expander("📄 View Raw Day Data"):

    st.dataframe(
        day_df,
        use_container_width=True,
        hide_index=True
    )


# ============================================================
# FOOTER
# ============================================================

st.markdown(
    """
    <div class="footer">

    LIFE-OS • Built with Streamlit + Pandas + Gemini

    <br>

    <small>
    Your data is your feedback loop.
    </small>

    </div>
    """,
    unsafe_allow_html=True
)