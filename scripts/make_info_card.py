#!/usr/bin/env python3
import os

def make_info_card():
    """Generate neofetch-style info card SVG with fade-in animation."""
    
    card_data = {
        "Title": "developer.sh",
        "Now": "Building scalable systems",
        "Prev": "Full-stack engineering",
        "Stack": "Python, TypeScript, Go",
        "Highlights": "API design, DevOps, ML"
    }
    
    svg_width = 490
    svg_height = 280
    
    svg_content = f"""<svg viewBox="0 0 {svg_width} {svg_height}" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <style>
      .card-line {{
        font-family: monospace;
        font-size: 13px;
        fill: #ccc;
        opacity: 0;
        animation: slideIn 0.5s ease-out forwards;
      }}
      .card-title {{
        fill: #0ff;
        font-weight: bold;
      }}
      .card-key {{
        fill: #0f0;
      }}
      @keyframes slideIn {{
        from {{
          opacity: 0;
          transform: translateX(-20px);
        }}
        to {{
          opacity: 1;
          transform: translateX(0);
        }}
      }}
    </style>
  </defs>
  <rect x="10" y="10" width="{svg_width - 20}" height="{svg_height - 20}" fill="#1a1a2e" stroke="#0ff" stroke-width="1"/>
"""
    
    y_pos = 30
    line_height = 35
    
    # Title
    svg_content += f'  <text x="20" y="{y_pos}" class="card-line card-title" style="animation-delay: 0s">github.com/yourname</text>\n'
    y_pos += line_height
    
    # Content lines
    lines = [
        ("Now", "Building scalable systems", 0.1),
        ("Prev", "Full-stack engineering", 0.2),
        ("Stack", "Python, TypeScript, Go", 0.3),
        ("Highlights", "API design, DevOps, ML", 0.4),
    ]
    
    for key, value, delay in lines:
        svg_content += f'  <text x="20" y="{y_pos}" class="card-line"><tspan class="card-key">{key:12}</tspan>{value}</text>\n'
        svg_content += f'  <style>.card-line {{ animation-delay: {delay}s; }}</style>\n'
        y_pos += line_height
    
    svg_content += '</svg>'
    
    with open("info-card.svg", "w") as f:
        f.write(svg_content)
    
    print("Saved: info-card.svg")

if __name__ == "__main__":
    make_info_card()