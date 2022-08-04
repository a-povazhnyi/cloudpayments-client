import asyncio
from base64 import b64encode
from typing import Type, Optional
from uuid import uuid4

from aiohttp import ClientResponse, TCPConnector
from aiohttp.client_exceptions import ContentTypeError
from marshmallow import Schema, ValidationError

from abstract_client import AbstractInteractionClient, InteractionResponseError
from schemas import CardChargeRequestSchema


class CloudPaymentsClient(AbstractInteractionClient):
    CONNECTOR = TCPConnector()

    REQUEST_TIMEOUT = None
    CONNECT_TIMEOUT = None

    SERVICE = 'CloudPayments'
    BASE_URL = 'https://api.cloudpayments.ru/payments/cards/'
    CHARGE_URL = 'charge'

    def __init__(self, public_id: str, api_secret: str):
        self._public_id = public_id
        self._api_secret = api_secret
        super().__init__()

    def get_public_id(self) -> str:
        return self._public_id

    def get_api_secret(self) -> str:
        return self._api_secret

    @staticmethod
    def _get_x_request_id_header() -> dict:
        return {'X-Request-ID': str(uuid4())}

    @staticmethod
    def _encode_auth_credentials(login: str, password: str) -> str:
        """HTTP basic access authentication encode"""
        return b64encode(bytes(f'{login}:{password}', 'ascii')).decode('ascii')

    def _get_base_auth_header(self) -> dict:
        encoded_credentials = self._encode_auth_credentials(
            login=self._public_id,
            password=self._api_secret
        )
        return {'Authentication': f'Basic {encoded_credentials}'}

    def _get_common_headers(self) -> dict:
        return self._get_x_request_id_header() | self._get_base_auth_header()

    def _make_headers(self, new_headers: Optional[dict] = None) -> dict:
        headers = self._get_common_headers()
        if new_headers:
            headers.update(new_headers)
        return headers

    def validate_data(self, schema: Type[Schema], data: dict) -> None:
        try:
            schema().load(data)
        except ValidationError as exc:
            self._handle_validation_error(exc)

    async def charge(self, request_data: dict):
        self.validate_data(schema=CardChargeRequestSchema, data=request_data)
        url = self.endpoint_url(relative_url=self.CHARGE_URL)
        headers = self._make_headers()
        return await self.post(interaction_method='charge',
                               url=url,
                               headers=headers,
                               data=request_data)

    def _handle_validation_error(self, exc):
        raise exc

    async def _handle_response_error(self, response: ClientResponse) -> None:
        try:
            response_json = await response.json()
            raise InteractionResponseError(
                status_code=response.status,
                method=response.method,
                service=self.SERVICE,
                response_status=response_json.get('Status'),
                message=response_json.get('Message')
            )
        except ContentTypeError:
            await super()._handle_response_error(response)


async def test():
    public_id = 'pk_71efb26a18397ec61b755221123cc'
    api_secret = '0ddb459b-e71e-43be-97a9-bcf1297fb5f9'
    charge_request_data = {
        'Amount': '0.8',
        'Currency': 'RUB',
        'IpAddress': '0.0.0.0',
        'CardCryptogramPacket': 'test',
        'Name': 'test',
        'CultureName': 'ru-RU',
        'Email': 'smth@mail.com',
        'Payer': {'FirstName': 'test', 'LastName': 'test'},
    }

    return await (
        CloudPaymentsClient(public_id, api_secret).charge(charge_request_data)
    )


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(test())
