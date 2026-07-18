#!/usr/bin/env python3
import requests
import json
from bs4 import BeautifulSoup
from datetime import datetime, timedelta

def fetch_contributions(username):
    """Fetch contribution calendar from GitHub without token."""
    
    url = f"https://github.com/users/{username}/contributions"
    
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Error fetching contributions: {e}")
        return None
    
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Find all contribution data cells
    contributions = []
    days_with_data = []
    
    for rect in soup.find_all('rect', {'data-count': True}):
        count = int(rect.get('data-count', 0))
        date = rect.get('data-date', '')
        
        if date:
            contributions.append({
                'date': date,
                'count': count
            })
            if count > 0:
                days_with_data.append(count)
    
    if not contributions:
        print("No contribution data found")
        return None
    
    # Calculate stats
    total = sum(c['count'] for c in contributions)
    current_streak = 0
    longest_streak = 0
    temp_streak = 0
    
    for c in reversed(contributions):
        if c['count'] > 0:
            temp_streak += 1
            longest_streak = max(longest_streak, temp_streak)
            if temp_streak == 1:
                current_streak += 1
        else:
            if temp_streak > 0:
                break
    
    stats = {
        'total_contributions': total,
        'current_streak': current_streak,
        'longest_streak': longest_streak,
        'contributions': contributions,
        'fetched_at': datetime.now().isoformat()
    }
    
    with open('data/contributions.json', 'w') as f:
        json.dump(stats, f, indent=2)
    
    print(f"Fetched {len(contributions)} days of contribution data")
    print(f"Total: {total} contributions")
    return stats

if __name__ == "__main__":
    import sys
    username = sys.argv[1] if len(sys.argv) > 1 else "avivashishta29"
    fetch_contributions(username)