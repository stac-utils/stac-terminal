import termtables as tt

from .utils import items_to_dataframe


def print_table(items, fields=['date', 'id'], sort=None, style='markdown'):
    _sort = fields[0] if sort is None else sort
    df = items_to_dataframe(items, sort=_sort)
    data = df[fields].values
    tt.print(data, header=fields, style=eval(f"tt.styles.{style}"))