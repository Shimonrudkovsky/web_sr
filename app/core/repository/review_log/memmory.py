from uuid import UUID

from fsrs.models import ReviewLog, SchedulingInfo

from app.core.models.card import Card

from ..interfaces import ReviewLogRepositoryInterface


class ReviewLogMemmoryRepository(ReviewLogRepositoryInterface):
    def __init__(self) -> None:
        self.storage: dict[UUID, SchedulingInfo] = dict()

    async def add(self, scheduled_card: SchedulingInfo) -> None:
        card: Card = scheduled_card.card
        review_log: ReviewLog = scheduled_card.review_log
        if card.id in self.storage:
            self.storage[card.id].append(review_log)
        else:
            self.storage[card.id] = [
                review_log,
            ]
