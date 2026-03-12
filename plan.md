# Plan: Swap Site Domains

## Summary

Swap the two domains so that:
- **This site** (AIRS framework docs) uses `airuntimesecurity.io` (currently `.co.za`)
- **Training/learning site** uses `airuntimesecurity.co.za` (currently `.io`)

## Files to change

### 1. GitHub Pages CNAME
**File:** `docs/CNAME`
**Change:** `airuntimesecurity.co.za` → `airuntimesecurity.io`

### 2. MkDocs main config
**File:** `mkdocs.yml` (line 2)
**Change:** `site_url: https://airuntimesecurity.co.za/` → `site_url: https://airuntimesecurity.io/`

### 3. MkDocs PDF config
**File:** `mkdocs-pdf.yml` (line 6)
**Change:** `site_url: https://airuntimesecurity.co.za/` → `site_url: https://airuntimesecurity.io/`

### 4. Security.txt
**File:** `docs/.well-known/security.txt`
**Change:** All `airuntimesecurity.co.za` URLs → `airuntimesecurity.io`

### 5. robots.txt
**File:** `docs/robots.txt` (line 16)
**Change:** Sitemap URL from `airuntimesecurity.co.za` → `airuntimesecurity.io`

### 6. Homepage learning callout
**File:** `docs/README.md` (line ~117)
**Change:** References to the learning site from `airuntimesecurity.io` → `airuntimesecurity.co.za`
(The learning site callout text and button link both need updating)

### 7. MASO page learning callout
**File:** `docs/maso/README.md` (line ~279)
**Change:** References to the learning site from `airuntimesecurity.io` → `airuntimesecurity.co.za`
(The learning site callout text and button link both need updating)

### 8. Author attribution
**File:** `docs/what-is-ai-runtime-security.md` (line ~89)
**Change:** `airuntimesecurity.co.za` → `airuntimesecurity.io` (this links to the main site, which will now be `.io`)

### 9. Position paper reference
**File:** `docs/insights/why-containment-beats-evaluation.md` (line ~9)
**Change:** `airuntimesecurity.co.za` → `airuntimesecurity.io` (this links to the main site)

## Out of scope (manual steps for the user)
- DNS record updates at the domain registrar
- GitHub Pages custom domain settings in repo Settings
- Any configuration on the training/learning site itself
