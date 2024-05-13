

async def fetch_with_lei(session, lei):
    url = f'https://api.gleif.org/api/v1/lei-records?filter[lei]={lei}'
    async with session.get(url) as response:
        data = await response.json()
        return data

