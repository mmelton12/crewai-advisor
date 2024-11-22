# CrewAI Advisor

A Streamlit application that helps design CrewAI-based solutions by providing expert recommendations on agents, tasks, and tools needed for your project.

## Features

- Get AI-powered recommendations for CrewAI project design
- Support for both OpenAI and Anthropic APIs
- Pre-built templates for common use cases
- Export recommendations as JSON
- View history of previous recommendations
- Save settings between sessions
- Input validation and error handling
- Detailed tips and guidance

## Setup

1. Clone the repository:
```bash
git clone https://github.com/mmelton12/crewai-advisor.git
cd crewai-advisor
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure your API settings:
   - Launch the application
   - Open the Settings panel
   - Choose your API type (OpenAI or Anthropic)
   - Enter your API key
   - Select your preferred model
   - Click "Save as Default" to persist settings

4. Run the application:
```bash
streamlit run app.py
```

## API Support

### OpenAI API
- Supports standard OpenAI API keys
- Available models:
  - gpt-3.5-turbo
  - gpt-4
  - gpt-4-32k

### Anthropic API
- Supports Anthropic API keys
- Available models:
  - claude-3-opus-20240229
  - claude-3-sonnet-20240229
  - claude-3-haiku-20240307
  - claude-2.1
  - claude-2.0
  - claude-instant-1.2

## Templates

- Web Scraping: Design systems for scraping and processing web data
- Content Creation: Create content generation and management systems
- Market Analysis: Build market research and analysis systems
- Custom: Define your own unique use case

## About CrewAI

CrewAI is a framework for orchestrating role-playing AI agents. It enables:
- Multi-agent collaboration
- Task delegation
- Complex workflow automation

## Contributing

Feel free to submit issues and enhancement requests!
