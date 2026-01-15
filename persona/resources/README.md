# Persona Resources

This file should be read by an agent to get the background structure of this resources directory.

This directory contains additional documents referenced by persona files, such as:

- **Resume/CV** - Professional background and experience (`resume.md`, `cv.pdf`, etc.)
- **Writing Samples** - Examples of your writing style (`.pdf`, `.md`, `.docx`)
- **Portfolio Pieces** - Published articles, blog posts, technical documents
- **Reference Materials** - Documents that inform your perspective or expertise
- **JSON persona files** (`professional-persona_prompts.json`, `spiratual_persona_prompts   .json`)

## Purpose

These resource files provide:
- **Concrete examples** of your writing style for agents to learn from
- **Detailed professional history** beyond what fits in markdown persona files
- **Actual writing samples** showing tone, voice, and structure
- **Reference materials** that inform your perspectives

## How to Reference in Persona Files

### Markdown Links

In your persona `.md` files, reference resources using relative markdown links:

```markdown
## Professional Background

For detailed professional experience, see: [My Resume](resources/resume.md)

## Writing Style Examples

Example writing samples demonstrating my voice:
- [Technical Blog Post 2025](resources/LinkedIn-cloud-forgot-to-be-a-cloud.pdf)
- [Conference Talk Transcript](persona/resources/What IS SRE-revised.pdf)
- [Published Article](resources/SRE2AUX_How_Flight_Controllers_were_the_first_SREs.pdf)
```

### Descriptive References

When referencing files that agents may not be able to directly read (like `.docx` or some `.pdf` files), provide context:

```markdown
## Professional Experience

My complete resume is available in [resources/resume.md](resources/resume.md). 
Key highlights relevant to this book include:
- 30+ years in SRE and system reliability
- Experience with [specific technology/systems]
- Principal-level expertise in [area]
```

## File Types

### Supported Formats
- **`.pdf`** - Many AI agents can read PDFs (varies by agent/model)
- **`.md`** - Markdown files (fully readable)
- **`.txt`** - Plain text (fully readable)
- **`.docx`** - Word documents (may require extraction/parsing)

### Best Practice
For maximum compatibility, consider:
- Converting `.docx` files to `.pdf` or extracting text to `.md`
- Including key content summaries in the persona `.md` files themselves
- Using `.pdf` for documents you want to preserve formatting

## Organization

Organize resources logically:

```
persona/resources/
├── professional/
│   ├── resume.md
│   ├── cv.pdf
│   └── portfolio-samples/
├── writing-samples/
│   ├── blog-posts/
│   ├── articles/
│   └── technical-docs/
└── references/
    ├── book-notes.pdf
    └── relevant-documents/
```

## Agent Access

**IMPORTANT:** Agents will:
1. Read the persona `.md` files first
2. See references to resources (via markdown links)
3. Attempt to read referenced files if they can (PDFs, markdown, text)
4. For files they cannot read (like `.docx`), they'll note the reference exists

To ensure agents can access content:
- **Option 1:** Include key information in the persona `.md` file itself
- **Option 2:** Convert important documents to `.pdf` or `.md` format
- **Option 3:** Provide summaries in the persona file and note "see resource for details"

## Example Usage

### In `professional-persona.md`:

```markdown
# Professional Persona

## Experience Summary

Principal-level SRE with 30+ years of experience in system reliability and infrastructure.

## Detailed Resume

For complete professional history, see: [My Resume](resources/resume.pdf)

Key points from resume relevant to this book:
- 1985-1995: Early career in [field]
- 1995-2010: Senior roles in [industry]
- 2010-present: Principal SRE at [company]
- Specializations: [list]

## Technical Expertise

[Your technical background and expertise]
```

### In `writing-voice.md`:

```markdown
# Writing Voice

## Style Characteristics

[Your writing style description]

## Writing Samples

To see my writing in practice, reference these samples:
- [Technical Blog Post 2024](resources/writing-samples/blog-post-2024.pdf) - Shows technical depth with accessibility
- [Conference Talk 2023](resources/writing-samples/talk-transcript.pdf) - Demonstrates storytelling approach
- [Published Article](resources/writing-samples/article.pdf) - Example of formal but conversational tone

## Voice Principles

[Principles derived from your writing samples]
```

## Privacy Considerations

These files may contain sensitive personal or professional information:

- **Resume/CV:** Contains contact info, work history
- **Writing samples:** May contain proprietary or confidential content
- Consider what you commit to version control
- Use `.gitignore` if needed for sensitive files
- Remember: Agents need access, so files must be in the workspace

## Git Configuration

If you want to track these files in git (recommended for agents):

```bash
# Add resources to git
git add persona/resources/

# Or exclude specific sensitive files
echo "persona/resources/resume.docx" >> .gitignore
```

If you want to exclude all resources from git but still use them locally:

```bash
# Add to .gitignore
echo "persona/resources/" >> .gitignore
```

**Note:** If excluded from git, remember to restore them on other machines or keep backups.

---

**Summary:** Place external documents here and reference them in persona `.md` files. Agents will attempt to read referenced files. For maximum compatibility, convert important documents to `.pdf` or `.md` format.

