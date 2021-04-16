from .validator import IntValidator, FloatValidator


class OrderObject:
    id = IntValidator()
    price = FloatValidator()
    quantity = IntValidator()


class Ask(OrderObject):
    pass


class Bid(OrderObject):
    pass
