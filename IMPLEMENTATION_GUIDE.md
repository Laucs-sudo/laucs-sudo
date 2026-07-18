# Animated GitHub Profile Implementation Guide

## Overview

This creates a terminal-style GitHub profile with three animated SVG components updated daily via GitHub Actions:

1. **avi-ascii.svg** - Photo converted to ASCII art that types itself
2. **info-card.svg** - Neofetch-style info panel (role, stack, highlights)
3. **contrib-heatmap.svg** - 53-week contribution calendar with real data

All animations use SVG/CSS only. No JavaScript. No third-party stats services. No GitHub token needed for contribution scraping.

## File Structure

```
your-username/
├── scripts/
│   ├── requirements.txt
│   ├── prep_photo.py           (local: convert image to ASCII-ready)
│   ├── make_ascii_svg.py       (local: photo → avi-ascii.svg)
│   ├── make_info_card.py       (local: generate info-card.svg)
│   ├── fetch_contributions.py  (daily: scrape GitHub contribution data)
│   └── render_heatmap_svg.py   (daily: data → contrib-heatmap.svg)
├── data/
│   └── contributions.json       (generated daily)
├── .github/workflows/
│   └── update-heatmap.yml      (GitHub Actions: runs daily at midnight UTC)
├── README.md                   (profile page)
├── avi-ascii.svg              (generated: commit this)
├── info-card.svg              (generated: commit this)
└── contrib-heatmap.svg        (generated: commit this)
```

## Step 1: Create the Profile Repository

GitHub gives every account one special repo: its own username. This is where your README renders as your profile:

```bash
gh repo create YOURUSERNAME --public --clone
cd YOURUSERNAME
mkdir -p scripts data .github/workflows
```

Replace `YOURUSERNAME` with your actual GitHub username.

## Step 2: Prepare Python Scripts

Copy all scripts from `scripts/` folder:
- `prep_photo.py`
- `make_ascii_svg.py`
- `make_info_card.py`
- `fetch_contributions.py`
- `render_heatmap_svg.py`
- `requirements.txt`

```bash
pip install -r scripts/requirements.txt
```

Optional: Only needed for local ASCII art generation:
- `pillow`
- `numpy`
- `opencv-python`
- `rembg`

Required for daily automation:
- `requests`
- `beautifulsoup4`

## Step 3: Generate Static SVGs (Local Only)

Run these once to create your ASCII portrait and info card.

### 3a. Prepare your photo

```bash
python scripts/prep_photo.py your-photo.jpg
```

Produces: `source-prepped.png` (background removed, contrast boosted, composited on white)

### 3b. Convert to ASCII SVG

```bash
python scripts/make_ascii_svg.py
```

Produces: `avi-ascii.svg` (typing animation, monochrome, ~100x53 characters)

Edit `make_ascii_svg.py` to customize:
- Character width: change `width=100` parameter
- Animation speed: change `0.03` delay multiplier
- Text color: change `#999` fill color
- Line height scaling: adjust `char_height` parameter

### 3c. Generate info card

```bash
python scripts/make_info_card.py
```

Produces: `info-card.svg` (neofetch-style panel)

Edit `make_info_card.py` to customize:
- Card data (Now, Prev, Stack, Highlights)
- Animation delays
- Colors: `#0ff` (cyan), `#0f0` (green), `#ccc` (text)

## Step 4: Set Up Daily Contribution Fetching

Copy `.github/workflows/update-heatmap.yml` to your repo:

```bash
cp update-heatmap.yml .github/workflows/
```

This workflow:
- Runs daily at midnight UTC (adjust cron if needed)
- Scrapes your public contribution calendar from GitHub
- Re-renders the heatmap with fresh data
- Auto-commits and pushes changes

No GitHub token required. Public contribution data is always accessible.

### First manual run

```bash
python scripts/fetch_contributions.py YOURUSERNAME
python scripts/render_heatmap_svg.py
```

Produces:
- `data/contributions.json` (contribution counts per day)
- `contrib-heatmap.svg` (animated heatmap with stats footer)

## Step 5: Customize the README

Copy `README.md` and edit:

```bash
cp README.md ./
```

Replace placeholders:
- `username@github` in `<h3>` tags
- Customize intro text if desired
- Adjust table column widths if needed (must sum to heatmap width: 860)

GitHub markdown quirks:
- No inline `style=` attributes (stripped)
- Use `<br><br>` for vertical spacing
- Use `<h3>` for section titles (avoids underline)
- `<table>` with `valign="top"` for side-by-side images

## Step 6: Commit and Push

```bash
git add scripts/ data/ .github/workflows/ *.svg README.md
git commit -m "feat: animated github profile"
git push origin main
```

Your README should now render at your GitHub profile with all three animated SVGs.

## Customization

### ASCII Art
- Adjust character ramp in `make_ascii_svg.py`: ` .`:-=+*cs#%@`
- Resize image: change `width=100` (larger = more detail, slower animation)
- Animation speed: scale `0.03` delay multiplier
- Colors: modify `fill="#999"`

### Info Card
- Edit `card_data` dict in `make_info_card.py`
- Adjust animation delays (scale all by same factor for consistency)
- Colors: `#0ff` (accent), `#0f0` (key), `#ccc` (value)

### Heatmap
- Contribution palette in `render_heatmap_svg.py`:
  ```python
  palette = ["#161b22", "#0e4429", "#006d32", "#26a641", "#39d353", "#69f0a0"]
  ```
- Box size: change `box_size = 12`
- Gap between boxes: change `gap = 2`
- Stats text: edit footer text and styling

## Troubleshooting

**SVGs don't animate**
- Ensure animations use CSS or SMIL (no JavaScript)
- GitHub only supports CSS `@keyframes` and SMIL `<animate>`
- Test locally: open SVG in browser to verify

**Contribution data not updating**
- Check GitHub Actions logs: repo → Actions tab
- Ensure `fetch_contributions.py` runs with correct username
- Verify `data/contributions.json` is in gitignore or committed

**ASCII art looks low-quality**
- Photo needs good contrast: use well-lit headshots
- Run `prep_photo.py` with your image: rembg removes background, CLAHE boosts local contrast
- Adjust character width: smaller = less detail, faster animation

**Markdown layout breaks**
- Keep heatmap width = side-by-side column widths (860 = 370 + 490)
- Use `<br><br>` not markdown `---` for spacing
- Use `<h3>` not `#` for section titles

## Performance Notes

- ASCII art animation: ~3-5 seconds (depends on grid size)
- Info card fade-in: ~2 seconds
- Heatmap reveal: ~3-4 seconds
- Total: ~8-12 seconds to see full profile load

Adjust delays by scaling the `delay = i * 0.03` multipliers down for faster, up for slower.

## GitHub Actions Cron

Default: `'0 0 * * *'` = midnight UTC daily

Other common schedules:
- `'0 9 * * *'` = 9 AM UTC
- `'0 */6 * * *'` = Every 6 hours
- `'0 0 * * 1'` = Mondays at midnight

Set to your timezone by adding hours offset to the cron minute/hour fields.

## What's Happening

1. **Local setup** (one-time):
   - Photo → ASCII via OpenCV/PIL
   - Info card SVG hand-authored
   - Both committed to repo

2. **Daily automation** (GitHub Actions):
   - Fetch your public contribution calendar (no token)
   - Parse HTML, extract day-by-day counts
   - Render as animated heatmap SVG
   - Auto-commit and push

3. **Profile rendering** (GitHub):
   - README displays three embedded SVGs
   - GitHub plays SVG animations on page load
   - Heatmap stays fresh via daily CI

## Files Included

- `prep_photo.py` - Image prep
- `make_ascii_svg.py` - ASCII conversion
- `make_info_card.py` - Info card generation
- `fetch_contributions.py` - Contribution scraper
- `render_heatmap_svg.py` - Heatmap rendering
- `update-heatmap.yml` - GitHub Actions workflow
- `requirements.txt` - Python dependencies
- `README.md` - Profile template
- `IMPLEMENTATION_GUIDE.md` - This file