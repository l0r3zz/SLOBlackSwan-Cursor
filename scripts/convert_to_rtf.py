#!/usr/bin/env python3
"""
Convert markdown files to RTF for Scrivener import.

Usage:
    python scripts/convert_to_rtf.py
    python scripts/convert_to_rtf.py --input staging/ready-for-scrivener/Chapter_5
"""

import pypandoc
from pathlib import Path
import argparse

class MarkdownToRTFConverter:
    def __init__(self, input_path, output_path=None):
        self.input_path = Path(input_path)
        self.output_path = Path(output_path) if output_path else self.input_path / "rtf"
        self.output_path.mkdir(parents=True, exist_ok=True)
    
    def convert_file(self, md_file):
        """Convert single markdown file to RTF."""
        rtf_filename = md_file.stem + ".rtf"
        rtf_path = self.output_path / rtf_filename
        
        try:
            pypandoc.convert_file(
                str(md_file),
                "rtf",
                outputfile=str(rtf_path),
                extra_args=[
                    "--standalone",
                    "--wrap=none"
                ]
            )
            print(f"  Converted: {md_file.name} → {rtf_filename}")
            return True
        except Exception as e:
            print(f"  Error converting {md_file.name}: {e}")
            return False
    
    def convert_all(self):
        """Convert all markdown files in input path."""
        md_files = list(self.input_path.rglob("*.md"))
        
        if not md_files:
            print(f"No markdown files found in {self.input_path}")
            return
        
        print(f"Converting {len(md_files)} files...")
        
        success_count = 0
        for md_file in md_files:
            if md_file.name == "MANIFEST.md":
                continue  # Skip manifest
            
            if self.convert_file(md_file):
                success_count += 1
        
        print(f"\n✓ Converted {success_count}/{len(md_files)} files")
        print(f"RTF files at: {self.output_path}")

def main():
    parser = argparse.ArgumentParser(
        description="Convert markdown to RTF for Scrivener"
    )
    parser.add_argument(
        "--input",
        default="staging/ready-for-scrivener",
        help="Input directory containing markdown files"
    )
    parser.add_argument(
        "--output",
        help="Output directory for RTF files (default: input/rtf/)"
    )
    
    args = parser.parse_args()
    
    converter = MarkdownToRTFConverter(args.input, args.output)
    converter.convert_all()

if __name__ == "__main__":
    main()
