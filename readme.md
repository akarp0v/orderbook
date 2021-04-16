## OrderBook - упрощенный биржевой стакан

#### Python | Pytest

Класс обеспечивает следующую функциональность:
1. Постановка заявок в стакан (без логики сведения заявок)
2. Снятие заявок по идентификатору
3. Получение данных заявки по идентификатору
4. Получение снапшота рыночных данных (market data). 
   Данные стакана агрегированы и отсортированы по цене в виде словаря следующей структуры:
```
{
"asks": [
    {
      "price": <value>,
      "quantity": <value>
},
... ],
  "bids": [...]
} 
```

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install dependencies

```
pip install requirements.txt 
```

## Usage

Run all tests using verbose mode
```
pytest -vs
```

Run only marked tests
```
pytest -vm positive
```

## License

[MIT](https://choosealicense.com/licenses/mit/)
