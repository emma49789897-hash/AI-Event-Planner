import os

import streamlit as st
from dotenv import load_dotenv
from crewai import Crew, Task, Process, LLM

from agents import create_agents


# ---------------------------------------
# LOAD ENVIRONMENT
# ---------------------------------------

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    st.error("GROQ_API_KEY is missing. Add it to your .env file.")
    st.stop()


# ---------------------------------------
# PAGE CONFIG
# ---------------------------------------

st.set_page_config(
    page_title="AI Event Planner",
    page_icon="🎉",
    layout="wide"
)


# ---------------------------------------
# UI STYLE
# ---------------------------------------

st.markdown("""
<style>

.stApp {
    background: #0B1020;
    color: white;
}

.main-title {
    font-size: 48px;
    font-weight: 700;
    text-align: center;
    color: white;
}

.subtitle {
    text-align: center;
    color: #CBD5E1;
    font-size: 18px;
    margin-bottom: 30px;
}

.card {
    background: #111A33;
    padding: 25px;
    border-radius: 18px;
    border: 1px solid #263354;
    margin-bottom: 20px;
}

.stButton > button {
    background: linear-gradient(90deg, #7C3AED, #A855F7);
    color: white;
    border: none;
    border-radius: 10px;
    font-weight: 600;
}

</style>
""", unsafe_allow_html=True)


# ---------------------------------------
# HEADER
# ---------------------------------------

st.markdown(
    '<div class="main-title">🎉 AI Event Planner</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'Your AI team for planning smarter events'
    '</div>',
    unsafe_allow_html=True
)


# ---------------------------------------
# GROQ LLM
# ---------------------------------------

llm = LLM(
    model="groq/openai/gpt-oss-120b",
    api_key=GROQ_API_KEY,
    temperature=0.3
)


# ---------------------------------------
# CREATE AGENTS
# ---------------------------------------

agents = create_agents(llm)


# ---------------------------------------
# INPUT FORM
# ---------------------------------------

st.markdown(
    '<div class="card"><h2>🎯 Create Your Event</h2>',
    unsafe_allow_html=True
)

col1, col2 = st.columns(2)

with col1:

    event_type = st.selectbox(
        "Event Type",
        [
            "Birthday Party",
            "Wedding",
            "Corporate Event",
            "University Event",
            "Workshop",
            "Product Launch",
            "Other"
        ]
    )

    location = st.text_input(
        "Location",
        placeholder="e.g. Multan"
    )

    guests = st.number_input(
        "Number of Guests",
        min_value=1,
        value=50
    )


with col2:

    budget = st.number_input(
        "Budget (PKR)",
        min_value=1000,
        value=150000,
        step=5000
    )

    theme = st.text_input(
        "Theme",
        placeholder="e.g. Elegant Blue & Silver"
    )

    cuisine = st.text_input(
        "Food Preference",
        placeholder="e.g. Pakistani"
    )


special_requirements = st.text_area(
    "Special Requirements",
    placeholder="Anything else you want for your event?"
)

st.markdown("</div>", unsafe_allow_html=True)


# ---------------------------------------
# AGENT INFORMATION
# ---------------------------------------

st.markdown("## 🤖 Your AI Planning Team")

col1, col2 = st.columns(2)

with col1:
    st.write("🧠 Requirement Agent")
    st.write("💰 Budget Agent")
    st.write("📍 Venue Agent")
    st.write("🎨 Theme Agent")

with col2:
    st.write("🍽️ Catering Agent")
    st.write("📅 Schedule Agent")
    st.write("🚨 Risk Agent")


# ---------------------------------------
# GENERATE EVENT PLAN
# ---------------------------------------

if st.button(
    "✨ Generate Event Plan",
    use_container_width=True
):

    if not location:
        st.warning("Please enter your event location.")
        st.stop()

    # -----------------------------------
    # EVENT INFORMATION
    # -----------------------------------

    event_info = f"""
    Event Type: {event_type}
    Location: {location}
    Number of Guests: {guests}
    Budget: PKR {budget}
    Theme: {theme}
    Food Preference: {cuisine}
    Special Requirements: {special_requirements}
    """


    # -----------------------------------
    # TASK 1
    # -----------------------------------

    requirement_task = Task(
        description=f"""
        Analyze this event:

        {event_info}

        Create a clear event brief containing:
        - Event type
        - Location
        - Guest count
        - Budget
        - Theme
        - Food preference
        - Special requirements
        """,

        expected_output="A clear structured event brief.",

        agent=agents["requirement"]
    )


    # -----------------------------------
    # TASK 2
    # -----------------------------------

    budget_task = Task(
        description=f"""
        Create a practical budget for:

        {event_info}

        Divide the budget into:
        - Venue
        - Food
        - Decoration
        - Entertainment
        - Photography
        - Miscellaneous
        - Emergency

        The total must not exceed PKR {budget}.
        """,

        expected_output="A detailed event budget.",

        agent=agents["budget"]
    )


    # -----------------------------------
    # TASK 3
    # -----------------------------------

    venue_task = Task(
        description=f"""
        Analyze this event:

        {event_info}

        Determine suitable venue requirements.

        Consider:
        - Guest capacity
        - Location
        - Budget
        - Parking
        - Indoor/outdoor
        - Required facilities
        """,

        expected_output="Venue requirements and recommendations.",

        agent=agents["venue"]
    )


    # -----------------------------------
    # TASK 4
    # -----------------------------------

    theme_task = Task(
        description=f"""
        Create a theme and decoration plan for:

        {event_info}

        Include:
        - Theme
        - Colors
        - Decorations
        - Lighting
        - Stage/backdrop
        - Photo area
        """,

        expected_output="A complete theme and decoration plan.",

        agent=agents["theme"]
    )


    # -----------------------------------
    # TASK 5
    # -----------------------------------

    catering_task = Task(
        description=f"""
        Create a catering plan for:

        {event_info}

        Include:
        - Starters
        - Main course
        - Dessert
        - Drinks
        - Quantity considerations
        - Budget considerations
        """,

        expected_output="A complete catering plan.",

        agent=agents["catering"]
    )


    # -----------------------------------
    # TASK 6
    # -----------------------------------

    schedule_task = Task(
        description=f"""
        Create a realistic event schedule for:

        {event_info}

        Include:
        - Guest arrival
        - Welcome
        - Activities
        - Food
        - Entertainment
        - Closing

        Avoid timing conflicts.
        """,

        expected_output="A complete event timeline.",

        agent=agents["schedule"]
    )


    # -----------------------------------
    # TASK 7
    # -----------------------------------

    risk_task = Task(
        description=f"""
        Identify possible risks for:

        {event_info}

        Consider:
        - Weather
        - Budget
        - Vendors
        - Schedule
        - Guest management

        Provide a backup solution for each important risk.
        """,

        expected_output="Event risks and backup plans.",

        agent=agents["risk"]
    )


    # -----------------------------------
    # CREATE CREW
    # -----------------------------------

    crew = Crew(
        agents=list(agents.values()),

        tasks=[
            requirement_task,
            budget_task,
            venue_task,
            theme_task,
            catering_task,
            schedule_task,
            risk_task
        ],

        process=Process.sequential,

        verbose=False
    )


    # -----------------------------------
    # RUN CREW
    # -----------------------------------

    with st.spinner(
        "🤖 Your AI agents are planning the event..."
    ):

        try:

            result = crew.kickoff()

        except Exception as e:

            st.error(f"Something went wrong: {e}")
            st.stop()


    # -----------------------------------
    # RESULT
    # -----------------------------------

    st.success("🎉 Event plan generated successfully!")

    st.markdown("## 📋 Your Event Plan")

    st.markdown(
        '<div class="card">',
        unsafe_allow_html=True
    )

    st.markdown(str(result))

    st.markdown("</div>", unsafe_allow_html=True)


    # -----------------------------------
    # DOWNLOAD
    # -----------------------------------

    st.download_button(
        "📥 Download Event Plan",
        data=str(result),
        file_name="event_plan.txt",
        mime="text/plain",
        use_container_width=True
    )
