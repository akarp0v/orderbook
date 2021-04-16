import pytest

from order_book import OrderBook
from helper import Helper


@pytest.fixture()
def order_book():
    book = OrderBook()
    yield book
    del book


@pytest.fixture()
def h():
    h = Helper()
    yield h
    del h
