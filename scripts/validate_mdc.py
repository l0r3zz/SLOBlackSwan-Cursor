#!/usr/bin/env python3
"""
Validator for .mdc files
Checks YAML frontmatter syntax and markdown structure
"""

import re
import sys
from pathlib import Path
from typing import List, Tuple, Dict

def extract_frontmatter(content: str) -> Tuple[str, str, str]:
    """Extract YAML frontmatter and markdown content.
    
    Expected structure:
    ---
    alwaysApply: true
    ---
    name: "..."
    ...
    ---
    
    [markdown content]
    """
    # Split by --- delimiters
    parts = content.split('---')
    
    if len(parts) < 3:
        return '', '', content
    
    # First block: alwaysApply (between first and second ---)
    first_block = parts[1].strip() if len(parts) > 1 else ''
    
    # Second block: main metadata (between second and third ---)
    second_block = parts[2].strip() if len(parts) > 2 else ''
    
    # Markdown content: everything after third ---
    markdown = '---'.join(parts[3:]).lstrip() if len(parts) > 3 else ''
    
    return first_block, second_block, markdown

def validate_yaml_basic(yaml_content: str) -> List[str]:
    """Basic YAML validation without external libraries."""
    errors = []
    lines = yaml_content.split('\n')
    
    # Check for common YAML issues
    quote_count = 0
    bracket_depth = 0
    brace_depth = 0
    
    for i, line in enumerate(lines, 1):
        stripped = line.strip()
        if not stripped or stripped.startswith('#'):
            continue
        
        # Check for unclosed quotes in value
        in_string = False
        quote_char = None
        for char in line:
            if char in ['"', "'"] and (i == 0 or line[i-1] != '\\'):
                if not in_string:
                    in_string = True
                    quote_char = char
                elif char == quote_char:
                    in_string = False
                    quote_char = None
        
        # Check bracket matching
        bracket_depth += line.count('[') - line.count(']')
        brace_depth += line.count('{') - line.count('}')
        
        # Check for colon without value (might be OK if next line is indented)
        if ':' in line and not line.strip().endswith(':'):
            parts = line.split(':', 1)
            if len(parts) == 2 and not parts[1].strip() and i < len(lines):
                # Check if next line is indented (nested structure)
                if i < len(lines):
                    next_line = lines[i] if i < len(lines) else ''
                    if not next_line.startswith(' ') and not next_line.startswith('\t'):
                        errors.append(f"Line {i}: Colon without value and no indented content following")
    
    if bracket_depth != 0:
        errors.append(f"Unmatched brackets: depth {bracket_depth}")
    if brace_depth != 0:
        errors.append(f"Unmatched braces: depth {brace_depth}")
    
    return errors

def validate_markdown_code_blocks(content: str) -> List[str]:
    """Validate markdown code blocks are properly closed."""
    errors = []
    
    # Find all code block markers
    code_block_pattern = r'```+'
    matches = list(re.finditer(code_block_pattern, content))
    
    if len(matches) % 2 != 0:
        errors.append(f"Unmatched code block markers: found {len(matches)} markers (should be even)")
        # Find the problematic one
        for i, match in enumerate(matches):
            line_num = content[:match.start()].count('\n') + 1
            if i % 2 == 0:
                errors.append(f"  Opening marker at line {line_num}")
            else:
                errors.append(f"  Closing marker at line {line_num}")
        if len(matches) > 0:
            last_match = matches[-1]
            line_num = content[:last_match.start()].count('\n') + 1
            errors.append(f"  Orphaned marker at line {line_num}")
    
    return errors

def validate_mdc_structure(content: str) -> List[str]:
    """Validate .mdc file structure."""
    errors = []
    
    # Must start with ---
    if not content.startswith('---'):
        errors.append("File must start with '---' (YAML frontmatter delimiter)")
        return errors
    
    # Count --- markers (should be exactly 3 for proper structure)
    delimiter_count = content.count('---')
    if delimiter_count < 3:
        errors.append(f"Expected at least 3 '---' delimiters (found {delimiter_count})")
        errors.append("Expected structure: --- (first block) --- (second block) --- (markdown)")
    
    return errors

def validate_file(filepath: Path) -> Dict:
    """Validate a single .mdc file."""
    results = {
        'file': str(filepath),
        'valid': True,
        'errors': [],
        'warnings': []
    }
    
    try:
        content = filepath.read_text(encoding='utf-8')
    except Exception as e:
        results['valid'] = False
        results['errors'].append(f"Cannot read file: {e}")
        return results
    
    # Validate structure
    structure_errors = validate_mdc_structure(content)
    results['errors'].extend(structure_errors)
    
    # Extract and validate frontmatter
    first_block, second_block, markdown = extract_frontmatter(content)
    
    # Combine both blocks for field checking
    combined_frontmatter = first_block + '\n' + second_block if first_block and second_block else (first_block or second_block)
    
    if first_block:
        yaml_errors = validate_yaml_basic(first_block)
        results['errors'].extend(yaml_errors)
    
    if second_block:
        yaml_errors = validate_yaml_basic(second_block)
        results['errors'].extend(yaml_errors)
        
        # Check for required fields in second block
        required_fields = ['name', 'model', 'description']
        for field in required_fields:
            if field + ':' not in second_block:
                results['errors'].append(f"Missing required YAML field in metadata block: '{field}'")
    
    # Validate markdown code blocks
    code_block_errors = validate_markdown_code_blocks(markdown)
    results['errors'].extend(code_block_errors)
    
    # Check for common issues
    if markdown:
        # Check for unclosed inline code (but ignore properly closed ones)
        # Count backticks - should be even for inline code
        inline_backticks = len(re.findall(r'`', markdown))
        # Subtract code block markers (each is 3 backticks)
        code_block_backticks = len(re.findall(r'```', markdown)) * 3
        remaining_backticks = inline_backticks - code_block_backticks
        
        # If odd number of remaining backticks, might have unclosed inline code
        if remaining_backticks % 2 != 0:
            results['warnings'].append("Possible unclosed inline code backticks (odd count after code blocks)")
    
    if results['errors']:
        results['valid'] = False
    
    return results

def main():
    """Main validation function."""
    if len(sys.argv) > 1:
        files_to_check = [Path(f) for f in sys.argv[1:]]
    else:
        # Find all .mdc files in agents directory
        agents_dir = Path(__file__).parent.parent / 'agents'
        files_to_check = list(agents_dir.glob('*.mdc'))
    
    if not files_to_check:
        print("No .mdc files found to validate")
        return 1
    
    print(f"Validating {len(files_to_check)} .mdc file(s)...\n")
    
    all_valid = True
    for filepath in files_to_check:
        results = validate_file(filepath)
        
        status = "✓ VALID" if results['valid'] else "✗ INVALID"
        print(f"{status}: {results['file']}")
        
        if results['errors']:
            all_valid = False
            for error in results['errors']:
                print(f"  ERROR: {error}")
        
        if results['warnings']:
            for warning in results['warnings']:
                print(f"  WARNING: {warning}")
        
        print()
    
    return 0 if all_valid else 1

if __name__ == '__main__':
    sys.exit(main())

