# Stay Manager System (Hotel Management API)

A robust, multi-property ready Hotel Management System API built with Django REST Framework. This project solves modern hotel administration challenges by combining robust Relational Database Modeling with Asynchronous Messaging and Role-Based Access Control (RBAC).

## 🚀 Key Features

* **Domain Modeling**: Deep entities tracking `Hotel`, `RoomType`, `Room`, `Guest`, `Booking`, and `Payment`.
* **Advanced Authentication & RBAC**:
  * Powered by `djangorestframework-simplejwt`.
  * Customized JWT Payload interceptor embedding Account `Role` & `is_staff` privileges directly in the Token.
  * Custom API Permissions (`IsStaffRole` & `HasRole`) effectively protecting specific Management endpoints.
* **Asynchronous Tasks (Celery + Redis)**:
  * **Emails:** Seamless, non-blocking Booking Confirmation emails triggered sequentially using `@shared_task`.
  * **Celery Beat (Cron):** A background automated job scheduling periodically (every 30 mins) to auto-transition the physical `Room` statuses if a Booking is `CANCELLED` or `CHECKED_OUT`.
* **API Filtering & Searching**: Out-of-the-box querying via `django-filter` supporting foreign relation lookups, Textual Search, and Ordering sorting over endpoints.
* **Fully Dockerized**: Complete multi-container orchestration wrapping the App, Postgres database, Redis broker, Celery workers, and Celery Beat scheduler.
* **CI/CD Quality Compliant**: Guaranteed strict compliance with Python standards (`isort`, `black`, `flake8`) and advanced SecOps analysis (`Bandit` & `Trivy`). Fully covered with native `unittest`.

---

## 🛠 Tech Stack

* **Backend:** Python 3.11 \ Django \ Django REST Framework
* **Database:** PostgreSQL 15
* **Broker & Cache:** Redis 7
* **Task Queue:** Celery
* **Environment:** Docker & Docker Compose
* **QA & Security:** Flake8, Black, Isort, Bandit, Trivy, ReviewDog

---

## ⚙️ Getting Started

### 1. Build & Run Containers
As the project is entirely dockerized, it takes just one command to get all isolated containers up and running.
```bash
docker compose up --build -d
```

### 2. Automated Setup (Entrypoint)
The project includes a `docker-entrypoint.sh` script that runs automatically on startup. You **do not** need to run migrations manually! The entrypoint will:
1. Wait for the PostgreSQL database to be ready.
2. Run `makemigrations` and `migrate`.
3. Auto-populate basic `Roles` in the DB.
4. Auto-create a Superuser for testing purposes.
   - **Username:** `admin`
   - **Password:** `admin123`

*The API should now be running at: `http://localhost:8000/hotel/api/`*

---

## 🧪 Running Tests

The application is bundled with automated tests verifying Authentication, Permission Access, and Celery Mock patching. 

```bash
# Run tests natively via Django test runner
docker compose exec web python manage.py test
```

---

## 📚 API Endpoints Summary

### Authentication Base
* `POST /auth/api/token/` - Obtain Access & Refresh Custom Tokens (Injecting Roles).
* `POST /auth/api/token/refresh/` - Refresh Access Token.
* `POST /auth/api/token/verify/` - Verify a Token signature.

### Hotel Ecosystem (Filters available)
* `GET/POST /hotel/api/hotels/` - Property endpoints (Staff).
* `GET/POST /hotel/api/room-types/` - Types & Prices (Staff).
* `GET/POST /hotel/api/rooms/` - Physical rooms availability (`?status=AVAILABLE&hotel=1`).
* `GET/POST /hotel/api/guests/` - Customer management endpoints.
* `GET/POST /hotel/api/bookings/` - Main Booking reservations (`?status=CHECKED_OUT`).
* `GET/POST /hotel/api/payments/` - Payment transactions.

---

## 👷 Architectural Decisions & Highlights
* **Fat Models, Skinny Views:** Leveraged `ModelViewSet` globally enforcing logic via `.perform_create()` preventing DRF View clutter.
* **Celery Scalability:** Fallback variables injected on `settings.py` mapped intrinsically by `.env` from the `docker-compose.yml`, preventing network mapping `Errno 111` mismatches inside bridges.
* **Separation of Concerns:** Isolated Authentication logic inside the `hotel_auth` app keeping the main `hotel` scope strictly focused on properties.

---

## 🚀 Potential Improvements & Next Steps

While the current architecture is robust, the following enhancements could elevate the system for large-scale enterprise scenarios:

* **Tenant-Scoped Roles:** Currently, `Account` and `Role` models operate globally across the system. A great next step is to introduce an associative entity (e.g., `HotelStaff`) to link a user's role specifically to one or more `Hotel` branches. This granular approach would isolate a user to be a Receptionist at "Hotel A" while simultaneously holding no access to "Hotel B".
* **Payment Gateway Integration:** The current `Payment` model acts as an internal ledger. It could easily be integrated with external APIs (like Stripe or PayPal), leveraging Celery webhooks to validate and register incoming transaction statuses asynchronously.
* **Advanced Test Isolation:** Expand the current native `unittest` suite to `pytest-django`, adopting fixture injections and parametrized testing for faster, modular execution in CI pipelines.
