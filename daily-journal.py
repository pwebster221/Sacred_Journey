# In your sacred_journey directory
from src.journey_logger import JourneyLogger

# Initialize your sacred space
logger = JourneyLogger()

# Create today's vessel for reflection
today_path = logger.create_daily_template()
print(f"Today's sacred space awaits at: {today_path}")