# LPG RouteX Web

Next.js (App Router) web app for LPG delivery route optimization, tracking, and analytics.

## Quick start

1) Install Node deps:

```
npm install
```

2) Set env:

```
cp .env.local.example .env.local
# Edit MAPBOX_TOKEN and OPTIMIZER_URL
```

3) Dev server:

```
npm run dev
```

Open http://localhost:3000

## API bridge
The app proxies optimization requests to a Python FastAPI service (optimizer-service). See ../optimizer_service.
