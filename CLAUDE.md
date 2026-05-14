# lab-research-feed

## Testing changes

Always test changes by running `main.py` end-to-end and confirming a test email is delivered:

```
source venv/bin/activate && python main.py
```

A successful run prints `200` and a `Queued. Thank you.` JSON response from Mailgun, followed by `Email sent successfully!`. Check the inbox to verify the new source actually appears in the rendered HTML. Don't rely solely on unit-style spot checks of individual scrape functions — the full pipeline (scrape → filter → email) is what matters.
