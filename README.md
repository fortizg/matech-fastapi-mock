# FastAPI Mock Server

This project is a simple mock server built using FastAPI. It simulates API endpoints for creating, fetching, and listing users, which can be used for development and testing purposes.

## Features

- GET /api/users: Retrieve a list of all users
- POST /api/users: Create a new user
- GET /api/users/{user_id}: Retrieve a specific user by ID

## Prerequisites

- Python 3.11.4 or higher
- Docker (optional, for containerized deployment)

## Installation

1. Clone the repository:

   ```
   git clone https://github.com/fortizg/fastapi-mock-server.git
   cd fastapi-mock-server
   ```

2. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

## Usage

### Running locally

To run the server locally:

```
python -m uvicorn app:app --host 0.0.0.0 --port 8000
```

The server will start at `http://localhost:8000`.

### Running with Docker

1. Build the Docker image:

   ```
   docker build -t fastapi-mock-server .
   ```

2. Run the container:
   ```
   docker run -p 8000:8000 fastapi-mock-server
   ```

Alternatively, you can use Docker Compose:

```
docker-compose up
```

## API Endpoints

- `GET /api/users`: Retrieve all users
- `POST /api/users`: Create a new user
  - Body: `{ "name": "string", "email": "string" }`
- `GET /api/users/{user_id}`: Retrieve a specific user

For detailed API documentation, visit `http://localhost:8000/docs` after starting the server.

## Running Tests

To run the tests for this project:

```
pytest
```

This will run all the tests defined in the `test_app.py` file.

## Development

To contribute to this project:

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
