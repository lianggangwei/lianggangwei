---
name: "jarvis-core"
description: "Core AI assistant framework integrating all skills. Invoke when user needs comprehensive assistant capabilities or system orchestration."
---

# JARVIS Core System

This is the central orchestration system that integrates all AI assistant capabilities, providing a unified interface for intelligent assistance.

## Features

- **Central Orchestration**: Coordinates all skills and modules
- **Natural Language Understanding**: Advanced NLU capabilities
- **Task Automation**: Automates complex workflows
- **Multi-Modal Support**: Text, voice, and visual inputs
- **Intelligent Routing**: Routes requests to appropriate handlers
- **Context Management**: Maintains conversation context

## When to Invoke

- User needs comprehensive assistant functionality
- Multiple skills need to work together
- User asks for system status or capabilities
- Complex multi-step tasks required
- System initialization or configuration

## Core Modules

1. **Memory Module**: Long-term and short-term memory
2. **Voice Module**: Voice activation and commands
3. **Learning Module**: Self-improvement capabilities
4. **Agent Module**: Persistent autonomous operation
5. **Task Module**: Workflow automation
6. **Communication Module**: Multi-channel interaction

## Usage

```python
# Initialize JARVIS
jarvis.initialize()

# Process user request
response = jarvis.process("Help me organize my project")

# Check system status
status = jarvis.get_status()

# Enable all modules
jarvis.enable_all_modules()
```

## Architecture

```
JARVIS Core
├── Memory System (ChromaDB)
├── Voice System (Wake Word Detection)
├── Learning System (Self-Improvement)
├── Agent System (Persistent Operation)
├── Task System (Automation)
└── Communication System (Multi-Channel)
```

## Configuration

- Memory: `./memory_db/`
- Voice: Microphone access required
- Learning: Auto-update enabled
- Agent: Background process mode
