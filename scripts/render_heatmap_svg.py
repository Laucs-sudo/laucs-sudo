#!/usr/bin/env python3
import json
from datetime import datetime, timedelta

def render_heatmap_svg():
    """Render contribution heatmap from data/contributions.json as animated SVG."""
    
    try:
        with open('data/contributions.json', 'r') as f:
            data = json.load(f)
    except FileNotFoundError:
        print("data/contributions.json not found. Run fetch_contributions.py first.")
        return
    
    contributions = data['contributions']
    
    # GitHub-ish green palette: level 0-5
    palette = ["#161b22", "#0e4429", "#006d32", "#26a641", "#39d353", "#69f0a0"]
    
    # Map contributions to levels
    if contributions:
        max_count = max(c['count'] for c in contributions)
        if max_count == 0:
            max_count = 1
    else:
        max_count = 1
    
    def get_color(count):
        if count == 0:
            return palette[0]
        level = min(5, int((count / max_count) * 5))
        return palette[level]
    
    # Build 53-week x 7-day grid
    box_size = 12
    gap = 2
    cell_size = box_size + gap
    
    weeks = 53
    days = 7
    
    svg_width = weeks * cell_size + 60
    svg_height = days * cell_size + 80
    
    svg_content = f"""<svg viewBox="0 0 {svg_width} {svg_height}" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <style>
      .heatmap-box {{
        opacity: 0;
        animation: slideIn 0.6s ease-out forwards;
      }}
      .heatmap-label {{
        font-family: monospace;
        font-size: 11px;
        fill: #888;
      }}
      @keyframes slideIn {{
        from {{
          opacity: 0;
          transform: translateY(-10px);
        }}
        to {{
          opacity: 1;
          transform: translateY(0);
        }}
      }}
    </style>
  </defs>
  <rect width="{svg_width}" height="{svg_height}" fill="#0d1117"/>
"""
    
    # Title
    svg_content += f'  <text x="30" y="25" class="heatmap-label" style="font-size: 14px; fill: #ccc">Contributions in the last year</text>\n'
    
    # Render boxes
    x_offset = 40
    y_offset = 45
    
    contribution_dict = {c['date']: c['count'] for c in contributions}
    
    box_index = 0
    for week in range(weeks):
        for day in range(days):
            x = x_offset + week * cell_size
            y = y_offset + day * cell_size
            
            # Get date for this cell
            date_obj = datetime.now() - timedelta(weeks=(weeks - week - 1), days=(6 - day))
            date_str = date_obj.strftime('%Y-%m-%d')
            
            count = contribution_dict.get(date_str, 0)
            color = get_color(count)
            
            delay = (week + day) * 0.02
            svg_content += f'  <rect x="{x}" y="{y}" width="{box_size}" height="{box_size}" fill="{color}" rx="2" class="heatmap-box" style="animation-delay: {delay}s" title="{count} contributions"/>\n'
            
            box_index += 1
    
    # Legend
    legend_y = y_offset + days * cell_size + 20
    svg_content += f'  <text x="40" y="{legend_y}" class="heatmap-label">Less</text>\n'
    
    for i, color in enumerate(palette):
        legend_x = 80 + i * (box_size + 4)
        svg_content += f'  <rect x="{legend_x}" y="{legend_y - box_size}" width="{box_size}" height="{box_size}" fill="{color}" rx="1"/>\n'
    
    svg_content += f'  <text x="{80 + len(palette) * (box_size + 4) + 10}" y="{legend_y}" class="heatmap-label">More</text>\n'
    
    # Stats footer
    total = data.get('total_contributions', 0)
    streak = data.get('current_streak', 0)
    svg_content += f'  <text x="40" y="{legend_y + 30}" class="heatmap-label" style="font-size: 12px">{total:,} contributions in the last year</text>\n'
    svg_content += f'  <text x="40" y="{legend_y + 50}" class="heatmap-label" style="font-size: 11px">Current streak: {streak} days</text>\n'
    
    svg_content += '</svg>'
    
    with open('contrib-heatmap.svg', 'w') as f:
        f.write(svg_content)
    
    print(f"Saved: contrib-heatmap.svg ({total} contributions)")

if __name__ == "__main__":
    render_heatmap_svg()