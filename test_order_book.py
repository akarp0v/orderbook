import pytest
from random import randint, random
from sys import maxsize, float_info

from order_book import Ask, Bid
from const import Errors as Err


POSITIVE_SET_GET_DEL_SUIT = [
    (0.005, 1),
    (0.01, 1),
    (10., maxsize),
    (55.5, 100),
    (float_info.max, 9),
    (10000.99, 99999),
    (100, 10)
]


@pytest.mark.ask
@pytest.mark.positive
@pytest.mark.parametrize("price, quantity",
                         POSITIVE_SET_GET_DEL_SUIT)
def test_set_get_ask_positive(h, order_book, price, quantity):
    book = order_book

    # set ask
    ask_id = book.set_ask(price, quantity)
    # get ask
    ask = book.get_ask(ask_id)
    # get market_data
    market_data = book.report_market_data()
    asks = market_data['asks']

    assert isinstance(ask, Ask)
    assert ask_id == ask.id
    assert len(asks) == 1
    assert (asks[0]['price'], asks[0]['quantity']) == (ask.price, ask.quantity)


@pytest.mark.bid
@pytest.mark.positive
@pytest.mark.parametrize("price, quantity",
                         POSITIVE_SET_GET_DEL_SUIT)
def test_set_get_bid_positive(h, order_book, price, quantity):
    book = order_book

    # set bid
    bid_id = book.set_bid(price, quantity)
    # get bid
    bid = book.get_bid(bid_id)
    # get market_data
    market_data = book.report_market_data()
    bids = market_data['bids']

    assert isinstance(bid, Bid)
    assert bid_id == bid.id
    assert len(bids) == 1
    assert (bids[0]['price'], bids[0]['quantity']) == (bid.price, bid.quantity)


@pytest.mark.ask
@pytest.mark.positive
@pytest.mark.parametrize("price, quantity",
                         POSITIVE_SET_GET_DEL_SUIT)
def test_del_ask_positive(order_book, price, quantity):
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
@pytest.mark.parametrize("price, quantity",
                         POSITIVE_SET_GET_DEL_SUIT)
def test_del_bid_positive(order_book, price, quantity):
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


POSITIVE_DOUBLE_SET_SUIT = [(99.99, 99)]


@pytest.mark.ask
@pytest.mark.positive
@pytest.mark.parametrize("price, quantity",
                         POSITIVE_DOUBLE_SET_SUIT)
def test_double_ask_positive(order_book, price, quantity):
    book = order_book

    # set identical asks
    ask_id = book.set_ask(price, quantity)
    book.set_ask(price, quantity)
    ask = book.get_ask(ask_id)
    # get market_data
    market_data = book.report_market_data()
    asks = market_data['asks']

    assert len(asks) == 1
    assert ask.price == price
    assert ask.quantity == quantity * 2


@pytest.mark.bid
@pytest.mark.positive
@pytest.mark.parametrize("price, quantity",
                         POSITIVE_DOUBLE_SET_SUIT)
def test_double_bid_positive(order_book, price, quantity):
    book = order_book

    # set identical bids
    bid_id = book.set_bid(price, quantity)
    book.set_bid(price, quantity)
    bid = book.get_bid(bid_id)
    # get market_data
    market_data = book.report_market_data()
    bids = market_data['bids']

    assert len(bids) == 1
    assert bid.price == price
    assert bid.quantity == quantity * 2


POSITIVE_MARKET_DATA_SUIT = [
    {"price": random() * 100, "quantity": randint(1, 1000)}
    for i in range(100)
]


@pytest.mark.report
@pytest.mark.positive
@pytest.mark.parametrize("order_objects",
                         [POSITIVE_MARKET_DATA_SUIT])
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


NEGATIVE_GET_DEL_SUIT = [
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
    (-1 * maxsize, Err.ID_ZERO),
    (1, None),
    (maxsize, None)
]


@pytest.mark.ask
@pytest.mark.negative
@pytest.mark.parametrize("ask_id, expect",
                         NEGATIVE_GET_DEL_SUIT)
def test_get_ask_negative(h, order_book, ask_id, expect):
    book = order_book
    exception = h.try_to_get_ask(book, ask_id)

    assert exception == expect


@pytest.mark.bid
@pytest.mark.negative
@pytest.mark.parametrize("bid_id, expect",
                         NEGATIVE_GET_DEL_SUIT)
def test_get_bid_negative(h, order_book, bid_id, expect):
    book = order_book
    exception = h.try_to_get_bid(book, bid_id)

    assert exception == expect


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
    (9999.9, -1 * maxsize, Err.QUANTITY_ZERO),
    # price
    (True, 7, Err.PRICE_TYPE),
    (None, 1, Err.PRICE_TYPE),
    ("", 99, Err.PRICE_TYPE),
    (" ", 9999999, Err.PRICE_TYPE),
    ("1", 1001, Err.PRICE_TYPE),
    (b"1", 100, Err.PRICE_TYPE),
    (1j, 77, Err.PRICE_TYPE),
    ([], 22, Err.PRICE_TYPE),
    ((), 9, Err.PRICE_TYPE),
    ({}, 2, Err.PRICE_TYPE),
    (-1., 555, Err.PRICE_ZERO),
    (-1 * float_info.max, 999, Err.PRICE_ZERO),
    (0.001, 99999, Err.PRICE_ZERO),
    (0, 10, Err.PRICE_ZERO)
]


@pytest.mark.ask
@pytest.mark.negative
@pytest.mark.parametrize("price, quantity, expect",
                         NEGATIVE_SET_SUIT)
def test_set_ask_negative(h, order_book, price, quantity, expect):
    book = order_book
    exception = h.try_to_set_ask(book, price, quantity)

    assert exception == expect


@pytest.mark.bid
@pytest.mark.negative
@pytest.mark.parametrize("price, quantity, expect",
                         NEGATIVE_SET_SUIT)
def test_set_bid_negative(h, order_book, price, quantity, expect):
    book = order_book
    exception = h.try_to_set_bid(book, price, quantity)

    assert exception == expect


@pytest.mark.ask
@pytest.mark.negative
@pytest.mark.parametrize("ask_id, expect",
                         NEGATIVE_GET_DEL_SUIT)
def test_del_ask_negative(h, order_book, ask_id, expect):
    book = order_book
    exception = h.try_to_del_ask(book, ask_id)

    assert exception == expect


@pytest.mark.bid
@pytest.mark.negative
@pytest.mark.parametrize("bid_id, expect",
                         NEGATIVE_GET_DEL_SUIT)
def test_del_bid_negative(h, order_book, bid_id, expect):
    book = order_book
    exception = h.try_to_del_bid(book, bid_id)

    assert exception == expect
