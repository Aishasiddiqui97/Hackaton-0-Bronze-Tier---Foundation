# 🚀 Bronze Tier Setup

## Installation

```bash
pip install -r requirements.txt
```

## Usage

Start the watcher:

```bash
python watcher.py
```

Drop .md files into `Inbox/` to trigger processing.

## Manual Processing

Process tasks without watcher:

```bash
python task_processor.py
```

## Structure

```
AI_Employee_Vault/
├── Inbox/              # Drop tasks here
├── Needs_Action/       # Active tasks
├── Done/               # Completed tasks
├── Logs/               # System logs
├── Skills/             # Agent skill definitions
├── Dashboard.md        # Status overview
├── Company_Handbook.md # Operating rules
├── watcher.py          # File monitor
└── task_processor.py   # Task executor
```
