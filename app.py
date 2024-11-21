import streamlit as st
import openai
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure page settings
st.set_page_config(
    page_title="CrewAI Advisor",
    page_icon="🤖",
    layout="wide"
)

# Configure OpenAI client
client = openai.OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

def get_crewai_advice(goal):
    """Get CrewAI advice from GPT-4"""
    try:
        response = client.chat.completions.create(
            model="gpt-4-0125-preview",
            messages=[
                {
                    "role": "system",
                    "content": """You are a master CrewAI consultant. Your expertise lies in designing agent-based systems 
                    using the CrewAI framework. When given a goal, you should:
                    1. Analyze the requirements
                    2. Define the necessary agents with their roles and backgrounds
                    3. Specify the tasks each agent should perform
                    4. Identify required tools and APIs
                    5. Suggest the optimal workflow and execution order
                    
                    Provide your response in a structured format that can be easily parsed:
                    
                    ```python
                    {
                        "agents": [
                            {
                                "name": "agent_name",
                                "role": "role_description",
                                "background": "agent_background",
                                "goals": ["goal1", "goal2"]
                            }
                        ],
                        "tasks": [
                            {
                                "name": "task_name",
                                "description": "task_description",
                                "agent": "assigned_agent_name",
                                "tools": ["tool1", "tool2"]
                            }
                        ],
                        "tools": [
                            {
                                "name": "tool_name",
                                "purpose": "tool_purpose",
                                "api_requirements": ["req1", "req2"]
                            }
                        ],
                        "workflow": [
                            "step1",
                            "step2"
                        ]
                    }
                    ```"""
                },
                {
                    "role": "user",
                    "content": goal
                }
            ],
            temperature=0.7,
            max_tokens=2000
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error: {str(e)}"

# Main app interface
st.title("🤖 CrewAI Project Advisor")
st.markdown("""
This app helps you design CrewAI-based solutions by providing expert recommendations 
on agents, tasks, and tools needed for your project.
""")

# Input form
with st.form("crewai_form"):
    goal = st.text_area(
        "What do you need CrewAI to do?",
        height=150,
        placeholder="Example: Create a clean and simple landing page, focused on Bitcoin. Include current price of bitcoin, and a pro-btc opinion piece, along with links to recent articles."
    )
    
    submitted = st.form_submit_button("Get CrewAI Advice")
    
    if submitted and goal:
        with st.spinner("Consulting with GPT-4 for CrewAI recommendations..."):
            advice = get_crewai_advice(goal)
            st.markdown("### 🎯 CrewAI Project Recommendations")
            st.markdown(advice)
    elif submitted:
        st.error("Please enter a goal for your CrewAI project.")

# Add helpful information in the sidebar
with st.sidebar:
    st.markdown("""
    ### 💡 Tips for Better Results
    
    When describing your goal, try to include:
    - The main objective
    - Required data sources
    - Expected outputs
    - Any specific constraints
    
    ### 📚 About CrewAI
    CrewAI is a framework for orchestrating role-playing AI agents. It enables:
    - Multi-agent collaboration
    - Task delegation
    - Complex workflow automation
    """)
