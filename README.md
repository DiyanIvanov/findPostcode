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
Authorization: Token <your-api-key>
```

API keys are created through the web portal after registering for an account.

**Example:**

```bash
curl -H "Authorization: Token abc123xyz..." \
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
curl -H "Authorization: Token abc123xyz..." \
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

## `POST /api/csv-export/`

Request a CSV export for a list of UK postcodes. Queues an async export task and returns a `task_id` to poll for the result.

**Request Body**

```json
{
  "postcodes": ["SW1A 1AA", "EC1A 1BB"]
}
```

**Success Response `200 OK`**

```json
{
  "task_id": "f695a1e6-59ac-41ec-8020-30b14e085ef6",
  "status": "submitted"
}
```

Use the returned `task_id` to poll for export status at `GET /api/csv-status/<task_id>/`.

**Error Response `400 Bad Request`**

```json
{
  "postcodes": ["This field is required."]
}
```
---

## `GET /api/csv-status/<task_id>/`

Check the status of a queued CSV export task.

**URL Parameters**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `task_id` | string | ✅ Yes | The UUID returned from `POST /api/csv-export/` |

**Example Request**

```bash
curl -H "Authorization: Token abc123xyz..." \
  https://your-domain.com/api/csv-status/f695a1e6-59ac-41ec-8020-30b14e085ef6/
```

**Success Response `200 OK` — export complete**

```json
{
  "status": "success",
  "url": "https://your-storage.com/find-postcode-csv-requests/f695a1e6-59ac-41ec-8020-30b14e085ef6.csv"
}
```

**Response `200 OK` — export in progress**

```json
{
  "task_id": "f695a1e6-59ac-41ec-8020-30b14e085ef6",
  "status": "PENDING"
}
```

The `status` field reflects the underlying Celery task state (e.g. `PENDING`, `STARTED`, `FAILURE`). Keep polling until `status` is `"success"`.

> **Note:** The `url` in the complete response is a presigned storage URL and may be time-limited depending on your storage backend configuration.

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
DEBUG=False
ALLOWED_HOSTS=localhost,127.0.0.1
DATABASE_URL=sqlite:///db.sqlite3
MAX_BATCH_POSTCODES=<max_number_of_postcodes_per_batch>
DAILY_THROTTLE_RATE=<max_number_of_daily_request_per_user>
PERMIN_THROTTLE_RATE=<max_number_of_request_per_minute>
CELERY_BROKER_URL='redis://redis:6379/0'
CELERY_RESULT_BACKEND='redis://redis:6379/0'
MINIO_ACCESS_KEY=<your_admin_name>
MINIO_SECRET_KEY=<your_admin_password>
MINIO_BUCKET_NAME=<bucket_name>
MINIO_ENDPOINT_URL='http://minio:9000'
MINIO_CUSTOM_DOMAIN='localhost:9000'
```

### Database Setup

```bash
python manage.py migrate
python manage.py createsuperuser  # optional: Django admin access
```

### Running Locally

This project requires Redis, Celery, and MinIO — use Docker Compose to run all services together.

```bash
docker compose up --build
```

The API will be available at `http://localhost:8000`.

> **MinIO Web Console:** The console is available on port `9001` but disabled by default. To enable it, uncomment the `9001` port mapping under the `minio` service in `docker-compose.yml`.

The following services will be started:

| Service | Description |
|---------|-------------|
| `api` | Django REST API |
| `celery` | Async worker for CSV export tasks |
| `redis` | Message broker for Celery |
| `minio` | S3-compatible object storage for CSV files |
| `minio_init` | One-off container that creates the storage bucket on first run |

---

## Data Source
Postcode data is sourced from the [ONS Postcode Directory](https://geoportal.statistics.gov.uk/search) (ONSPD), 
an open dataset published in csv format quarterly by the Office for National Statistics.

The dataset includes active and terminated postcodes across the UK with coordinates, 
dates and administrative geography.

---

### Keeping data up to date
To update the postcode database with the latest ONSPD data, run:

```bash
python manage.py update_postcode_db \
    --url <onspd_download_url> \
    --file Data/<file_name>.csv
```

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
