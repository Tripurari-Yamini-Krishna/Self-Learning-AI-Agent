# Self-Learning-AI-Agent

## About the Project

This project is about building a personal AI agent using Python. It can answer questions, remember useful information about the user, and refer to previous conversations when needed.

The agent stores personal facts and conversation history in JSON files, so the information remains available even after restarting the program. It uses the Groq API to generate responses.

## Features

- AI chat and question answering
- Saving and updating personal memories
- Recalling stored information
- Storing conversation history
- Viewing and clearing conversation history
- Handling API limits and connection errors
- Basic protection against missing or corrupted JSON files

## Technologies Used

- Python
- Groq API
- openai/gpt-oss-20b
- python-dotenv
- JSON

## How It Works

The user interacts with the agent through a command-line interface. When a message is entered, the agent checks whether it is a memory-related request or a normal question.

Personal facts and conversation history are saved in JSON files. When the program starts again, it loads the stored information and uses it when relevant.

## Getting Started

### 1. Clone the Repository

    git clone https://github.com/Tripurari-Yamini-Krishna/Self-Learning-AI-Agent.git
    cd Self-Learning-AI-Agent

### 2. Create a Virtual Environment

    python -m venv .venv
    .\.venv\Scripts\Activate.ps1

### 3. Install Dependencies

    pip install -r requirements.txt

### 4. Configure the API Key

Create a `.env` file in the project folder and add your Groq API key:

    GROQ_API_KEY=your_groq_api_key

Replace the placeholder with your own key. Never upload your `.env` file or expose your API key publicly.

### 5. Run the Agent

    python main.py

## Available Commands

| Command | Description |
|---|---|
| /help | Shows available commands |
| /memory | Displays saved facts |
| /history | Shows recent conversations |
| /clearhistory | Clears conversation history after confirmation |
| exit | Closes the application |

## Testing

The project includes tests for memory safety, conversation-history safety, API efficiency, API failures, and command-line error handling.

To run the memory safety tests:

    python Test_Memory_Safety.py

## Future Improvements

- Improve natural-language memory updates
- Improve contextual recall
- Add more capabilities and reliability improvements

## Author

Tripurari Yamini Krishna
