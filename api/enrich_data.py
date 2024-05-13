import aiohttp, asyncio
import pandas as pd
from typing import List
from api.repo import gleif_api
from api.repo.transaction_repo import PandasTransactionRepo, TransactionRepo
from api.models.transaction import TransactionModel



async def _process_transaction(session, transaction: TransactionModel) -> TransactionModel:
    lei = transaction.lei

    gleif_dto = await gleif_api.fetch_with_lei(session, lei)

    transaction.legalName = gleif_dto.legal_name
    transaction.bic = gleif_dto.bic

    # On the assignment there were two columns mentioned, "transaction_costs" and "transactions_costs".
    # I'm assuming that is a typing error
    transaction.transaction_costs = transaction.get_transaction_costs(gleif_dto.country_code)
    
    return transaction


async def _process_data(repo: TransactionRepo) -> List[TransactionModel]:
    async with aiohttp.ClientSession() as session:
        tasks = [_process_transaction(session, transaction) for transaction in repo.iterate_all()]
        transactions = await asyncio.gather(*tasks)

        return transactions


# we abstracted all the rest, pandas is only used here
async def enrich_data(data):
    raw_df = pd.read_csv(data)
    repo = PandasTransactionRepo(raw_df)

    transactions = await _process_data(repo)

    processed_df = pd.DataFrame([transaction.row for transaction in transactions])

    csv_data = processed_df.to_csv(index=False)
    return csv_data

