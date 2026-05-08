# Spread Smile

A Django app where **organizations** register, create fundraising **events**, and visitors **donate** (via [SSLCommerz](https://developer.sslcommerz.com/)). **Admins** approve organizations before they go live.

![Spread Smile banner](static/images/ssms2.png)

## Requirements

- Python 3.8+ (3.9+ recommended)
- pip

## Setup

1. Clone the repository and go into the project directory:

   ```bash
   cd spreadsmile
   ```

2. Create and activate a virtual environment:

   **macOS / Linux**

   ```bash
   python3 -m venv env
   source env/bin/activate
   ```

   **Windows (PowerShell)**

   ```powershell
   python -m venv env
   .\env\Scripts\Activate.ps1
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Configure environment variables (optional for local dev; **required for production**).

   Copy the list below into a `.env` file in the project root and adjust values. The app reads standard environment variables (Django does not load `.env` automatically unless you use a tool such as `django-environ` or export variables in your shell).

   | Variable | Description |
   |----------|-------------|
   | `SECRET_KEY` | Django secret key. Generate a new one for production. |
   | `DEBUG` | `True` or `False`. Use `False` in production. |
   | `ALLOWED_HOSTS` | Comma-separated hostnames (e.g. `example.com,www.example.com`). |
   | `SSLCOMMERZ_STORE_ID` | SSLCommerz store ID. |
   | `SSLCOMMERZ_STORE_PASSWD` | SSLCommerz store password. |
   | `SSLCOMMERZ_USE_SANDBOX` | `True` for sandbox, `False` for live gateway. |

   If `SECRET_KEY` is unset, a development default in `settings.py` is used. **Never deploy with that default.**  
   Keep `.env` out of version control (it is listed in `.gitignore`).

5. Apply migrations and run the development server:

   ```bash
   python manage.py migrate
   python manage.py runserver
   ```

   Open [http://127.0.0.1:8000](http://127.0.0.1:8000).

## Project notes

- **SQLite** is the default database (`db.sqlite3`); `*.sqlite3` is gitignored.
- **User groups** `organizations` and `admins` must exist (create them in the Django admin or via fixtures) for role-based views to work as intended.
- Payments use SSLCommerz **session + validation** APIs; use sandbox credentials until you switch `SSLCOMMERZ_USE_SANDBOX` and live keys.

## Optional walkthrough

A [setup video](https://drive.google.com/file/d/1coWXVfEjEysmnmyV-bebagUFDiqCaarD/view?usp=sharing) is available from an earlier version of the project; some steps (e.g. environment variables) may differ from the README above.
