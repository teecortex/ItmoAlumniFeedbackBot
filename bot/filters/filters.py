from aiogram.filters import BaseFilter
from aiogram.types import Message

class EmailTypeFilter(BaseFilter):
    async def __call__(self, message: Message) -> bool | dict[str: str]:
        if message.entities:
            for item in message.entities:
                if item.type == 'email':
                    return {'email': item.extract_from(message.text)}
            return False
        return False