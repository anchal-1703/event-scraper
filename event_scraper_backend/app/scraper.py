from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright
import logging

logging.basicConfig(level=logging.INFO)

def scrape_eventbrite(page=1):
    events = []
    
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            context = browser.new_context(
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                           "AppleWebKit/537.36 (KHTML, like Gecko) "
                           "Chrome/112.0.0.0 Safari/537.36"
            )
            page_obj = context.new_page()
            url = f"https://www.eventbrite.com.au/d/australia--sydney/all-events/?page={page}"
            page_obj.goto(url, timeout=60000)
            page_obj.wait_for_timeout(5000)
            html = page_obj.content()
            browser.close()

        logging.info(f"Scraping Eventbrite page {page}")
        soup = BeautifulSoup(html, "html.parser")

        card_selectors = ["div.discover-search-desktop-card"]
        cards = soup.select(",".join(card_selectors))

        if not cards:
            logging.warning(f"No event cards found on page {page}")
            return []

        for card in cards:
            try:
                title_tag = card.select_one("h3.event-card__clamp-line--two")
                title = title_tag.get_text(strip=True) if title_tag else "No Title"

                url_tag = card.select_one("a.event-card-link")
                url = url_tag["href"] if url_tag else None

                image_tag = card.select_one("img.event-card-image")
                image = image_tag["src"] if image_tag else ""

                all_p_tags = card.select("p")

                badge = None
                badge_div = card.select_one(".event-card-badge")
                if badge_div and badge_div.select_one("p"):
                    badge = badge_div.select_one("p").get_text(strip=True)

                date_tags = [
                    p
                    for p in all_p_tags
                    if not p.find_parent("aside")
                    and not p.find_parent("div", class_="event-card-badge")
                ]

                date = date_tags[0].get_text(strip=True) if len(date_tags) > 0 else "Unknown"
                venue = date_tags[1].get_text(strip=True) if len(date_tags) > 1 else "Unknown"

                events.append({
                    "source": "Eventbrite",
                    "title": title,
                    "url": url,
                    "date": date,
                    "venue": venue,
                    "image": image,
                    "badge": badge,
                })

            except Exception as e:
                logging.error("Event parsing failed:", exc_info=e)
                continue

    except Exception as e:
        logging.error(f"Scraping failed for page {page}:", exc_info=e)
        return []

    return events
