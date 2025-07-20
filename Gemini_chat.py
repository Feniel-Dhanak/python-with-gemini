from rich.markdown import Markdown
from rich.console import Console
from rich.prompt import Prompt
from rich.panel import Panel
from rich.text import Text
import google.generativeai as genai
from serpapi import GoogleSearch
import json
import os

console = Console()

#=== CONFIGURATION ===  
serpapi_key = "Your API key here"
genai.configure(api_key="Your API key here")

model = genai.GenerativeModel('gemini-2.0-flash')

#=== SAVING HISTORY ===
def save_history():
    with open("Chat_History.json", 'w') as f:
        clean_history = [
            {"role": item.role, "parts": [part.text for part in item.parts]}
            for item in chat.history
        ]
        json.dump(clean_history, f, indent=2)

#=== RESTORE CHAT HISTORY IF EXISTS ===
if os.path.exists("Chat_History.json"):
    try:
        with open("Chat_History.json", 'r') as f:
            c_history = json.load(f)
        chat = model.start_chat(history=c_history)
    except(json.JSONDecodeError, KeyError, TypeError):
        console.print("[red]\nHistory file is corrupted or unreadable. Starting fresh.[/red]\n")
        chat = model.start_chat()
else:
    chat = model.start_chat()

# === GOOGLE SEARCH FUNCTIONS ===
def google_search(query):
    params = {
        "q": query,
        "hl": "en",
        "gl": "us",
        "api_key": serpapi_key
    }

    search = GoogleSearch(params)
    results = search.get_dict()

    snippets = []

    for result in results.get("organic_results", [])[:5]:
        title = result.get("title", "")
        snippet = result.get("snippet", "")
        link = result.get("link", "")
        snippets.append(f"{title}\n{snippet}\n{link}\n")

    return "\n---\n".join(snippets) if snippets else "No result found."

#=== MAIN CHAT LOOP ===
console.print(Panel.fit("Welcome to Gemini chat!", style="bold cyan", border_style="blue"))
console.print(
    Text.assemble(
        ("Type ", "dim"),
        ("'help'", "bold green"),
        (" to see all commands. Type ", "dim"),
        ("'exit'", "bold red"),
        (" to quit.\n", "dim")
    )
)

try:
    while True:
        user_input = Prompt.ask("[bold magenta]You[/bold magenta]")

        if user_input.lower() in ['exit', 'quit']:
            console.print("[red]Exiting...[/red]")
            save_history()
            break

        elif user_input.lower() == "clear":
            if os.path.exists("Chat_History.json"):
                os.remove("Chat_History.json")
                console.print(Panel("Chat history deleted.", style="bold red", width=100, border_style="red"))
                chat = model.start_chat()
            else:
                console.print("[yellow]File not found.[/yellow]")

        elif user_input.lower() == "help":
            help_text = """[bold green]Available Commands:[/bold green]
                            - [cyan]exit[/cyan]: Quit the program
                            - [cyan]clear[/cyan]: Delete chat history
                            - [cyan]search: <your query>[/cyan]: Perform a real-time Google search"""
            console.print(Panel(help_text, title="[bold blue]Help[/bold blue]", width=100, border_style="blue"))

        elif user_input.lower().startswith("search:"):
            query = user_input[7:].strip()
            if not query:
                console.print("[red]Please provide a search query after 'search:'.[/red]")
                continue
            search_result = google_search(query)

            search_prompt = f"""I searched Google for \"{query}\" and found the following information:\n\n{search_result}\n\nBased on this, please give me a concise and helpful answer."""
            response = chat.send_message(search_prompt)
            markdown = Markdown(response.text)
            console.print(Panel(markdown, title="[bold green]Gemini (Search)[/bold green]", width=100, border_style="bright_blue"))

        else:
            if user_input.strip().split()[0].lower().endswith(":") and not user_input.lower().startswith("search:"):
                console.print("[red]Spelling Error! Did you mean 'search:'?[/red]")
                continue
            response = chat.send_message(user_input)
            markdown = Markdown(response.text)
            console.print(Panel(markdown, title="[bold green]Gemini[/bold green]", width=100, border_style="green"))

except KeyboardInterrupt:
    console.print("\n\n[red]Chat Interrupted. Saving history...[/red]")
    save_history()

finally:
    save_history()