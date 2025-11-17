# Open Projects Reference

**Last Updated:** 2025-01-27  
**Workspace:** Multi-root workspace in Cursor

---

## Overview

This Cursor workspace contains two projects working together for the book "SLOs Can't Catch a Black Swan":

1. **SLOBlackSwan-Cursor** - AI-assisted writing workflow (active development)
2. **Scrivener Input** - Content repository for Scrivener import (Dropbox synced)

---

## Project 1: SLOBlackSwan-Cursor

**Path:** `/Users/geoffwhite/Documents/SLOBlackSwan-Cursor`  
**Type:** AI-assisted book writing workflow  
**Purpose:** Research, drafting, critique, and technical validation using multiple AI agents

### Key Components

#### AI Agents (`agents/`)
- **research-agent.mdc** - Perplexity-based research specialist
- **writing-agent.mdc** - Claude Sonnet 4 drafting agent (alwaysApply: true)
- **critique-agent.mdc** - GPT-4o editorial reviewer
- **technical-agent.mdc** - Gemini 2.5 Pro technical validator

#### Generated Outputs (`outputs/`)
- **research/** - Research notes and findings
  - Recent: `novelty-definition-research.md`, `research_black_swan_incidents_2025_20250127.md`
- **drafts/** - Draft chapters and sections (with versions)
  - Examples: `draft_black_swan_incidents_2025_v1.md`, `draft_2020_covid19_infrastructure_impact_v1.md`
- **critiques/** - Editorial feedback and validations
  - Recent: `critique_black_swan_incidents_2025_20250127.md`, `validation_black_swan_incidents_2025_20250127.md`
- **images/** - Visual assets (currently empty)

#### Source Materials (`input/`)
- `1980-ARPANET-collapse.md`
- `1988-Internet-Worm.md`
- `2008-financial-crisis.md`
- `2020-COVID19-infrastructure-impact.md`

#### Automation Scripts (`scripts/`)
- `organize_outputs.py` - Organize outputs by chapter for Scrivener
- `convert_to_rtf.py` - Markdown to RTF conversion
- `cost_tracker.py` - API cost estimation
- `post_process_markdown_headers.py` - Header formatting fixes
- `validate_mdc.py` - Validate agent configurations

#### Staging Area (`staging/`)
- `ready-for-scrivener/` - Curated outputs organized for Scrivener import

#### Author Persona (`persona/`)
- **`persona/`** - Author persona files (professional, spiritual, writing voice)
  - `persona/professional-persona.md` - Professional background and expertise
  - `persona/spiritual-persona.md` - Spiritual beliefs and worldview
  - `persona/writing-voice.md` - Writing style preferences
  - Additional persona files as needed
  - **IMPORTANT:** All agents read persona files before generating content

#### Configuration
- **`.cursorrules`** - Global agent behavior rules (includes persona file references)
- **`SLO Black Swan Book Project.code-workspace`** - Multi-root workspace config
- **`.env`** - API keys (git-ignored)

### Workflow

1. **Research Phase:** Use `@agents/research-agent.mdc` to gather information
2. **Drafting Phase:** Use `@agents/writing-agent.mdc` to create content
3. **Review Phase:** Use critique and technical agents for feedback
4. **Staging:** Run `python scripts/organize_outputs.py` to prepare for Scrivener
5. **Import:** Review staged files, then manually import to Scrivener

### Key Files

- **README.md** - Project overview and quick start
- **cursor-book-workflow-guide.md** - Complete implementation guide
- **mcp_coaching_guide.md** - MCP configuration and usage
- **cursor_ai_book_test_plan.md** - Testing strategy

---

## Project 2: Scrivener Input

**Path:** `/Users/geoffwhite/Desktop/Dropbox/GEN-AI/SLO-BLACKSWAN/Scrivener-input`  
**Type:** Content repository  
**Purpose:** Markdown files and assets ready for or imported from Scrivener (Dropbox synced)

### Content Categories

#### Book Sections (Markdown)
- **Core Concepts:**
  - `slo-nature-of-slos.md`, `the-nature-of-slos-expanded.md`
  - `slo-black-swan-intro.md`, `slo-black-swan-theory.md`
  - `slo-bestiary-intro.md`

- **Animal Metaphors:**
  - `black_jellyfish_section.md`, `black-jellyfish.png`
  - `grey_swan_section.md`, `grey_swan.png`
  - `grey_rhino_section.md`, `grey-rhino.png`
  - `elephant_in_room_section.md`, `grey-elephant.png`
  - `hybrid_animals_section.md`, `hybrid_animals_continuation.md`
  - `incident_mgmt_menagerie.md`

- **Case Studies:**
  - `aws_outage_blackjellyfish_clean.md`
  - `AWS-Outage-Oct-20.md`, `AWS-Outage-book.md`
  - `2008-financial-crisis.md`
  - `2008-vs-2025-crypto-comparison.md`

- **Theory & Analysis:**
  - `black-swan-deep-dive.md`
  - `black-swan-to-grey-swan-transition.md`
  - `comparative_analysis_section.md`
  - `Messy_Reality_Updated_Section.md`

- **Reference Materials:**
  - `master_reference_table.md`
  - `field_guide_section.md`
  - `stress_test_section_fix.md`

- **Transitions & Flow:**
  - `Transition_Flow_Preview.md`
  - `black-swan-conclusion.md`

#### Images & Assets
- `animal-matrix-improved-small.png`
- `black-swan.png`, `black-jellyfish.png`
- `grey_swan.png`, `grey-rhino.png`, `grey-elephant.png`
- `Errorbudgetburndowngraph.png`
- `levelofeffortforeach9.png`
- `new-sla-graphic-small.png`, `slo-new-illustration-small.png`
- `SLO-SWAN-4.png`

#### Documents
- `AWS-Outage-book.pdf`
- `black-swan-slo-black-swan-theory.docx`
- `Integration_Guide.md`

### Purpose

This folder serves as:
1. **Import destination** - Files from SLOBlackSwan-Cursor staging area are reviewed here before Scrivener
2. **Export source** - Content edited in Scrivener can be exported here
3. **Backup/sync** - Dropbox ensures content is synced and backed up
4. **Version control** - Multiple versions of sections can coexist

---

## Workflow Between Projects

### Content Flow: Cursor → Scrivener

```
SLOBlackSwan-Cursor/outputs/
    ↓ (AI agents generate content)
staging/ready-for-scrivener/
    ↓ (manual review: 2-5 min)
Scrivener Input/ (review here)
    ↓ (drag into Scrivener)
Scrivener Project (final manuscript)
```

### Typical Workflow Steps

1. **Generate in Cursor:**
   ```bash
   # Use agents to create content
   @agents/writing-agent.mdc
   # Prompt: Draft section on [topic]
   ```

2. **Organize for Scrivener:**
   ```bash
   cd ~/Documents/SLOBlackSwan-Cursor
   python scripts/organize_outputs.py --chapter 5
   ```

3. **Review Staged Files:**
   - Check `staging/ready-for-scrivener/Chapter_5/`
   - Review quality and formatting

4. **Copy to Scrivener Input (Optional):**
   - Manually copy files to Dropbox folder for backup
   - Or skip this step and go directly to Scrivener

5. **Import to Scrivener:**
   - Open Scrivener project
   - Drag markdown files from staging or Dropbox folder
   - Scrivener converts markdown automatically

### Content Flow: Scrivener → Cursor

If you need to edit content from Scrivener in Cursor:

1. Export from Scrivener as markdown
2. Save to `input/` or `outputs/drafts/` in SLOBlackSwan-Cursor
3. Use agents to refine or expand
4. Re-import to Scrivener

---

## File Naming Conventions

### SLOBlackSwan-Cursor

- **Research:** `research_TOPIC_YYYYMMDD.md`
- **Drafts:** `draft_CHAPTER_SECTION_vN.md`
- **Critiques:** `critique_CHAPTER_SECTION_YYYYMMDD.md`
- **Validations:** `validation_CHAPTER_SECTION_YYYYMMDD.md`

### Scrivener Input

- **Sections:** `section-name.md` or `topic-section.md`
- **Images:** `image-name.png` (descriptive names)
- **Documents:** `document-name.pdf` or `.docx`

---

## Key Differences

| Aspect | SLOBlackSwan-Cursor | Scrivener Input |
|--------|---------------------|-----------------|
| **Purpose** | Content generation & workflow | Content storage & import |
| **Location** | Local Documents folder | Dropbox (synced) |
| **Structure** | Organized by output type | Organized by topic/section |
| **Version Control** | Git tracked | Dropbox version history |
| **AI Integration** | Full agent workflow | Manual import/export |
| **File Types** | Markdown, Python scripts | Markdown, images, PDFs |

---

## Quick Reference

### Working in SLOBlackSwan-Cursor

```bash
# Organize all outputs
python scripts/organize_outputs.py

# Organize specific chapter
python scripts/organize_outputs.py --chapter 5

# Convert to RTF (optional)
python scripts/convert_to_rtf.py

# Track costs
python scripts/cost_tracker.py
```

### Agent Shortcuts

- `Cmd/Ctrl + L` - Open Agent
- `@agents/research-agent.mdc` - Research agent
- `@agents/writing-agent.mdc` - Writing agent (auto-applied)
- `@agents/critique-agent.mdc` - Critique agent
- `@agents/technical-agent.mdc` - Technical validator

### File Paths

- **Staging:** `~/Documents/SLOBlackSwan-Cursor/staging/ready-for-scrivener/`
- **Scrivener Input:** `~/Desktop/Dropbox/GEN-AI/SLO-BLACKSWAN/Scrivener-input/`

---

## Current Status

### Active Work

- Recently generated: `research_black_swan_incidents_2025_20250127.md`
- Recent drafts: `draft_black_swan_incidents_2025_v1.md` and `v2.md`
- Recent critiques/validations: January 27, 2025

### Next Steps

1. Review staged content in `staging/ready-for-scrivener/`
2. Import approved content to Scrivener
3. Continue drafting new sections using agents
4. Iterate on existing content based on critiques

---

## Notes

- **Cursor Rules:** `.cursorrules` file contains comprehensive guidelines for all agents
- **Multi-root Workspace:** Both projects open simultaneously for easy file access
- **Dropbox Sync:** Scrivener Input folder syncs automatically via Dropbox
- **Version Control:** SLOBlackSwan-Cursor uses git (outputs/ excluded)

---

**Remember:** SLOBlackSwan-Cursor is for **generation and refinement**, Scrivener Input is for **storage and import**. The staging area is the bridge between them.

