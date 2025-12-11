# CORS (Cross-Origin Resource Sharing) - Deep Dive

## 🔒 What is CORS and Why Does It Exist?

### The Problem CORS Solves

Imagine you're logged into your bank's website (`https://bank.com`). While on that page, a malicious website (`https://evil.com`) tries to make a request to `https://bank.com/api/transfer-money` using your saved cookies.

**Without CORS protection:**
- Evil website could steal your money
- Any website could access your data from other sites
- Your authentication cookies could be hijacked

**With CORS:**
- Browser blocks the request
- Only `https://bank.com` can make requests to `https://bank.com`
- Your data stays safe

### The Same-Origin Policy

Browsers enforce the **Same-Origin Policy**:
- **Same Origin**: Same protocol (`http` vs `https`), domain (`example.com`), and port (`80` vs `3000`)
- **Different Origin**: Any difference in protocol, domain, or port

**Examples:**

| Request From | Request To | Same Origin? |
|-------------|------------|--------------|
| `http://localhost:5173` | `http://localhost:5173` | ✅ Yes |
| `http://localhost:5173` | `http://localhost:8000` | ❌ No (different port) |
| `https://myapp.com` | `https://api.myapp.com` | ❌ No (different subdomain) |
| `http://myapp.com` | `https://myapp.com` | ❌ No (different protocol) |
| `https://myapp.com` | `https://myapp.com:443` | ✅ Yes (443 is default for HTTPS) |

---

## 🛡️ How CORS Works

### The CORS Request Flow

When your frontend makes a request to a different origin, the browser does this:

#### 1. **Preflight Request** (for complex requests)

For POST requests with custom headers, the browser first sends an **OPTIONS** request:

```
Browser → Backend: OPTIONS /api/player
Headers:
  Origin: https://clash-royale-wrapped2.vercel.app
  Access-Control-Request-Method: POST
  Access-Control-Request-Headers: Content-Type
```

**Backend must respond with:**
```
Backend → Browser:
Headers:
  Access-Control-Allow-Origin: https://clash-royale-wrapped2.vercel.app
  Access-Control-Allow-Methods: POST, GET, OPTIONS
  Access-Control-Allow-Headers: Content-Type
  Access-Control-Max-Age: 600
```

**If backend doesn't send these headers → Browser blocks the request**

#### 2. **Actual Request**

Only if preflight succeeds, browser sends the real request:

```
Browser → Backend: POST /api/player
Headers:
  Origin: https://clash-royale-wrapped2.vercel.app
  Content-Type: application/json
Body: {"tag": "#ABC123"}
```

**Backend must include in response:**
```
Backend → Browser:
Headers:
  Access-Control-Allow-Origin: https://clash-royale-wrapped2.vercel.app
```

---

## 🔧 How We Implemented CORS in This Project

### Backend Configuration (FastAPI)

```python
from fastapi.middleware.cors import CORSMiddleware

allowed_origins = os.getenv("ALLOWED_ORIGINS", "http://localhost:5173").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,  # Which domains can access this API
    allow_credentials=True,        # Allow cookies/auth headers
    allow_methods=["*"],           # Which HTTP methods (GET, POST, etc.)
    allow_headers=["*"],           # Which headers are allowed
)
```

### What Each Setting Does

**`allow_origins`**
- List of frontend URLs that can call your API
- Must match **exactly** (including `https://` and no trailing slash)
- Example: `["https://clash-royale-wrapped2.vercel.app"]`

**`allow_credentials=True`**
- Allows sending cookies and authentication headers
- Required if you use sessions or JWT tokens
- If `True`, cannot use `allow_origins=["*"]` (must specify domains)

**`allow_methods=["*"]`**
- Which HTTP methods are allowed (GET, POST, PUT, DELETE, etc.)
- `["*"]` means all methods
- More secure: `["GET", "POST"]` (only allow what you need)

**`allow_headers=["*"]`**
- Which request headers are allowed
- `["*"]` means all headers
- More secure: `["Content-Type", "Authorization"]`

---

## 🚨 Why CORS is a Common Deployment Issue

### The Problem

**Development:**
- Frontend: `http://localhost:5173`
- Backend: `http://localhost:8000`
- CORS configured for: `http://localhost:5173`
- ✅ Works perfectly

**Production:**
- Frontend: `https://clash-royale-wrapped2.vercel.app`
- Backend: `https://harmonious-upliftment-production-d363.up.railway.app`
- CORS still configured for: `http://localhost:5173` ❌
- **Browser blocks the request!**

### Why This Happens

1. **Different URLs in production**
   - Localhost vs production domain
   - Preview deployments get random URLs
   - Custom domains

2. **Environment variables not updated**
   - Forgot to set `ALLOWED_ORIGINS` in production
   - Set wrong URL (typo, missing `https://`, trailing slash)

3. **Multiple environments**
   - Development: `localhost:5173`
   - Staging: `staging.yourapp.com`
   - Production: `yourapp.com`
   - Each needs to be whitelisted

### Real Example from This Project

**What happened:**
1. We set CORS for: `https://clash-royale-wrapped2-gfxtitb50-aryans-projects-b743d20a.vercel.app`
2. Vercel created new deployment: `https://clash-royale-wrapped2-4hz5uskdf-aryans-projects-b743d20a.vercel.app`
3. Browser blocked request → CORS error

**The fix:**
- Updated `ALLOWED_ORIGINS` in Railway to include the new URL
- Railway redeployed
- ✅ Works now

---

## 🎯 Best Practices

### 1. **Never Use `allow_origins=["*"]` in Production**

```python
# ❌ BAD - Allows any website to call your API
allow_origins=["*"]

# ✅ GOOD - Only your frontend can call it
allow_origins=["https://yourapp.com"]
```

**Why?**
- Any malicious website could call your API
- Could abuse your API (rate limiting, costs)
- Security risk

### 2. **Use Environment Variables**

```python
# ✅ GOOD
allowed_origins = os.getenv("ALLOWED_ORIGINS", "http://localhost:5173").split(",")

# ❌ BAD
allowed_origins = ["https://yourapp.com"]  # Hardcoded
```

**Why?**
- Different origins for dev/staging/production
- Easy to update without code changes
- Supports multiple frontend domains

### 3. **Include All Your Frontend URLs**

```python
# If you have multiple frontends or preview deployments
allowed_origins = [
    "https://yourapp.com",                    # Production
    "https://staging.yourapp.com",            # Staging
    "https://yourapp-*.vercel.app",           # Preview deployments (if supported)
    "http://localhost:5173",                  # Local development
]
```

### 4. **Test CORS in Production**

**Why?**
- CORS only enforced by browser (not curl/Postman)
- Different behavior in dev vs production
- Browser extensions can affect CORS

**How to test:**
1. Open browser DevTools (F12)
2. Go to Network tab
3. Make a request from your frontend
4. Check for CORS errors in console
5. Check response headers for `Access-Control-Allow-Origin`

---

## 🔍 Debugging CORS Issues

### Common Error Messages

**1. "No 'Access-Control-Allow-Origin' header"**
```
Access to fetch at 'https://api.example.com/data' from origin 
'https://app.example.com' has been blocked by CORS policy: 
No 'Access-Control-Allow-Origin' header is present on the requested resource.
```

**Meaning:** Backend didn't send CORS headers

**Fix:** Check backend CORS configuration

---

**2. "Response to preflight request doesn't pass access control check"**
```
Response to preflight request doesn't pass access control check: 
No 'Access-Control-Allow-Origin' header is present on the requested resource.
```

**Meaning:** Preflight (OPTIONS) request failed

**Fix:** Backend must handle OPTIONS requests and return CORS headers

---

**3. "The request client is not a secure context"**
```
The request client is not a secure context and the resource is on a secure origin.
```

**Meaning:** Trying to access HTTPS from HTTP (or vice versa)

**Fix:** Use same protocol (both HTTP or both HTTPS)

---

### Debugging Steps

1. **Check the actual origin**
   ```javascript
   console.log('Origin:', window.location.origin)
   ```

2. **Check what backend expects**
   - Look at `ALLOWED_ORIGINS` environment variable
   - Must match exactly (including protocol, no trailing slash)

3. **Test with curl (bypasses CORS)**
   ```bash
   curl -X POST https://your-backend.com/api/player \
     -H "Content-Type: application/json" \
     -d '{"tag":"#ABC123"}'
   ```
   - If this works, it's a CORS issue
   - If this fails, it's a different problem

4. **Check browser Network tab**
   - Look for OPTIONS request (preflight)
   - Check response headers
   - Look for `Access-Control-Allow-Origin` header

5. **Check backend logs**
   - See if request reaches backend
   - Check for errors in CORS middleware

---

## 🎓 Key Takeaways

1. **CORS is browser security** - Protects users from malicious websites
2. **Only affects browser requests** - curl/Postman don't enforce CORS
3. **Must configure on backend** - Frontend can't fix CORS issues
4. **Exact match required** - `https://app.com` ≠ `https://app.com/`
5. **Test in production** - CORS issues often only appear in production
6. **Environment variables** - Use them for different environments
7. **Never use `*` in production** - Security risk

---

## 💡 Real-World Scenarios

### Scenario 1: Multiple Frontend Apps

You have:
- Web app: `https://app.example.com`
- Mobile app backend: `https://api.example.com`
- Admin panel: `https://admin.example.com`

**Solution:**
```python
allowed_origins = [
    "https://app.example.com",
    "https://admin.example.com",
    # Mobile apps don't need CORS (not browsers)
]
```

### Scenario 2: Preview Deployments

Vercel creates URLs like:
- `https://myapp-abc123.vercel.app`
- `https://myapp-xyz789.vercel.app`

**Solution:**
- Use production domain: `https://myapp.vercel.app`
- Or update CORS for each preview (tedious)
- Or use wildcards if platform supports it

### Scenario 3: Development Team

Team members use:
- `http://localhost:3000`
- `http://localhost:5173`
- `http://127.0.0.1:3000` (different origin!)

**Solution:**
```python
allowed_origins = [
    "http://localhost:3000",
    "http://localhost:5173",
    "http://127.0.0.1:3000",
    "http://127.0.0.1:5173",
]
```

---

## 🚀 Advanced: CORS with Credentials

If you need to send cookies or authentication:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://yourapp.com"],  # Cannot be ["*"]
    allow_credentials=True,                 # Required for cookies
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type", "Authorization"],
)
```

**Frontend:**
```javascript
fetch('https://api.example.com/data', {
    credentials: 'include',  // Send cookies
    headers: {
        'Authorization': 'Bearer token'
    }
})
```

---

## 📚 Further Reading

- [MDN CORS Guide](https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS)
- [FastAPI CORS Documentation](https://fastapi.tiangolo.com/tutorial/cors/)
- [CORS Explained Simply](https://www.codecademy.com/article/what-is-cors)

---

## 🎯 Remember

**CORS is not a bug - it's a security feature!**

When you see a CORS error:
1. Don't panic - it's a configuration issue
2. Check your `ALLOWED_ORIGINS` matches your frontend URL exactly
3. Test in production (CORS only enforced by browsers)
4. Use environment variables for flexibility

This is one of the most common deployment issues, and now you understand it completely! 🎉

