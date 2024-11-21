import streamlit as st
import openai
import json
from datetime import datetime
import re
import toml
import os
from openai import AzureOpenAI, OpenAI

# Configure page settings
st.set_page_config(
    page_title="CrewAI Advisor",
    page_icon="🤖",
    layout="wide"
)

# Initialize session state
if 'history' not in st.session_state:
    st.session_state.history = []
if 'api_key' not in st.session_state:
    st.session_state.api_key = ''
if 'selected_model' not in st.session_state:
    st.session_state.selected_model = 'gpt-3.5-turbo'
if 'api_type' not in st.session_state:
    st.session_state.api_type = 'openai'

# Available models
AVAILABLE_MODELS = {
    'openai': [
        'gpt-3.5-turbo',
        'gpt-4',
        'gpt-4-turbo-preview',
        'gpt-4-0125-preview'
    ],
    'azure': [
        'gpt-35-turbo',
        'gpt-4',
        'gpt-4-turbo',
        'gpt-4-32k'
    ]
}

# Example templates
TEMPLATES = {
    "Web Scraping": "Create a CrewAI system to scrape product information from e-commerce websites, including prices, reviews, and specifications. Store the data in a structured format.",
    "Content Creation": "Design a CrewAI system to generate blog posts about technology trends. Include research, writing, editing, and SEO optimization.",
    "Market Analysis": "Build a CrewAI system to analyze cryptocurrency market trends, gather news, price data, and social media sentiment to provide investment insights.",
    "Custom": ""
}

def get_client(api_key, api_type='openai'):
    """Get appropriate OpenAI client based on API type"""
    if api_type == 'azure':
        return AzureOpenAI(
            api_key=api_key,
            api_version="2024-02-15-preview",
            azure_endpoint=os.getenv('AZURE_OPENAI_ENDPOINT', "https://api.azure.openai.com")
        )
    else:
        return OpenAI(api_key=api_key)

def validate_input(goal):
    """Validate user input"""
    if len(goal.strip()) < 10:
        return False, "Please provide a more detailed description of your goal (at least 10 characters)."
    return True, ""

def get_crewai_advice(goal, api_key, model, api_type='openai'):
    """Get CrewAI advice from OpenAI"""
    try:
        client = get_client(api_key, api_type)
        
        # Adjust model name for Azure
        if api_type == 'azure':
            model = model.replace('.', '')  # Remove periods for Azure model names
        
        response = client.chat.completions.create(
            model=model,
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
                    
                    Return ONLY the JSON response without any additional text or markdown formatting:
                    
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
                    }"""
                },
                {
                    "role": "user",
                    "content": goal
                }
            ],
            temperature=0.7,
            max_tokens=2000
        )
        return True, response.choices[0].message.content
    except Exception as e:
        return False, f"""
        Error: {str(e)}
        
        Please ensure:
        1. Your API key is valid
        2. You have selected the correct API type (OpenAI or Azure)
        3. You have access to the selected model ({model})
        4. Your API key has sufficient credits
        
        Current settings:
        - API Type: {api_type}
        - Model: {model}
        """

def save_to_history(goal, advice):
    """Save recommendation to history"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    st.session_state.history.append({
        "timestamp": timestamp,
        "goal": goal,
        "advice": advice
    })

def extract_json(text):
    """Extract JSON from text that might contain markdown or code blocks"""
    # Try to parse as pure JSON first
    try:
        return json.loads(text)
    except:
        pass
    
    # Try to extract JSON from code blocks
    try:
        # Look for JSON between code blocks or just the content itself
        json_match = re.search(r'```(?:json|python)?\s*(\{.*?\})\s*```', text, re.DOTALL)
        if json_match:
            return json.loads(json_match.group(1))
        
        # If no code blocks, try to find JSON object directly
        json_match = re.search(r'\{.*\}', text, re.DOTALL)
        if json_match:
            return json.loads(json_match.group(0))
    except:
        pass
    
    raise ValueError("Could not extract valid JSON from the response")

def format_json_display(data):
    """Format JSON data for display"""
    # Format agents section
    agents_md = "### 👥 Agents\n\n"
    for agent in data['agents']:
        agents_md += f"#### {agent['name']}\n"
        agents_md += f"**Role:** {agent['role']}\n\n"
        agents_md += f"**Background:** {agent['background']}\n\n"
        agents_md += "**Goals:**\n"
        for goal in agent['goals']:
            agents_md += f"- {goal}\n"
        agents_md += "\n"

    # Format tasks section
    tasks_md = "### 📋 Tasks\n\n"
    for task in data['tasks']:
        tasks_md += f"#### {task['name']}\n"
        tasks_md += f"**Description:** {task['description']}\n\n"
        tasks_md += f"**Assigned to:** {task['agent']}\n\n"
        tasks_md += "**Tools:**\n"
        for tool in task['tools']:
            tasks_md += f"- {tool}\n"
        tasks_md += "\n"

    # Format tools section
    tools_md = "### 🛠️ Tools\n\n"
    for tool in data['tools']:
        tools_md += f"#### {tool['name']}\n"
        tools_md += f"**Purpose:** {tool['purpose']}\n\n"
        if tool['api_requirements']:
            tools_md += "**API Requirements:**\n"
            for req in tool['api_requirements']:
                tools_md += f"- {req}\n"
        tools_md += "\n"

    # Format workflow section
    workflow_md = "### 🔄 Workflow\n\n"
    for i, step in enumerate(data['workflow'], 1):
        workflow_md += f"{i}. {step}\n"

    return f"{agents_md}\n{tasks_md}\n{tools_md}\n{workflow_md}"

# Main app interface
st.title("🤖 CrewAI Project Advisor")
st.markdown("""
This app helps you design CrewAI-based solutions by providing expert recommendations 
on agents, tasks, and tools needed for your project.
""")

# Settings section
with st.expander("⚙️ Settings", expanded=not bool(st.session_state.api_key)):
    settings_col1, settings_col2 = st.columns([3, 1])
    
    with settings_col1:
        # API Type selection
        api_type = st.radio(
            "API Type",
            options=['OpenAI', 'Azure OpenAI'],
            index=0 if st.session_state.api_type == 'openai' else 1,
            help="Choose between standard OpenAI API or Azure OpenAI API"
        )
        st.session_state.api_type = 'openai' if api_type == 'OpenAI' else 'azure'
        
        # API Key input
        api_key = st.text_input(
            "API Key",
            value=st.session_state.api_key,
            type="password",
            help="Enter your API key"
        )
        
        if st.session_state.api_type == 'azure':
            azure_endpoint = st.text_input(
                "Azure OpenAI Endpoint",
                value=os.getenv('AZURE_OPENAI_ENDPOINT', "https://api.azure.openai.com"),
                help="Enter your Azure OpenAI endpoint URL"
            )
        
        # Model selection
        model = st.selectbox(
            "Select Model",
            options=AVAILABLE_MODELS[st.session_state.api_type],
            index=0,
            help="Choose the model to use. Different models have different capabilities and costs."
        )
    
    with settings_col2:
        st.markdown("<br><br>", unsafe_allow_html=True)  # Add some spacing
        # Save settings button
        if st.button("Save for Session"):
            st.session_state.api_key = api_key
            st.session_state.selected_model = model
            if st.session_state.api_type == 'azure':
                os.environ['AZURE_OPENAI_ENDPOINT'] = azure_endpoint
            st.success("Settings saved for this session!")
        
        # Save as default button
        if st.button("Save as Default"):
            try:
                secrets = {
                    'openai_api_key': api_key,
                    'selected_model': model,
                    'api_type': st.session_state.api_type
                }
                if st.session_state.api_type == 'azure':
                    secrets['azure_openai_endpoint'] = azure_endpoint
                
                secrets_path = os.path.join('.streamlit', 'secrets.toml')
                os.makedirs(os.path.dirname(secrets_path), exist_ok=True)
                with open(secrets_path, 'w') as f:
                    toml.dump(secrets, f)
                
                st.session_state.api_key = api_key
                st.session_state.selected_model = model
                if st.session_state.api_type == 'azure':
                    os.environ['AZURE_OPENAI_ENDPOINT'] = azure_endpoint
                st.success("Settings saved as default!")
            except Exception as e:
                st.error(f"Error saving settings: {str(e)}")

# Check if API key is set
if not st.session_state.api_key:
    st.warning("Please enter your API key in the Settings section above.")
    st.stop()

# Template selection
template_choice = st.selectbox(
    "Choose a template or create custom goal:",
    list(TEMPLATES.keys())
)

# Main input form
with st.form("crewai_form"):
    goal = st.text_area(
        "What do you need CrewAI to do?",
        value=TEMPLATES[template_choice],
        height=150,
        help="Describe your project goal in detail. Include any specific requirements, constraints, or preferences."
    )
    
    submitted = st.form_submit_button("Get CrewAI Advice")
    
    if submitted:
        # Validate input
        is_valid, error_message = validate_input(goal)
        
        if is_valid:
            with st.spinner(f"Consulting with {st.session_state.selected_model} for CrewAI recommendations..."):
                success, advice = get_crewai_advice(
                    goal, 
                    st.session_state.api_key, 
                    st.session_state.selected_model,
                    st.session_state.api_type
                )
                
                if success:
                    try:
                        # Parse and format the JSON response
                        json_data = extract_json(advice)
                        
                        # Save to history
                        save_to_history(goal, json_data)
                        
                        # Display formatted results
                        st.markdown(format_json_display(json_data))
                        
                        # Export option
                        st.download_button(
                            label="Download Recommendations (JSON)",
                            data=json.dumps(json_data, indent=2),
                            file_name="crewai_recommendations.json",
                            mime="application/json"
                        )
                    except Exception as e:
                        st.error(f"Error processing response: {str(e)}")
                        st.text("Raw response:")
                        st.text(advice)
                else:
                    st.error(advice)  # Display error message
        else:
            st.error(error_message)

# Sidebar with history and help
with st.sidebar:
    st.markdown("### 💡 Tips for Better Results")
    st.markdown("""
    When describing your goal, try to include:
    - The main objective
    - Required data sources
    - Expected outputs
    - Any specific constraints
    """)
    
    st.markdown("### 📚 About CrewAI")
    st.markdown("""
    CrewAI is a framework for orchestrating role-playing AI agents. It enables:
    - Multi-agent collaboration
    - Task delegation
    - Complex workflow automation
    """)
    
    # Display history
    if st.session_state.history:
        st.markdown("### 📜 Previous Recommendations")
        for i, item in enumerate(reversed(st.session_state.history[-5:])):  # Show last 5 entries
            with st.expander(f"#{len(st.session_state.history)-i}. {item['timestamp']}"):
                st.markdown("**Goal:**")
                st.markdown(item['goal'])
                st.markdown("**Recommendation:**")
                st.markdown(format_json_display(item['advice']))
