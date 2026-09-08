# Betting Automation Bot

## Overview

Automation tool that monitors betting information from a source website, extracts betting data and automatically replicates selected bets.

The system can be controlled remotely through a Telegram bot and supports notifications and data storage using CSV files.

## Features

- Web scraping
- Automated bet replication
- Telegram bot control
- Notifications
- CSV data storage
- Process monitoring

## Technologies

- Python
- Telegram Bot API
- Web Scraping
- CSV Processing
- Automation

## Configuration

No credentials are stored in this repository. Copy the templates and fill them in
locally — all of them are git-ignored:

```bash
cp .env.example .env
cp login_to_mail.csv.example login_to_mail.csv
cp infromation_for_header.csv.example infromation_for_header.csv
cp user_id.csv.example user_id.csv
```

| Variable | Purpose |
| --- | --- |
| `TELEGRAM_BOT_TOKEN` | Token of the Telegram bot used for control and notifications |
| `IMAP_SERVER` / `IMAP_PORT` | IMAP host and port of the mailbox that receives bet notifications |
| `PATH_TO_EMAIL_DATA` | Optional path override for the mailbox credentials file |

## Running

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python main.py
```
