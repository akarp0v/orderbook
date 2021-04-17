from pprint import pprint

from .order_object import OrderObject, Ask, Bid
from .utils import bin_insert, find_position, format_market_data


class BookHandler:
    @staticmethod
    def set_object(obj: OrderObject, in_array: list):
        bin_insert(obj, in_array)

    @staticmethod
    def get_object(by_id: int, from_array: list):
        if not isinstance(by_id, int) or isinstance(by_id, bool):
            raise ValueError('<id> must be Integer')
        if by_id <= 0:
            raise ValueError('<id> must be bigger than Zero')

        position = find_position(by_id, from_array)
        if position is None:
            print(f'#{by_id} is not exist')
            return

        obj = from_array[position]
        print(f'{obj.__class__.__name__} #{obj.id} info: price={obj.price}, quantity={obj.quantity}')

        return obj

    @staticmethod
    def del_object(by_id: int, from_array: list):
        if not isinstance(by_id, int) or isinstance(by_id, bool):
            raise ValueError('<id> must be Integer')
        if by_id <= 0:
            raise ValueError('<id> must be bigger than Zero')

        position = find_position(by_id, from_array)
        if position is None:
            print(f'#{by_id} is not exist')
            return

        return from_array.pop(position)


class OrderBook(BookHandler):
    def __init__(self):
        self._ask_id = 0
        self._bid_id = 0
        self._asks = []
        self._bids = []

    @property
    def ask_id(self):
        return self._ask_id

    @property
    def bid_id(self):
        return self._bid_id

    @property
    def asks(self):
        return self._asks

    @property
    def bids(self):
        return self._bids

    def set_ask(self, price: float, quantity: int) -> int:
        self._ask_id += 1
        ask = Ask()
        ask.id, ask.price, ask.quantity = self._ask_id, price, quantity
        super().set_object(ask, self._asks)

        return ask.id

    def set_bid(self, price: float, quantity: int) -> int:
        self._bid_id += 1
        bid = Bid()
        bid.id, bid.price, bid.quantity = self._bid_id, price, quantity
        super().set_object(bid, self._bids)

        return bid.id

    def get_ask(self, by_id: int):
        return super().get_object(by_id, self._asks)

    def get_bid(self, by_id: int):
        return super().get_object(by_id, self._bids)

    def del_ask(self, by_id: int):
        return super().del_object(by_id, self._asks)

    def del_bid(self, by_id: int):
        return super().del_object(by_id, self._bids)

    def report_market_data(self) -> dict:
        market_data = {
            **{"asks": format_market_data(self._asks)},
            **{"bids": format_market_data(self._bids)}
        }
        pprint(market_data)

        return market_data
