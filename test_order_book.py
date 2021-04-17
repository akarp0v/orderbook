import pytest
from random import randint, random
from sys import maxsize, float_info

from order_book import Ask, Bid
from const import Errors as Err


POSITIVE_SET_GET_DEL_SUIT = [
    (0.005, 1),  # проверка округления цены до 0.01
    (0.01, 1),  # проверка минимальной цены и количества
    (10., maxsize),  # проверка максимального количества
    (float_info.max, 9),  # проверка максимальной цены
    (55.5, 50),  # проверка средних значений в диапазоне до 100
    (99999.99, 99999),  # проверка предельных значений в диапазоне до 100000
    (9999, 999)  # проверка целых значений
]


@pytest.mark.ask
@pytest.mark.positive
@pytest.mark.parametrize("price, quantity",
                         POSITIVE_SET_GET_DEL_SUIT)
def test_set_get_ask_positive(h, order_book, price, quantity):
    # arrange
    book = order_book

    # act
    ask_id = book.set_ask(price, quantity)
    ask = book.get_ask(ask_id)
    market_data = book.report_market_data()
    asks = market_data['asks']

    # assert
    assert isinstance(ask, Ask)
    assert ask_id == ask.id
    assert len(asks) == 1
    assert (asks[0]['price'], asks[0]['quantity']) == (ask.price, ask.quantity)


@pytest.mark.bid
@pytest.mark.positive
@pytest.mark.parametrize("price, quantity",
                         POSITIVE_SET_GET_DEL_SUIT)
def test_set_get_bid_positive(h, order_book, price, quantity):
    # arrange
    book = order_book

    # act
    bid_id = book.set_bid(price, quantity)
    bid = book.get_bid(bid_id)
    market_data = book.report_market_data()
    bids = market_data['bids']

    # assert
    assert isinstance(bid, Bid)
    assert bid_id == bid.id
    assert len(bids) == 1
    assert (bids[0]['price'], bids[0]['quantity']) == (bid.price, bid.quantity)


@pytest.mark.ask
@pytest.mark.positive
@pytest.mark.parametrize("price, quantity",
                         POSITIVE_SET_GET_DEL_SUIT)
def test_del_ask_positive(order_book, price, quantity):
    # arrange
    book = order_book

    # act
    ask_id = book.set_ask(price, quantity)
    ask = book.get_ask(ask_id)
    deleted_ask = book.del_ask(ask_id)
    market_data = book.report_market_data()
    asks = market_data['asks']

    # assert
    assert isinstance(deleted_ask, Ask)
    assert deleted_ask.id == ask.id
    assert book.get_ask(ask_id) is None
    assert len(asks) == 0


@pytest.mark.bid
@pytest.mark.positive
@pytest.mark.parametrize("price, quantity",
                         POSITIVE_SET_GET_DEL_SUIT)
def test_del_bid_positive(order_book, price, quantity):
    # arrange
    book = order_book

    # act
    bid_id = book.set_bid(price, quantity)
    bid = book.get_bid(bid_id)
    deleted_bid = book.del_bid(bid_id)
    market_data = book.report_market_data()
    bids = market_data['bids']

    # assert
    assert isinstance(deleted_bid, Bid)
    assert deleted_bid.id == bid.id
    assert book.get_bid(bid_id) is None
    assert len(bids) == 0


POSITIVE_DOUBLE_SET_SUIT = [(99.99, 99)]  # цена и количество в диапазоне до 100 для повторяющихся заявок


@pytest.mark.ask
@pytest.mark.positive
@pytest.mark.parametrize("price, quantity",
                         POSITIVE_DOUBLE_SET_SUIT)
def test_double_ask_positive(order_book, price, quantity):
    # arrange
    book = order_book

    # act
    ask_id = book.set_ask(price, quantity)
    book.set_ask(price, quantity)
    ask = book.get_ask(ask_id)
    market_data = book.report_market_data()
    asks = market_data['asks']

    # assert
    assert len(asks) == 1
    assert ask.price == price
    assert ask.quantity == quantity * 2


@pytest.mark.bid
@pytest.mark.positive
@pytest.mark.parametrize("price, quantity",
                         POSITIVE_DOUBLE_SET_SUIT)
def test_double_bid_positive(order_book, price, quantity):
    # arrange
    book = order_book

    # act
    bid_id = book.set_bid(price, quantity)
    book.set_bid(price, quantity)
    bid = book.get_bid(bid_id)
    market_data = book.report_market_data()
    bids = market_data['bids']

    # assert
    assert len(bids) == 1
    assert bid.price == price
    assert bid.quantity == quantity * 2


# генерируем массив случайных пар значений {"price": float, "quantity": integer}
POSITIVE_MARKET_DATA_SUIT = [
    {"price": random() * 100, "quantity": randint(1, 1000)}
    for i in range(100)
]


@pytest.mark.report
@pytest.mark.positive
@pytest.mark.parametrize("order_objects",
                         [POSITIVE_MARKET_DATA_SUIT])
def test_is_market_data_sorted(h, order_book, order_objects):
    # arrange
    book = order_book

    # act
    for obj in order_objects:
        price = obj['price']
        quantity = obj['quantity']
        book.set_ask(price, quantity)
        book.set_bid(price, quantity)

    market_data = book.report_market_data()
    asks = market_data['asks']
    bids = market_data['bids']

    # assert
    assert h.is_sorted_by_price(asks)
    assert h.is_sorted_by_price(bids)
    assert asks == bids


NEGATIVE_GET_DEL_SUIT = [
    (True, Err.ID_TYPE),  # попытка передать в ID значение типа bool
    ('', Err.ID_TYPE),  # попытка передать в ID пустую строку
    (' ', Err.ID_TYPE),  # попытка передать в ID пробел
    ("1", Err.ID_TYPE),  # попытка передать в ID строку
    (b"1", Err.ID_TYPE),  # попытка передать в ID значение типа bytes
    (1j, Err.ID_TYPE),  # попытка передать в ID значение типа complex
    (None, Err.ID_TYPE),  # попытка передать в ID пустое значение None
    ([], Err.ID_TYPE),  # попытка передать в ID пустой list
    ({}, Err.ID_TYPE),  # попытка передать в ID пустой dict
    ((), Err.ID_TYPE),  # попытка передать в ID пустой tuple
    (1., Err.ID_TYPE),  # попытка передать в ID значение типа float
    (0, Err.ID_ZERO),  # попытка передать в ID ноль
    (-1, Err.ID_ZERO),  # попытка передать в ID отрицательное значение типа integer
    (-1 * maxsize, Err.ID_ZERO),  # попытка передать в ID отрицательное значение max integer
    (1, None),  # попытка передать несуществующий ID (положительное значение типа integer)
    (maxsize, None)  # попытка передать несуществующий ID (положительное значение max integer)
]


@pytest.mark.ask
@pytest.mark.negative
@pytest.mark.parametrize("ask_id, expect",
                         NEGATIVE_GET_DEL_SUIT)
def test_get_ask_negative(h, order_book, ask_id, expect):
    # arrange
    book = order_book

    # act
    exception = h.try_to_get_ask(book, ask_id)

    # assert
    assert exception == expect


@pytest.mark.bid
@pytest.mark.negative
@pytest.mark.parametrize("bid_id, expect",
                         NEGATIVE_GET_DEL_SUIT)
def test_get_bid_negative(h, order_book, bid_id, expect):
    # arrange
    book = order_book

    # act
    exception = h.try_to_get_bid(book, bid_id)

    # assert
    assert exception == expect


NEGATIVE_SET_SUIT = [
    # quantity
    (100., 1., Err.QUANTITY_TYPE),  # попытка передать в Quantity значение типа float
    (5, True, Err.QUANTITY_TYPE),  # попытка передать в Quantity значение типа bool
    (1, '', Err.QUANTITY_TYPE),  # попытка передать в Quantity пустую строку
    (0.1, ' ', Err.QUANTITY_TYPE),  # попытка передать в Quantity пробел
    (0.99, '1', Err.QUANTITY_TYPE),  # попытка передать в Quantity строку
    (99.99, b'1', Err.QUANTITY_TYPE),  # попытка передать в Quantity значение типа bytes
    (99, 1j, Err.QUANTITY_TYPE),  # попытка передать в Quantity значение типа complex
    (0.55, [], Err.QUANTITY_TYPE),  # попытка передать в Quantity пустой list
    (0.01, (), Err.QUANTITY_TYPE),  # попытка передать в Quantity пустой tuple
    (1000000.01, {}, Err.QUANTITY_TYPE),  # попытка передать в Quantity пустой dict
    (5.4, None, Err.QUANTITY_TYPE),  # попытка передать в Quantity пустое значение None
    (10.5, 0, Err.QUANTITY_ZERO),  # попытка передать в Quantity ноль
    (11.11, -1, Err.QUANTITY_ZERO),  # попытка передать в Quantity отрицательное значение типа integer
    (9999.9, -1 * maxsize, Err.QUANTITY_ZERO),  # попытка передать в Quantity отрицательное значение max integer
    # price
    (True, 7, Err.PRICE_TYPE),  # попытка передать в Price значение типа bool
    (None, 1, Err.PRICE_TYPE),  # попытка передать в Price пустое значение None
    ("", 99, Err.PRICE_TYPE),  # попытка передать в Price пустую строку
    (" ", 9999999, Err.PRICE_TYPE),  # попытка передать в Price пробел
    ("1", 1001, Err.PRICE_TYPE),  # попытка передать в Price строку
    (b"1", 100, Err.PRICE_TYPE),  # попытка передать в Price значение типа bytes
    (1j, 77, Err.PRICE_TYPE),  # попытка передать в Price значение типа complex
    ([], 22, Err.PRICE_TYPE),  # попытка передать в Price пустой list
    ((), 9, Err.PRICE_TYPE),  # попытка передать в Price пустой tuple
    ({}, 2, Err.PRICE_TYPE),  # попытка передать в Price пустой dict
    (-0.01, 555, Err.PRICE_ZERO),  # попытка передать в Price отрицательное значение типа float
    (-1 * float_info.max, 999, Err.PRICE_ZERO),  # попытка передать в Price отрицательное значение max float
    (-1, 1000000, Err.PRICE_ZERO),  # попытка передать в Price отрицательное значение типа integer
    (-1 * maxsize, 9999, Err.PRICE_ZERO),  # попытка передать в Price отрицательное значение max integer
    (0.001, 99999, Err.PRICE_ZERO),  # попытка передать в Price значение типа float, которое должно округлится до нуля
    (0, 10, Err.PRICE_ZERO)  # попытка передать в Price ноль
]


@pytest.mark.ask
@pytest.mark.negative
@pytest.mark.parametrize("price, quantity, expect",
                         NEGATIVE_SET_SUIT)
def test_set_ask_negative(h, order_book, price, quantity, expect):
    # arrange
    book = order_book

    # act
    exception = h.try_to_set_ask(book, price, quantity)

    # assert
    assert exception == expect


@pytest.mark.bid
@pytest.mark.negative
@pytest.mark.parametrize("price, quantity, expect",
                         NEGATIVE_SET_SUIT)
def test_set_bid_negative(h, order_book, price, quantity, expect):
    # arrange
    book = order_book

    # act
    exception = h.try_to_set_bid(book, price, quantity)

    # assert
    assert exception == expect


@pytest.mark.ask
@pytest.mark.negative
@pytest.mark.parametrize("ask_id, expect",
                         NEGATIVE_GET_DEL_SUIT)
def test_del_ask_negative(h, order_book, ask_id, expect):
    # arrange
    book = order_book

    # act
    exception = h.try_to_del_ask(book, ask_id)

    # assert
    assert exception == expect


@pytest.mark.bid
@pytest.mark.negative
@pytest.mark.parametrize("bid_id, expect",
                         NEGATIVE_GET_DEL_SUIT)
def test_del_bid_negative(h, order_book, bid_id, expect):
    # arrange
    book = order_book

    # act
    exception = h.try_to_del_bid(book, bid_id)

    # assert
    assert exception == expect
