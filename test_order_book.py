import pytest
from random import randint, random
import sys
from order_book import Ask, Bid
from const import Errors as Err


POSITIVE_SET = [
    (0.005, 1),
    (0.01, 1),
    (10., sys.maxsize),
    (55.5, 105),
    (sys.float_info.max, 5),
    (1000.99, 9999),
    (100, 10)
]


@pytest.mark.ask
@pytest.mark.positive
@pytest.mark.parametrize("price, quantity", POSITIVE_SET)
def test_set_get_del_ask(order_book, price, quantity):
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
@pytest.mark.parametrize("price, quantity", POSITIVE_SET)
def test_set_get_del_bid(order_book, price, quantity):
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


NEGATIVE_SET = [
    # quantity
    (100., 2.5, Err.QUANTITY_TYPE),
    (1, '', Err.QUANTITY_TYPE),
    (0.1, ' ', Err.QUANTITY_TYPE),
    (0.55, [], Err.QUANTITY_TYPE),
    (0.01, (), Err.QUANTITY_TYPE),
    (1000000.01, {}, Err.QUANTITY_TYPE),
    (5.4, None, Err.QUANTITY_TYPE),
    (10.5, 0, Err.QUANTITY_ZERO),
    (10.4, -1, Err.QUANTITY_ZERO),
    # price
    (None, 1, Err.PRICE_TYPE),
    ("", 20, Err.PRICE_TYPE),
    (" ", 2000000, Err.PRICE_TYPE),
    ([], 22, Err.PRICE_TYPE),
    ((), 9, Err.PRICE_TYPE),
    ({}, 2, Err.PRICE_TYPE),
    (-1, 5, Err.PRICE_ZERO),
    (0.001, 999, Err.PRICE_ZERO),
    (0, 999, Err.PRICE_ZERO)
]


@pytest.mark.ask
@pytest.mark.negative
@pytest.mark.parametrize("price, quantity, expect", NEGATIVE_SET)
def test_ask_price_quantity(h, order_book, price, quantity, expect):
    book = order_book
    # get error
    response = h.try_to_set_ask(book, price, quantity)

    assert response == expect


@pytest.mark.bid
@pytest.mark.negative
@pytest.mark.parametrize("price, quantity, expect", NEGATIVE_SET)
def test_bid_price_quantity(h, order_book, price, quantity, expect):
    book = order_book
    # get error
    response = h.try_to_set_bid(book, price, quantity)

    assert response == expect


DOUBLE_SET = [
    (10.55, 10)
]


@pytest.mark.ask
@pytest.mark.positive
@pytest.mark.parametrize("price, quantity", DOUBLE_SET)
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
@pytest.mark.parametrize("price, quantity", DOUBLE_SET)
def test_double_bid(order_book, price, quantity):
    book = order_book
    # set identical bids
    bid_id = book.set_bid(price, quantity)
    book.set_bid(price, quantity)
    bid = book.get_bid(bid_id)

    assert bid.price == price
    assert bid.quantity == quantity * 2


@pytest.mark.report
@pytest.mark.positive
@pytest.mark.parametrize("order_objects", [
    [{"price": random() * 1000, "quantity": randint(1, 1000)}
     for i in range(100)]
])
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
