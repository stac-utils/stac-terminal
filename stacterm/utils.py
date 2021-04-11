import pandas as pd
from dateutil.parser import parse


def items_to_dataframe(item_collection, sort=None):
    _items = []
    for item in item_collection['features']:
        dt = parse(item['properties']['datetime'])
        _items.append({
            "id": item['id'],
            "collection": item['collection'],
            "date": dt.date(),
            **item['properties']
        })
    df = pd.DataFrame(_items)
    if sort is not None:
        df.sort_values(sort, inplace=True)
    return df