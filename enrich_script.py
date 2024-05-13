import aiohttp, asyncio, os
import pandas as pd


async def fetch_with_lei(session, lei):
    url = f'https://api.gleif.org/api/v1/lei-records?filter[lei]={lei}'
    async with session.get(url) as response:
        data = await response.json()
        return data

async def _process_row(session, row):
    lei = row['lei']

    data = await fetch_with_lei(session, lei)

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


async def enrich_data(input_path: str, output_path: str):
    print(f'Starting process for: {input_path}')
    # may change later
    raw_df = pd.read_csv(input_path)

    processed_df = await _process_data(raw_df)

    pd.DataFrame.to_csv(processed_df, output_path)
    print(f'Process finished, output: {output_path}')


async def enrich_directory(in_folder, out_folder):
    files = os.listdir(in_folder)
    
    tasks = []
    for file in files:
        if not file.endswith('.csv'):
            continue
        in_path = os.path.join(in_folder, file)
        out_path = os.path.join(out_folder, f'enriched_{file}')
        tasks.append(enrich_data(in_path, out_path))

    await asyncio.gather(*tasks)


#TODO may be good to add error handling later
if __name__ == "__main__":
    input_folder = './in'
    output_folder = './out'

    os.makedirs(input_folder, exist_ok=True)
    os.makedirs(output_folder, exist_ok=True)
    
    asyncio.run(enrich_directory(input_folder, output_folder))