from .order_object import OrderObject


# поиск позиции для вставки элемента в массив
# с помощью алгоритма приближенного бинарного поиска
def bin_insert(obj: OrderObject, in_array: list) -> None:
    price = obj.price
    low = 0  # нижний (начальный) индекс
    mid = 0
    high = len(in_array) - 1  # верхний (конечный) индекс
    while low <= high:
        mid = (low + high) // 2
        if price < in_array[mid].price:
            high = mid - 1
        elif price > in_array[mid].price:
            low = mid + 1
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
        pos = mid + 1 if in_array[mid].price < price else mid
        in_array.insert(pos, obj)


def find_position(by_id: int, in_array: list) -> int:
    for obj in in_array:
        if obj.id == by_id:
            return in_array.index(obj)


def format_market_data(in_array: list) -> list:
    return [{"price": elem.price, "quantity": elem.quantity} for elem in in_array]
