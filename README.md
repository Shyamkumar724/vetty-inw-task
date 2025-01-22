# Coin API - README

## Overview
Coin API is an HTTP RESTful application designed to provide coin-related information, including coin listings, categories, and market data against the Canadian Dollar (CAD). The application ensures secure access through authentication, is documented with Swagger, and is tested to ensure robustness.

---

## Features (Version 1.0)
### Basic Features
1. **List all coins**
   - Endpoint: `v1/coin-list`
   - Functionality: Provides a list of all coins, including their IDs.
   - Pagination: Defaults to 10 items per call; customizable with `page_num` and `per_page` query parameters.

2. **List coin categories**
   - Endpoint: `v1/coin-categories`
   - Functionality: Lists all coin categories.

3. **List coin Marker**
    - Endpoint: `v1/coin-market`
    - Functionality: Lists all coin market

### Extra Features
4. **Health Check & Version Information**
   - Endpoint: `/health`
   - Functionality: Verifies application and 3rd-party service health.
   - Includes version details.

5. **Authentication**
   - Mechanism: JWT Authentication (JSON Web Tokens).
   - Secures all endpoints.

6. **Documentation**
   - Tool: Swagger (available at `/api/schema/swagger-ui/`).
   - Provides detailed API information.

7. **Dockerization**
   - Dockerized environment for easy setup and deployment.

8. **Code Quality Control**
   - Integrated linting (e.g., `flake8`, `black`).
   - Follows PEP-8 standards.

---

## Installation and Setup

### Prerequisites
- Python 3.12+
- Docker
- Poetry

### Local Setup
1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd <repository-directory>
   ```

2. Install dependencies:
   ```bash
   poetry install
   ```

3. Create `.env` file:
   ```plaintext
   SECRET_KEY=your-secret-key
   DATABASE_URL=DATABASE
   DEBUG=True
   ```

4. Run the server:
   ```bash
   python manage.py runserver
   ```

5. Access the application:
   - API: [http://localhost:8000](http://localhost:8000)
   - Swagger Docs: [http://localhost:8000/api/schema/swagger-ui/](http://localhost:8000/api/schema/swagger-ui/)

### Docker Setup
1. Build the Docker image:
   ```bash
   docker build -t coin-api .
   ```

2. Run the container:
   ```bash
   docker run -p 8080:8080 coin-api
   ```

---

## Endpoints
| Endpoint                | Method | Description                             | Authentication |
|-------------------------|--------|-----------------------------------------|-----------------|
| `/coin-list`            | GET    | List all coins                          | Required        |
| `/coin-categories`      | GET    | List coin categories                    | Required        |
| `/coin-market`          | GET    | Retrieve specific coin market           | Required        |
| `/health`               | GET    | Application and 3rd-party health check  | Not Required    |

---

## Health Check and Versioning
The `/health` endpoint provides insights into the application's operational status and its dependencies, along with the current application version.

---

## Development Standards
1. **Code Quality**
   - PEP-8 compliant.
   - Followed best practices: KISS, DRY, Zen of Python.

2. **Project Structure**
   - Follows Django best practices for structuring apps and settings.

3. **Sensitive Data Handling**
   - Environment variables stored in `.env`.

---

## Additional Notes
- Ensure environment variables are configured correctly for production.
- Test coverage should remain above 80%.
- Regularly update dependencies and maintain quality checks.

---

## License
This project is licensed under the MIT License. See the LICENSE file for details.

---

## Author
Developed by Shyamkumar S S.

