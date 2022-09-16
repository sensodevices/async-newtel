import hashlib
import json
import time

import httpx


class AsyncClient:

    def __init__(
        self,
        api_key,
        signing_key,
        host: str = 'https://api.new-tel.net/',
        session=None,
    ):
        self.host = host
        self.session = session
        self.api_key = api_key
        self.signing_key = signing_key
        self.headers = {
            "Accept": "*/*",
            "Content-Type": "application/json",
        }

    async def __aenter__(self):
        await self.open()
        return self

    async def __aexit__(self, exc_type, exc, tb):
        await self.close()

    async def open(self):
        if self.session is None:
            self.session = httpx.AsyncClient(
                headers=self.headers,
            )

    async def close(self):
        if self.session is not None:
            await self.session.aclose()
            self.session = None

    def _get_request_signature(self, endpoint, data):
        timestamp = str(int(time.time()))
        signature_content = [
            endpoint,
            timestamp,
            self.api_key,
            json.dumps(data, separators=(',', ':')),
            self.signing_key,
        ]
        signature_str = "\n".join(signature_content)
        signature = hashlib.sha256(signature_str.encode('utf-8')).hexdigest()
        return f"{self.api_key}{timestamp}{signature}"

    async def request(self, endpoint, data):
        url = f"{self.host}{endpoint}"
        signature = self._get_request_signature(endpoint, data)
        headers = {
            "Authorization": f"Bearer {signature}",
            "Content-Type": "application/json",
        }
        response = await self.session.post(
            url=url,
            data=json.dumps(data, separators=(',', ':')),
            headers=headers,
        )
        return response

    async def call(self, number: str, code: int | str, timeout: int = 45):
        response = await self.request(
            endpoint="call-password/start-password-call",
            data={
                "async": 1,
                "dstNumber": number.removeprefix("+"),
                "pin": str(code),
                "timeout": timeout,
            },
        )
        response_body = response.json()
        if response.status_code != 200:
            return response_body["data"]["message"]
        return response_body["data"]["callDetails"]["callId"]
