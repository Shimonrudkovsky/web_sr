from uuid import uuid4

from fsrs.models import SchedulingInfo

from app.db.postgres import AsyncPGStorage

from ..interfaces import ReviewLogRepositoryInterface


class ReviewLogPostgresRepository(ReviewLogRepositoryInterface):
    def __init__(self, storage: AsyncPGStorage) -> None:
        self.storage = storage

    async def add(self, scheduling_info: SchedulingInfo):
        query = """
        INSERT INTO web_sr.review_log (id, card_id, rating, scheduled_days, elapsed_days, review, state)
        VALUES (%s, %s, %s, %s, %s, %s, %s);
        """

        await self.storage.execute(
            query=query,
            params=(
                uuid4(),
                scheduling_info.card.id,
                scheduling_info.review_log.rating,
                scheduling_info.review_log.scheduled_days,
                scheduling_info.review_log.elapsed_days,
                scheduling_info.review_log.review,
                scheduling_info.review_log.state,
            ),
        )
