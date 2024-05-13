import aiohttp, asyncio, os, sys
import pandas as pd
import api.config as config
from api.repo import gleif_api



async def _process_row(session, row):
    lei = row['lei']

    data = await gleif_api.fetch_with_lei(session, lei)

    # TODO find out later if other indexes in the list are important
    attributes = data.get('data', [{}])[0].get('attributes', {})
    entity = attributes.get('entity', {})

    row['legalName'] = entity.get('legalName', {}).get('name')
    row['bic'] = attributes.get('bic')


    country = entity.get('legalAddress', {}).get('country')

    notional = row['notional']
    rate = row['rate']

    # On the assignment there were two columns mentioned, "transaction_costs" and "transactions_costs".
    # I'm assuming that is a typing error
    if country == 'GB':
        row['transaction_costs'] = (notional*rate) - notional
    elif country == 'NL':
        row['transaction_costs'] = abs((notional*(1/rate) - notional))
    else:
        row['transaction_costs'] = None

    return row


async def _process_data(df: pd.DataFrame) -> pd.DataFrame:
    async with aiohttp.ClientSession() as session:
        tasks = [_process_row(session, row) for _, row in df.iterrows()]
        results = await asyncio.gather(*tasks)

        processed_df = pd.DataFrame(results)
        return processed_df


async def enrich_data(data):
    # may change later
    raw_df = pd.read_csv(data)

    processed_df = await _process_data(raw_df)

    return processed_df
    # pd.DataFrame.to_csv(processed_df, output_path)

