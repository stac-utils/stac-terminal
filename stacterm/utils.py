import pandas as pd
from dateutil.parser import parse
from datetime import datetime

DATE_FIELDS = ['datetime', 'date', 'year', 'year-month']


def items_to_dataframe(item_collection, sort=None):
    _items = []
    for item in item_collection['features']:
        dt = parse(item['properties']['datetime'])
        _items.append({
            "datetime": dt,
            "year": dt.year,
            "year-month": f"{dt.year}-{dt.month}",
            "id": item['id'],
            "collection": item['collection'],
            'timestamp': dt.timestamp(),
            **item['properties']
        })
    
    df = pd.DataFrame(_items)
    df['datetime'] = pd.to_datetime(df['datetime'])
    df['date'] = df['datetime'].apply(datetime.date)
    if sort is not None:
        df.sort_values(sort, inplace=True)

    return df
