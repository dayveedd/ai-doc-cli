import os
from google import genai
from rich.console import Console
from rich.markdown import Markdown
import markdown
from weasyprint import HTML, CSS


api_key = os.environ.get("GEMINI_API_KEY")

if not api_key:
    print("Error: GEMINI_API_KEY environment variable not found.")
    print("To use this tool, please set your API key first by running:")
    print("export GEMINI_API_KEY='your_api_key_here'")
    exit(1)

# 2. Configure New Gemini Client
client = genai.Client(api_key=api_key)

SYSTEM_PROMPT = """
You are a professional document architect. 
When asked to generate a document (resume, proposal, report, etc.), 
provide ONLY the Markdown content. 
Do not include conversational filler like 'Sure' or 'Here is your document'. 
Use clear Markdown headers (#, ##), bullet points, and tables where appropriate.
"""

chat = client.chats.create(model='gemini-2.5-flash', config={'system_instruction': SYSTEM_PROMPT})

# Initialize Rich console for terminal UI
console = Console()

# 2. Define the PDF Styling
PROFESSIONAL_CSS = """
    @page { size: A4; margin: 2cm; }
    body { font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; font-size: 11pt; line-height: 1.6; color: #333333; }
    h1 { font-size: 24pt; color: #111111; border-bottom: 2px solid #eeeeee; padding-bottom: 5px; margin-top: 0; }
    h2 { font-size: 18pt; color: #222222; margin-top: 20px; }
    h3 { font-size: 14pt; color: #444444; }
    p, ul, ol { margin-bottom: 15px; }
    li { margin-bottom: 5px; }
    code { font-family: 'Courier New', Courier, monospace; background-color: #f4f4f4; padding: 2px 4px; border-radius: 4px; font-size: 10pt; }
    pre { background-color: #f4f4f4; padding: 15px; border-radius: 5px; overflow-x: auto; }
    pre code { background-color: transparent; padding: 0; }
"""

# 3. State Management
current_document = ""


def export_to_pdf(markdown_text, filename):
    """Converts markdown text to a styled PDF file."""
    if not markdown_text:
        console.print("[red]No document to export yet! Ask the AI to generate something first.[/red]")
        return

    try:
        html_content = markdown.markdown(markdown_text, extensions=['fenced_code', 'tables'])
        weasy_html = HTML(string=html_content)
        weasy_css = CSS(string=PROFESSIONAL_CSS)

        weasy_html.write_pdf(filename, stylesheets=[weasy_css])
        console.print(f"[bold green]Success! PDF saved to {os.path.abspath(filename)}[/bold green]")
    except Exception as e:
        console.print(f"[bold red]Failed to generate PDF: {e}[/bold red]")


# 4. The Interactive CLI Loop
def main():
    global current_document

    console.print("[bold cyan]=========================================[/bold cyan]")
    console.print("[bold cyan]   AI Document Generator Initialized   [/bold cyan]")
    console.print("[bold cyan]=========================================[/bold cyan]")
    console.print("Type your prompt to generate or edit a document.")
    console.print("Commands:")
    console.print("  [bold yellow]/pdf [filename.pdf][/bold yellow] - Export current document to PDF")
    console.print("  [bold yellow]/exit[/bold yellow]               - Quit the application\n")

    while True:
        try:
            user_input = console.input("[bold green]You>[/bold green] ").strip()

            if not user_input:
                continue

            # Handle Commands
            if user_input.lower() == "/exit":
                console.print("[cyan]Goodbye![/cyan]")
                break

            elif user_input.lower().startswith("/pdf"):
                parts = user_input.split(" ", 1)
                filename = parts[1] if len(parts) > 1 else "output.pdf"
                if not filename.endswith(".pdf"):
                    filename += ".pdf"

                with console.status("[bold blue]Generating PDF...[/bold blue]"):
                    export_to_pdf(current_document, filename)

            # Handle AI Prompts
            else:
                try:
                    # Added 'spinner="dots"' for the ticking ellipsis animation
                    with console.status("[bold blue]Fetching response...[/bold blue]", spinner="dots"):
                        response = chat.send_message(user_input)
                        current_document = response.text

                    console.print("\n[bold magenta]--- Current Document ---[/bold magenta]")
                    console.print(Markdown(current_document))
                    console.print("[bold magenta]------------------------[/bold magenta]\n")

                except Exception as api_error:
                    # Graceful error handling for network or API failures
                    console.print(f"\n[bold red]⚠️ Could not fetch response:[/bold red] {api_error}")
                    console.print("[yellow]Please check your internet connection or try a different prompt.[/yellow]\n")

        except KeyboardInterrupt:
            console.print("\n[cyan]Process interrupted. Goodbye![/cyan]")
            break
        except Exception as e:
            console.print(f"[bold red]An unexpected error occurred: {e}[/bold red]")

if __name__ == "__main__":
    main()