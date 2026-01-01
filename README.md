# AI Research Feed

Scrapes research updates from Anthropic and OpenAI and sends email notifications via Mailgun for new publications since the last business day.

## Features

- **Anthropic**: Scrapes https://www.anthropic.com/research directly
- **OpenAI**: Parses https://openai.com/news/rss.xml RSS feed (filters for research-related content)
- Filters papers published after the last business day
- Sends combined email notifications grouped by source

## Setup

1. Create a virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create a `key.txt` file with your Mailgun API key:
```bash
echo "your-mailgun-api-key" > key.txt
```

4. Update the Mailgun domain and recipient email in [main.py](main.py):
   - Line 180: Update the Mailgun domain URL
   - Line 184: Update the recipient email address

## Usage

Run the script:
```bash
python main.py
```

The script will:
- Scrape both Anthropic and OpenAI sources
- Filter papers published after the last business day
- Send an email notification if new papers are found (grouped by source)

## Scheduling

To run this automatically, set up a cron job:
```bash
# Run every weekday at 9 AM
0 9 * * 1-5 cd /path/to/lab-research-feed && ./venv/bin/python main.py
```