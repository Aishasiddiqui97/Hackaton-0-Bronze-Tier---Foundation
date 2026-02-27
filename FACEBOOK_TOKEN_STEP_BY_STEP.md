# 🔧 Facebook Token Fix - Step by Step Guide

## 🎯 **The Problem**
Your Facebook token expired (Error 190: "The access token could not be decrypted")

## ✅ **The Solution** 
Get a new long-lived Facebook access token in 5 minutes

---

## 📋 **Step-by-Step Instructions**

### **Step 1: Open Facebook Graph API Explorer**
1. Go to: https://developers.facebook.com/tools/explorer/
2. Log in with your Facebook account if needed

### **Step 2: Select Your App**
1. Look for a dropdown that says "Facebook App" or shows an app name
2. Click it and select your app (the one you created for posting)
3. If you don't see your app, you may need to create one first

### **Step 3: Generate Access Token**
1. Look for a button that says "Generate Access Token" or "Get Token"
2. Click it
3. A popup will appear asking for permissions

### **Step 4: Select Permissions**
In the permissions popup, make sure these are checked:
- ✅ `pages_manage_posts` (required for posting)
- ✅ `pages_read_engagement` (for reading page info)
- ✅ `pages_show_list` (to see your pages)

### **Step 5: Generate and Copy Token**
1. Click "Generate Access Token" or "Continue"
2. Facebook will show you a long token (starts with something like `EAAVLp...`)
3. **IMPORTANT**: Copy the ENTIRE token - it's very long (200+ characters)

### **Step 6: Use Our Fix Script**
```powershell
python facebook_quick_token_fix.py
```
1. Paste your token when prompted
2. The script will test it and update your .env file automatically

---

## 🚨 **Common Issues & Solutions**

### **Issue 1: "Invalid Client ID"**
**Problem**: You entered App ID instead of App Secret
**Solution**: Use the simple fix script instead (no App Secret needed)

### **Issue 2: "Token too short"**
**Problem**: You didn't copy the complete token
**Solution**: Make sure to copy the ENTIRE token from Facebook

### **Issue 3: "App not found"**
**Problem**: You don't have a Facebook app set up
**Solution**: Create a Facebook app first:
1. Go to: https://developers.facebook.com/apps/
2. Click "Create App"
3. Choose "Business" type
4. Add your page to the app

### **Issue 4: "Permission denied"**
**Problem**: Your app doesn't have permission to post to your page
**Solution**: 
1. Go to your Facebook page
2. Settings → Page roles
3. Add your app as a page admin

---

## 🔧 **Alternative: Manual Token Update**

If the script doesn't work, manually update your `.env` file:

1. Open `.env` file in a text editor
2. Find the line: `FACEBOOK_ACCESS_TOKEN=...`
3. Replace the old token with your new token:
   ```
   FACEBOOK_ACCESS_TOKEN=EAAVLpJsehhwBQ5tEZBzLeNXK60ZCGZABd2RP5g1gxr9FaaykIqBGK00MxiQbc5ES71ZCcgGZBKlZA0qOvopM08F2ZA5swT4hZBQqBOhnfeZB9ujJWhqkNWZBOQ36qpQ5mELFZC40YdDEYM4dZAP8BeANlE3aAAxZCD6Fjd9mwSW50tUK2VfHiJIydA4bwqEo5uSEmM5MYEFfGeioSWXR6FOFlJPjJuZBkJNYOfceSRwbhPFACEBOOK
   ```
4. Save the file

---

## ✅ **Test Your Fix**

After updating the token:

```powershell
# Test Facebook posting
python api_facebook_poster_fixed.py

# If successful, restart your system
python gold_tier_autonomous.py
```

---

## 📞 **Still Having Issues?**

### **Quick Diagnostics:**
```powershell
# Test current token
python facebook_quick_token_fix.py

# Check system status
python verify_silver_tier.py
```

### **Token Lifespan:**
- **Short-lived tokens**: 1-2 hours (what you get initially)
- **Long-lived tokens**: 60 days (what we want)
- **Page tokens**: Can be permanent (best for automation)

### **Pro Tip:**
For permanent tokens, use a Page Access Token instead of User Access Token:
1. In Graph API Explorer, change token type to "Page Access Token"
2. Select your page
3. This token won't expire as long as your app has permissions

---

## 🎉 **Success Checklist**

- [ ] Got new token from Facebook Graph API Explorer
- [ ] Token is 200+ characters long
- [ ] Tested token with our script
- [ ] Updated .env file
- [ ] Facebook posting works
- [ ] System running without errors

**Once complete, your Facebook posting will work perfectly! 🚀**

---

## 📋 **Quick Reference**

**Facebook Graph API Explorer**: https://developers.facebook.com/tools/explorer/
**Required Permissions**: `pages_manage_posts`, `pages_read_engagement`, `pages_show_list`
**Token Format**: Starts with `EAAVLp...` and is 200+ characters
**Fix Script**: `python facebook_quick_token_fix.py`
**Test Script**: `python api_facebook_poster_fixed.py`