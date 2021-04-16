import pytest
from random import randint, random
import sys

from order_book import Ask, Bid
from const import Errors as Err


NEGATIVE_GET_SUIT = [
    (True, Err.ID_TYPE),
    ('', Err.ID_TYPE),
    (' ', Err.ID_TYPE),
    ("1", Err.ID_TYPE),
    (b"1", Err.ID_TYPE),
    (1j, Err.ID_TYPE),
    (None, Err.ID_TYPE),
    ([], Err.ID_TYPE),
    ({}, Err.ID_TYPE),
    ((), Err.ID_TYPE),
    (1., Err.ID_TYPE),
    (0, Err.ID_ZERO),
    (-1, Err.ID_ZERO),
    (-1 * sys.maxsize, Err.ID_ZERO),
    (1, None),
    (sys.maxsize, None)
]


@pytest.mark.ask
@pytest.mark.negative
@pytest.mark.parametrize("ask_id, expect", NEGATIVE_GET_SUIT)
def test_set_get_ask(h, order_book, ask_id, expect):
    book = order_book
    response = h.try_to_get_ask(book, ask_id)

    assert response == expect


@pytest.mark.bid
@pytest.mark.negative
@pytest.mark.parametrize("bid_id, expect", NEGATIVE_GET_SUIT)
def test_set_get_bid(h, order_book, bid_id, expect):
    book = order_book
    response = h.try_to_get_bid(book, bid_id)

    assert response == expect


NEGATIVE_SET_SUIT = [
    # quantity
    (100., 1., Err.QUANTITY_TYPE),
    (5, True, Err.QUANTITY_TYPE),
    (1, '', Err.QUANTITY_TYPE),
    (0.1, ' ', Err.QUANTITY_TYPE),
    (0.99, '1', Err.QUANTITY_TYPE),
    (99.99, b'1', Err.QUANTITY_TYPE),
    (99, 1j, Err.QUANTITY_TYPE),
    (0.55, [], Err.QUANTITY_TYPE),
    (0.01, (), Err.QUANTITY_TYPE),
    (1000000.01, {}, Err.QUANTITY_TYPE),
    (5.4, None, Err.QUANTITY_TYPE),
    (10.5, 0, Err.QUANTITY_ZERO),
    (11.11, -1, Err.QUANTITY_ZERO),
    (9999.9, -1 * sys.maxsize, Err.QUANTITY_ZERO),
    # price
    (True, 7, Err.PRICE_TYPE),
    (None, 1, Err.PRICE_TYPE),
    ("", 20, Err.PRICE_TYPE),
    (" ", 2000000, Err.PRICE_TYPE),
    ("1", 1001, Err.PRICE_TYPE),
    (b"1", 100, Err.PRICE_TYPE),
    (1j, 77, Err.PRICE_TYPE),
    ([], 22, Err.PRICE_TYPE),
    ((), 9, Err.PRICE_TYPE),
    ({}, 2, Err.PRICE_TYPE),
    (-1., 5, Err.PRICE_ZERO),
    (-1 * sys.float_info.max, 5, Err.PRICE_ZERO),
    (0.001, 999, Err.PRICE_ZERO),
    (0, 10, Err.PRICE_ZERO)
]


@pytest.mark.ask
@pytest.mark.negative
@pytest.mark.parametrize("price, quantity, expect", NEGATIVE_SET_SUIT)
def test_ask_price_quantity(h, order_book, price, quantity, expect):
    book = order_book

    # get error
    response = h.try_to_set_ask(book, price, quantity)

    assert response == expect


@pytest.mark.bid
@pytest.mark.negative
@pytest.mark.parametrize("price, quantity, expect", NEGATIVE_SET_SUIT)
def test_bid_price_quantity(h, order_book, price, quantity, expect):
    book = order_book

    # get error
    response = h.try_to_set_bid(book, price, quantity)

    assert response == expect


POSITIVE_DEL_SUIT = [
    (0.005, 1),
    (0.01, 1),
    (10., sys.maxsize),
    (55.5, 100),
    (sys.float_info.max, 9),
    (10000.99, 99999),
    (100, 10)
]


@pytest.mark.ask
@pytest.mark.positive
@pytest.mark.parametrize("price, quantity", POSITIVE_DEL_SUIT)
def test_del_ask(order_book, price, quantity):
    book = order_book

    # set ask
    ask_id = book.set_ask(price, quantity)
    # get ask
    ask = book.get_ask(ask_id)
    assert isinstance(ask, Ask)
    assert ask.id == ask_id
    # delete ask
    deleted_ask = book.del_ask(ask_id)
    assert isinstance(deleted_ask, Ask)
    assert deleted_ask.id == ask_id

    assert book.get_ask(ask_id) is None


@pytest.mark.bid
@pytest.mark.positive
@pytest.mark.parametrize("price, quantity", POSITIVE_DEL_SUIT)
def test_del_bid(order_book, price, quantity):
    book = order_book

    # set bid
    bid_id = book.set_bid(price, quantity)
    # get bid
    bid = book.get_bid(bid_id)
    assert isinstance(bid, Bid)
    assert bid.id == bid_id
    # delete bid
    deleted_bid = book.del_bid(bid_id)
    assert isinstance(deleted_bid, Bid)
    assert deleted_bid.id == bid_id

    assert book.get_bid(bid_id) is None


DOUBLE_SUIT = [(99.99, 99)]


@pytest.mark.ask
@pytest.mark.positive
@pytest.mark.parametrize("price, quantity", DOUBLE_SUIT)
def test_double_ask(order_book, price, quantity):
    book = order_book

    # set identical asks
    ask_id = book.set_ask(price, quantity)
    book.set_ask(price, quantity)
    ask = book.get_ask(ask_id)

    assert ask.price == price
    assert ask.quantity == quantity * 2


@pytest.mark.bid
@pytest.mark.positive
@pytest.mark.parametrize("price, quantity", DOUBLE_SUIT)
def test_double_bid(order_book, price, quantity):
    book = order_book

    # set identical bids
    bid_id = book.set_bid(price, quantity)
    book.set_bid(price, quantity)
    bid = book.get_bid(bid_id)

    assert bid.price == price
    assert bid.quantity == quantity * 2


MARKET_DATA_SUIT = [{"price": random() * 1000, "quantity": randint(1, 1000)}
                    for i in range(100)]


@pytest.mark.report
@pytest.mark.positive
@pytest.mark.parametrize("order_objects", [MARKET_DATA_SUIT])
def test_is_market_data_sorted(h, order_book, order_objects):
    book = order_book

    # fill asks and bids
    for obj in order_objects:
        price = obj['price']
        quantity = obj['quantity']
        book.set_ask(price, quantity)
        book.set_bid(price, quantity)
    # get market_data
    market_data = book.report_market_data()
    asks = market_data['asks']
    bids = market_data['bids']

    assert h.is_sorted_by_price(asks)
    assert h.is_sorted_by_price(bids)
    assert asks == bids
