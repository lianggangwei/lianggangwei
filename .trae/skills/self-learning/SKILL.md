---
name: "self-learning"
description: "Enables automatic learning and improvement from interactions. Invoke when user wants the assistant to learn from feedback or improve over time."
---

# Self-Learning System

This skill enables the AI assistant to automatically learn and improve from every interaction, continuously enhancing its capabilities.

## Features

- **Incremental Learning**: Learns from every interaction
- **Feedback Integration**: Incorporates user feedback
- **Pattern Recognition**: Identifies user patterns
- **Knowledge Expansion**: Expands knowledge base
- **Performance Optimization**: Improves response quality
- **Adaptive Behavior**: Adapts to user preferences

## When to Invoke

- User provides feedback on responses
- User wants the assistant to learn
- User mentions "improve" or "learn from this"
- User corrects assistant's behavior
- User wants personalized responses

## Learning Mechanisms

1. **Conversation Learning**: Learns from dialogue patterns
2. **Preference Learning**: Adapts to user preferences
3. **Error Learning**: Learns from mistakes
4. **Context Learning**: Understands context better
5. **Skill Learning**: Acquires new capabilities
6. **Optimization Learning**: Improves efficiency

## Usage

```python
# Enable self-learning
learning.enable()

# Learn from feedback
learning.from_feedback(
    interaction_id="123",
    feedback="Response was too verbose",
    correction="Be more concise"
)

# Get learning stats
stats = learning.get_stats()

# Apply learned knowledge
learning.apply_to_category("preferences")
```

## Learning Categories

- **Communication Style**: How to communicate
- **Task Patterns**: Common task sequences
- **Error Patterns**: What to avoid
- **Success Patterns**: What works well
- **User Preferences**: Individual preferences
- **Context Patterns**: Contextual understanding

## Data Storage

- Learning data: `./learning_db/`
- Feedback log: `./logs/feedback.json`
- Pattern database: `./patterns/`
- Improvement history: `./improvements/`

## Privacy

- All learning data stored locally
- No external data sharing
- User-controlled learning scope
- Option to disable learning
- Data export capability
