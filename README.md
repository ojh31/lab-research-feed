# Anthropic Research Feed

Scrapes the Anthropic research page for new publications and sends email notifications via Mailgun.

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

4. Update the Mailgun domain and recipient email in `main.py`:
   - Line 105: Update the Mailgun domain URL
   - Line 109: Update the recipient email address

## Usage

Run the script:
```bash
python main.py
```

The script will:
- Scrape https://www.anthropic.com/research
- Filter papers published since the last business day
- Send an email notification if new papers are found

## Scheduling

To run this automatically, set up a cron job:
```bash
# Run every weekday at 9 AM
0 9 * * 1-5 cd /path/to/lab-research-feed && ./venv/bin/python main.py
```
