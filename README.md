# SLOs Can't Catch a Black Swan - Book Writing Workflow

A multi-agent AI-assisted workflow for writing "SLOs Can't Catch a Black Swan," a technical book about Site Reliability Engineering and risk management. This project uses Cursor 2.0 to orchestrate multiple AI agents (Claude, Perplexity, OpenAI, Gemini) for research, drafting, critique, and technical validation, with semi-automated integration into Scrivener.

**Author:** Geoff White  
**Project Type:** Technical Book Writing  
**Status:** Active Development

---

## Overview

This workspace implements a streamlined book writing process that:

- Reduces manual copy-paste work by 70%+
- Enables parallel agent execution for faster iteration
- Maintains Scrivener as the manuscript source of truth
- Provides consistent output formatting and organization
- Tracks costs and optimizes model selection

**Expected ROI:** Save 10-15 hours/month of tedious content transfer work.

---

## Project Structure

```
SLOBlackSwan-Cursor/
├── agents/                    # AI agent configurations (.mdc files)
│   ├── research-agent.mdc     # Perplexity research specialist
│   ├── writing-agent.mdc      # Claude drafting agent
│   ├── critique-agent.mdc     # GPT-4 editorial reviewer
│   └── technical-agent.mdc    # Gemini technical validator
├── outputs/                   # Generated content (git-ignored)
│   ├── research/              # Research notes and findings
│   ├── drafts/                # Draft chapters and sections
│   ├── critiques/             # Editorial feedback
│   └── images/                # Visual assets
├── staging/                   # Curated outputs for Scrivener
│   └── ready-for-scrivener/   # Organized by chapter
├── scripts/                   # Python automation helpers
│   ├── organize_outputs.py    # Organize outputs by chapter
│   ├── convert_to_rtf.py      # Markdown to RTF conversion
│   ├── cost_tracker.py        # API cost estimation
│   └── validate_mdc.py        # Validate agent configs
├── .cursorrules               # Global agent behavior rules
├── .env                       # API keys (git-ignored)
└── README.md                  # This file
```

---

## Quick Start

### Prerequisites

- **Cursor 2.0** (or later) with subscription
- **Python 3.8+** for automation scripts
- **Pandoc** (for RTF conversion, optional)
- **API Keys** for:
  - Anthropic (Claude)
  - OpenAI (GPT-4)
  - Perplexity
  - Google AI (Gemini)

### Initial Setup

1. **Clone or navigate to the workspace:**
   ```bash
   cd ~/Documents/SLOBlackSwan-Cursor
   ```

2. **Configure API keys:**
   Create `.env` file in workspace root:
   ```bash
   ANTHROPIC_API_KEY=sk-ant-xxxxx
   OPENAI_API_KEY=sk-xxxxx
   PERPLEXITY_API_KEY=pplx-xxxxx
   GOOGLE_AI_API_KEY=xxxxx
   ```
   ⚠️ **Never commit `.env` to git.**

3. **Set up Python environment (optional, for scripts):**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install pypandoc python-dotenv pathlib
   ```

4. **Install Pandoc (for RTF conversion, optional):**
   - Mac: `brew install pandoc`
   - Windows: Download from https://pandoc.org/installing.html
   - Linux: `sudo apt install pandoc`

5. **Configure MCP in Cursor:**
   - Press `Cmd/Ctrl + Shift + P`
   - Search for "Cursor Settings" → MCP
   - Add MCP servers for API access (see `cursor-book-workflow-guide.md` for details)

6. **Open workspace in Cursor:**
   - File → Open Folder
   - Select `SLOBlackSwan-Cursor`

---

## Workflow

### Basic Research → Draft → Critique Flow

1. **Research Phase:**
   - Open Agent in Cursor (`Cmd/Ctrl + L`)
   - Select "Research Agent" from dropdown
   - Provide research query:
     ```
     Research recent black swan events in tech infrastructure from 2024-2025. 
     Focus on incidents that were genuinely unprecedented. Find 3-5 examples with postmortems.
     
     Save output to outputs/research/research_black_swans_2024_25.md
     ```

2. **Drafting Phase:**
   - Switch to "Writing Agent"
   - Provide writing prompt:
     ```
     Using the research in outputs/research/research_black_swans_2024_25.md,
     draft a 1500-word section for Chapter 2 covering:
     - Brief intro to each incident
     - Why each qualifies as black swan
     - Lessons learned
     
     Match author's voice per .cursorrules.
     Save to outputs/drafts/draft_chapter2_black_swans_2024_v1.md
     ```

3. **Review Phase:**
   - Use "Critique Agent" for editorial feedback
   - Use "Technical Agent" for fact-checking
   - Review outputs in Cursor

4. **Staging for Scrivener:**
   ```bash
   python scripts/organize_outputs.py --chapter 2
   ```

5. **Import to Scrivener:**
   - Review files in `staging/ready-for-scrivener/`
   - Drag markdown files into Scrivener project
   - Scrivener automatically converts markdown

### Parallel Multi-Agent Workflow

Run multiple agents simultaneously for faster iteration:

1. **Chat 1 - Writing Agent:** Draft technical explanation
2. **Chat 2 - Technical Agent:** Validate best practices (parallel)
3. **Chat 3 - Research Agent:** Find real-world examples (parallel)

All agents work in parallel, then combine insights.

---

## Agent System

### Research Agent (`research-agent.mdc`)
- **Model:** Perplexity
- **Purpose:** Web research, fact-finding, citation gathering
- **Output:** Structured research notes with sources
- **Use for:** Finding incidents, postmortems, industry reports

### Writing Agent (`writing-agent.mdc`)
- **Model:** Claude Sonnet 4
- **Purpose:** Drafting book content matching author voice
- **Output:** Markdown drafts with proper formatting
- **Use for:** Initial drafts, revisions, code examples

### Critique Agent (`critique-agent.mdc`)
- **Model:** GPT-4o
- **Purpose:** Editorial feedback on clarity, flow, impact
- **Output:** Structured critiques with specific suggestions
- **Use for:** Reviewing drafts before finalizing

### Technical Validation Agent (`technical-agent.mdc`)
- **Model:** Gemini 2.5 Pro
- **Purpose:** Technical fact-checking, accuracy validation
- **Output:** Validation reports with verified claims
- **Use for:** Ensuring technical accuracy, identifying gaps

---

## Scripts

### `organize_outputs.py`

Organizes generated content into staging area for Scrivener import.

```bash
# Organize all outputs
python scripts/organize_outputs.py

# Organize specific chapter
python scripts/organize_outputs.py --chapter 5

# Organize only research notes
python scripts/organize_outputs.py --research

# Organize only images
python scripts/organize_outputs.py --images
```

**Output:** Creates organized folders in `staging/ready-for-scrivener/` with manifest.

### `convert_to_rtf.py`

Converts markdown files to RTF format for Scrivener (optional).

```bash
# Convert all markdown in staging
python scripts/convert_to_rtf.py

# Convert specific directory
python scripts/convert_to_rtf.py --input staging/ready-for-scrivener/Chapter_5
```

### `cost_tracker.py`

Estimates API costs based on usage patterns.

```bash
python scripts/cost_tracker.py
```

**Expected Costs (Moderate Usage):**
- Light (10 hours/month): $50-75
- Moderate (20 hours/month): $100-150
- Heavy (40 hours/month): $200-300

---

## File Naming Conventions

All outputs follow consistent naming patterns:

- **Research:** `research_TOPIC_YYYYMMDD.md`
- **Drafts:** `draft_CHAPTER_SECTION_vN.md`
- **Critiques:** `critique_CHAPTER_SECTION_YYYYMMDD.md`
- **Validations:** `validation_CHAPTER_SECTION_YYYYMMDD.md`

Examples:
- `research_black_swan_incidents_2025_20250127.md`
- `draft_chapter2_black_swans_2024_v1.md`
- `critique_chapter2_black_swans_2024_20250128.md`

---

## Integration with Scrivener

### Manual Import (Recommended)

1. Organize outputs: `python scripts/organize_outputs.py`
2. Review staged files in `staging/ready-for-scrivener/`
3. Check `MANIFEST.md` for file list
4. Drag markdown files into Scrivener project
5. Scrivener automatically converts markdown

**Advantages:**
- Zero risk of project corruption
- Quality gate before import
- Full control over organization

### Watch Folder (Semi-Automated)

1. In Scrivener: **File → Sync → with External Folder**
2. Choose sync folder: `staging/scrivener-sync`
3. Format: Plain Text or RTF
4. Sync on project open/close

When you open Scrivener, it detects changes and prompts to import.

---

## Writing Style Guidelines

The `.cursorrules` file defines the author's voice and style:

- **Technical but accessible** - Principal-level depth without academic jargon
- **Concrete examples** - Real incidents, not just theory
- **Short paragraphs** - 3-5 sentences max
- **Active voice** - Direct and engaging
- **Informal tone** - Occasional dry humor
- **Code examples** - Python pseudo-code for clarity

All agents follow these guidelines when generating content.

---

## Cost Management

### Optimization Tips

1. **Use cheaper models for drafts:**
   - Claude Haiku for initial drafts
   - Claude Sonnet for final polish
   - GPT-4o-mini for quick critiques

2. **Batch operations:**
   - Process multiple sections in one prompt
   - Reduces per-request overhead

3. **Cache context:**
   - Reuse research across multiple drafts
   - Store frequently used instructions in `.cursorrules`

4. **Monitor usage:**
   - Check provider dashboards regularly
   - Set budget alerts at 50%, 75%, 90%

See `scripts/cost_tracker.py` for cost estimation.

---

## Troubleshooting

### Agent not using correct model
- Check `.mdc` file has correct `model:` in frontmatter
- Verify API keys in `.env`
- Restart Cursor
- Manually select model from dropdown in Agent chat

### Files not saving to correct location
- Be explicit in prompt: "Save to outputs/research/filename.md"
- Check workspace folder is correctly set in Cursor
- Use full paths if relative paths fail

### API rate limits hit
- Add delays between agent calls
- Use cheaper models for drafts
- Monitor usage at provider dashboards

### Markdown formatting lost in Scrivener
- Use RTF conversion: `python scripts/convert_to_rtf.py`
- In Scrivener, ensure "Preserve formatting" is checked
- Set Scrivener to recognize markdown: Preferences → Import → Markdown

### Context window exceeded
- Break large tasks into smaller chunks
- Reference specific sections, not entire files
- Use `@file` mentions to only include relevant files
- Upgrade to long-context models (Claude Sonnet 4: 200K tokens)

---

## Documentation

- **`cursor-book-workflow-guide.md`** - Complete implementation guide
- **`mcp_coaching_guide.md`** - MCP configuration and usage
- **`cursor_ai_book_test_plan.md`** - Testing strategy

---

## Keyboard Shortcuts (Cursor)

- `Cmd/Ctrl + L` - Open Agent
- `Cmd/Ctrl + K` - Inline edit
- `Cmd/Ctrl + I` - Insert at cursor
- `Cmd/Ctrl + Shift + P` - Command palette
- `Cmd/Ctrl + N` - New agent chat
- `Shift + Tab` - Toggle Plan Mode
- `@` - Context menu (tag files, docs, etc.)

---

## Development

### Adding New Agents

1. Create new `.mdc` file in `agents/` directory
2. Define frontmatter with model, description, tools
3. Add agent-specific instructions
4. Test with simple query
5. Update this README

### Extending Scripts

Scripts are modular and can be extended:
- Add new organization patterns to `organize_outputs.py`
- Add format conversions to `convert_to_rtf.py`
- Add cost tracking for new models in `cost_tracker.py`

---

## License

Use freely for SLO Black Swan book project.

---

## Version History

- **v1.0** (November 2025) - Initial workflow implementation
- Active development - See git history for changes

---

## Support

For issues or questions:
1. Check `cursor-book-workflow-guide.md` for detailed instructions
2. Review troubleshooting section above
3. Check Cursor documentation: https://cursor.com/docs

---

**Remember:** The automation eliminates tedium, not thinking. Always review agent outputs before importing to Scrivener. Your judgment on quality, tone, and narrative flow is irreplaceable.



