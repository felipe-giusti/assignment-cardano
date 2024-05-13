

class GleifDTO:
    def __init__(self, legal_name, bic, country_code) -> None:
        self.legal_name = legal_name
        self.bic = bic
        self.country_code = country_code

    @classmethod
    def from_response(cls, response):
        # TODO find out later if other indexes in the list are important
        attributes = response.get('data', [{}])[0].get('attributes', {})
        entity = attributes.get('entity', {})

        legal_name = entity.get('legalName', {}).get('name')
        bic = attributes.get('bic')
        country = entity.get('legalAddress', {}).get('country')
        return cls(legal_name, bic, country)



async def fetch_with_lei(session, lei: str) -> GleifDTO:
    url = f'https://api.gleif.org/api/v1/lei-records?filter[lei]={lei}'
    async with session.get(url) as response:
        data = await response.json()
        return GleifDTO.from_response(data)

