import os
import json
import requests
import click
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich import print as rprint

DEFAULT_BASE_URL = "http://127.0.0.1:8000"
CONFIG_FILE = os.path.expanduser("~/.devforge_cli_config.json")

console = Console()

def save_config(config):
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f)

def load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r') as f:
            return json.load(f)
    return {}

def get_base_url():
    c = load_config()
    return c.get('base_url', DEFAULT_BASE_URL)

def get_headers():
    config = load_config()
    token = config.get('token')
    if not token:
        rprint("[bold red]Error:[/bold red] Not logged in. Run `devforge login` first.")
        exit(1)
    return {'Authorization': f'Token {token}'}

def print_branded_header(title):
    console.print(Panel(f"[bold magenta]DEVFORGE[/bold magenta] | {title}", style="magenta", border_style="magenta", box=click.style("rounded", fg="magenta")))

def print_footer():
    console.print(f"\n[dim magenta]DevForge CLI System v1.1.0[/dim magenta] | [bold cyan]{get_base_url()}[/bold cyan]\n")

@click.group()
def cli():
    """DevForge CLI - Manage your projects and tickets from the terminal."""
    pass

@cli.group()
def config():
    """Configure CLI settings."""
    pass

@config.command()
@click.argument('url')
def set_url(url):
    """Set the DevForge base URL."""
    c = load_config()
    c['base_url'] = url.rstrip('/')
    save_config(c)
    rprint(f"[bold green]Base URL set to:[/bold green] {c['base_url']}")

@cli.command()
@click.option('--username', prompt=True)
@click.option('--password', prompt=True, hide_input=True)
def login(username, password):
    """Authenticate with DevForge."""
    print_branded_header("Authentication System")
    url = f"{get_base_url()}/api-token-auth/"
    try:
        response = requests.post(url, data={'username': username, 'password': password})
        if response.status_code == 200:
            token = response.json().get('token')
            save_config({**load_config(), 'token': token, 'username': username})
            rprint(f"[bold green]Success![/bold green] Welcome back, {username}.")
        else:
            rprint("[bold red]Login failed.[/bold red] Check your credentials.")
    except Exception as e:
        rprint(f"[bold red]Error:[/bold red] {str(e)}")
    print_footer()

@cli.command()
def whoami():
    """Show current logged in user."""
    print_branded_header("User Profile")
    config = load_config()
    username = config.get('username')
    if username:
        rprint(f"Logged in as [bold cyan]{username}[/bold cyan]")
    else:
        rprint("Not logged in.")
    print_footer()

@cli.command()
def reputation():
    """View your reputation points."""
    print_branded_header("Reputation System")
    # This would call an API, for now mock
    rprint("Current Reputation: [bold yellow]1250[/bold yellow]")
    print_footer()

@cli.group()
def tickets():
    """Manage tickets (submissions)."""
    pass

@tickets.command(name='list')
def list_tickets():
    """List all open tickets."""
    print_branded_header("Tickets Repository")
    url = f"{get_base_url()}/review/api/tickets/"
    try:
        response = requests.get(url, headers=get_headers())
        if response.status_code == 200:
            tickets_data = response.json()
            table = Table(title="DevForge Tickets", style="magenta")
            table.add_column("ID", style="dim magenta")
            table.add_column("Title", style="white bold")
            table.add_column("Type", style="magenta")
            table.add_column("Priority", style="yellow")
            table.add_column("Status", style="green")
            
            for t in tickets_data:
                table.add_row(str(t['id']), t['title'], t['ticket_type'], t['priority'], t['status'])
            console.print(table)
        else:
            rprint("[bold red]Failed to fetch tickets.[/bold red]")
    except Exception as e:
        rprint(f"[bold red]Error:[/bold red] {str(e)}")
    print_footer()

@tickets.command()
@click.argument('ticket_id')
def view(ticket_id):
    """View ticket details."""
    print_branded_header(f"Ticket Detail View")
    url = f"{get_base_url()}/review/api/tickets/{ticket_id}/"
    try:
        response = requests.get(url, headers=get_headers())
        if response.status_code == 200:
            t = response.json()
            panel_content = f"""
[bold magenta]Title:[/bold magenta] {t['title']}
[bold magenta]Type:[/bold magenta] {t['ticket_type']}
[bold yellow]Priority:[/bold yellow] {t['priority']}
[bold green]Status:[/bold green] {t['status']}
[bold white]Submitter:[/bold white] {t['submitter']['username']}
[bold white]Language:[/bold white] {t['language']}

[bold white]Code:[/bold white]
{t['code']}
"""
            console.print(Panel(panel_content, title=f"Ticket #{ticket_id}", border_style="magenta"))
        else:
            rprint("[bold red]Ticket not found.[/bold red]")
    except Exception as e:
        rprint(f"[bold red]Error:[/bold red] {str(e)}")
    print_footer()

@cli.command()
@click.argument('filepath')
@click.option('--title', help="Snippet title")
def push_snippet(filepath, title):
    """Push a local file as a snippet to DevForge."""
    if not os.path.exists(filepath):
        rprint(f"[bold red]Error:[/bold red] File not found.")
        return
    print_branded_header("Snippet Upload")
    with open(filepath, 'r') as f:
        code = f.read()
    url = f"{get_base_url()}/review/api/tickets/"
    data = {
        'title': title or os.path.basename(filepath),
        'language': filepath.split('.')[-1] if '.' in filepath else 'text',
        'code': code,
        'ticket_type': 'task',
        'status': 'open',
        'priority': 'medium'
    }
    try:
        response = requests.post(url, json=data, headers=get_headers())
        if response.status_code == 201:
            rprint("[bold green]Success![/bold green] Snippet pushed.")
        else:
            rprint(f"[bold red]Failed:[/bold red] {response.text}")
    except Exception as e:
        rprint(f"[bold red]Error:[/bold red] {str(e)}")
    print_footer()

@cli.command()
@click.argument('username')
@click.option('--body', prompt="Message")
def send_message(username, body):
    """Send a private message."""
    print_branded_header(f"Direct Message: @{username}")
    url = f"{get_base_url()}/messages/api/send/{username}/"
    try:
        response = requests.post(url, json={'body': body}, headers=get_headers())
        if response.status_code == 200:
            rprint("[bold green]Message sent successfully.[/bold green]")
        else:
            rprint(f"[bold red]Failed:[/bold red] {response.text}")
    except Exception as e:
        rprint(f"[bold red]Error:[/bold red] {str(e)}")
    print_footer()

@cli.command()
def projects():
    """List your projects."""
    print_branded_header("Project Board")
    # Mock
    rprint("1. [bold cyan]DevForge Platform[/bold cyan] - Active")
    rprint("2. [bold cyan]ResumeForge AI[/bold cyan] - Completed")
    print_footer()

if __name__ == '__main__':
    cli()
