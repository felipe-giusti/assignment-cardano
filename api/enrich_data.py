import aiohttp, asyncio
import pandas as pd
from api.repo import gleif_api
from api.services.enrich_service import get_transaction_costs



async def _process_row(session, row):
    lei = row['lei']

    gleif_dto = await gleif_api.fetch_with_lei(session, lei)

    row['legalName'] = gleif_dto.legal_name
    row['bic'] = gleif_dto.bic

    notional = row['notional']
    rate = row['rate']

    # On the assignment there were two columns mentioned, "transaction_costs" and "transactions_costs".
    # I'm assuming that is a typing error
    row['transaction_costs'] = get_transaction_costs(notional, rate, gleif_dto.country_code)
    
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

