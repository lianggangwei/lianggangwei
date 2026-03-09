---
name: "persistent-agent"
description: "Enables persistent autonomous agent operation. Invoke when user needs background tasks, continuous monitoring, or autonomous execution."
---

# Persistent Agent System

This skill enables the AI assistant to operate as a persistent autonomous agent, running continuously in the background and executing tasks autonomously.

## Features

- **Background Operation**: Runs continuously without user interaction
- **Autonomous Execution**: Executes tasks independently
- **Task Scheduling**: Schedules recurring tasks
- **Monitoring**: Monitors system and application states
- **Auto-Recovery**: Recovers from errors automatically
- **State Persistence**: Maintains state across restarts

## When to Invoke

- User needs background task execution
- User wants continuous monitoring
- User mentions "always on" or "run in background"
- User needs scheduled task execution
- User wants autonomous operation

## Agent Capabilities

1. **Task Execution**: Run tasks automatically
2. **File Monitoring**: Watch for file changes
3. **System Monitoring**: Monitor system resources
4. **Scheduled Jobs**: Execute at specific times
5. **Event Handling**: Respond to system events
6. **Auto-Updates**: Self-update capabilities

## Usage

```python
# Start persistent agent
agent.start()

# Add background task
agent.add_task(
    name="daily_backup",
    schedule="0 2 * * *",  # Daily at 2 AM
    action=backup_system
)

# Monitor file changes
agent.watch_directory("./data", on_change=process_file)

# Check agent status
status = agent.get_status()
```

## Configuration

- **Mode**: Background service
- **Auto-Start**: Enabled on system boot
- **Recovery**: Automatic restart on failure
- **Logging**: Full activity logging
- **Memory**: Persistent state storage

## Task Types

- Scheduled tasks (cron-style)
- Event-driven tasks
- Continuous monitoring
- Periodic checks
- Triggered actions
