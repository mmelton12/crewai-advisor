# CrewAI Project Advisor

A Streamlit web application that helps design CrewAI-based solutions by providing expert recommendations on agents, tasks, and tools needed for your project.

## Features

- Interactive web interface for inputting project goals
- GPT-4 powered CrewAI consulting
- Structured output format for easy implementation
- Helpful tips and CrewAI information

## Setup

1. Clone the repository:
```bash
git clone https://github.com/your-username/crewai-advisor.git
cd crewai-advisor
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file in the project root and add your OpenAI API key:
```bash
OPENAI_API_KEY=your_api_key_here
```

4. Run the application:
```bash
streamlit run app.py
```

## Usage

1. Enter your project goal in the text area
2. Click "Get CrewAI Advice"
3. Receive structured recommendations for:
   - Agents with roles and backgrounds
   - Tasks with descriptions
   - Required tools and APIs
   - Step-by-step workflow

## Output Format

The application provides recommendations in a structured Python dictionary format:

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
```

## Security Note

Never commit your `.env` file or expose your API keys. The `.gitignore` file is set up to prevent this.

## License

MIT License
