from sacred_tracker import SacredCycleTracker

# Initialize your sacred space
tracker = SacredCycleTracker()

# Create a lunar review template
lunar_path = tracker.create_lunar_review('new')  # or 'full' for full moon
print(f"Lunar template created at: {lunar_path}")

# Create a solar review template
solar_path = tracker.create_solar_review()
print(f"Solar template created at: {solar_path}")

# See your upcoming sacred reviews
upcoming = tracker.schedule_next_reviews()
for review, date in upcoming.items():
    print(f"{review}: {date.strftime('%Y-%m-%d %H:%M UTC')}")