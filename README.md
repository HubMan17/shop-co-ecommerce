# SHOP.CO - E-commerce Store

A modern full-stack e-commerce application built with Vue 3 and FastAPI.

![Vue.js](https://img.shields.io/badge/Vue.js-3.x-4FC08D?logo=vue.js)
![FastAPI](https://img.shields.io/badge/FastAPI-0.109-009688?logo=fastapi)
![TypeScript](https://img.shields.io/badge/TypeScript-5.x-3178C6?logo=typescript)
![Tailwind CSS](https://img.shields.io/badge/Tailwind_CSS-3.x-38B2AC?logo=tailwind-css)

## Features

- Product catalog with filtering and sorting
- Category-based navigation
- Shopping cart functionality
- User authentication (JWT)
- Responsive design
- Product search
- Price range filtering

## Tech Stack

### Frontend
- **Vue 3** - Progressive JavaScript framework
- **TypeScript** - Type-safe JavaScript
- **Tailwind CSS** - Utility-first CSS framework
- **Pinia** - State management
- **Vue Router** - Client-side routing
- **Axios** - HTTP client
- **Vite** - Build tool

### Backend
- **FastAPI** - Modern Python web framework
- **SQLAlchemy** - SQL toolkit and ORM
- **SQLite** - Lightweight database
- **JWT** - JSON Web Tokens for authentication
- **Pydantic** - Data validation

## Project Structure

```
├── backend/
│   ├── app/
│   │   ├── models/       # Database models
│   │   ├── routers/      # API endpoints
│   │   ├── schemas/      # Pydantic schemas
│   │   ├── services/     # Business logic
│   │   ├── config.py     # Configuration
│   │   ├── database.py   # Database setup
│   │   └── main.py       # FastAPI app
│   ├── requirements.txt
│   └── run.py
│
└── frontend/
    ├── src/
    │   ├── components/   # Vue components
    │   ├── views/        # Page components
    │   ├── stores/       # Pinia stores
    │   ├── services/     # API services
    │   ├── router/       # Vue Router config
    │   └── types/        # TypeScript types
    ├── package.json
    └── vite.config.ts
```

## Getting Started

### Prerequisites

- Python 3.10+
- Node.js 18+
- npm or yarn

### Backend Setup

```bash
cd backend

# Create virtual environment (optional)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the server
python run.py
```

The API will be available at `http://localhost:8000`

API Documentation: `http://localhost:8000/docs`

### Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Run development server
npm run dev
```

The app will be available at `http://localhost:5173`

### Running Both Services

For development, run both services in separate terminals:

**Terminal 1 (Backend):**
```bash
cd backend && python run.py
```

**Terminal 2 (Frontend):**
```bash
cd frontend && npm run dev
```

## API Endpoints

### Authentication
- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - Login user
- `GET /api/auth/me` - Get current user

### Products
- `GET /api/products` - List products (with filters)
- `GET /api/products/{slug}` - Get product details
- `GET /api/products/new-arrivals` - Get new arrivals
- `GET /api/products/top-selling` - Get top selling products

### Categories
- `GET /api/categories` - List all categories
- `GET /api/categories/{slug}` - Get category details

### Cart
- `GET /api/cart` - Get cart
- `POST /api/cart/items` - Add item to cart
- `PUT /api/cart/items/{id}` - Update cart item
- `DELETE /api/cart/items/{id}` - Remove item from cart

### Orders
- `POST /api/orders` - Create order
- `GET /api/orders` - List user orders
- `GET /api/orders/{id}` - Get order details

## Environment Variables

### Backend
Create `.env` file in `backend/` directory:

```env
SECRET_KEY=your-secret-key-here
DATABASE_URL=sqlite+aiosqlite:///./shop.db
```

## Building for Production

### Frontend
```bash
cd frontend
npm run build
```

Build output will be in `frontend/dist/`

### Backend
For production, use a proper ASGI server:

```bash
pip install gunicorn
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker
```

## License

MIT License
