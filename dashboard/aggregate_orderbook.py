import math
from decimal import Decimal
import pandas as pd


def aggregate_levels(levels_df, agg_level=Decimal('0.1'), side='bids'):
    min_level = math.floor(Decimal(min(levels_df.price)) / agg_level - 1) * agg_level
    max_level = math.ceil(Decimal(max(levels_df.price)) / agg_level + 1) * agg_level
    if side == 'bids':
        right = False
        label_func = lambda x: x.right
    elif side == 'asks':
        right = False
        label_func = lambda x: x.left

    level_bounds = [
       float(min_level + agg_level * x) for x in range(int((max_level - min_level) / agg_level) + 1)
    ]
    levels_df['bin'] = pd.cut(levels_df.price, bins=level_bounds, precision=10, right=right)

    levels_df = levels_df.groupby('bin', observed=False).agg(
        quantity=('quantity', 'sum')
    ).reset_index()

    levels_df['price'] = levels_df.bin.apply(label_func)
    levels_df = levels_df[levels_df.quantity > 0]
    levels_df = levels_df[['price', 'quantity']]
    return levels_df
