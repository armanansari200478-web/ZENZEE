# ZENZEE Viva Preparation

## 1. Project in one answer

ZENZEE is a Django-based fashion e-commerce website for youth streetwear. It supports user registration and login, product browsing, cart and wishlist management, checkout, Cash on Delivery, Razorpay test checkout, order history, reviews, an AI-style rule-based recommendation assistant, and a staff dashboard.

The Django project is inside `backend/`. The project package is `config`, and the main apps are `accounts`, `products`, `cart`, `wishlist`, `orders`, `reviews`, `ai`, and `dashboard`.

## 2. What is currently working

- Live Render homepage: `https://zenzee.onrender.com/`
- Live smoke checks passed for `/`, `/products/`, `/accounts/login/`, and `/ai/stylist/`.
- Django system check passed.
- Backend automated tests: 12 passed when run from `backend/`.
- Render deployment uses Gunicorn, migrations, and WhiteNoise static files.
- Razorpay integration is in test mode, so no real money should be charged.

Correct local test command:

```powershell
cd backend
..\.venv\Scripts\python.exe manage.py test
```

## 3. Honest limitations and viva risks

1. Test coverage is limited. Current tests mainly cover the custom user model, account pages, product pricing, AI response, and basic checkout access. Cart actions, wishlist actions, order creation, Razorpay signature verification, reviews, and dashboard permissions need more tests.
2. Render's local SQLite database is not a durable production database. A PostgreSQL database is recommended for persistent users, products, carts, and orders.
3. Render's local filesystem is ephemeral. Uploaded profile and product media should use cloud storage in a real production deployment.
4. The payment verification endpoint is CSRF-exempt because Razorpay posts to it. It still validates the Razorpay signature when keys are configured, but the endpoint should also verify that the Razorpay order ID belongs to the local order.
5. The project contains a demo payment fallback when Razorpay keys are absent. This is useful for presentation, but it must not be treated as secure production payment behavior.
6. Order detail access should ideally be restricted to the order owner or staff. The current view looks up an order by order number without requiring login.
7. `check --deploy` reports security hardening warnings for HTTPS redirect, secure cookies, and HSTS. These should be enabled only after confirming Render's proxy/HTTPS setup.
8. Gunicorn cannot be tested on Windows because it imports Linux's `fcntl` module. Render runs Linux, so the production Gunicorn command is appropriate there.

## 4. Important viva questions and short answers

### Django and architecture

**Q: Why did you choose Django?**  
A: Django provides routing, ORM, authentication, forms, templates, admin, security middleware, and a clear app structure, so it is suitable for a database-driven e-commerce system.

**Q: What is the role of `manage.py`?**  
A: It is the command-line entry point for Django commands such as `runserver`, `migrate`, `makemigrations`, `test`, and `collectstatic`.

**Q: What is `config`?**  
A: `config` is the Django project package. It contains settings, URL configuration, WSGI, and ASGI entry points.

**Q: Why are features separated into apps?**  
A: Each app owns one business capability, which improves maintainability, reuse, testing, and separation of responsibility.

**Q: What is MTV in Django?**  
A: Model stores data, Template displays data, and View contains request/response logic. Django's MTV pattern is similar to MVC.

**Q: What is the ORM?**  
A: Django ORM maps Python model classes to database tables and lets the application query data without writing most SQL manually.

**Q: What are migrations?**  
A: Migrations are version-controlled database schema changes generated from model changes and applied with `migrate`.

### Models and e-commerce logic

**Q: How is the product price calculated?**  
A: `get_effective_price()` returns the discount price only when it exists and is lower than the original price; otherwise it returns the original price.

**Q: Why is `ProductSize` a separate model?**  
A: A product can have many sizes, and each size needs its own stock quantity. `ProductSize` represents that product-size inventory relationship.

**Q: How does the cart work for guests and users?**  
A: Authenticated users are identified by their user relation; guests are identified by a session key stored on the cart.

**Q: Why are prices copied into `OrderItem`?**  
A: It preserves the historical purchase price even if the product price changes later.

**Q: Why is `OrderItem` separate from `Order`?**  
A: One order contains multiple products, and each item needs its own product, size, quantity, and price.

**Q: How is shipping calculated?**  
A: Shipping is free when the subtotal is greater than ₹1,499; otherwise the fee is ₹99.

### Authentication and security

**Q: Why use a custom user model?**  
A: ZENZEE needs extra profile fields such as phone number and bio, so the custom model extends the default authentication data.

**Q: What does `login_required` do?**  
A: It redirects unauthenticated users to login and prevents protected pages from being accessed anonymously.

**Q: What is CSRF protection?**  
A: It prevents malicious websites from submitting unauthorized state-changing requests using a user's browser session.

**Q: Why is payment verification CSRF-exempt?**  
A: The payment callback is an external gateway request rather than a normal browser form. Security is provided by Razorpay signature verification, but additional order ownership validation should be added.

**Q: What is the purpose of `SECRET_KEY`?**  
A: Django uses it for cryptographic signing, sessions, CSRF tokens, and other security features. It must be stored as an environment variable.

### Razorpay

**Q: Explain the Razorpay flow.**  
A: The server creates a local order, sends the amount to Razorpay, the browser opens Razorpay Checkout, Razorpay returns payment details, and the server verifies the signature before setting `is_paid=True`.

**Q: Why is the amount multiplied by 100?**  
A: Razorpay expects the amount in the smallest currency unit, so ₹100 becomes 10,000 paise.

**Q: Why should payment status never be trusted from the browser?**  
A: Browser data can be modified. The server must verify the gateway signature before marking an order as paid.

**Q: What is test mode?**  
A: Test mode uses Razorpay sandbox credentials and simulated payment details, so development and viva demonstrations do not charge real money.

**Q: What happens if Razorpay keys are missing?**  
A: The current project enters demo mode so the presentation checkout remains usable. In real production this fallback should be disabled.

### AI stylist

**Q: Is this using a real AI model?**  
A: The current default implementation is a rule-based recommendation engine. It examines words such as oversized, hoodie, streetwear, cargo, budget, or under and filters available products. It can be extended with an external LLM provider.

**Q: Why keep a fallback engine?**  
A: It keeps the feature functional without an external API key, avoids unnecessary API cost, and makes the viva demo reliable.

### Deployment and testing

**Q: Why does Render use `cd backend`?**  
A: `manage.py` and the `config` package are inside `backend`, so Gunicorn must start from that directory to import `config.wsgi`.

**Q: What does WhiteNoise do?**  
A: It serves collected static CSS, JavaScript, and image files directly from the Django deployment.

**Q: Why run `collectstatic`?**  
A: It gathers static files from the project into `STATIC_ROOT`, where WhiteNoise can serve them in production.

**Q: Why run migrations during deployment?**  
A: A fresh Render environment may not have the database tables. Running migrations creates the schema before requests reach the application.

**Q: What tests were actually run?**  
A: `accounts` and `products` test modules ran successfully with 12 tests passing. Public live route smoke tests also returned HTTP 200. Full business-flow coverage is still incomplete.

**Q: What would you improve next?**  
A: Add PostgreSQL, durable media storage, stronger order ownership checks, idempotent payment handling, complete integration tests, secure production cookie settings, and monitoring/logging.

## 5. Demo order for viva

1. Open the live homepage.
2. Browse products and open a product detail page.
3. Add a product and size to the cart.
4. Show wishlist behavior after login.
5. Open the AI stylist and submit a fashion query.
6. Go to checkout and explain COD versus Razorpay test mode.
7. Place a COD order and show order detail/history.
8. Explain the Razorpay signature verification flow rather than claiming a real payment.
9. Show the staff dashboard only with a staff account.
10. Mention the production limitations honestly and explain the planned improvements.
