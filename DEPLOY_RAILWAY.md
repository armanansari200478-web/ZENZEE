Railway deployment steps for ZENZEE

1) Prepare repository
- Commit all changes and push to GitHub.

2) Create Railway project
- Go to https://railway.app and create a new project.
- Choose "Deploy from GitHub" and connect your repo + branch.

3) Add Postgres add-on (optional but recommended)
- In Railway project, Add Plugin → Postgres. Railway provides a `DATABASE_URL`.

4) Environment variables (Railway Dashboard → Variables)
- Add the following keys:
  - SECRET_KEY = <your production secret key>
  - DEBUG = False
  - ALLOWED_HOSTS = yourdomain.com,*.railway.app (comma-separated)
  - RAZORPAY_KEY_ID = <your_razorpay_test_or_live_key>
  - RAZORPAY_KEY_SECRET = <your_razorpay_secret>
  - STRIPE_SECRET_KEY = <optional, if using Stripe>
  - STRIPE_PUBLISHABLE_KEY = <optional>

5) Procfile & start command
- Ensure `Procfile` exists with a web command. Example (this project uses `config.wsgi`):
  web: gunicorn config.wsgi --log-file -

6) Requirements
- Ensure `requirements.txt` is present at repo root. Railway will install packages from it.

7) After deployment
- Run migrations from Railway console or via `Deploy → Run Command`:
  python backend/manage.py migrate
- Collect static files (if needed):
  python backend/manage.py collectstatic --noinput

8) Test the site
- Visit the Railway URL and perform a test checkout.

Notes
- For Razorpay, use TEST keys until KYC/live setup is complete. Test keys work without KYC.
- For production, ensure `SECRET_KEY` is a secure random string and never in source control.
- If using SQLite locally, production will use `DATABASE_URL` (Postgres) automatically if configured.
