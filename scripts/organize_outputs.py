#!/usr/bin/env python3
"""
Organize Cursor outputs into staging area for Scrivener import.

Usage:
    python scripts/organize_outputs.py
    python scripts/organize_outputs.py --chapter 5
"""

import os
import shutil
from pathlib import Path
from datetime import datetime
import argparse

class OutputOrganizer:
    def __init__(self, workspace_root):
        self.root = Path(workspace_root)
        self.outputs = self.root / "outputs"
        self.staging = self.root / "staging" / "ready-for-scrivener"
        self.staging.mkdir(parents=True, exist_ok=True)
        
    def organize_by_chapter(self, chapter=None):
        """Organize outputs by chapter."""
        print(f"Organizing outputs for chapter {chapter if chapter else 'all'}...")
        
        # Scan draft files
        drafts = list((self.outputs / "drafts").glob("*.md"))
        
        organized = {}
        for draft in drafts:
            # Parse filename: draft_chapter_section_v1.md
            parts = draft.stem.split("_")
            if len(parts) >= 3 and parts[0] == "draft":
                ch = parts[1]
                if chapter and ch != str(chapter):
                    continue
                    
                if ch not in organized:
                    organized[ch] = []
                organized[ch].append(draft)
        
        # Create chapter folders in staging
        for ch, files in organized.items():
            ch_folder = self.staging / f"Chapter_{ch}"
            ch_folder.mkdir(exist_ok=True)
            
            for file in files:
                dest = ch_folder / file.name
                shutil.copy2(file, dest)
                print(f"  Staged: {file.name} → Chapter_{ch}/")
        
        return organized
    
    def organize_research(self):
        """Copy research notes to staging."""
        research_staging = self.staging / "Research_Notes"
        research_staging.mkdir(exist_ok=True)
        
        research_files = list((self.outputs / "research").glob("*.md"))
        
        for file in research_files:
            dest = research_staging / file.name
            shutil.copy2(file, dest)
            print(f"  Staged: {file.name} → Research_Notes/")
    
    def organize_images(self):
        """Copy images to staging."""
        images_staging = self.staging / "Images"
        images_staging.mkdir(exist_ok=True)
        
        image_exts = {".png", ".jpg", ".jpeg", ".gif", ".svg"}
        image_files = []
        
        for ext in image_exts:
            image_files.extend((self.outputs / "images").glob(f"*{ext}"))
        
        for file in image_files:
            dest = images_staging / file.name
            shutil.copy2(file, dest)
            print(f"  Staged: {file.name} → Images/")
    
    def create_manifest(self):
        """Create manifest of staged files."""
        manifest_path = self.staging / "MANIFEST.md"
        
        with open(manifest_path, "w") as f:
            f.write(f"# Staged Files Manifest\n")
            f.write(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            
            # Walk staging directory
            for root, dirs, files in os.walk(self.staging):
                if files:
                    rel_path = Path(root).relative_to(self.staging)
                    f.write(f"## {rel_path}\n\n")
                    for file in sorted(files):
                        if file != "MANIFEST.md":
                            f.write(f"- {file}\n")
                    f.write("\n")
        
        print(f"\nManifest created: {manifest_path}")

def main():
    parser = argparse.ArgumentParser(
        description="Organize Cursor outputs for Scrivener import"
    )
    parser.add_argument(
        "--chapter", 
        type=int, 
        help="Organize specific chapter only"
    )
    parser.add_argument(
        "--research", 
        action="store_true",
        help="Organize research notes"
    )
    parser.add_argument(
        "--images", 
        action="store_true",
        help="Organize images"
    )
    
    args = parser.parse_args()
    
    # Get workspace root (parent of scripts/)
    workspace = Path(__file__).parent.parent
    organizer = OutputOrganizer(workspace)
    
    # Organize based on flags
    if args.chapter:
        organizer.organize_by_chapter(chapter=args.chapter)
    elif args.research:
        organizer.organize_research()
    elif args.images:
        organizer.organize_images()
    else:
        # Do everything
        organizer.organize_by_chapter()
        organizer.organize_research()
        organizer.organize_images()
    
    # Always create manifest
    organizer.create_manifest()
    
    print("\n✓ Organization complete!")
    print(f"Staged files ready at: {organizer.staging}")
    print("\nNext step: Review files, then drag into Scrivener")

if __name__ == "__main__":
    main()
