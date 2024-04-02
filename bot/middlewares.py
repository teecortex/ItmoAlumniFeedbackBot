from aiogram.filters import BaseFilter
from aiogram.types import Message

class EmailTypeFilter(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        entities = message.entities
        if entities is None:
            return False

        return len(entities) == 1 and entities[0].type == 'email'