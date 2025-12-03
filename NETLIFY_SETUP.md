# Netlify Setup Guide for RDG Translation Corrections

This guide walks you through setting up the serverless function to securely submit translation corrections to GitHub.

## Overview

**What we're setting up:**
- Netlify serverless function that receives corrections from tmaster forms
- Secure GitHub API integration to commit corrections to your repository
- Backup download functionality if GitHub submission fails

## Prerequisites

- GitHub account with access to the `rdgtrans` repository
- GitHub Personal Access Token with repo write permissions
- Free Netlify account

---

## Step 1: Create GitHub Personal Access Token

1. Go to GitHub Settings → Developer settings → Personal access tokens → Tokens (classic)
   - Direct link: https://github.com/settings/tokens

2. Click "Generate new token" → "Generate new token (classic)"

3. Configure the token:
   - **Note:** `RDG Translation Corrections API`
   - **Expiration:** Choose expiration (recommend 90 days or 1 year)
   - **Scopes:** Check `repo` (Full control of private repositories)

4. Click "Generate token"

5. **IMPORTANT:** Copy the token immediately and save it securely
   - Format: `ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`
   - You won't be able to see it again!

---

## Step 2: Create Netlify Account

1. Go to https://netlify.com

2. Click "Sign up" → "Sign up with GitHub"

3. Authorize Netlify to access your GitHub account

4. Complete account creation (no credit card required for free tier)

---

## Step 3: Deploy to Netlify

### Option A: Deploy via Netlify Dashboard (Recommended)

1. Log in to Netlify dashboard

2. Click "Add new site" → "Import an existing project"

3. Choose "Deploy with GitHub"

4. Authorize Netlify to access your repositories (if not already done)

5. Select the `rdgtrans` repository

6. Configure build settings:
   - **Branch to deploy:** `main`
   - **Build command:** Leave empty (or use: `echo 'No build required'`)
   - **Publish directory:** `.`
   - **Functions directory:** `netlify/functions`

7. Click "Deploy site"

8. Wait for deployment to complete (should take 1-2 minutes)

### Option B: Deploy via Netlify CLI

```bash
# Install Netlify CLI
npm install -g netlify-cli

# Navigate to your repository
cd /home/scott/gitrepos/rdgtrans

# Login to Netlify
netlify login

# Initialize new site
netlify init

# Follow prompts:
# - Create & configure a new site
# - Choose team
# - Site name: rdgtrans (or your preferred name)
# - Build command: (leave empty)
# - Directory to deploy: .
# - Netlify functions folder: netlify/functions

# Deploy
netlify deploy --prod
```

---

## Step 4: Configure Environment Variables in Netlify

1. In Netlify dashboard, go to your site

2. Navigate to: **Site settings** → **Environment variables**

3. Add the following variables:

   **Variable 1:**
   - **Key:** `GITHUB_TOKEN`
   - **Value:** Your GitHub Personal Access Token (from Step 1)
   - **Scopes:** Check all scopes (Production, Deploy previews, Branch deploys)

   **Variable 2:**
   - **Key:** `GITHUB_OWNER`
   - **Value:** `scott009` (or your GitHub username)
   - **Scopes:** Check all scopes

   **Variable 3:**
   - **Key:** `GITHUB_REPO`
   - **Value:** `rdgtrans`
   - **Scopes:** Check all scopes

4. Click "Save" for each variable

5. **Trigger a redeploy** to apply environment variables:
   - Go to **Deploys** tab
   - Click "Trigger deploy" → "Deploy site"

---

## Step 5: Get Your Function URL

1. After deployment completes, note your site URL:
   - Format: `https://YOUR-SITE-NAME.netlify.app`
   - Example: `https://rdgtrans.netlify.app`

2. Your function URL will be:
   ```
   https://YOUR-SITE-NAME.netlify.app/.netlify/functions/submit-corrections
   ```

3. **Optional:** Customize your site name:
   - Go to **Site settings** → **Site details**
   - Click "Change site name"
   - Enter preferred name (e.g., `rdgtrans`, `rdg-translations`)

---

## Step 6: Update HTML Files with Function URL

You need to update the function URL in two places:

### A. Update submit-handler.js

Edit: `netlify/submit-handler.js`

Replace:
```javascript
const NETLIFY_FUNCTION_URL = 'https://YOUR-SITE-NAME.netlify.app/.netlify/functions/submit-corrections';
```

With your actual URL:
```javascript
const NETLIFY_FUNCTION_URL = 'https://rdgtrans.netlify.app/.netlify/functions/submit-corrections';
```

### B. Update tmaster HTML files

Run the Python script to update all tmaster files:

```bash
cd /home/scott/gitrepos/rdgtrans
python3 py/update_tmaster_submission.py
```

Then manually update the NETLIFY_FUNCTION_URL in each file, OR:

Create a configuration file that can be included in all HTML files.

---

## Step 7: Host submit-handler.js

The tmaster HTML files need to load `submit-handler.js`. You have two options:

### Option A: Host on GitHub Pages (Recommended)

1. Copy `submit-handler.js` to your GitHub Pages docs folder:
   ```bash
   cp /home/scott/gitrepos/rdgtrans/netlify/submit-handler.js \
      /mnt/c/Users/scott/Documents/RecoveryDharma/RDGBook/output_V1/docs/
   ```

2. Update the script URL in tmaster HTML files to:
   ```html
   <script src="submit-handler.js"></script>
   ```

### Option B: Host on Netlify

1. Create a `public` folder in your repo and copy the script there

2. Update netlify.toml to publish the public folder

3. Reference the script from your Netlify domain

---

## Step 8: Test the Function

### Test via curl (from terminal)

```bash
curl -X POST https://YOUR-SITE-NAME.netlify.app/.netlify/functions/submit-corrections \
  -H "Content-Type: application/json" \
  -d '{
    "metadata": {
      "language": "test",
      "editor": "Test User",
      "editor_email": "test@example.com",
      "timestamp": "2024-12-02T12:00:00Z",
      "source_file": "test.md",
      "total_items": 1,
      "edited_items": 1,
      "chapters_covered": [1]
    },
    "corrections": [{
      "id": "test-1",
      "chapter": 1,
      "original": "Original text",
      "edited": "Edited text",
      "status_update": "corrected"
    }]
  }'
```

**Expected response:**
```json
{
  "success": true,
  "message": "Successfully saved 1 corrections",
  "file": "corrections/test_2024-12-02_12-00-00.json",
  "commit_url": "https://github.com/scott009/rdgtrans/commit/...",
  "download_url": "https://raw.githubusercontent.com/..."
}
```

### Test via Browser

1. Open one of your tmaster HTML files in a browser

2. Make a small edit to a paragraph

3. Fill in reviewer information

4. Click "Submit"

5. Check for success message and verify file appears in GitHub repo

---

## Step 9: Create corrections Folder in GitHub

The function saves files to `corrections/` folder in your repo.

1. Create the folder:
   ```bash
   cd /home/scott/gitrepos/rdgtrans
   mkdir -p corrections
   echo "# Translation Corrections" > corrections/README.md
   git add corrections/
   git commit -m "Add corrections folder for submitted translations"
   git push
   ```

---

## Troubleshooting

### Function returns 500 error

**Check Netlify function logs:**
1. Go to Netlify dashboard → Functions
2. Click on `submit-corrections`
3. Check logs for errors

**Common issues:**
- `GITHUB_TOKEN` not set or invalid
- Token doesn't have `repo` permissions
- Repository name incorrect

### CORS errors in browser

**Symptoms:** Error in browser console: `Access to fetch blocked by CORS policy`

**Fix:** CORS headers should already be configured in the function. If still seeing errors:
1. Check netlify.toml has correct headers
2. Redeploy the function

### File not appearing in GitHub

**Check:**
1. Verify branch name is `main` (not `master`)
2. Check repository name in environment variables
3. Look at function logs in Netlify
4. Verify GitHub token has write permissions

---

## Security Notes

- ✅ **DO:** Store GITHUB_TOKEN in Netlify environment variables
- ❌ **DON'T:** Put GITHUB_TOKEN in code or commit to Git
- ✅ **DO:** Use token with minimal required permissions (just `repo`)
- ❌ **DON'T:** Share your GitHub token with anyone
- ✅ **DO:** Rotate token periodically (every 90 days recommended)

---

## Monitoring

### View submitted corrections

All corrections are saved to: `https://github.com/scott009/rdgtrans/tree/main/corrections`

### View function activity

Netlify Dashboard → Functions → submit-corrections → Function log

### Set up notifications

Netlify can notify you via:
- Email when deploys succeed/fail
- Slack/Discord webhooks for function errors

---

## Cost

- **Netlify Free Tier:**
  - 125,000 function requests/month
  - 100 hours function runtime/month
  - More than enough for this use case

- **GitHub:** Free for public and private repos

**Total cost: $0** ✅

---

## Next Steps

After setup is complete:

1. Test with one language (Thai recommended)
2. Verify corrections appear in GitHub repo
3. Roll out to all languages
4. Document the process for reviewers
5. Set up a workflow to process submitted corrections

---

## Support

If you encounter issues:

1. Check Netlify function logs
2. Verify environment variables are set correctly
3. Test function directly with curl
4. Check GitHub token permissions

For more help:
- Netlify Docs: https://docs.netlify.com/functions/overview/
- GitHub API Docs: https://docs.github.com/en/rest
