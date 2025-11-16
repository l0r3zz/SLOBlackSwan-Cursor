# Cursor 2.0 Multi-Agent Book Writing Workflow Implementation Guide

**For: SLOs Can't Catch a Black Swan**  
**Author: Geoff White**  
**Date: November 8, 2025**

## Executive Summary

This guide implements a workflow using Cursor 2.0 to orchestrate multiple AI agents (Claude, Perplexity, OpenAI, Gemini) for book writing, with semi-automated integration into Scrivener. The system reduces manual content transfer by 70%+ while maintaining Scrivener as the manuscript source of truth.

**Implementation Timeline:**
- Phase 1 (Week 1): Cursor setup and basic agents - 5-8 hours
- Phase 2 (Weeks 2-3): Python automation helpers - 5-10 hours
- Phase 3 (Ongoing): Optimization and refinement

**Expected ROI:** Save 10-15 hours/month of tedious copy-paste work at zero additional software cost (you already have Cursor subscription).

---

## Table of Contents

1. [Architecture Overview](#architecture-overview)
2. [Phase 1: Cursor Setup](#phase-1-cursor-setup)
3. [Phase 2: Agent Configuration](#phase-2-agent-configuration)
4. [Phase 3: Python Automation](#phase-3-python-automation)
5. [Phase 4: Scrivener Integration](#phase-4-scrivener-integration)
6. [Workflow Examples](#workflow-examples)
7. [Troubleshooting](#troubleshooting)
8. [Cost Management](#cost-management)

---

## Architecture Overview

### System Design

```
Book Project Workspace (Cursor)
├── agents/
│   ├── research-agent.mdc        # Perplexity research
│   ├── writing-agent.mdc         # Claude drafting
│   ├── critique-agent.mdc        # GPT-4 editorial
│   └── technical-agent.mdc       # Gemini validation
├── outputs/
│   ├── research/                 # Research notes
│   ├── drafts/                   # Draft chapters
│   ├── critiques/                # Feedback
│   └── images/                   # Visual assets
├── staging/
│   └── ready-for-scrivener/     # Curated outputs
├── scripts/
│   ├── organize_outputs.py
│   ├── convert_to_rtf.py
│   └── batch_process.py
├── .cursorrules                  # Global agent behavior
└── README.md                     # Workspace documentation
```

### Data Flow

```
Topic/Query
    ↓
[Cursor Agent: Research] → research.md
    ↓
[Cursor Agent: Draft] → draft.md
    ↓
[Cursor Agent: Critique] → critique.md
    ↓
[Cursor Agent: Validate] → validation.md
    ↓
[Review in Cursor]
    ↓
[Python: organize + convert]
    ↓
[staging/ready-for-scrivener/]
    ↓
[Manual review: 2-5 min]
    ↓
[Drag into Scrivener]
```

---

## Phase 1: Cursor Setup

### Step 1.1: Create Workspace

**Time: 15 minutes**

1. Create project folder structure:

```bash
mkdir -p ~/Documents/SLOBlackSwan-Cursor/{agents,outputs/{research,drafts,critiques,images},staging/ready-for-scrivener,scripts}
cd ~/Documents/SLOBlackSwan-Cursor
```

2. Open in Cursor:
   - Launch Cursor
   - File → Open Folder
   - Select `SLOBlackSwan-Cursor`

3. Initialize git (recommended):

```bash
git init
echo "outputs/" >> .gitignore
echo "staging/" >> .gitignore
echo ".env" >> .gitignore
git add .
git commit -m "Initial workspace setup"
```

### Step 1.2: Configure API Keys

**Time: 10 minutes**

Create `.env` file in workspace root:

```bash
# .env - NEVER commit this file
ANTHROPIC_API_KEY=sk-ant-xxxxx
OPENAI_API_KEY=sk-xxxxx
PERPLEXITY_API_KEY=pplx-xxxxx
GOOGLE_AI_API_KEY=xxxxx
```

In Cursor, configure Model Context Protocol (MCP) for API access:

1. Press `Cmd/Ctrl + Shift + P`
2. Search for "Cursor Settings"
3. Go to Tools & Integrations → Add Custom MCP
4. This opens your MCP config file at:
   - Mac: `~/Library/Application Support/Cursor/User/globalStorage/mcp.json`
   - Windows: `%APPDATA%\Cursor\User\globalStorage\mcp.json`

Add this configuration:

```json
{
  "mcpServers": {
    "anthropic": {
      "command": "npx",
      "args": ["-y", "@anthropic-ai/mcp-server-anthropic"],
      "env": {
        "ANTHROPIC_API_KEY": "${ANTHROPIC_API_KEY}"
      }
    },
    "openai": {
      "command": "npx",
      "args": ["-y", "@openai/mcp-server-openai"],
      "env": {
        "OPENAI_API_KEY": "${OPENAI_API_KEY}"
      }
    }
  }
}
```

Restart Cursor after saving.

### Step 1.3: Create Global Rules

**Time: 20 minutes**

Create `.cursorrules` in workspace root:

```markdown
# Book Writing Assistant Rules

## Project Context
You are assisting with writing "SLOs Can't Catch a Black Swan," a technical book about Site Reliability Engineering and risk management. The author is Geoff White, a Principal-level SRE with 30+ years of experience.

## Writing Style
- Technical but accessible
- Use concrete examples from real incidents
- Balance theory with practical guidance
- Code examples in Python (pseudo-code for clarity)
- Informal tone with occasional humor
- Short paragraphs (3-5 sentences max)
- Active voice preferred

## Formatting Standards
- All outputs in Markdown
- Use ATX-style headers (# ## ###)
- Code blocks with language identifiers
- Citations as [Source] when referencing research
- Em-dashes as -- not the unicode character
- No smart quotes, use straight quotes

## Agent Behavior
- Research agents: Cite sources, provide URLs
- Writing agents: Match author's voice and technical depth
- Critique agents: Focus on clarity, technical accuracy, narrative flow
- Technical agents: Verify claims, identify gaps

## File Naming
- Research: `research_TOPIC_YYYYMMDD.md`
- Drafts: `draft_CHAPTER_SECTION_v1.md`
- Critiques: `critique_CHAPTER_SECTION_YYYYMMDD.md`

## Quality Standards
- Technical accuracy is paramount
- Every claim should be verifiable
- Practical examples required for abstract concepts
- Clear action items in "what to do" sections
```

---

## Phase 2: Agent Configuration

### How to Select and Use Agents

**Important:** Cursor doesn't have an "agent dropdown" menu. Instead, you select agents by referencing their `.mdc` files using the `@` syntax in the Agent chat.

**Steps to use an agent:**

1. **Open Agent chat:** Press `Cmd+L` (Mac) or `Ctrl+L` (Windows/Linux)

2. **Reference the agent file:** Type `@` followed by the agent file path:
   ```
   @agents/research-agent.mdc
   ```
   
   You can also use autocomplete: Type `@` and start typing the filename, then select it from the dropdown.

3. **Give your prompt:** After referencing the agent, type your task or question. The agent's instructions from the `.mdc` file will be included in the context.

4. **For agents with `alwaysApply: true`:** Once you reference the agent file once in a chat session, its instructions remain active for subsequent messages in that chat.

**Example:**
```
@agents/writing-agent.mdc

Draft a section on circuit breakers for Chapter 3.
```

**Switching agents:**
- In the same chat: Just reference a different agent file with `@`
- In a new chat: Press `Cmd+N` to open a new chat, then reference the agent

### Step 2.1: Research Agent (Perplexity)

**Time: 15 minutes**

Create `agents/research-agent.mdc`:

```markdown
---
name: "Research Agent"
model: "perplexity"
description: "Conducts research using web search and synthesizes findings into structured notes"
type: ["Research", "Fact-checking"]
icon: "🔍"
actions:
  auto_apply_edits: false
  auto_run: false
tools:
  all: false
  search:
    web: true
    codebase: false
  edit:
    edit_and_reapply: true
---

# Research Agent Instructions

You are a research specialist for a technical book about SRE and system reliability.

## Your Role
- Search for recent examples of system failures, SRE practices, and risk management
- Focus on 2020-2025 for current relevance
- Prioritize authoritative sources: AWS blogs, Google SRE, academic papers, industry reports
- Synthesize findings into structured notes

## Research Output Format

```markdown
# Research: [Topic]
**Date:** YYYY-MM-DD
**Query:** [Original research question]

## Summary
[2-3 sentence overview of findings]

## Key Findings

### Finding 1: [Title]
- **Source:** [Name] - [URL]
- **Date:** YYYY-MM-DD
- **Summary:** [What this tells us]
- **Relevance:** [Why this matters for the book]

### Finding 2: [Title]
[Same structure]

## Quotes Worth Using
> "[Direct quote]"
- Source: [Name, URL]

## Gaps Identified
- [What we still need to research]

## Recommended Next Steps
- [Follow-up research needed]
```

## Search Strategy
1. Start broad, then narrow
2. Look for incident reports and postmortems
3. Find multiple perspectives on same event
4. Verify dates and facts across sources
5. Note contradictions or disagreements

## Quality Checks
- Are sources authoritative?
- Are dates within target range (2020-2025)?
- Can claims be verified?
- Are there examples, not just theory?

Save all output to `outputs/research/research_[topic]_[YYYYMMDD].md`
```

### Step 2.2: Writing Agent (Claude)

**Time: 15 minutes**

Create `agents/writing-agent.mdc`:

```markdown
---
name: "Writing Agent"
model: "claude-sonnet-4"
description: "Drafts book content matching author's technical voice and style"
type: ["Writing", "Content Creation"]
icon: "✍️"
actions:
  auto_apply_edits: true
  auto_run: false
tools:
  all: true
---

# Writing Agent Instructions

You are the primary writing agent for Geoff White's book "SLOs Can't Catch a Black Swan."

## Author Voice
Geoff is a Principal-level SRE with 30+ years of experience. He writes:
- Technical but not academic
- Practical with concrete examples
- Informal with occasional dry humor
- Direct and opinionated when needed
- Short paragraphs, active voice

## Writing Process

### When given research notes:
1. Extract key themes and patterns
2. Identify best examples for illustration
3. Structure content logically
4. Draft prose matching author voice
5. Include code examples where helpful

### When given an outline:
1. Expand each section to full prose
2. Add transitions between ideas
3. Include examples for abstract concepts
4. Create "what this means for you" practical guidance
5. Add sidebars or callouts for important points

## Content Structure

### For Concept Chapters:
```markdown
# [Chapter Title]

[Hook: Real incident or provocative question]

## The Problem
[What challenge does this address?]

## The Theory
[Explain the concept]

## Real-World Examples
[2-3 concrete cases]

## Why This Matters
[Practical implications]

## What You Can Do
[Action items]
```

### For Technical Sections:
- Lead with the "why"
- Explain before showing code
- Use Python pseudo-code for clarity
- Comment code liberally
- Show both anti-patterns and good patterns

## Quality Standards
- Every abstract claim needs a concrete example
- Technical depth appropriate for Principal-level engineers
- No buzzword bingo
- Actionable takeaways in every section

## Output Format
- Markdown with proper header hierarchy
- Code blocks with language tags
- No smart quotes or em-dash unicode
- File naming: `draft_[chapter]_[section]_v[N].md`

Save to `outputs/drafts/`
```

### Step 2.3: Critique Agent (GPT-4)

**Time: 15 minutes**

Create `agents/critique-agent.mdc`:

```markdown
---
name: "Critique Agent"
model: "gpt-4o"
description: "Provides editorial feedback on drafts for clarity, flow, and impact"
type: ["Editing", "Quality Assurance"]
icon: "📝"
actions:
  auto_apply_edits: false
  auto_run: false
tools:
  all: false
  search:
    codebase: true
  edit:
    edit_and_reapply: false
---

# Critique Agent Instructions

You are an editorial reviewer for a technical book on SRE and system reliability.

## Your Role
Provide constructive feedback on drafts to improve:
- Clarity and readability
- Technical accuracy
- Narrative flow
- Engagement and impact
- Actionability

## Review Process

### Read for Structure
- Is the argument clear?
- Do sections flow logically?
- Are transitions smooth?
- Is the pacing appropriate?

### Assess Technical Content
- Are claims accurate?
- Are examples relevant and current?
- Is technical depth appropriate for audience?
- Are there gaps in explanation?

### Evaluate Readability
- Are paragraphs too long?
- Is jargon explained?
- Are complex ideas broken down?
- Would diagrams help?

### Check Practicality
- Are action items clear?
- Can readers apply this?
- Is advice specific enough?

## Feedback Format

```markdown
# Critique: [Draft Title]
**Date:** YYYY-MM-DD
**Draft Version:** v[N]
**Reviewer:** Critique Agent

## Overall Assessment
[2-3 sentences: strengths and main areas for improvement]

## Strengths
- [What works well]
- [Effective elements]

## Areas for Improvement

### Structure & Flow
- **Issue:** [Specific problem]
  - **Location:** [Section/paragraph]
  - **Suggestion:** [How to fix]

### Technical Accuracy
- **Issue:** [Specific problem]
  - **Suggestion:** [Correction or clarification needed]

### Clarity & Readability
- **Issue:** [Where readers might struggle]
  - **Suggestion:** [How to improve]

### Examples & Evidence
- **Issue:** [Weak or missing examples]
  - **Suggestion:** [What to add]

## Line-by-Line Notes
[Specific edits, organized by section]

### Section: [Name]
- Line X: [Specific feedback]
- Paragraph Y: [Specific feedback]

## Priority Actions
1. [Most important fix]
2. [Second priority]
3. [Third priority]

## Questions for Author
- [Clarifications needed]
```

## Feedback Principles
- Be specific, not vague
- Explain the "why" behind suggestions
- Offer alternatives, not just criticism
- Prioritize high-impact changes
- Respect author's voice

Save to `outputs/critiques/critique_[chapter]_[section]_[YYYYMMDD].md`
```

### Step 2.4: Technical Validation Agent (Gemini)

**Time: 15 minutes**

Create `agents/technical-agent.mdc`:

```markdown
---
name: "Technical Validator"
model: "gemini-2.5-pro"
description: "Validates technical claims, identifies gaps, suggests improvements"
type: ["Validation", "Fact-checking"]
icon: "🔬"
actions:
  auto_apply_edits: false
  auto_run: false
tools:
  all: false
  search:
    web: true
    codebase: true
---

# Technical Validation Agent Instructions

You are a technical fact-checker and validator for an SRE book.

## Your Mission
Ensure technical accuracy and completeness of all content.

## Validation Process

### Technical Claims
For every technical statement:
- Can this be verified?
- Is this current best practice (2025)?
- Are there exceptions or edge cases?
- Is the claim too broad or too narrow?

### Code Examples
- Does code actually work?
- Are there bugs or anti-patterns?
- Is error handling appropriate?
- Are there security issues?

### Architecture Patterns
- Is this pattern still recommended?
- Are there better alternatives in 2025?
- What are the tradeoffs?
- Are prerequisites mentioned?

### Data and Statistics
- Are numbers accurate?
- Are sources cited?
- Is context provided?
- Could data be misinterpreted?

## Validation Output

```markdown
# Technical Validation: [Section]
**Date:** YYYY-MM-DD
**Validator:** Technical Agent

## Claims Verified ✓
- **Claim:** [Statement from draft]
  - **Verification:** [How verified]
  - **Source:** [Reference]
  - **Status:** ACCURATE

## Claims Requiring Revision ⚠️
- **Claim:** [Statement from draft]
  - **Issue:** [What's wrong]
  - **Correction:** [What it should say]
  - **Source:** [Supporting evidence]

## Missing Context 📝
- **Topic:** [What needs elaboration]
  - **Gap:** [What's missing]
  - **Suggestion:** [What to add]

## Outdated Information 🕐
- **Claim:** [Statement from draft]
  - **Problem:** [Why outdated]
  - **Update:** [Current state as of 2025]

## Code Review 💻
- **Code Block:** [Location]
  - **Issues:** [Problems found]
  - **Fixes:** [Corrections]

## Additional Research Needed 🔍
- [Topics requiring deeper investigation]

## Technical Depth Assessment
- Current level: [Beginner/Intermediate/Advanced]
- Target audience level: [Principal-level SRE]
- Recommendation: [Adjust up/down/maintain]
```

## Validation Standards
- Prioritize accuracy over style
- Flag speculation as speculation
- Note when practices have changed
- Identify potential misunderstandings
- Suggest authoritative sources

Save to `outputs/critiques/validation_[chapter]_[section]_[YYYYMMDD].md`
```

---

## Phase 3: Python Automation

### Step 3.1: Setup Python Environment

**Time: 10 minutes**

```bash
cd ~/Documents/SLOBlackSwan-Cursor
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install pypandoc python-dotenv pathlib
```

Install Pandoc (required for markdown to RTF conversion):

- Mac: `brew install pandoc`
- Windows: Download from https://pandoc.org/installing.html
- Linux: `sudo apt install pandoc`

### Step 3.2: File Organization Script

**Time: 30 minutes**

Create `scripts/organize_outputs.py`:

```python
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
```

Make executable:
```bash
chmod +x scripts/organize_outputs.py
```

### Step 3.3: RTF Conversion Script (Optional)

**Time: 20 minutes**

Create `scripts/convert_to_rtf.py`:

```python
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
```

Make executable:
```bash
chmod +x scripts/convert_to_rtf.py
```

---

## Phase 4: Scrivener Integration

### Option A: Manual Import (Recommended)

**Time per batch: 2-5 minutes**

This is the safest and most pragmatic approach.

**Process:**

1. **Organize outputs:**
   ```bash
   python scripts/organize_outputs.py
   ```

2. **Review staged files:**
   - Open `staging/ready-for-scrivener/` in Finder/Explorer
   - Check `MANIFEST.md` for file list
   - Review content quality

3. **Import to Scrivener:**
   - Open Scrivener project
   - Select target folder in Binder (e.g., "Draft/Chapter 5")
   - Drag markdown files from staging folder
   - Scrivener automatically converts markdown to its format

4. **Organize in Scrivener:**
   - Create folder structure as needed
   - Apply labels/status
   - Add to compile settings

**Advantages:**
- Zero risk of project corruption
- Quality gate before import
- Full control over organization

### Option B: Watch Folder (Semi-Automated)

**Time: 15 minutes setup**

Use Scrivener's sync feature for automatic import.

**Setup:**

1. In Scrivener: **File → Sync → with External Folder**
2. Choose sync folder: `~/Documents/SLOBlackSwan-Cursor/staging/scrivener-sync`
3. Format: Plain Text or RTF
4. Sync on project open/close

**Workflow:**

```bash
# Organize to sync folder instead of staging
python scripts/organize_outputs.py --output ../staging/scrivener-sync
```

When you open Scrivener, it will detect changes and prompt to import.

**Advantages:**
- Less manual dragging
- Automatic format conversion

**Disadvantages:**
- Less review control
- Can be confusing with conflicts

---

## Workflow Examples

### Example 1: Research and Draft Workflow

**Goal:** Research black swan events in 2024-2025, then draft section.

**Steps:**

1. **In Cursor, open Agent (Cmd+L)**

2. **Reference the Research Agent file using @ syntax:**
   ```
   @agents/research-agent.mdc
   
   Research recent black swan events in tech infrastructure from 2024-2025. 
   Focus on incidents that were genuinely unprecedented (not just rare). 
   Find 3-5 examples with postmortems.
   
   Save output to outputs/research/research_black_swans_2024_25.md
   ```
   
   **Alternative:** If the agent has `alwaysApply: true`, you can just reference it once, then use it in subsequent messages without repeating the @ reference.

4. **Agent executes, creates research file**

5. **Switch to Writing Agent** (in a new chat or by referencing it):
   ```
   @agents/writing-agent.mdc
   
   Using the research in outputs/research/research_black_swans_2024_25.md,
   draft a 1500-word section for Chapter 2 covering:
   - Brief intro to each incident
   - Why each qualifies as black swan
   - Lessons learned
   
   Match author's voice per .cursorrules.
   Save to outputs/drafts/draft_chapter2_black_swans_2024_v1.md
   ```

7. **Review draft in Cursor**

8. **If satisfied, organize:**
   ```bash
   python scripts/organize_outputs.py --chapter 2
   ```

9. **Import to Scrivener manually**

**Time:** 15-20 minutes (vs. 45-60 minutes manual)

### Example 2: Parallel Multi-Agent Workflow

**Goal:** Get multiple perspectives on technical architecture.

**Steps:**

1. **Open multiple Agent chats in Cursor (Cmd+N for new chat)**

2. **Chat 1 - Writing Agent:**
   ```
   @agents/writing-agent.mdc
   
   Draft explanation of circuit breaker pattern for black jellyfish chapter.
   Target: 500 words, with Python pseudo-code example.
   ```

3. **Chat 2 - Technical Agent (simultaneously):**
   ```
   @agents/technical-agent.mdc
   
   Review circuit breaker pattern best practices as of 2025.
   Identify any changes from older implementations.
   Note common mistakes.
   ```

4. **Chat 3 - Research Agent (simultaneously):**
   ```
   @agents/research-agent.mdc
   
   Find 2-3 real examples of circuit breaker failures or successes 
   from major tech companies. Need postmortems or blog posts.
   ```

5. **All agents work in parallel**

6. **Review outputs:**
   - Compare writing vs. technical recommendations
   - Merge best elements
   - Add research examples

7. **Create final draft combining insights**

**Time:** 10-15 minutes (vs. 60-90 minutes sequential)

### Example 3: Draft-Critique-Refine Loop

**Goal:** Polish a draft section through multiple revisions.

**Steps:**

1. **Initial draft (Writing Agent):**
   ```
   @agents/writing-agent.mdc
   
   Draft section on Grey Rhino detection strategies.
   Use outline from outputs/outlines/chapter3_outline.md
   ```

2. **First critique (Critique Agent):**
   ```
   @agents/critique-agent.mdc
   
   Review outputs/drafts/draft_chapter3_grey_rhino_detection_v1.md
   Focus on: clarity, flow, actionability
   ```

3. **Technical validation (Technical Agent):**
   ```
   @agents/technical-agent.mdc
   
   Validate technical claims in same draft.
   Check for outdated practices or missing context.
   ```

4. **Refinement (Writing Agent):**
   ```
   @agents/writing-agent.mdc
   
   Revise draft_chapter3_grey_rhino_detection_v1.md based on:
   - outputs/critiques/critique_chapter3_grey_rhino_detection.md
   - outputs/critiques/validation_chapter3_grey_rhino_detection.md
   
   Create v2 with improvements.
   ```

5. **Final review and stage**

**Time:** 25-30 minutes (vs. 2-3 hours manual iteration)

---

## Troubleshooting

### Issue: Agent not using correct model

**Symptom:** Research agent using Claude instead of Perplexity

**Fix:**
1. Check agent .mdc file has correct `model:` in frontmatter
2. Verify API keys in .env
3. Restart Cursor
4. In Agent chat, manually select model from model dropdown (top of chat)
5. Make sure you're referencing the agent file with `@agents/research-agent.mdc` to load its configuration

### Issue: Files not saving to correct location

**Symptom:** Agent creates files in wrong directory

**Fix:**
1. Be explicit in prompt: "Save to outputs/research/filename.md"
2. Check workspace folder is correctly set in Cursor
3. Agent may need full path, not relative

### Issue: API rate limits hit

**Symptom:** "Rate limit exceeded" errors

**Fix:**
1. Add delays between agent calls
2. Use cheaper models for drafts (Claude Haiku)
3. Switch to GPT-4o-mini for critiques
4. Monitor usage at provider dashboards

### Issue: Markdown formatting lost in Scrivener

**Symptom:** Headers, code blocks don't import correctly

**Fix:**
1. Use RTF conversion: `python scripts/convert_to_rtf.py`
2. Or: In Scrivener, ensure "Preserve formatting" is checked on import
3. Set Scrivener to recognize markdown: Preferences → Import → Markdown

### Issue: Context window exceeded

**Symptom:** "Context length exceeded" error

**Fix:**
1. Break large tasks into smaller chunks
2. Reference specific sections, not entire files
3. Use @file mentions to only include relevant files
4. Upgrade to long-context models (Claude Sonnet 4: 200K, Gemini 2.5: 1M tokens)

### Issue: Agent generates incorrect file names

**Symptom:** Files named generically like "output.md"

**Fix:**
1. Include filename explicitly in prompt
2. Update .cursorrules with file naming standards
3. Post-process with script:
   ```python
   # scripts/rename_outputs.py
   # Rename files based on content
   ```

---

## Cost Management

### Track API Usage

Create `scripts/cost_tracker.py`:

```python
#!/usr/bin/env python3
"""Track API costs across providers."""

import os
from datetime import datetime
import json

class CostTracker:
    # Approximate costs per 1M tokens (as of Nov 2025)
    COSTS = {
        "claude-sonnet-4": {"input": 3.00, "output": 15.00},
        "claude-haiku": {"input": 0.25, "output": 1.25},
        "gpt-4o": {"input": 5.00, "output": 15.00},
        "gpt-4o-mini": {"input": 0.15, "output": 0.60},
        "gemini-2.5-pro": {"input": 1.25, "output": 5.00},
        "perplexity": {"request": 0.005}  # per request
    }
    
    def estimate_monthly(self, usage_pattern):
        """
        Estimate monthly costs based on usage pattern.
        
        usage_pattern = {
            "claude-sonnet-4": {"input_tokens": 1000000, "output_tokens": 500000},
            "gpt-4o": {"input_tokens": 500000, "output_tokens": 200000},
            ...
        }
        """
        total = 0
        breakdown = {}
        
        for model, usage in usage_pattern.items():
            if model not in self.COSTS:
                continue
            
            if "input_tokens" in usage:
                cost = (
                    (usage["input_tokens"] / 1_000_000) * self.COSTS[model]["input"] +
                    (usage["output_tokens"] / 1_000_000) * self.COSTS[model]["output"]
                )
            elif "requests" in usage:
                cost = usage["requests"] * self.COSTS[model]["request"]
            else:
                cost = 0
            
            breakdown[model] = round(cost, 2)
            total += cost
        
        return {
            "total": round(total, 2),
            "breakdown": breakdown
        }

# Example usage
if __name__ == "__main__":
    tracker = CostTracker()
    
    # Moderate book writing usage
    moderate_usage = {
        "claude-sonnet-4": {
            "input_tokens": 5_000_000,   # Reading research, context
            "output_tokens": 2_000_000    # Drafting
        },
        "gpt-4o": {
            "input_tokens": 2_000_000,   # Reading drafts
            "output_tokens": 500_000      # Critiques
        },
        "gemini-2.5-pro": {
            "input_tokens": 1_000_000,   # Technical validation
            "output_tokens": 300_000
        },
        "perplexity": {
            "requests": 200              # Research queries
        }
    }
    
    estimate = tracker.estimate_monthly(moderate_usage)
    
    print("=== Monthly Cost Estimate ===")
    print(f"Total: ${estimate['total']}")
    print("\nBreakdown:")
    for model, cost in estimate['breakdown'].items():
        print(f"  {model}: ${cost}")
```

### Cost Optimization Tips

1. **Use cheaper models for drafts:**
   - Claude Haiku for initial drafts
   - Claude Sonnet for final polish
   - GPT-4o-mini for quick critiques

2. **Batch operations:**
   - Process multiple sections in one prompt
   - Reduces per-request overhead

3. **Cache context:**
   - Reuse research across multiple drafts
   - Store frequently used instructions in .cursorrules

4. **Monitor daily:**
   ```bash
   # Check usage
   curl https://api.anthropic.com/v1/usage \
     -H "x-api-key: $ANTHROPIC_API_KEY"
   ```

5. **Set budget alerts:**
   - Configure in provider dashboards
   - Alert at 50%, 75%, 90% of budget

**Expected Costs (Moderate Usage):**
- Light (10 hours/month): $50-75
- Moderate (20 hours/month): $100-150
- Heavy (40 hours/month): $200-300

---

## Next Steps

### Week 1: Foundation
- [ ] Set up Cursor workspace
- [ ] Configure API keys
- [ ] Create .cursorrules
- [ ] Test basic agent (Research Agent)
- [ ] Verify output files created correctly

### Week 2: Expand Agents
- [ ] Configure all 4 agents
- [ ] Test each agent individually
- [ ] Run parallel workflow test
- [ ] Set up Python scripts
- [ ] Test organize_outputs.py

### Week 3: Integration
- [ ] Test Scrivener import workflow
- [ ] Refine agent prompts based on output quality
- [ ] Document personal workflow patterns
- [ ] Set up cost tracking
- [ ] Optimize for your specific use cases

### Ongoing
- [ ] Review agent outputs weekly, refine prompts
- [ ] Track costs monthly
- [ ] Update .cursorrules as patterns emerge
- [ ] Share learnings (blog post?)
- [ ] Consider MCP integrations for advanced workflows

---

## Advanced: Model Context Protocol (MCP) Integration

For future enhancement, consider MCP servers for:

**NotebookLM Integration (when API available):**
- Query your NotebookLM research directly from Cursor
- Auto-sync research notes

**Scrivener Direct Integration:**
- Read binder structure from Cursor
- Query document content
- Potentially write back to project (risky)

**Custom Tools:**
- Citation manager integration
- Plagiarism checker
- Technical term consistency checker

**Setup Example:**

```json
{
  "mcpServers": {
    "scrivener-reader": {
      "command": "node",
      "args": ["./mcp-servers/scrivener-reader.js"],
      "env": {
        "SCRIVENER_PROJECT_PATH": "/Users/geoff/Documents/SLOBlackSwan.scriv"
      }
    }
  }
}
```

See: https://modelcontextprotocol.io for MCP development docs.

---

## Conclusion

This workflow gives you:

**Immediate Benefits:**
- 70%+ reduction in copy-paste time
- Parallel agent execution
- Consistent output formatting
- Version control via git

**Medium-term Benefits:**
- Refined agent prompts optimized for your voice
- Automated batch processing
- Cost-optimized model selection

**Long-term Benefits:**
- Extensible via MCP
- Reusable for future books
- Shareable with other authors

**The key insight:** Don't try to automate everything. Keep the human review step. Your judgment on quality, tone, and narrative flow is irreplaceable. The automation should eliminate tedium, not thinking.

Start simple. Test with one agent and one chapter. Iterate based on what actually saves you time.

**You're ready to begin.**

---

## Appendix: Quick Reference

### Common Commands

```bash
# Organize all outputs
python scripts/organize_outputs.py

# Organize specific chapter
python scripts/organize_outputs.py --chapter 5

# Convert to RTF
python scripts/convert_to_rtf.py

# Check costs
python scripts/cost_tracker.py
```

### Agent Selection Guide

| Task | Best Agent | Model |
|------|-----------|-------|
| Web research | Research Agent | Perplexity |
| Initial draft | Writing Agent | Claude Sonnet |
| Editorial review | Critique Agent | GPT-4o |
| Fact checking | Technical Agent | Gemini 2.5 |
| Quick revisions | Writing Agent | Claude Haiku |
| Code examples | Writing Agent | Claude Sonnet |

### File Naming Conventions

```
outputs/research/research_TOPIC_YYYYMMDD.md
outputs/drafts/draft_CHAPTER_SECTION_vN.md
outputs/critiques/critique_CHAPTER_SECTION_YYYYMMDD.md
outputs/critiques/validation_CHAPTER_SECTION_YYYYMMDD.md
```

### Keyboard Shortcuts (Cursor)

- `Cmd/Ctrl + L`: Open Agent
- `Cmd/Ctrl + K`: Inline edit
- `Cmd/Ctrl + I`: Insert at cursor
- `Cmd/Ctrl + Shift + P`: Command palette
- `Cmd/Ctrl + N`: New agent chat
- `Shift + Tab`: Toggle Plan Mode
- `@`: Context menu (tag files, docs, etc.)

---

**Document Version:** 1.0  
**Last Updated:** November 8, 2025  
**Author:** Perplexity AI (for Geoff White)  
**License:** Use freely for SLO Black Swan book project
