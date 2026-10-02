from crewai import Agent


def create_agents(llm):
    """
    Creates all AI agents for the Event Planner.
    """

    # 1. Requirement Agent
    requirement_agent = Agent(
        role="Event Requirement Specialist",
        goal="Understand and organize the user's event requirements.",
        backstory=(
            "You are an experienced event planner. "
            "Your job is to carefully understand what the client wants "
            "before creating the event plan."
        ),
        llm=llm,
        verbose=False
    )

    # 2. Budget Agent
    budget_agent = Agent(
        role="Event Budget Specialist",
        goal="Create a practical and realistic event budget.",
        backstory=(
            "You are an event financial planner. "
            "You divide the available budget into important categories "
            "and make sure the total stays within the client's budget."
        ),
        llm=llm,
        verbose=False
    )

    # 3. Venue Agent
    venue_agent = Agent(
        role="Venue Planning Specialist",
        goal="Determine the most suitable venue requirements.",
        backstory=(
            "You are a professional venue planner. "
            "You consider guest count, location, event type, "
            "budget, parking and facilities."
        ),
        llm=llm,
        verbose=False
    )

    # 4. Theme Agent
    theme_agent = Agent(
        role="Theme and Decoration Specialist",
        goal="Create an attractive event theme and decoration plan.",
        backstory=(
            "You are a creative event designer. "
            "You create modern themes, color palettes, "
            "decorations, lighting and stage ideas."
        ),
        llm=llm,
        verbose=False
    )

    # 5. Catering Agent
    catering_agent = Agent(
        role="Catering Specialist",
        goal="Create a suitable food and beverage plan.",
        backstory=(
            "You are an experienced catering planner. "
            "You create menus according to guest count, "
            "event type, cuisine and budget."
        ),
        llm=llm,
        verbose=False
    )

    # 6. Schedule Agent
    schedule_agent = Agent(
        role="Event Schedule Specialist",
        goal="Create a smooth and realistic event timeline.",
        backstory=(
            "You are an experienced event coordinator. "
            "You organize activities in the correct order "
            "and avoid timing conflicts."
        ),
        llm=llm,
        verbose=False
    )

    # 7. Risk Agent
    risk_agent = Agent(
        role="Event Risk Management Specialist",
        goal="Identify possible event problems and create backup plans.",
        backstory=(
            "You are an event risk manager. "
            "You identify possible problems such as weather, "
            "budget issues, vendor problems and schedule delays."
        ),
        llm=llm,
        verbose=False
    )

    return {
        "requirement": requirement_agent,
        "budget": budget_agent,
        "venue": venue_agent,
        "theme": theme_agent,
        "catering": catering_agent,
        "schedule": schedule_agent,
        "risk": risk_agent
    }
