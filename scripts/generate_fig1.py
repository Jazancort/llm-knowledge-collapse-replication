import os
import sys
from pathlib import Path
from playwright.sync_api import sync_playwright
import fitz

BASE_DIR = Path(r"G:\Lab\Labcity\LLM\Artigo\Paradoxo - springer\Paradoxo\llm-knowledge-collapse (paper)")

HTML_CONTENT = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<style>
  @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
  
  @page {
    size: 900pt 336pt;
    margin: 0;
  }

  * {
    box-sizing: border-box;
    margin: 0;
    padding: 0;
  }

  body {
    width: 900px;
    height: 336px;
    background: #ffffff;
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    color: #111827;
    position: relative;
    overflow: hidden;
    -webkit-font-smoothing: antialiased;
  }

  /* SVG connectors layer */
  .connectors {
    position: absolute;
    top: 0;
    left: 0;
    width: 900px;
    height: 336px;
    pointer-events: none;
    z-index: 1;
  }

  /* Grid container for cards */
  .grid {
    position: absolute;
    top: 0;
    left: 0;
    width: 900px;
    height: 336px;
    z-index: 2;
  }

  /* Card base */
  .card {
    position: absolute;
    width: 254px;
    height: 144px;
    background: #ffffff;
    border-radius: 8px;
    border: 1.5px solid #e5e7eb;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
    display: flex;
    flex-direction: column;
    overflow: hidden;
  }

  /* Positions */
  .card-1 { left: 32px; top: 12px; border-top: 3.5px solid #0072b2; }
  .card-2 { left: 323px; top: 12px; border-top: 3.5px solid #009e73; }
  .card-3 { left: 614px; top: 12px; border-top: 3.5px solid #e69f00; }
  .card-4 { left: 32px; top: 180px; border-top: 3.5px solid #d55e00; }
  .card-5 { left: 323px; top: 180px; border-top: 3.5px solid #cc79a7; }
  .card-6 { left: 614px; top: 180px; border-top: 3.5px solid #56b4e9; }

  /* Header */
  .card-header {
    display: flex;
    align-items: center;
    gap: 8px;
    padding: 8px 12px 6px;
  }

  .badge {
    width: 20px;
    height: 20px;
    border-radius: 50%;
    color: #ffffff;
    font-size: 11px;
    font-weight: 800;
    display: flex;
    align-items: center;
    justify-content: center;
    flex-shrink: 0;
  }

  .b1 { background: #0072b2; }
  .b2 { background: #009e73; }
  .b3 { background: #e69f00; }
  .b4 { background: #d55e00; }
  .b5 { background: #cc79a7; }
  .b6 { background: #56b4e9; }

  .title {
    font-size: 12.5px;
    font-weight: 700;
    color: #111827;
    letter-spacing: -0.01em;
  }

  /* Body list */
  .card-body {
    padding: 2px 12px 8px;
    display: flex;
    flex-direction: column;
    gap: 5px;
    flex: 1;
    justify-content: flex-start;
  }

  .item {
    display: flex;
    align-items: flex-start;
    gap: 6px;
    font-size: 9.8px;
    line-height: 1.35;
    color: #374151;
  }

  .bullet {
    width: 4.5px;
    height: 4.5px;
    border-radius: 50%;
    margin-top: 4.5px;
    flex-shrink: 0;
  }

  .bul1 { background: #0072b2; }
  .bul2 { background: #009e73; }
  .bul3 { background: #e69f00; }
  .bul4 { background: #d55e00; }
  .bul5 { background: #cc79a7; }
  .bul6 { background: #56b4e9; }

  .item strong {
    font-weight: 600;
    color: #111827;
  }

  /* Loop box in Card 2 */
  .loop-box {
    margin-top: 3px;
    background: #f3f4f6;
    border: 1px solid #e5e7eb;
    border-radius: 4px;
    padding: 2px 6px;
    font-size: 9px;
    font-style: italic;
    color: #4b5563;
    text-align: center;
  }

  /* Regimes in Card 5 */
  .regimes {
    display: flex;
    flex-direction: column;
    gap: 5px;
    margin-top: 2px;
  }

  .regime-pill {
    padding: 3px 7px;
    border-radius: 4px;
    font-size: 8.8px;
    font-weight: 500;
    display: flex;
    align-items: center;
    border: 1px solid;
    white-space: nowrap;
  }

  .reg-homeo {
    background: #ecfdf5;
    border-color: #a7f3d0;
    color: #065f46;
  }
  .reg-homeo strong { font-weight: 700; color: #047857; margin-right: 4px; }

  .reg-bounded {
    background: #fefce8;
    border-color: #fde047;
    color: #854d0e;
  }
  .reg-bounded strong { font-weight: 700; color: #a16207; margin-right: 4px; }

  .reg-deg {
    background: #fef2f2;
    border-color: #fecaca;
    color: #991b1b;
  }
  .reg-deg strong { font-weight: 700; color: #b91c1c; margin-right: 4px; }

</style>
</head>
<body>

  <!-- SVG Connectors Layer -->
  <svg class="connectors" viewBox="0 0 900 336">
    <defs>
      <marker id="arrow" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
        <path d="M 0 1.5 L 8 5 L 0 8.5 z" fill="#6b7280"/>
      </marker>
      <marker id="arrow-down" viewBox="0 0 10 10" refX="5" refY="6" markerWidth="6" markerHeight="6" orient="auto">
        <path d="M 1.5 0 L 5 8 L 8.5 0 z" fill="#6b7280"/>
      </marker>
    </defs>

    <!-- Arrow 1 -> 2 -->
    <line x1="289" y1="84" x2="317" y2="84" stroke="#6b7280" stroke-width="1.8" marker-end="url(#arrow)" />

    <!-- Arrow 2 -> 3 -->
    <line x1="580" y1="84" x2="608" y2="84" stroke="#6b7280" stroke-width="1.8" marker-end="url(#arrow)" />

    <!-- U-turn Connector 3 -> 4 -->
    <!-- Starts at bottom of Card 3 (x=741, y=156), goes down to y=168, left to x=159, down to Card 4 (y=176) -->
    <path d="M 741 156 L 741 168 L 159 168 L 159 176" fill="none" stroke="#6b7280" stroke-width="1.8" marker-end="url(#arrow-down)" stroke-linejoin="round" />

    <!-- Arrow 4 -> 5 -->
    <line x1="289" y1="252" x2="317" y2="252" stroke="#6b7280" stroke-width="1.8" marker-end="url(#arrow)" />

    <!-- Arrow 5 -> 6 -->
    <line x1="580" y1="252" x2="608" y2="252" stroke="#6b7280" stroke-width="1.8" marker-end="url(#arrow)" />
  </svg>

  <div class="grid">
    <!-- Card 1 -->
    <div class="card card-1">
      <div class="card-header">
        <div class="badge b1">1</div>
        <div class="title">Data Preparation</div>
      </div>
      <div class="card-body">
        <div class="item">
          <div class="bullet bul1"></div>
          <div><strong>TriviaQA</strong> rc.nocontext</div>
        </div>
        <div class="item">
          <div class="bullet bul1"></div>
          <div><strong>2,000 train</strong> / 200 eval questions</div>
        </div>
        <div class="item">
          <div class="bullet bul1"></div>
          <div><strong>K&#8320; factual baseline</strong> (held-out)</div>
        </div>
        <div class="item">
          <div class="bullet bul1"></div>
          <div>Bidirectional substring matching</div>
        </div>
      </div>
    </div>

    <!-- Card 2 -->
    <div class="card card-2">
      <div class="card-header">
        <div class="badge b2">2</div>
        <div class="title">Recursive Training</div>
      </div>
      <div class="card-body">
        <div class="item">
          <div class="bullet bul2"></div>
          <div><strong>QLoRA</strong> 4-bit NF4 / FFT</div>
        </div>
        <div class="item">
          <div class="bullet bul2"></div>
          <div>Fresh adapter each generation</div>
        </div>
        <div class="item">
          <div class="bullet bul2"></div>
          <div><strong>10 generations</strong> G&#8321; &rarr; G&#8321;&#8320;</div>
        </div>
        <div class="item">
          <div class="bullet bul2"></div>
          <div>3 backbones: Qwen, Gemma 3, 4</div>
        </div>
        <div class="loop-box">
          &#8635; Output Gen t &rarr; training for Gen t+1
        </div>
      </div>
    </div>

    <!-- Card 3 -->
    <div class="card card-3">
      <div class="card-header">
        <div class="badge b3">3</div>
        <div class="title">Pressure Axes</div>
      </div>
      <div class="card-body">
        <div class="item">
          <div class="bullet bul3"></div>
          <div><strong>Adapter rank</strong> &mdash; 4, 16, 32, 64, 128, 256</div>
        </div>
        <div class="item">
          <div class="bullet bul3"></div>
          <div><strong>Learning rate</strong> &mdash; 1e-6 to 2e-5</div>
        </div>
        <div class="item">
          <div class="bullet bul3"></div>
          <div><strong>Rank &times; LR</strong> interaction matrix</div>
        </div>
        <div class="item">
          <div class="bullet bul3"></div>
          <div><strong>Exposure</strong> &mdash; 0/10/25/50% removal</div>
        </div>
      </div>
    </div>

    <!-- Card 4 -->
    <div class="card card-4">
      <div class="card-header">
        <div class="badge b4">4</div>
        <div class="title">Multi-Metric Evaluation</div>
      </div>
      <div class="card-body">
        <div class="item">
          <div class="bullet bul4"></div>
          <div><strong>K&#8320; retention</strong> &mdash; factual preservation</div>
        </div>
        <div class="item">
          <div class="bullet bul4"></div>
          <div><strong>Distribution shift</strong> &mdash; KL, JS, Distinct-n</div>
        </div>
        <div class="item">
          <div class="bullet bul4"></div>
          <div><strong>Lexical diversity</strong> &mdash; MTLD, Stopword Ratio</div>
        </div>
        <div class="item">
          <div class="bullet bul4"></div>
          <div><strong>Effective rank</strong> &mdash; exp(H(&sigma;)) of B&times;A</div>
        </div>
      </div>
    </div>

    <!-- Card 5 -->
    <div class="card card-5">
      <div class="card-header">
        <div class="badge b5">5</div>
        <div class="title">Regime Classification</div>
      </div>
      <div class="card-body">
        <div class="regimes">
          <div class="regime-pill reg-homeo">
            <strong>Homeostatic</strong> &mdash; retention &gt; 90%, stable
          </div>
          <div class="regime-pill reg-bounded">
            <strong>Bounded</strong> &mdash; stable retention, distribution drifts
          </div>
          <div class="regime-pill reg-deg">
            <strong>Degradative</strong> &mdash; retention declines ~2&ndash;6 pp/gen
          </div>
        </div>
      </div>
    </div>

    <!-- Card 6 -->
    <div class="card card-6">
      <div class="card-header">
        <div class="badge b6">6</div>
        <div class="title">Pressure-Regime Mapping</div>
      </div>
      <div class="card-body">
        <div class="item">
          <div class="bullet bul6"></div>
          <div><strong>ETP threshold</strong> identification</div>
        </div>
        <div class="item">
          <div class="bullet bul6"></div>
          <div><strong>Regime transitions:</strong> threshold-like within grid</div>
        </div>
        <div class="item">
          <div class="bullet bul6"></div>
          <div><strong>Cross-backbone</strong> generalization</div>
        </div>
        <div class="item">
          <div class="bullet bul6"></div>
          <div>Rank, LR, exposure &rarr; unified pressure</div>
        </div>
      </div>
    </div>
  </div>

</body>
</html>
"""

def generate():
    # 1. Write HTML to source locations
    src_paths = [
        BASE_DIR / "v4" / "figs" / "src" / "fig1_overview.html",
        BASE_DIR / "v4" / "manuscript" / "figs" / "src" / "fig1_overview.html",
        BASE_DIR / "v4" / "docs" / "overleaf" / "figs" / "src" / "fig1_overview.html",
        BASE_DIR / "v3" / "figs" / "fig1_overview.html",
    ]
    for p in src_paths:
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(HTML_CONTENT, encoding="utf-8")
        print(f"Updated HTML: {p}")

    # 2. Render vector PDF via Playwright
    pdf_out = BASE_DIR / "v4" / "manuscript" / "figs" / "scratch" / "fig1_overview.pdf"
    pdf_out.parent.mkdir(parents=True, exist_ok=True)

    with sync_playwright() as p:
        browser = p.chromium.launch(executable_path=r"C:\Program Files\Google\Chrome\Application\chrome.exe")
        page = browser.new_page(viewport={"width": 900, "height": 336})
        page.set_content(HTML_CONTENT)
        page.wait_for_load_state("networkidle")
        
        # Save vector PDF with exact 900px x 336px dimensions
        page.pdf(
            path=str(pdf_out),
            width="900px",
            height="336px",
            print_background=True,
            margin={"top": "0px", "right": "0px", "bottom": "0px", "left": "0px"},
        )
        print(f"Rendered vector PDF: {pdf_out}")

        # Also save high-res PNG preview
        png_out = BASE_DIR / "v4" / "manuscript" / "figs" / "scratch" / "fig1_overview.png"
        page.screenshot(path=str(png_out), scale="device")
        print(f"Rendered PNG preview: {png_out}")

        browser.close()

    # Copy PDF and PNG to other scratch folders
    target_scratch = [
        BASE_DIR / "v4" / "docs" / "overleaf" / "figs" / "scratch",
        BASE_DIR / "v4" / "figs" / "scratch",
    ]
    for d in target_scratch:
        d.mkdir(parents=True, exist_ok=True)
        import shutil
        try:
            shutil.copy2(str(pdf_out), str(d / "fig1_overview.pdf"))
            shutil.copy2(str(png_out), str(d / "fig1_overview.png"))
            print(f"Copied to: {d}")
        except Exception as e:
            print(f"Notice when copying to {d}: {e}")

    # 3. Verify PDF with PyMuPDF
    doc = fitz.open(str(pdf_out))
    page = doc[0]
    print(f"PDF verified: pages={len(doc)}, mediabox={page.rect}, drawings={len(page.get_drawings())}, text_len={len(page.get_text())}")
    pix = page.get_pixmap(dpi=150)
    preview_path = BASE_DIR / "fig1_new_preview.png"
    pix.save(str(preview_path))
    print(f"Saved visual verification preview to: {preview_path}")

if __name__ == "__main__":
    generate()
