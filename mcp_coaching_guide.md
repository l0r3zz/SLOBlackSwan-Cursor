# Model Context Protocol (MCP) Coaching Guide for Cursor AI IDE
**For: Geoff White**  
**Date: November 11, 2025**

## Executive Summary: MCP vs MDC Files

First, let me clear up the confusion: **MCP is not about .mcp files**. Your implementation guide mentions two different systems:

1. **`.mdc` files (Model Definition Cards)** - These are agent configuration files specific to your workflow
2. **MCP (Model Context Protocol)** - A JSON-based configuration system for connecting external tools to AI models

MCP is an open standard developed by Anthropic that standardizes how AI assistants connect to external data sources and tools -- think of it as the "USB-C for AI integrations". It's configured through JSON files, not .mcp files.

---

## What is Model Context Protocol (MCP)?

Model Context Protocol is an open standard that enables seamless integration between LLM applications and external data sources and tools. It replaces fragmented, custom integrations with a single protocol. 

### Key Concepts

MCP provides three fundamental building blocks:
- **Prompts**: Pre-defined templates or instructions that guide language model interactions
- **Resources**: Structured data or content that provides additional context to the model  
- **Tools**: Executable functions that allow models to perform actions or retrieve information

### Architecture

MCP follows a client-host-server architecture where:
- **Host**: The container application (like Cursor) that manages multiple clients
- **Client**: MCP-compatible AI applications that connect to servers
- **Server**: Lightweight programs that expose specific capabilities

---

## MCP Configuration in Cursor

### Configuration File Locations

In Cursor, MCP is configured through JSON files at two levels:

1. **Global Configuration**: `~/.cursor/mcp.json`
   - Available across all projects
   - Located in your home directory

2. **Project Configuration**: `.cursor/mcp.json`  
   - Specific to individual projects
   - Located in project root

### JSON Configuration Structure

```json
{
  "mcpServers": {
    "server-name": {
      "command": "executable",
      "args": ["arg1", "arg2"],
      "env": {
        "API_KEY": "your-key-here"
      }
    }
  }
}
```

### Real Examples from Your Guide

Your implementation guide shows MCP configuration for API access:

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

---

## Understanding the Difference: MCP vs MDC

### Your .mdc Files (Model Definition Cards)
These are agent configuration files specific to your workflow:
- `research-agent.mdc`
- `writing-agent.mdc`
- `critique-agent.mdc`

These define agent behaviors, models, and instructions within Cursor.

### MCP Servers
These are external tools that extend Cursor's capabilities:
- Database connectors
- API integrations
- File system access
- Web scraping tools

---

## Quick Setup Guide

### Step 1: Access MCP Settings in Cursor

Navigate to Cursor Settings:
1. Press `Cmd/Ctrl + Shift + P`
2. Type "View: Open MCP Settings"
3. Or go to File → Preferences → Cursor Settings → MCP

### Step 2: Add a Simple MCP Server

Here's a basic example for a filesystem server:

```json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "/path/to/directory"]
    }
  }
}
```


### Step 3: Verify Connection
- Restart Cursor
- Check for green indicator next to server name
- Test by using `Cmd/Ctrl + L` to open chat

---

## Recommended Learning Resources

### Video Tutorials

1. **"Build Anything with MCP Agents - Here's How"** by Tech with Tim
   20-minute developer-focused tutorial covering:
   - Understanding protocols and standards
   - MCP fundamentals
   - Installing Node.js and adding MCP servers to Cursor
   - Installing from Smithery
   - Setting up auto-calling tools
   
2. **"MCP in Cursor Made Simple"** - Search YouTube for recent tutorials
   - Focus on practical implementation
   - Look for videos from 2025

### Essential Articles

1. **Official Documentation**
   - [Model Context Protocol Documentation](https://modelcontextprotocol.io)
   - Start with the Introduction and Quickstart guides
   
2. **Cursor-Specific Guides**
   Medium has excellent guides including:
   - "Integrating Model Context Protocol with Cursor: A Comprehensive Guide"
   - "Cursor MCP -- A 5-Minute Quick Start Guide"

3. **Community Resources**
   - GitHub: Model Context Protocol organization (github.com/modelcontextprotocol)
   - Community registry of MCP servers
   - Example implementations in Python, TypeScript, Rust

### Quick Reference Sites

1. **Smithery.ai** - Curated collection of MCP servers with one-click install
2. **Cursor Directory** - MCP server directory specific to Cursor
3. **Composio** - 100+ managed MCP servers with built-in authentication

---

## Popular MCP Servers to Try First

### For Development

1. **GitHub MCP Server**
   ```json
   {
     "mcpServers": {
       "github": {
         "command": "docker",
         "args": ["run", "-i", "--rm", "-e", "GITHUB_PERSONAL_ACCESS_TOKEN", 
                  "ghcr.io/github/github-mcp-server"],
         "env": {
           "GITHUB_PERSONAL_ACCESS_TOKEN": "${input:github_token}"
         }
       }
     }
   }
   ```

2. **Filesystem Server** - Access local files
3. **Database Servers** - PostgreSQL, MongoDB, etc.

### For Research/Writing

1. **Perplexity MCP** - Web search integration
2. **YouTube Transcript Server** - Extract video transcripts
3. **Notion/Google Drive** - Document access

---

## Advanced Integration for Your Book Project

### Combining MCP with Your Agent Workflow

Your current workflow uses:
- `.mdc` files for agent configuration
- `.cursorrules` for global behavior
- Python scripts for automation

MCP can enhance this by adding:
- **Research capabilities**: Direct web search from agents
- **Data persistence**: Database connections for storing research
- **External tool access**: Citation managers, plagiarism checkers

### Example: Research Enhancement

```json
{
  "mcpServers": {
    "web-search": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-perplexity"],
      "env": {
        "PERPLEXITY_API_KEY": "${PERPLEXITY_API_KEY}"
      }
    },
    "citations": {
      "command": "python",
      "args": ["/path/to/citation-manager-mcp.py"]
    }
  }
}
```

---

## Security Considerations

Important security concerns with MCP servers:
- **Malicious servers**: Always review server code before installation
- **Vulnerable dependencies**: Check for security vulnerabilities
- **Prompt injection**: Some servers might manipulate AI behavior

Best practices:
- Use trusted, open-source servers
- Review permissions requested
- Keep servers updated
- Use project-specific servers when testing

---

## Troubleshooting Common Issues

### Server Won't Connect
- Check Node.js is installed: `node --version`
- Verify JSON syntax (no trailing commas!)
- Ensure file paths are absolute
- Check API keys are correctly set

### Tool Not Available in Chat
- Restart Cursor after configuration changes
- Use Agent mode, not Ask mode
- Check server logs for errors
- Verify green indicator in MCP settings

---

## Your Next Steps

### Week 1: Foundation
1. **Understand the distinction**: MCP (tools/data) vs MDC (agent config)
2. **Install Node.js** if not already installed
3. **Try a simple server**: Start with filesystem or time server
4. **Watch Tech with Tim's tutorial** for visual learning

### Week 2: Integration
1. **Add relevant servers** for your book project:
   - GitHub for version control integration
   - Web search for research
   - Database for storing notes
2. **Test with your agents**: See how MCP tools appear in chat
3. **Document what works** for your specific workflow

### Week 3: Advanced
1. **Create custom MCP server** for book-specific tools
2. **Integrate with your Python scripts**
3. **Optimize server selection** based on task

---

## Key Takeaways

1. **MCP uses JSON configuration**, not .mcp files
2. **It's complementary** to your existing .mdc agent setup
3. **Start simple** with pre-built servers before creating custom ones
4. **Security matters** -- review servers before installation
5. **The ecosystem is growing rapidly** -- check for new servers regularly

---

## Resources Summary

### Must-Read
- [modelcontextprotocol.io](https://modelcontextprotocol.io) - Official docs
- [Cursor MCP Documentation](https://cursor.com/docs/context/mcp)

### Must-Watch
- Tech with Tim's "Build Anything with MCP Agents"
- Search YouTube for "MCP Cursor 2025" tutorials

### Communities
- MCP Discord Server
- Cursor Community Forum
- GitHub Discussions on modelcontextprotocol repo

---

**Remember**: MCP extends what your AI can access and do, while your .mdc files control how your agents behave. Together, they create a powerful system for AI-assisted book writing.

The protocol is evolving rapidly, so stay connected with the community for updates and new capabilities. Focus first on understanding the JSON configuration structure, then gradually add servers that enhance your specific workflow.

**You're now equipped to leverage MCP effectively in your Cursor setup!**