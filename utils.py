import shutil
from colorama import Fore, Style, init

def print_section_header(title):
    """Print a section header with a dynamic width based on terminal size."""
    width = shutil.get_terminal_size().columns
    print("-" * width)
    print(title.center(width))
    print("-" * width)

def print_section_footer():
    """Print a section footer with a dynamic width based on terminal size."""
    width = shutil.get_terminal_size().columns
    print("-" * width)

def initialize_colorama():
    """Initialize colorama for colored output on Windows."""
    init(autoreset=True)

def format_currency(amount):
    """Format currency with color: red for negative, green for positive."""
    if amount < 0:
        return f"{Fore.RED}{amount:.2f} EUR{Style.RESET_ALL}"
    else:
        return f"{Fore.GREEN}{amount:.2f} EUR{Style.RESET_ALL}"
