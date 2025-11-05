# LPG Smart Route Optimizer Platform

A complete LPG delivery route optimization system with web interface, backend API, and standalone demo.

## 🚀 Components

### 1. Web Application (`lpg_web/`)
Modern Next.js web app for LPG delivery management with route planning, live tracking, and analytics.

**Features:**
- 📊 Dashboard with real-time KPIs
- 🗺️ Interactive route planner with Mapbox
- 📍 Live delivery tracking
- 📈 Analytics and performance charts
- 🔥 Delivery heatmap visualization

**Quick Start:**
```bash
cd lpg_web
npm install
cp .env.local.example .env.local
# Edit .env.local with your Mapbox token
npm run dev
```

### 2. Optimizer Service (`optimizer_service/`)
FastAPI microservice providing route optimization API using Google OR-Tools.

**Quick Start:**
```bash
cd optimizer_service
pip install -r requirements.txt
uvicorn app:app --host 0.0.0.0 --port 8001
```

### 3. Standalone Demo (`lpg_optimizer/`)
Streamlit-based demo for visualizing route optimization with mock data.

**Quick Start:**
```bash
cd lpg_optimizer
pip install -r requirements.txt
streamlit run src/app.py
```

## 📦 Deployment

### Web App
The Next.js app is ready for deployment to Netlify or Vercel.

**Netlify:**
```bash
cd lpg_web
npx netlify-cli deploy --prod
```

**Vercel:**
```bash
cd lpg_web
vercel --prod
```

See `lpg_web/DEPLOYMENT.md` for detailed deployment instructions.

### Backend Service
Deploy the FastAPI service to platforms like Render, Railway, or Fly.io.

## 🔑 Environment Variables

### Web App
- `NEXT_PUBLIC_MAPBOX_TOKEN` - Get from https://account.mapbox.com
- `OPTIMIZER_URL` - URL of deployed optimizer service (optional)

## 🛠️ Tech Stack

- **Frontend**: Next.js 14, React, TypeScript, TailwindCSS
- **Backend**: FastAPI, Python
- **Optimization**: Google OR-Tools (VRPTW solver)
- **Maps**: Mapbox GL JS
- **Charts**: Recharts
- **Deployment**: Netlify/Vercel (frontend), Render/Railway (backend)

## 📄 License

MIT

## 🤝 Contributing

Contributions welcome! Please open an issue or submit a pull request.
