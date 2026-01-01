from datetime import datetime, time, timedelta
from typing import Dict, List

import requests
from bs4 import BeautifulSoup
from dateutil import parser


def get_last_business_day():
    today = datetime.now().date()
    offset = max(1, (today.weekday() + 6) % 7 - 3)
    last_business_day = today - timedelta(days=offset)
    return datetime.combine(last_business_day, time.min)


def scrape_anthropic_research() -> List[Dict[str, str]]:
    """Scrape from Anthropic's research page."""
    url = "https://www.anthropic.com/research"
    response = requests.get(url)
    response.raise_for_status()

    soup = BeautifulSoup(response.content, "html.parser")
    papers = []

    # Find all links that point to research publications (not team pages)
    for link in soup.find_all("a", href=True):
        href = link.get("href", "")

        # Filter for research publications, excluding team pages
        if "/research/" in href and "/research/team/" not in href:
            # Try to find time element for date
            date_elem = link.find("time")
            date_str = date_elem.get_text(strip=True) if date_elem else ""

            # Try to find title - look for span with 'title' in class name
            title_elem = link.find("span", class_=lambda x: x and "title" in x.lower())

            # Fallback to heading tags
            if not title_elem:
                title_elem = link.find(["h2", "h3", "h4", "h5", "h6"])

            # Extract title text
            if title_elem:
                title = title_elem.get_text(strip=True)
            else:
                # Skip if we can't find a proper title element
                continue

            # Skip if we don't have essential info
            if not title or not href:
                continue

            # Make URL absolute if needed
            if href.startswith("/"):
                href = f"https://www.anthropic.com{href}"

            papers.append({"title": title, "url": href, "date": date_str})

    # Remove duplicates by URL
    seen_urls = set()
    unique_papers = []
    for paper in papers:
        if paper["url"] not in seen_urls:
            seen_urls.add(paper["url"])
            unique_papers.append(paper)

    return unique_papers


def filter_new_papers(
    papers: List[Dict[str, str]], since_date: datetime
) -> List[Dict[str, str]]:
    """Filter papers published since the given date."""
    new_papers = []

    for paper in papers:
        if not paper["date"]:
            # If no date available, skip it
            continue

        try:
            # Parse the date string
            paper_date = parser.parse(paper["date"])
            # Use > instead of >= to exclude papers from exactly the since_date
            if paper_date > since_date:
                new_papers.append(paper)
        except (ValueError, TypeError):
            # If date parsing fails, skip it
            continue

    return new_papers


def create_email_html(papers: List[Dict[str, str]]) -> str:
    """Create HTML email content for new papers."""
    if not papers:
        return "<p>No new papers found.</p>"

    html = "<h2>New Anthropic Research</h2>"
    html += f"<p>Found {len(papers)} new paper(s) since the last business day:</p>"
    html += "<ul>"

    for paper in papers:
        html += f'<li><a href="{paper["url"]}">{paper["title"]}</a>'
        if paper["date"]:
            html += f" - {paper['date']}"
        html += "</li>"

    html += "</ul>"
    return html


def send_simple_message(subject: str, html: str):
    with open("key.txt", "r") as file:
        api_key = file.read().strip()
    response = requests.post(
        "https://api.mailgun.net/v3/sandbox9e8f7a4f3d3d469c9c07ce895892fa11.mailgun.org/messages",  # noqa: E501
        auth=("api", api_key),
        data={
            "from": "Anthropic Research Feed<mailgun@sandbox9e8f7a4f3d3d469c9c07ce895892fa11.mailgun.org>",  # noqa: E501
            "to": "oskar@far.ai",
            "subject": subject,
            "html": html,
        },
    )
    print(response.status_code)
    print(response.text)


def main():
    """Main execution function."""
    print("Scraping Anthropic research page...")
    papers = scrape_anthropic_research()
    print(f"Found {len(papers)} total papers")

    last_business_day = get_last_business_day()
    print(f"Checking for papers published after: {last_business_day.date()}")

    new_papers = filter_new_papers(papers, last_business_day)
    print(f"Found {len(new_papers)} new papers")

    if new_papers:
        email_html = create_email_html(new_papers)
        subject = f"New Anthropic Research - {datetime.now().strftime('%Y-%m-%d')}"
        print("Sending email notification...")
        send_simple_message(subject, email_html)
        print("Email sent successfully!")
    else:
        print("No new papers to report.")


if __name__ == "__main__":
    main()
