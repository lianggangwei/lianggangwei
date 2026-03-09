---
name: "long-term-memory"
description: "Enables permanent long-term memory storage. Invoke when user wants to save/retrieve conversation history, preferences, habits, or needs across sessions."
---

# Long-Term Memory System

This skill provides permanent long-term memory capabilities for the AI assistant, ensuring all conversations, preferences, habits, and user needs are preserved across sessions.

## Features

- **Persistent Storage**: All data stored in local ChromaDB database
- **Automatic Learning**: Incrementally learns from every interaction
- **Context Retrieval**: Retrieves relevant past information automatically
- **Preference Tracking**: Remembers user preferences and habits
- **Git Sync**: Synchronizes memory database with Git repository

## When to Invoke

- User mentions "remember this" or "save this"
- User asks about past conversations
- User wants to retrieve preferences or habits
- Starting a new conversation session
- User wants to sync memory to Git

## Memory Categories

1. **Conversation History**: Complete dialogue records
2. **User Preferences**: Settings, styles, formats
3. **Habits**: Common patterns and workflows
4. **Needs**: Recurring requirements
5. **Personality**: User's communication style
6. **Commands**: Frequently used instructions

## Usage

```python
# Save to memory
memory.save(category="preferences", content="User prefers Python code")

# Retrieve from memory
results = memory.query("What are my preferences?")

# Sync to Git
memory.sync_to_git()
```

## Database Location

- Local: `./memory_db/`
- Git Sync: Automatic push on changes
