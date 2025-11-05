# 🚀 Deployment Instructions

## ✅ GitHub Repository Created

**Repository URL**: https://github.com/sr-857/lpg-route-optimizer

Your code has been successfully pushed to GitHub!

---

## 🌐 Deploy Web App to Netlify

### Option 1: Netlify Web Interface (Easiest)

1. **Go to Netlify**: https://app.netlify.com
2. **Import from Git**:
   - Click "Add new site" → "Import an existing project"
   - Choose "Deploy with GitHub"
   - Select repository: `sr-857/lpg-route-optimizer`
   - Configure build settings:
     - **Base directory**: `lpg_web`
     - **Build command**: `npm run build`
     - **Publish directory**: `lpg_web/.next`
3. **Add Environment Variables**:
   - Go to Site settings → Environment variables
   - Add:
     ```
     NEXT_PUBLIC_MAPBOX_TOKEN = pk.your_mapbox_token_here
     OPTIMIZER_URL = https://your-backend-url.com (optional)
     ```
4. **Deploy**: Click "Deploy site"

### Option 2: Netlify CLI

```bash
# Install Netlify CLI
npm install -g netlify-cli

# Login to Netlify
netlify login

# Navigate to web app
cd lpg_web

# Deploy
netlify deploy --prod

# Follow prompts:
# - Create & configure new site
# - Build command: npm run build
# - Publish directory: .next
```

### Option 3: Vercel (Recommended for Next.js)

```bash
# Install Vercel CLI
npm install -g vercel

# Login
vercel login

# Navigate to web app
cd lpg_web

# Deploy
vercel --prod

# Vercel auto-detects Next.js settings
```

---

## 🔧 Deploy Backend Service

### Option 1: Render.com

1. Go to https://render.com
2. Click "New +" → "Web Service"
3. Connect GitHub repository: `sr-857/lpg-route-optimizer`
4. Configure:
   - **Name**: lpg-optimizer-service
   - **Root Directory**: `optimizer_service`
   - **Runtime**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn app:app --host 0.0.0.0 --port $PORT`
5. Deploy

### Option 2: Railway.app

```bash
# Install Railway CLI
npm install -g @railway/cli

# Login
railway login

# Navigate to service
cd optimizer_service

# Initialize and deploy
railway init
railway up
```

### Option 3: Fly.io

```bash
# Install Fly CLI
curl -L https://fly.io/install.sh | sh

# Login
fly auth login

# Navigate to service
cd optimizer_service

# Create fly.toml and deploy
fly launch
```

---

## 🔑 Get Mapbox Token

1. Go to https://account.mapbox.com
2. Sign up or log in
3. Go to "Access tokens"
4. Create a new token or copy existing one
5. Add to deployment environment variables

---

## 📊 Deployment Checklist

- [x] Code pushed to GitHub
- [ ] Mapbox token obtained
- [ ] Web app deployed to Netlify/Vercel
- [ ] Backend service deployed (optional)
- [ ] Environment variables configured
- [ ] Test deployment URLs
- [ ] Configure custom domain (optional)

---

## 🔗 Quick Links

- **GitHub Repo**: https://github.com/sr-857/lpg-route-optimizer
- **Netlify Dashboard**: https://app.netlify.com
- **Vercel Dashboard**: https://vercel.com/dashboard
- **Render Dashboard**: https://dashboard.render.com
- **Mapbox Account**: https://account.mapbox.com

---

## 📝 Next Steps

1. **Get Mapbox token** (required for maps)
2. **Choose deployment platform** (Netlify or Vercel for web app)
3. **Deploy web app** using one of the options above
4. **Deploy backend** (optional - for route optimization API)
5. **Test your deployment**

For detailed deployment guide, see `lpg_web/DEPLOYMENT.md`
