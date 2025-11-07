import csv
import random
from datetime import datetime, timedelta
import hashlib

# Seed for reproducibility
random.seed(42)

# Helper function to hash user IDs (privacy-safe)
def hash_id(base_id, salt="project_salt_2025"):
    """
    Hashes a user ID with a salt for privacy.
    In production, the salt would be stored securely (not in code).
    """
    return hashlib.sha256(f"{base_id}{salt}".encode()).hexdigest()[:16]

# Configuration
start_date = datetime(2025, 1, 1)
num_days = 90
num_users = 5000
num_campaigns = 8
num_content_items = 50

campaigns = [f"CPG_{i+1:02d}" for i in range(num_campaigns)]
placements = ["pre_roll", "mid_roll", "display_banner", "sponsored_tile"]
devices = ["mobile", "desktop", "tablet", "tv"]
geos = ["US", "CA", "UK", "DE", "FR", "JP", "AU"]

# Generate content_catalog.csv
print("Generating content_catalog.csv...")
with open('seeds/content_catalog.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['content_id', 'title', 'genre', 'rating', 'duration_s', 'release_year'])
    
    genres = ["Action", "Comedy", "Drama", "Documentary", "Thriller", "Sci-Fi"]
    ratings = ["G", "PG", "PG-13", "R", "TV-MA"]
    
    for i in range(num_content_items):
        writer.writerow([
            f"content_{i+1:04d}",
            f"Title_{i+1}",
            random.choice(genres),
            random.choice(ratings),
            random.randint(1800, 7200),  # 30 min to 2 hours
            random.randint(2020, 2025)
        ])

print(f"✓ Created content_catalog.csv with {num_content_items} items")

# Generate ad_events.csv
print("Generating ad_events.csv...")
impression_counter = 0

with open('seeds/ad_events.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow([
        'event_ts', 'event_type', 'user_id_hash', 'impression_id', 
        'campaign_id', 'content_id', 'placement', 'device', 'geo',
        'view_time_ms', 'pct_quartile', 'audible', 'clicked'
    ])
    
    for day in range(num_days):
        date = start_date + timedelta(days=day)
        # More events on weekends (realistic pattern)
        daily_events = random.randint(8000, 12000) if date.weekday() < 5 else random.randint(10000, 15000)
        
        for _ in range(daily_events):
            user_id = f"user_{random.randint(1, num_users):05d}"
            user_hash = hash_id(user_id)
            campaign = random.choice(campaigns)
            content = f"content_{random.randint(1, num_content_items):04d}"
            placement = random.choice(placements)
            device = random.choice(devices)
            geo = random.choice(geos)
            
            # Impression
            impression_counter += 1
            imp_id = f"imp_{impression_counter:010d}"
            event_ts = date + timedelta(
                hours=random.randint(0, 23),
                minutes=random.randint(0, 59),
                seconds=random.randint(0, 59)
            )
            
            # Viewability and engagement logic
            # 70% of impressions are "viewable" (>= 2 seconds view time)
            viewed = random.random() < 0.7
            view_time = random.randint(2000, 15000) if viewed else random.randint(0, 1500)
            
            # Video completion quartiles (only for viewed impressions)
            if viewed:
                quartile = random.choice([0, 25, 50, 75, 100])
            else:
                quartile = 0
            
            # 85% of impressions have audio enabled
            audible = random.random() < 0.85
            
            # 2% click-through rate (industry realistic)
            clicked = random.random() < 0.02
            
            writer.writerow([
                event_ts.isoformat(),
                'impression',
                user_hash,
                imp_id,
                campaign,
                content,
                placement,
                device,
                geo,
                view_time,
                quartile,
                1 if audible else 0,
                1 if clicked else 0
            ])

print(f"✓ Created ad_events.csv with {impression_counter:,} impressions")

# Generate conversions.csv
print("Generating conversions.csv...")
conversion_counter = 0

with open('seeds/conversions.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow([
        'conversion_id', 'event_ts', 'user_id_hash', 'campaign_id',
        'conversion_type', 'revenue'
    ])
    
    # Conversions happen for ~3% of exposed users
    for day in range(num_days):
        date = start_date + timedelta(days=day)
        daily_conversions = random.randint(80, 150)
        
        for _ in range(daily_conversions):
            conversion_counter += 1
            user_id = f"user_{random.randint(1, num_users):05d}"
            user_hash = hash_id(user_id)
            campaign = random.choice(campaigns)
            conversion_type = random.choice(['sign_up', 'purchase', 'subscription'])
            
            # Revenue varies by conversion type
            if conversion_type == 'sign_up':
                revenue = 0
            elif conversion_type == 'purchase':
                revenue = round(random.uniform(9.99, 149.99), 2)
            else:  # subscription
                revenue = random.choice([9.99, 14.99, 19.99])
            
            event_ts = date + timedelta(
                hours=random.randint(0, 23),
                minutes=random.randint(0, 59),
                seconds=random.randint(0, 59)
            )
            
            writer.writerow([
                f"conv_{conversion_counter:08d}",
                event_ts.isoformat(),
                user_hash,
                campaign,
                conversion_type,
                revenue
            ])

print(f"✓ Created conversions.csv with {conversion_counter:,} conversions")
print("\n" + "="*50)
print("Data generation complete! 🎉")
print("="*50)
print(f"\nSummary:")
print(f"  • Content items: {num_content_items}")
print(f"  • Ad impressions: {impression_counter:,}")
print(f"  • Conversions: {conversion_counter:,}")
print(f"  • Date range: {start_date.date()} to {(start_date + timedelta(days=num_days-1)).date()}")
print(f"  • Unique users: ~{num_users:,}")