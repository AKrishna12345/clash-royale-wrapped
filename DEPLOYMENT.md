# Deployment Guide

This guide will help you deploy Clash Royale Wrapped to production.

## Deployment Options

### Option 1: Vercel (Frontend) + Railway/Render (Backend) - Recommended

This is the easiest and most cost-effective option.

#### Backend Deployment (Railway)

1. **Sign up for Railway**: Go to [railway.app](https://railway.app) and sign up with GitHub

2. **Create a new project**:
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Choose your `clash-royale-wrapped` repository
   - Select the `backend` folder as the root directory

3. **Set environment variables**:
   - In Railway dashboard, go to your project → Variables
   - Add the following:
     ```
     CLASH_ROYALE_API_TOKEN=your_api_token_here
     ALLOWED_ORIGINS=https://your-frontend-domain.vercel.app
     PORT=8000
     ```

4. **Deploy**:
   - Railway will automatically detect it's a Python project
   - It will install dependencies from `requirements.txt`
   - The app will deploy automatically

5. **Get your backend URL**:
   - Railway will provide a URL like `https://your-app.railway.app`
   - Copy this URL - you'll need it for the frontend

#### Frontend Deployment (Vercel)

1. **Sign up for Vercel**: Go to [vercel.com](https://vercel.com) and sign up with GitHub

2. **Import your project**:
   - Click "Add New" → "Project"
   - Import your GitHub repository
   - Set the **Root Directory** to `frontend`

3. **Configure build settings**:
   - Framework Preset: Vite
   - Build Command: `npm run build`
   - Output Directory: `dist`
   - Install Command: `npm install`

4. **Set environment variables**:
   - Go to Project Settings → Environment Variables
   - Add:
     ```
     VITE_API_BASE_URL=https://your-backend-url.railway.app
     ```

5. **Deploy**:
   - Click "Deploy"
   - Vercel will build and deploy your frontend
   - You'll get a URL like `https://your-app.vercel.app`

6. **Update backend CORS**:
   - Go back to Railway backend settings
   - Update `ALLOWED_ORIGINS` to include your Vercel URL:
     ```
     ALLOWED_ORIGINS=https://your-app.vercel.app
     ```
   - Redeploy the backend

---

### Option 2: Render (Both Frontend and Backend)

#### Backend Deployment

1. **Sign up for Render**: Go to [render.com](https://render.com) and sign up

2. **Create a new Web Service**:
   - Click "New" → "Web Service"
   - Connect your GitHub repository
   - Set:
     - **Name**: `clash-royale-wrapped-backend`
     - **Root Directory**: `backend`
     - **Environment**: Python 3
     - **Build Command**: `pip install -r requirements.txt`
     - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`

3. **Set environment variables**:
   - `CLASH_ROYALE_API_TOKEN`: Your API token
   - `ALLOWED_ORIGINS`: Your frontend URL (update after deploying frontend)
   - `PORT`: 10000 (Render default)

4. **Deploy** and copy your backend URL

#### Frontend Deployment

1. **Create a new Static Site**:
   - Click "New" → "Static Site"
   - Connect your GitHub repository
   - Set:
     - **Root Directory**: `frontend`
     - **Build Command**: `npm install && npm run build`
     - **Publish Directory**: `dist`

2. **Set environment variables**:
   - `VITE_API_BASE_URL`: Your backend URL from step above

3. **Deploy** and update backend `ALLOWED_ORIGINS` with your frontend URL

---

### Option 3: Netlify (Frontend) + Any Backend Host

#### Frontend on Netlify

1. **Sign up for Netlify**: Go to [netlify.com](https://netlify.com)

2. **Deploy from GitHub**:
   - Click "Add new site" → "Import an existing project"
   - Connect your repository
   - Set:
     - **Base directory**: `frontend`
     - **Build command**: `npm run build`
     - **Publish directory**: `dist`

3. **Set environment variables**:
   - Go to Site settings → Environment variables
   - Add `VITE_API_BASE_URL` with your backend URL

4. **Deploy**

---

## Post-Deployment Checklist

- [ ] Backend is accessible and returns health check
- [ ] Frontend can communicate with backend (check browser console)
- [ ] CORS is properly configured
- [ ] Environment variables are set correctly
- [ ] API token is working
- [ ] Test with a real Clash Royale tag

## Troubleshooting

### CORS Errors
- Make sure `ALLOWED_ORIGINS` in backend includes your exact frontend URL (with https://)
- No trailing slashes in the URL
- Redeploy backend after changing CORS settings

### API Connection Errors
- Check that `VITE_API_BASE_URL` in frontend matches your backend URL
- Ensure backend is running and accessible
- Check browser console for specific error messages

### Build Errors
- Make sure all dependencies are in `package.json` and `requirements.txt`
- Check build logs for specific errors
- Ensure Node.js and Python versions are compatible

## Custom Domain (Optional)

### Vercel
1. Go to Project Settings → Domains
2. Add your custom domain
3. Follow DNS configuration instructions

### Railway/Render
1. Go to your service settings
2. Add custom domain
3. Configure DNS as instructed

---

## Cost Estimates

- **Vercel**: Free tier (hobby) - Perfect for personal projects
- **Railway**: Free tier with $5 credit/month, then pay-as-you-go
- **Render**: Free tier available, but limited
- **Netlify**: Free tier available

For a personal project, the free tiers should be sufficient!

