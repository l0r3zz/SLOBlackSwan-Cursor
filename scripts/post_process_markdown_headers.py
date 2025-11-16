#!/usr/bin/env python3
"""
Post-process markdown files to adjust header levels.

Algorithm:
- Add an increment (1-5, default 3) to each header level
- If the result would be > 5, replace with **heading** (bold)
- Output to filename.vN.md where N auto-increments
"""

import argparse
import re
import sys
from pathlib import Path


def process_header(line, increment):
    """
    Process a markdown header line.
    
    Args:
        line: The header line (must start with #)
        increment: Integer 1-5 to add to header level
    
    Returns:
        Processed header line
    """
    # Match header pattern: optional spaces, # characters, space, header text
    match = re.match(r'^(\s*)(#{1,6})\s+(.+)$', line)
    if not match:
        return line
    
    indent = match.group(1)
    hashes = match.group(2)
    heading_text = match.group(3).rstrip()
    
    current_level = len(hashes)
    new_level = current_level + increment
    
    if new_level > 5:
        # Replace with bold formatting (level 6 and above not supported in markdown)
        return f"{indent}**{heading_text}**\n"
    else:
        # Replace with new level of hashes
        new_hashes = '#' * new_level
        return f"{indent}{new_hashes} {heading_text}\n"


def get_next_version_number(input_path):
    """
    Find the next version number for output filename.
    
    Looks for existing filename.vN.md files and increments.
    """
    base_path = input_path.with_suffix('')
    stem = base_path.name
    parent = base_path.parent
    
    # Find all existing version files
    pattern = re.compile(rf'^{re.escape(stem)}\.v(\d+)\.md$')
    versions = []
    
    for file in parent.glob(f'{stem}.v*.md'):
        match = pattern.match(file.name)
        if match:
            try:
                versions.append(int(match.group(1)))
            except ValueError:
                continue
    
    if versions:
        next_version = max(versions) + 1
    else:
        next_version = 2  # Start with v2 (assuming original is v1 or unversioned)
    
    return next_version


def process_markdown_file(input_path, increment):
    """
    Process a markdown file and adjust header levels.
    
    Args:
        input_path: Path to input markdown file
        increment: Integer 1-5 to add to each header level
    
    Returns:
        Path to output file
    """
    # Read input file
    try:
        with open(input_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
    except FileNotFoundError:
        print(f"Error: File not found: {input_path}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error reading file: {e}", file=sys.stderr)
        sys.exit(1)
    
    # Process each line
    processed_lines = []
    for line in lines:
        # Check if line is a header (starts with # after optional whitespace)
        if re.match(r'^\s*#', line):
            processed_line = process_header(line, increment)
        else:
            processed_line = line
        processed_lines.append(processed_line)
    
    # Determine output filename
    version = get_next_version_number(input_path)
    base_path = input_path.with_suffix('')
    stem = base_path.name
    parent = base_path.parent
    output_path = parent / f'{stem}.v{version}.md'
    
    # Write output file
    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            f.writelines(processed_lines)
    except Exception as e:
        print(f"Error writing file: {e}", file=sys.stderr)
        sys.exit(1)
    
    return output_path


def main():
    parser = argparse.ArgumentParser(
        description='Post-process markdown files to adjust header levels.',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s draft_2008_financial_crisis_v1.md
  %(prog)s draft_2008_financial_crisis_v1.md --increment 3
  %(prog)s draft_2008_financial_crisis_v1.md -i 2
        """
    )
    parser.add_argument(
        'input_file',
        type=str,
        help='Input markdown file to process'
    )
    parser.add_argument(
        '-i', '--increment',
        type=int,
        default=3,
        choices=range(1, 6),
        metavar='N',
        help='Integer between 1-5 to add to each header level (default: 3)'
    )
    
    args = parser.parse_args()
    
    input_path = Path(args.input_file)
    
    if not input_path.exists():
        print(f"Error: Input file does not exist: {input_path}", file=sys.stderr)
        sys.exit(1)
    
    if not input_path.suffix == '.md':
        print(f"Warning: Input file does not have .md extension: {input_path}", file=sys.stderr)
    
    print(f"Processing {input_path} with increment {args.increment}...")
    output_path = process_markdown_file(input_path, args.increment)
    print(f"Output written to: {output_path}")


if __name__ == '__main__':
    main()
