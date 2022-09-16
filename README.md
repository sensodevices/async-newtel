# Async-NewTel

New-Tel simple async client based on httpx.

# Installation

```bash
pip install async-newtel
```

# Usage

```python
import async_newtel
import os

API_KEY = os.environ.get('API_KEY')
SIGNING_KEY = os.environ.get('SIGNING_KEY')

number = '+1234567890'
code = '1234'
# Send email with context manager

async with async_newtel.AsyncClient(
    api_key=API_KEY,
    signing_key=SIGNING_KEY
) as client:
    response = await client.call(number, code)

# Send email without context manager

client = simple_sendgrid.AsyncClient(api_key=API_KEY, signing_key=SIGNING_KEY)
await client.open()
response = await client.call(number, code)
await client.close()

```
