# Animated GitHub Profile

<div align="center">

<h3><code>username@github ~ $ ./contributions.sh</code></h3>

![Contributions](./contrib-heatmap.svg)

<br><br>

<h3><code>username@github ~ $ whoami</code></h3>

<table>
  <tr>
    <td valign="top"><img src="./avi-ascii.svg" width="370" /></td>
    <td valign="top"><img src="./info-card.svg" width="490" /></td>
  </tr>
</table>

</div>

## Setup

Replace `YOURUSERNAME` with your GitHub username, then:

```bash
gh repo create YOURUSERNAME --public --clone
cd YOURUSERNAME
mkdir -p scripts data .github/workflows
pip install -r scripts/requirements.txt
python scripts/prep_photo.py your-photo.jpg
python scripts/make_ascii_svg.py
python scripts/make_info_card.py
python scripts/fetch_contributions.py YOURUSERNAME
python scripts/render_heatmap_svg.py
```

Commit and push all SVG files to GitHub.

## GitHub Actions Daily Refresh

Create `.github/workflows/update-heatmap.yml`:

```yaml
name: Update Contribution Heatmap
on:
  schedule:
    - cron: '0 0 * * *'
  workflow_dispatch:

jobs:
  update:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - run: |
          pip install requests beautifulsoup4
          python scripts/fetch_contributions.py ${{ github.repository_owner }}
          python scripts/render_heatmap_svg.py
      - uses: stefanzweifel/git-auto-commit-action@v4
        with:
          commit_message: "chore: update contribution heatmap"
          file_pattern: "contrib-heatmap.svg data/contributions.json"
```

## Notes

- All animations are SVG/CSS based, no JavaScript needed
- GitHub strips `<script>` tags but renders embedded SVGs with animations
- Use `<h3>` for section titles to avoid full-width underlines
- Align SVG widths: `370 + 490 = 860` (heatmap width)
- `<br><br>` provides vertical spacing (inline styles don't work on GitHub)