# Gemini TUI Chat with Real-Time Google Search

A terminal-based chat interface that connects with Google's Gemini (Generative AI) and integrates real-time search results using SerpAPI. Styled using the Rich library for a clean and readable text UI.

## Features

- Chat with Gemini directly from your terminal
- Retains chat history between sessions
- Use the `search:` command to perform real-time Google searches
- Smart markdown rendering for AI responses
- Clean and color-coded UI using the Rich library

## Commands

- `search: your query` – Performs a real-time Google search and passes results to Gemini
- `help` – Shows available commands
- `clear` – Deletes the current chat history
- `exit` – Exits the program safely and saves history

## Requirements

1) - Python 3.10 or higher
2) Install dependencies using:
    ```bash
    pip install -r requirements.txt
    ```
    
**## Setup**

1) Clone this repository or download the Python script.

2) Open the script and replace the placeholder strings "Your API key here" with:
    Your Gemini API key from Google AI Studio
    Your SerpAPI key from serpapi.com

3) Save the file.

4) Run the script in your terminal:
    **python Gemini_chat.py**
    The chat will start, and a Chat_History.json file will be created after the first exit to store your conversation history.
