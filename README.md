# RESTful Product CRUD API

A Django REST Framework API for managing products. Products are owned by the
user who creates them, and authenticated users can only view and manage their
own products.

## Features

- Product CRUD using Django REST Framework's `ModelViewSet`
- User registration and token-based authentication
- Token and session authentication for protected API requests
- Owner-scoped product access and automatic owner assignment
- Product validation and database constraints for prices
- Filtering, searching, ordering, and page-number pagination
- OpenAPI schema with Swagger UI and ReDoc

## Requirements

- Python compatible with Django 6.1
- Dependencies pinned in `requirements.txt`
- `drf-spectacular` for the OpenAPI schema and API documentation endpoints

> `drf-spectacular` is imported by the application but is not currently listed
> in `requirements.txt`; install it separately as shown below.

## Setup

Run these commands from the project directory in PowerShell:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m pip install drf-spectacular
python manage.py migrate
python manage.py runserver
```

The development server runs at `http://127.0.0.1:8000/`. SQLite is used by
default. To create an admin user for `/admin/`, run:

```powershell
python manage.py createsuperuser
```

## API documentation

Once the development server is running, visit:

- Swagger UI: `http://127.0.0.1:8000/api/docs/`
- ReDoc: `http://127.0.0.1:8000/api/redoc/`
- OpenAPI schema: `http://127.0.0.1:8000/api/schema/`

## Authentication

### Register

Submit a username, email, password, and matching `password2` to create an
account. Passwords must be at least eight characters and satisfy Django's
configured password validators. Registration returns the new user's ID,
username, email, and an authentication token.

```http
POST /api/register/
Content-Type: application/json

{
  "username": "your-username",
  "email": "you@example.com",
  "password": "your-password",
  "password2": "your-password"
}
```

### Obtain a token

Existing users can obtain a token by posting their credentials:

```http
POST /api/token/
Content-Type: application/json

{
  "username": "your-username",
  "password": "your-password"
}
```

The token endpoint returns a token in this shape. Registration also returns
the new user's `id`, `username`, and `email`:

```json
{
  "token": "your-token"
}
```

Include the token in requests to protected endpoints:

```http
Authorization: Token your-token
```

Product endpoints require authentication. Product lists are scoped to the
authenticated user, so another user's products cannot be retrieved or changed.

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
| `description` | string | Optional; defaults to an empty string |
| `price` | decimal | Must be greater than zero |
| `sale_price` | decimal or `null` | Optional; when set, must be positive and lower than `price` |
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

- Filter by exact `price`, `stock`, or `is_active` values, for example
  `/api/products/?is_active=true`.
- Search `name` and `description` with `?search=keyboard`.
- Order by `name`, `price`, `stock`, or `created_at` with `?ordering=price`.
  Prefix a field with `-` for descending order, such as
  `?ordering=-created_at`.
- Pagination uses 10 products per page by default. Use `?page=2` to request
  another page, or set `?page_size=20` (maximum 100).

Filtering, search, ordering, and pagination parameters can be combined.

## Run tests

```powershell
python manage.py test
```
