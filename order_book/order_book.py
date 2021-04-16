from pprint import pprint

from .order_object import OrderObject, Ask, Bid


class BookHandler:
    def set_object(self, obj: OrderObject, objects: list):
        self.bin_insert(obj, objects)

    def get_object(self, obj_id: int, obj_type: str, objects: list):
        if not isinstance(obj_id, int) or isinstance(obj_id, bool):
            raise ValueError('<id> must be Integer')

        if obj_id <= 0:
            raise ValueError('<id> must be bigger than Zero')

        position = self.find_position(obj_id, objects)
        if position is None:
            print(f'{obj_type} #{obj_id} is not exist')
            return

        obj = objects[position]
        print(f'{obj_type} #{obj.id} info: price={obj.price}, quantity={obj.quantity}')

        return obj

    def del_object(self, obj_id: int, obj_type: str, objects: list):
        position = self.find_position(obj_id, objects)
        if position is None:
            print(f'{obj_type} #{obj_id} is not exist')
            return

        return objects.pop(position)

    @staticmethod
    def bin_insert(obj: OrderObject, in_array: list):
        # поиск позиции для вставки элемента в массив
        # с помощью алгоритма приближенного бинарного поиска
        price = obj.price
        low, mid = 0, 0  # нижний (начальный) индекс
        high = len(in_array) - 1  # верхний (конечный) индекс
        # как только нижний индекс станет больше на 1 верхнего
        # или верхний на 1 меньше нижнего цикл остановится
        while low <= high:
            # находится индекс середины массива или отрезка массива
            mid = (low + high) // 2
            # Если искомое число меньше числа с индексом середины
            if price < in_array[mid].price:
                # то верхняя граница сдвигается к середине
                high = mid - 1
            # Если искомое число больше числа с индексом середины
            elif price > in_array[mid].price:
                # то нижняя граница сдвигается за середину
                low = mid + 1
            # Все остальные случаи возникают, когда искомое число
            # равно числу с индексом mid, т.е. оно есть в массиве и найдено
            else:
                in_array[mid].quantity += obj.quantity
                return
        else:
            if low >= len(in_array):
                in_array.insert(low, obj)
                return
            if high < 0:
                in_array.insert(0, obj)
                return
            pos = mid+1 if in_array[mid].price < price else mid
            in_array.insert(pos, obj)

    @staticmethod
    def find_position(by_id: int, in_array: list):
        for obj in in_array:
            if obj.id == by_id:
                return in_array.index(obj)


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

    def get_ask(self, ask_id: int):
        return super().get_object(ask_id, 'Ask', self._asks)

    def get_bid(self, bid_id: int):
        return super().get_object(bid_id, 'Bid', self._bids)

    def del_ask(self, ask_id: int):
        return super().del_object(ask_id, 'Ask', self._asks)

    def del_bid(self, bid_id: int):
        return super().del_object(bid_id, 'Bid', self._bids)

    def report_market_data(self) -> dict:
        asks = {"asks": self.format_market_data(self._asks)}
        bids = {"bids": self.format_market_data(self._bids)}
        market_data = {**asks, **bids}
        pprint(market_data)

        return market_data

    @staticmethod
    def format_market_data(array: list) -> list:
        return [{"price": elem.price, "quantity": elem.quantity} for elem in array]
