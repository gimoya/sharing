#!/usr/bin/env python3
"""
Generic script to generate an index.html file listing all files and directories
in the current folder, matching the existing style with responsive font sizing.
"""

import os
import sys
from pathlib import Path


def format_file_size(size_bytes):
    """
    Format file size in bytes to human-readable format.
    
    Args:
        size_bytes (int): File size in bytes
        
    Returns:
        str: Formatted file size (e.g., "1.2 MB", "456 KB")
    """
    if size_bytes == 0:
        return "0 B"
    
    # Define size units and their byte equivalents
    size_units = [
        ("B", 1),
        ("KB", 1024),
        ("MB", 1024**2),
        ("GB", 1024**3),
        ("TB", 1024**4)
    ]
    
    # Find the appropriate unit
    for unit, unit_size in reversed(size_units):
        if size_bytes >= unit_size:
            # Calculate the size in the current unit
            size_in_unit = size_bytes / unit_size
            # Format with appropriate decimal places
            if unit == "B":
                return f"{int(size_in_unit)} {unit}"
            elif size_in_unit >= 100:
                return f"{int(size_in_unit)} {unit}"
            else:
                return f"{size_in_unit:.1f} {unit}"
    
    return f"{size_bytes} B"


def generate_index_html(folder_path=".", output_file="index.html"):
    """
    Generate an index.html file listing all files and directories in the specified folder.
    
    Args:
        folder_path (str): Path to the folder to index (default: current directory)
        output_file (str): Name of the output HTML file (default: index.html)
    """
    folder = Path(folder_path).resolve()
    
    if not folder.exists() or not folder.is_dir():
        print(f"Error: '{folder_path}' is not a valid directory")
        return False
    
    # Get all items in the directory, sorted alphabetically
    items = []
    try:
        for item in sorted(folder.iterdir(), key=lambda x: (x.is_file(), x.name.lower())):
            # Skip the output file itself and this script to avoid self-reference
            if item.name in [output_file, "generate_index.py"]:
                continue
            items.append(item)
    except PermissionError:
        print(f"Error: Permission denied accessing '{folder_path}'")
        return False
    
    # Get the folder name for the title
    folder_name = folder.name if folder.name else "Root"
    
    # Generate HTML content
    html_content = f"""<!doctype html>
<meta charset="utf-8">
<title>Index of /{folder_name}</title>
<style>
  html {{ font-family: Consolas, "Courier New", monospace; font-size: clamp(14px, 2.5vw, 18px); }}
  body {{ margin: clamp(16px, 4vw, 24px); color: #0f172a; background: #f8fafc; }}
  h1 {{ font-size: clamp(18px, 3.5vw, 20px); margin: 0 0 clamp(8px, 2vw, 12px); font-weight: 600; }}
  ul {{
    list-style: none;
    padding: 0;
    margin: 0;
    border: 1px solid #e2e8f0;
    border-radius: 8px;
    background: #ffffff;
  }}
  li + li {{ border-top: 1px solid #e2e8f0; }}
  a {{ display: flex; justify-content: space-between; align-items: center; padding: clamp(8px, 2vw, 12px); color: #0f172a; text-decoration: none; }}
  a:hover {{ background: #f1f5f9; }}
  .file-size {{ color: #64748b; font-size: 0.9em; margin-left: 12px; }}
  @media (max-width: 768px) {{
    html {{ font-size: 14px; }}
    body {{ margin: 16px; }}
    h1 {{ font-size: 18px; margin-bottom: 8px; }}
    a {{ padding: 8px; }}
  }}
</style>
<h1>Index of /{folder_name}</h1>
<ul>
"""
    
    # Add each item to the list
    for item in items:
        # Determine if it's a directory (add trailing slash)
        display_name = item.name + "/" if item.is_dir() else item.name
        
        # Get file size for files (directories don't have meaningful sizes)
        if item.is_file():
            try:
                file_size = item.stat().st_size
                size_display = f'<span class="file-size">{format_file_size(file_size)}</span>'
            except (OSError, PermissionError):
                size_display = '<span class="file-size">-</span>'
        else:
            size_display = '<span class="file-size">-</span>'
        
        html_content += f'  <li><a href="{item.name}">{display_name}{size_display}</a></li>\n'
    
    html_content += "</ul>\n"
    
    # Write the HTML file
    output_path = folder / output_file
    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        print(f"Successfully generated '{output_file}' in '{folder_path}'")
        print(f"Indexed {len(items)} items")
        return True
    except PermissionError:
        print(f"Error: Permission denied writing to '{output_path}'")
        return False
    except Exception as e:
        print(f"Error writing file: {e}")
        return False


def main():
    """Main function to handle command line arguments and generate the index."""
    # Check for help flag first
    if len(sys.argv) > 1 and sys.argv[1] in ['-h', '--help', 'help']:
        print("Usage: python generate_index.py [folder_path] [output_file]")
        print("")
        print("Arguments:")
        print("  folder_path  Path to folder to index (default: current directory)")
        print("  output_file  Name of output HTML file (default: index.html)")
        print("")
        print("Examples:")
        print("  python generate_index.py                    # Index current directory")
        print("  python generate_index.py /path/to/folder    # Index specific folder")
        print("  python generate_index.py . index.html       # Custom output filename")
        return
    
    # Parse command line arguments
    folder_path = sys.argv[1] if len(sys.argv) > 1 else "."
    output_file = sys.argv[2] if len(sys.argv) > 2 else "index.html"
    
    # Generate the index
    success = generate_index_html(folder_path, output_file)
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
