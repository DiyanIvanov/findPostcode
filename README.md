# 📮 UK Postcode Geocoder API

A Django REST API that resolves UK postcodes to geographic coordinates (latitude and longitude), with a built-in web portal for user registration and API key management.

---

## Features

- 🔍 Look up latitude and longitude for any valid UK postcode
- ⚡ Fast, simple JSON responses
- 🧹 Handles postcode formatting automatically (spaces, casing)
- ❌ Clear error responses for invalid or unknown postcodes
- 🔑 API key authentication — keys generated and managed via web portal
- 👤 User registration and login for self-service key management

---

## Web Portal

The project includes a simple web interface where users can:

- Register for an account
- Log in and manage their profile
- Generate and revoke API keys
- View their request usage

---

## Authentication

All API requests must include a valid API key in the request header:

```
Authorization: Api-Key <your-api-key>
```

API keys are created through the web portal after registering for an account.

**Example:**

```bash
curl -H "Authorization: Api-Key abc123xyz..." \
  https://your-domain.com/api/postcode/M1+1AE/
```

Requests without a valid key will receive a `401 Unauthorized` response:

```json
{
  "error": "Invalid or missing API key"
}
```

---

## Endpoints

### `GET /postcode/<postcode>/`

Returns the latitude and longitude for a given UK postcode.

**URL Parameters**

| Parameter  | Type   | Required | Description                         |
|------------|--------|----------|-------------------------------------|
| `postcode` | string | ✅ Yes   | A valid UK postcode (e.g. `M1 1AE`) |

**Example Request**

```bash
curl -H "Authorization: Api-Key abc123xyz..." \
  https://your-domain.com/api/postcode/M1+1AE/
```

**Success Response** `200 OK`

```json
{
  "postcode": "M1 1AE",
  "latitude": 53.4794,
  "longitude": -2.2453
}
```

**Error Response** `404 Not Found`

```json
{
  "detail": "Postcode <postcode> not found"
}
```

**Error Response** `400 Bad Request`

```json
{
  "error": "Invalid postcode format"
}
```

---

### `POST /postcode/batch/`

Look up coordinates for multiple postcodes in a single request.

**Request Body**

```json
{
  "postcodes": ["M1 1AE", "SW1A 1AA", "EC1A 1BB"]
}
```

**Success Response** `200 OK`

```json
{
  "results": [
    { "postcode": "M1 1AE",   "latitude": 53.4794, "longitude": -2.2453 },
    { "postcode": "SW1A 1AA", "latitude": 51.5010, "longitude": -0.1247 },
    { "postcode": "EC1A 1BB", "latitude": 51.5196, "longitude": -0.1026 }
  ]
}
```

Postcodes that cannot be resolved will include an `error` field instead of coordinates:

```json
{ "postcode": "XX1 1XX", "error": "Postcode not found" }
```

Maximum postcodes per batch is configurable via MAX_BATCH_POSTCODES in .env

---

## Getting Started

### Prerequisites

- Python 3.13+
- pip
- PostgreSQL (or SQLite for development)

### Installation

```bash
git clone https://github.com/your-username/uk-postcode-geocoder.git
cd uk-postcode-geocoder
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### Environment Variables

Create a `.env` file in the project root:

```env
SECRET_KEY=your-django-secret-key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
DATABASE_URL=sqlite:///db.sqlite3
```

### Database Setup

```bash
python manage.py migrate
python manage.py createsuperuser  # optional: Django admin access
```

### Running Locally

```bash
python manage.py runserver
```

The API and web portal will be available at `http://localhost:8000`.

---

## Data Source

Postcode coordinates are sourced from the [ONS Postcode Directory](https://geoportal.statistics.gov.uk/) open dataset.

---

## Error Codes

| Status | Meaning                                   |
|--------|-------------------------------------------|
| `200`  | Success                                   |
| `400`  | Bad request — invalid postcode format     |
| `401`  | Unauthorized — missing or invalid API key |
| `404`  | Postcode not found                        |
| `429`  | Rate limit exceeded                       |
| `500`  | Internal server error                     |

---

## Rate Limiting

Requests are limited to **100 per minute** per API key. Batch requests count as a single request regardless of postcode count.

---

## Contributing

Contributions are welcome! Please open an issue or submit a pull request.

1. Fork the repo
2. Create a feature branch (`git checkout -b feature/my-feature`)
3. Commit your changes (`git commit -m 'Add my feature'`)
4. Push to the branch (`git push origin feature/my-feature`)
5. Open a Pull Request

---

## License

MIT — see [LICENSE](LICENSE) for details.
