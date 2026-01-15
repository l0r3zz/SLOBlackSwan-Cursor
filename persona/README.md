# Persona Files

This directory contains persona files that define Geoff White's professional and spiritual identity. These files provide essential context for all AI agents working on writing projects.

## Purpose

These persona files ensure that:
- Writing agents match my authentic voice and perspective
- Technical content reflects my  professional background and experience
- Content aligns with my spiritual worldview when relevant
- All agents understand I am are as a person and professional

## File Structure

Persona files in this directory:

- `README.md` - Overview of persona files
- `PERSONA.md` - link to README.md
- `professional-persona.md` - Professional background, experience, technical expertise
- `spiritual-persona.md` - Spiritual beliefs, worldview, values that inform my writing
- `writing-voice.md` - Specific writing style preferences, tone, examples
- `background.md` - Personal history, context that shapes my perspective

### External Resources

The `resources/` subdirectory contains external documents referenced by persona files:

- `resources/` - External documents (resumes, writing samples, PDFs, etc.)
  - See `resources/README.md` for details on referencing external documents
  - Place resume, CV, writing samples, and other reference materials here
  - Reference them in persona `.md` files using markdown links
  - JSON format prompts for us by advisor agents as as well as assistant agents. (.json files) 

## Usage

### Automatic Access

The `.cursorrules` file references this directory, so all agents automatically have access to persona context.

**Important:** When agents read persona files, they will:
1. Read the persona `.md` files
2. Follow any markdown links to external resources in `resources/` subdirectory
3. Attempt to read referenced files (PDFs, markdown, text files) if accessible
4. Note the existence of referenced files even if they cannot directly read them (e.g., `.docx`)

### Referencing External Documents

In your persona `.md` files, you can reference external documents using markdown links:

```markdown
## Professional Background

See [My Resume](resources/resume.pdf) for complete professional history.

## Writing Examples

Examples of my writing style:
- [Blog Post 2025](resources/LinkedIn-unwritten-law-of-information-flow.pdf)
- [Technical Article](resources/writing-samples/article.pdf)
```

Agents will automatically read these referenced files when processing persona information.

### Manual Reference

You can also explicitly reference persona files (and their resources) in agent chats:

```
@persona/professional-persona.md @persona/spiritual-persona.md

Draft a section on [topic] that reflects both my professional expertise and spiritual perspective.
```

This will include all referenced resources from the persona files.

### In Agent Configurations

The `writing-agent.mdc` file references persona files to ensure all writing matches your voice.

## Best Practices

1. **Keep files updated** - Update persona files as your perspective evolves
2. **Be specific** - Include concrete examples, anecdotes, and preferences
3. **Include context** - Explain why certain perspectives matter for the book
4. **Reference in prompts** - When in doubt, explicitly reference persona files in agent chats

## File Naming

Use clear, descriptive names:
- `professional-persona.md`
- `spiritual-persona.md`
- `writing-voice.md`
- `background.md`
- `values.md` (if separate from spiritual-persona)

## Privacy

These files contain personal information. Consider:
- Not committing sensitive personal details to git
- Using `.gitignore` if needed (but they're needed for agents)
- Storing only what's necessary for the book context

---

**Note:** Place your persona files in this directory, and they'll be automatically accessible to all agents through `.cursorrules`.

