# Investment App - AI Coding Agent Instructions

## 🎯 Core Concept (Critical!)

**This is NOT a stock trading app** — it's a **portfolio allocation management system** for index funds/ETFs.

The `UserStock` table represents **target vs actual allocation percentages**, not individual stock positions. Think "I want 60% S&P 500 (VOO), 30% International (VXUS), 10% Bonds (BND)" rather than "I bought 10 shares of AAPL."

## 🏗️ Architecture & Workflows

### Service Layer Pattern (Mandatory)

All business logic lives in `backend/services/`, NOT in route handlers:

- Routes (`backend/routes/backend_api.py`) are thin controllers — just validation, service calls, response formatting
- Services handle DB queries, calculations, external API calls
- Example: `create_user()` in `user_service.py` does existence checks, bcrypt hashing, DB operations

### Running the Backend (Critical Setup)

**Always use the virtual environment's Python directly:**

```bash
cd backend
./venv/bin/python -m uvicorn main:app --reload
```

**DO NOT** use global Python or `source venv/bin/activate && uvicorn` — this causes import errors with SQLAlchemy.

### Database Connection

- Local PostgreSQL on `localhost:5432`, database: `investment_app`, user: `postgres`, password: `password`
- Connection string: `postgresql+psycopg://postgres:password@localhost:5432/investment_app`
- Table creation happens automatically on startup via `Base.metadata.create_all(bind=engine)` in `main.py`
- Critical: SQLAlchemy relationship names must match — User has `user_stocks` (not `stocks`), UserStock references `back_populates="user_stocks"`

### Frontend Setup

```bash
cd frontend
npm install  # if first time
npm start    # runs on http://localhost:3000
```

**Known Issue**: Frontend UI assumes stock trading interface. Backend is portfolio allocation focused. StockCard, Portfolio, and Dashboard components need redesign.

## 📁 Key Files & Patterns

### Models (`backend/db/models.py`)

Four core models with cascade delete relationships:

- `User` → has `user_stocks`, `deposits`, `purchases`
- `UserStock` → portfolio allocation entry (has typo: `precentage` should be `percentage`)
- `Deposit` → money added to account
- `Purchase` → ETF/stock transaction records

### API Response Filtering

Services like `protfolio_service.py` explicitly SELECT columns to exclude `id` and `user_id` from responses:

```python
stocks = db.query(
    UserStock.index_name,
    UserStock.fund_number,
    # ... explicit columns, no UserStock.id or UserStock.user_id
).filter(UserStock.user_id == user_id).all()
```

This pattern keeps internal database IDs out of API responses.

### External API Integration

Financial Modeling Prep API via `services/fmp_api.py`:

- API key: `4cDgO8QI4anGo1puGjCsXj0xRS62Tiyd` (in `.env`)
- Used for real-time ETF/stock prices and company info
- No rate limiting implemented yet

## 🚨 Common Pitfalls

1. **Don't treat UserStock as individual stock holdings** — it's portfolio allocation targets
2. **Server must run from venv Python** — `./venv/bin/python -m uvicorn`, not global Python
3. **Relationship names must match** — User's `user_stocks` = UserStock's `back_populates="user_stocks"`
4. **No authentication yet** — all endpoints are public, no JWT/session management
5. **Frontend is outdated** — shows stock trading UI, needs portfolio allocation redesign

## 🔄 Development Commands

### Backend Testing

```bash
# Test API endpoint
curl -X POST "http://localhost:8000/api/users/register?username=testuser&email=test@example.com&password=pass123"

# Check database connection
cd backend && ./venv/bin/python -c "from db.models import User; print('Import successful')"
```

### Database Management

```bash
# Create postgres user (if needed)
createuser -s postgres

# Access database
psql -U postgres -d investment_app
```

## 📋 When Adding Features

1. **New endpoints**: Add service function first, then thin route handler
2. **Database changes**: Update models.py, ensure relationships use correct names
3. **API responses**: Explicitly SELECT columns in services to exclude internal IDs
4. **Authentication** (future): Add JWT middleware, protect routes, validate user_id matches token
5. **Frontend updates**: Remember the portfolio allocation focus — percentages, not share counts

## 🔗 Context Documentation

Detailed docs in `.context/` directory:

- `README.md` — project overview and tech stack
- `database_schema.md` — complete table definitions
- `api_endpoints.md` — all 17 endpoints documented
- `development_status.md` — completed features and roadmap
- `frontend_backend_sync.md` — UI alignment issues

Use these for architecture decisions and understanding design rationale.
