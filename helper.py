from order_book import OrderBook


class Helper:
    @staticmethod
    def try_to_set_ask(book: OrderBook, price: float, quantity: int):
        try:
            book.set_ask(price, quantity)
        except ValueError as err:
            return err.args[0]

    @staticmethod
    def is_sorted_by_price(objects: list) -> bool:
        for i in range(len(objects)-1):
            if objects[i]['price'] > objects[i+1]['price']:
                return False
        else:
            return True
