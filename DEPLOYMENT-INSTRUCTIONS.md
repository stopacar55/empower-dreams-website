# How to Deploy the Empower Dreams Website

Hi Paul! Here's how to make the website live at empowerdreams.org.

## Option A: GitHub Pages (Recommended — Free)

### Step 1: Accept the GitHub Invitation
- You should have received an email invitation to collaborate on the repository
- Click the link to accept access to `bsvor/empower-dreams-website`

### Step 2: Enable GitHub Pages
1. Go to https://github.com/bsvor/empower-dreams-website/settings/pages
2. Under **Source**, select **Deploy from a branch**
3. Select the **main** branch and **/ (root)** folder
4. Click **Save**
5. The site will be live within a few minutes at a temporary GitHub URL

### Step 3: Connect Your Custom Domain
1. On the same GitHub Pages settings page, enter your domain (e.g. `empowerdreams.org`) in the **Custom domain** field and click **Save**
2. Go to your domain registrar (wherever you bought empowerdreams.org) and update the DNS settings:

   **For the root domain (empowerdreams.org):**
   Add these A records:
   ```
   185.199.108.153
   185.199.109.153
   185.199.110.153
   185.199.111.153
   ```

   **For www (www.empowerdreams.org):**
   Add a CNAME record:
   ```
   www -> bsvor.github.io
   ```

3. Back on the GitHub Pages settings, check **Enforce HTTPS** (may take a few minutes to become available)

### Step 4: Wait for DNS
- DNS changes can take up to 24-48 hours to propagate, but usually work within an hour
- Once propagated, your site will be live at your domain with HTTPS

## Option B: Netlify (Alternative — Also Free)

1. Go to https://netlify.com and sign up with your GitHub account
2. Click **Add new site** > **Import an existing project**
3. Select the `empower-dreams-website` repository
4. Leave build settings blank (no build command needed)
5. Click **Deploy**
6. Go to **Domain settings** > **Add custom domain** and follow the DNS instructions Netlify provides

## Need Help?

If you run into any issues, feel free to reach out to Brent.
