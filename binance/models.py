from typing import Dict, Any, List

from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorDatabase


class DepthUpdateModel:

    def __init__(
            self,
            collection: AsyncIOMotorDatabase,
            e: str = None,
            E: int = None,
            s: str = None,
            U: int = None,
            u: int = None,
            b: List[List[str, str]] = None,
            a: List[List[str, str]] = None,
            _id: str = None,
    ) -> None:
        self.__collection = collection
        self.e = e  # Event type
        self.E = E  # Event time
        self.s = s  # Symbol
        self.U = U  # First update ID in event
        self.u = u  # Final update ID in event
        self.b = b  # Bids to be updated [[Price level to be updated, Quantity]]
        self.a = a  # Asks to be updated [[Price level to be updated, Quantity]]

    async def get(self, _id: str, ):
        document = await self.__collection.cars.find_one(
            {'_id': ObjectId(_id)}
        )
        return document

    def to_dict(self) -> Dict[str, Any]:
        return {
            'event_type': self.e,
            'event_time': self.E,
            'symbol': self.s,
            'first_update_id': self.U,
            'final_update_id': self.u,
            'bids': self.b,
            'asks': self.a,
        }

    async def delete(self, _id):
        await self.__collection.cars.delete_one({'_id': ObjectId(_id)})
