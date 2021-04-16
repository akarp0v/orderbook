import pytest
from random import randint, random
import sys
from order_book import Ask, Bid
from const import Errors as Err


@pytest.mark.positive
@pytest.mark.parametrize("price, quantity", [
    (0.005, 1),
    (0.01, 1),
    (10., sys.maxsize),
    (55.5, 105),
    (sys.float_info.max, 5),
    (1000.99, 9999),
    (100, 10)
])
def test_set_get_del_ask(order_book, price, quantity):
    book = order_book

    ask_id = book.set_ask(price, quantity)
    ask = book.get_ask(ask_id)
    assert isinstance(ask, Ask)
    assert ask.id == ask_id

    deleted_ask = book.del_ask(ask_id)
    assert isinstance(deleted_ask, Ask)
    assert deleted_ask.id == ask_id

    assert book.get_ask(ask_id) is None


@pytest.mark.positive
@pytest.mark.parametrize("price, quantity", [
    (0.005, 1),
    (0.01, 1),
    (10., sys.maxsize),
    (55.555, 105),
    (sys.float_info.max, 5),
    (1000.99, 9999),
    (100, 10)
])
def test_set_get_del_bid(order_book, price, quantity):
    book = order_book
    bid_id = book.set_bid(price, quantity)
    bid = book.get_bid(bid_id)
    assert isinstance(bid, Bid)
    assert bid.id == bid_id

    deleted_bid = book.del_bid(bid_id)
    assert isinstance(deleted_bid, Bid)
    assert deleted_bid.id == bid_id

    assert book.get_bid(bid_id) is None


@pytest.mark.positive
@pytest.mark.parametrize("order_objects", [
    ([{"price": random() * 1000, "quantity": randint(1, 1000)}
      for i in range(100)])
])
def test_is_market_data_sorted(h, order_book, order_objects):
    book = order_book
    for obj in order_objects:
        price = obj['price']
        quantity = obj['quantity']
        book.set_ask(price, quantity)
        book.set_bid(price, quantity)

    market_data = book.report_market_data()
    asks = market_data['asks']
    bids = market_data['bids']

    assert h.is_sorted_by_price(asks)
    assert h.is_sorted_by_price(bids)
    assert asks == bids


@pytest.mark.negative
@pytest.mark.parametrize("price, quantity, expects", [
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
])
def test_price_quantity_prop(h, order_book, price, quantity, expects):
    book = order_book
    response = h.try_to_set_ask(book, price, quantity)
    assert expects == response
