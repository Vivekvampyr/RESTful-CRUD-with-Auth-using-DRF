# RESTful Product CRUD API

A Django REST Framework API for managing products. The API uses a `ModelViewSet`,
token authentication, and owner-based access control: authenticated users can
only list and manage products they own.

## Features

- Create, retrieve, update, partially update, and delete products
- Token and session authentication
- Automatic assignment of the authenticated user as product owner
- Product validation: regular price must be greater than zero, and sale price
  must be lower than regular price
- Filtering by price, stock, and active status
- Search by product name and description
- Ordering by name, price, stock, or creation date
- Page-number pagination (10 products per page by default; up to 100 per page)

## Requirements

- Python version supported by Django 6.1
- Dependencies listed in `requirements.txt`

## Setup

Run these commands from the project directory in PowerShell:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

The development server runs at `http://127.0.0.1:8000/`. The project uses
SQLite by default.

## Authentication

Obtain a token by posting a valid username and password to `/api/token/`:

```http
POST /api/token/
Content-Type: application/json

{
  "username": "your-username",
  "password": "your-password"
}
```

The response contains a token:

```json
{
  "token": "your-token"
}
```

Send it with each API request:

```http
Authorization: Token your-token
```

All product endpoints require authentication. Product lists are scoped to the
authenticated user; another user's product is not accessible.

## Product API

The product resource is available at `/api/products/`.

| Method | Endpoint | Description |
| --- | --- | --- |
| `GET` | `/api/products/` | List your products |
| `POST` | `/api/products/` | Create a product |
| `GET` | `/api/products/{id}/` | Retrieve one of your products |
| `PUT` | `/api/products/{id}/` | Replace one of your products |
| `PATCH` | `/api/products/{id}/` | Partially update one of your products |
| `DELETE` | `/api/products/{id}/` | Delete one of your products |

Product fields:

| Field | Type | Notes |
| --- | --- | --- |
| `id` | integer | Read-only |
| `name` | string | Maximum 150 characters |
| `description` | string | Optional |
| `price` | decimal | Must be greater than zero |
| `sale_price` | decimal or `null` | Optional; when set, must be lower than `price` |
| `stock` | integer | Defaults to `0`; cannot be negative |
| `is_active` | boolean | Defaults to `true` |
| `owner` | integer | Read-only; set from the authenticated user |
| `created_at` | datetime | Read-only |
| `updated_at` | datetime | Read-only |

Example create request:

```http
POST /api/products/
Content-Type: application/json
Authorization: Token your-token

{
  "name": "Mechanical Keyboard",
  "description": "Compact wireless keyboard",
  "price": "100.00",
  "sale_price": "80.00",
  "stock": 5,
  "is_active": true
}
```

### Filtering, search, ordering, and pagination

- Filter with `price`, `stock`, or `is_active`, for example
  `/api/products/?is_active=true`.
- Search `name` and `description` with `?search=keyboard`.
- Order by `name`, `price`, `stock`, or `created_at` with `?ordering=price`.
  Prefix the field with `-` for descending order, such as `?ordering=-created_at`.
- Use `?page=2` to request another page. Change the page size with
  `?page_size=20` (maximum 100).

Filters, search, ordering, and pagination parameters can be combined.

## Run tests

```powershell
python manage.py test
```