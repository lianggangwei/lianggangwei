---
name: "voice-wakeup"
description: "Enables voice activation and wake word detection. Invoke when user wants hands-free operation or voice commands."
---

# Voice Wakeup System

This skill enables voice activation capabilities, allowing the AI assistant to be activated and controlled through voice commands.

## Features

- **Wake Word Detection**: Activates on custom wake words
- **Voice Commands**: Execute commands through voice
- **Hands-Free Operation**: No keyboard required
- **Multi-Language Support**: Supports multiple languages
- **Noise Cancellation**: Works in noisy environments

## When to Invoke

- User mentions "voice activation" or "wake word"
- User wants hands-free operation
- User asks to set up voice commands
- User mentions "Hey Assistant" or similar triggers

## Wake Words

Default wake words:
- "Hey Assistant"
- "OK Assistant"
- "小龙虾" (Chinese)
- "小助手" (Chinese)

## Usage

```python
# Start voice listener
voice.start_listening(wake_word="Hey Assistant")

# Add custom wake word
voice.add_wake_word("小龙虾")

# Execute voice command
voice.execute_command("open browser")
```

## Requirements

- Microphone access
- Speech recognition library
- Audio processing capabilities

## Supported Commands

- Open applications
- Search the web
- Control system functions
- Query information
- Execute scripts
