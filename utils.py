import shutil

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
