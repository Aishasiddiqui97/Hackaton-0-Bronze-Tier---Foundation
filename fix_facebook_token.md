# Facebook Access Token Fix Guide

## Problem
Your Facebook access token has expired or is invalid.

Error: `"The access token could not be decrypted"`

## Solution: Get New Access Token

### Method 1: Facebook Graph API Explorer (Easiest)

1. Go to: https://developers.facebook.com/tools/explorer/

2. Click "Generate Access Token"

3. Select permissions:
   - `pages_manage_posts`
   - `pages_read_engagement`
   - `pages_show_list`

4. Copy the new access token

5. Update `.env` file:
   ```env
   FACEBOOK_ACCESS_TOKEN=<your_new_token>
   ```

### Method 2: Get Long-Lived Token (Lasts 60 days)

1. Get short-lived token from Graph Explorer (above)

2. Exchange for long-lived token:
   ```
   https://graph.facebook.com/v18.0/oauth/access_token?
   grant_type=fb_exchange_token&
   client_id=YOUR_APP_ID&
   client_secret=YOUR_APP_SECRET&
   fb_exchange_token=SHORT_LIVED_TOKEN
   ```

3. Copy the long-lived token

4. Update `.env`:
   ```env
   FACEBOOK_ACCESS_TOKEN=<long_lived_token>
   ```

### Method 3: Get Page Access Token (Never Expires)

1. Get your User Access Token (from Method 1 or 2)

2. Get your Page ID:
   ```
   https://graph.facebook.com/v18.0/me/accounts?access_token=USER_TOKEN
   ```

3. Find your page in the response and copy its `access_token`

4. This Page Access Token never expires!

5. Update `.env`:
   ```env
   FACEBOOK_ACCESS_TOKEN=<page_access_token>
   FACEBOOK_PAGE_ID=<your_page_id>
   ```

## Quick Fix Script

Run this to test your new token:

```powershell
python api_facebook_poster.py "03_Posted\History\Facebook_Post_20260225_165309.md"
```

## Verify Token

Check if token is valid:
```
https://graph.facebook.com/v18.0/me?access_token=YOUR_TOKEN
```

Should return your user/page info.

## Common Issues

### Token Expired
- Short-lived tokens expire in 1-2 hours
- Long-lived tokens expire in 60 days
- Page tokens never expire (best option)

### Wrong Permissions
Make sure token has:
- `pages_manage_posts` - To create posts
- `pages_read_engagement` - To read page data

### Wrong Page ID
- Use numeric ID, not URL
- Get from: `https://graph.facebook.com/v18.0/me/accounts`

## Recommended: Use Page Access Token

Page Access Tokens are best because:
- ✅ Never expire
- ✅ Work for posting
- ✅ No refresh needed

Get it from:
```
https://graph.facebook.com/v18.0/YOUR_PAGE_ID?fields=access_token&access_token=USER_TOKEN
```

---

After getting new token, test with:
```powershell
python api_facebook_poster.py
```
