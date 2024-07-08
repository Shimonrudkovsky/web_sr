from datetime import datetime, timezone
from fsrs import FSRS
from fsrs.models import Card, State

# Initialize FSRS model
fsrs_model = FSRS()

# Create a new card
card = Card(
    due=datetime.now(timezone.utc),
    stability=1.0,
    difficulty=3.0,
    state=State.New
)

# Simulate a review session
now = datetime.now(timezone.utc)
review_results = fsrs_model.repeat(card, now)

# Print the scheduling information for different ratings
for rating, scheduling_info in review_results.items():
    print(f"Rating: {rating}")
    print(f"Scheduled Days: {scheduling_info.review_log.scheduled_days}")
    print(f"Due Date: {scheduling_info.card.due}")
    print(f"Stability: {scheduling_info.card.stability}")
    print(f"Difficulty: {scheduling_info.card.difficulty}")
    print(f"State: {scheduling_info.card.state}")
    print("-" * 40)
