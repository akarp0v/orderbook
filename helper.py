from order_book import OrderBook


class Helper:
    @staticmethod
    def try_to_set_ask(book: OrderBook, price: float, quantity: int) -> str:
        try:
            book.set_ask(price, quantity)
        except ValueError as err:
            return err.__str__()
        except Exception as exp:
            return exp.__str__()

    @staticmethod
    def try_to_set_bid(book: OrderBook, price: float, quantity: int) -> str:
        try:
            book.set_bid(price, quantity)
        except ValueError as err:
            return err.__str__()
        except Exception as exp:
            return exp.__str__()

    @staticmethod
    def try_to_get_ask(book: OrderBook, ask_id: int) -> str:
        try:
            book.get_ask(ask_id)
        except ValueError as err:
            return err.__str__()
        except Exception as exp:
            return exp.__str__()

    @staticmethod
    def try_to_get_bid(book: OrderBook, bid_id: int) -> str:
        try:
            book.get_bid(bid_id)
        except ValueError as err:
            return err.__str__()
        except Exception as exp:
            return exp.__str__()

    @staticmethod
    def try_to_del_ask(book: OrderBook, ask_id: int) -> str:
        try:
            book.del_ask(ask_id)
        except ValueError as err:
            return err.__str__()
        except Exception as exp:
            return exp.__str__()

    @staticmethod
    def try_to_del_bid(book: OrderBook, bid_id: int) -> str:
        try:
            book.del_bid(bid_id)
        except ValueError as err:
            return err.__str__()
        except Exception as exp:
            return exp.__str__()

    @staticmethod
    def is_sorted_by_price(objects: list) -> bool:
        for i in range(len(objects)-1):
            if objects[i]['price'] > objects[i+1]['price']:
                return False
        else:
            return True
