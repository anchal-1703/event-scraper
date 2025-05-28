from flask import Blueprint, request, jsonify
from .scraper import scrape_eventbrite
from .redis_client import cache_events, get_cached_events, get_persistent_events, save_email
from .utils import is_valid_email, is_valid_url
import time

main = Blueprint("main", __name__)

@main.route("/api/events", methods=["GET"], strict_slashes=False)
def get_events():
    print("Getting events")
    # Get the page parameter from the request, default to 1 if not provided
    page = request.args.get('page', 1, type=int)
    
    # Create a cache key that includes the page number
    cache_key = f"events_page_{page}"
    
    # Try to get from regular cache first
    cached = get_cached_events(cache_key)
    if cached:
        return jsonify({
            "from_cache": True, 
            "events": cached, 
            "page": page,
            "message": None
        })

    # Try to scrape new data
    scraped = scrape_eventbrite(page)
    
    # If scraping succeeded (found events)
    if scraped:
        # Store in both regular cache and persistent storage
        cache_events(scraped, cache_key, persistent=True)
        
        return jsonify({
            "from_cache": False, 
            "events": scraped, 
            "page": page,
            "message": None
        })
    else:
        # Scraping failed or no events found, try to get from persistent storage
        persistent_data = get_persistent_events(cache_key)
        
        if persistent_data:
            return jsonify({
                "from_cache": True, 
                "events": persistent_data, 
                "page": page,
                "message": "No new events found. Showing last available data."
            })
        else:
            # No data available at all
            return jsonify({
                "from_cache": False, 
                "events": [], 
                "page": page,
                "message": "No events found"
            })

@main.route("/api/email", methods=["POST"], strict_slashes=False)
def save_email_route():
    email = request.json.get('email')
    if not email or not is_valid_email(email):
        return jsonify({"success": False, "message": "Invalid email"}), 400

    save_email(email)
    return jsonify({"success": True, "message": "Email saved"}), 200