import gradio as gr
from datetime import datetime
import html
import re

APP_NAME = "Krishna Competitor Analysis"

# NOTE:
# This starter version provides a polished UI and a local demo analysis.
# It does not connect to paid tools or fetch live competitor data yet.
# Real live analysis can be added later with official APIs / permitted data sources.

TOOLS = {
    "Klue": "Competitive intelligence & sales enablement",
    "Crayon": "Competitive tracking & market intelligence",
    "Kompyte": "Competitor monitoring & insights",
    "AlphaSense": "Market intelligence & search",
    "Semrush": "SEO & digital marketing analysis",
    "Contify": "Competitive & market intelligence",
    "Valona Intelligence": "Alternative data & insights",
    "Softly": "AI-powered competitive insights",
    "Feedly AI": "News & content intelligence",
    "AI Phasesense": "AI search & research platform",
}

CUSTOM_CSS = r"""
:root {
  --pink: #f56da5;
  --pink-dark: #df397d;
  --pink-light: #fff0f6;
  --pink-pale: #fff8fb;
  --ink: #171923;
  --muted: #697386;
  --line: #f5d9e5;
}
.gradio-container {
  max-width: 1440px !important;
  margin: auto !important;
  background: #fffafd !important;
  color: var(--ink) !important;
  font-family: Inter, ui-sans-serif, system-ui, -apple-system, Segoe UI, sans-serif !important;
}
body { background: #fffafd !important; }
#app-header {
  border: 1px solid var(--line);
  background: linear-gradient(110deg, #fff0f6 0%, #ffffff 65%, #fff7fb 100%);
  border-radius: 20px;
  padding: 18px 24px;
  margin-bottom: 16px;
}
.brand { display:flex; gap:14px; align-items:center; }
.brand-icon {
  width:48px;height:48px;border-radius:16px;background:#ffd8e8;color:#d92f78;
  display:flex;align-items:center;justify-content:center;font-size:26px;
}
.brand-title {font-size:25px;font-weight:800;line-height:1.1;color:#171923;}
.brand-sub {font-size:13px;color:#697386;margin-top:5px;}
.hero {
  background:linear-gradient(115deg,#ffeaf3 0%,#fff5fa 55%,#ffffff 100%);
  border:1px solid #f7d5e4;border-radius:20px;padding:24px;
}
.hero h1 {font-size:29px;line-height:1.2;margin:8px 0 12px;color:#171923;}
.hero p {font-size:15px;line-height:1.65;color:#525b6d;max-width:800px;}
.pill {
 display:inline-block;border:1px solid #f5d0e0;background:#fff;border-radius:99px;
 padding:7px 12px;margin:5px 5px 0 0;font-size:12px;color:#313747;
}
.section-card {
 border:1px solid #f4d8e5 !important;border-radius:18px !important;
 background:#ffffff !important;padding:16px !important;
}
.section-title {font-size:19px;font-weight:750;margin-bottom:4px;}
.section-sub {font-size:13px;color:#697386;margin-bottom:14px;}
.stat-card {
 border:1px solid #f6dce7;border-radius:16px;padding:16px;background:linear-gradient(140deg,#fff5fa,#ffffff);
 min-height:115px;
}
.stat-label {font-size:12px;color:#596273;}
.stat-number {font-size:29px;font-weight:800;margin:9px 0 4px;color:#171923;}
.stat-note {font-size:11px;color:#8a6174;}
.tool-card {
 border:1px solid #f5dce7;border-radius:12px;padding:10px 12px;margin:7px 0;background:#fffafd;
}
.tool-name {font-weight:700;font-size:13px;color:#171923;}
.tool-desc {font-size:11px;color:#697386;margin-top:3px;}
.small-note {font-size:12px;color:#697386;}
button.primary {
 background:linear-gradient(90deg,#f56da5,#e9488b) !important;
 border:0 !important;color:#fff !important;border-radius:12px !important;font-weight:700 !important;
}
button {border-radius:10px !important;}
input, textarea, select {
 border-color:#efd4e0 !important;border-radius:11px !important;
}
footer {display:none !important;}
"""

def safe_text(value):
    return html.escape(str(value or "").strip())

def make_tool_list():
    rows = []
    for name, desc in TOOLS.items():
        rows.append(
            f'<div class="tool-card"><div class="tool-name">✦ {html.escape(name)}</div>'
            f'<div class="tool-desc">{html.escape(desc)}</div></div>'
        )
    return "\n".join(rows)

def run_analysis(company_or_url, industry, selected_tool, focus):
    target = (company_or_url or "").strip()
    if not target:
        return (
            "### Please enter a competitor name or website\n"
            "For example: `Nike`, `apple.com`, or `online grocery delivery`."
        )

    target_clean = safe_text(target)
    industry_clean = safe_text(industry) or "Not specified"
    tool_clean = safe_text(selected_tool) or "All tools"
    focus_clean = safe_text(focus) or "Overall competitor overview"
    now = datetime.now().strftime("%d %b %Y, %I:%M %p")

    # This is an honest local demo, not a live competitor research result.
    # Avoid inventing facts about a real company.
    report = f"""
## 🔎 Competitor Analysis: {target_clean}

> **Demo mode:** This screen is a UI starter. It has not fetched live company, traffic,
> pricing, news, or market-share data. Connect verified sources/APIs to generate evidence-based findings.

### Analysis setup
- **Competitor / topic:** {target_clean}
- **Industry:** {industry_clean}
- **Analysis source selection:** {tool_clean}
- **Analysis focus:** {focus_clean}
- **Created:** {now}

### Recommended research checklist
1. **Positioning:** Identify the target audience, value proposition, and main product categories from the company's official pages.
2. **Products & features:** Compare the core features, service levels, integrations, and customer support options.
3. **Pricing:** Record publicly listed plans and billing terms. Mark anything unavailable as “Not found” rather than guessing.
4. **Marketing & SEO:** Review public search keywords, content themes, social channels, and landing-page messaging using permitted sources.
5. **Customer signals:** Review public customer reviews and announcements. Separate customer opinions from verified facts.
6. **Recent changes:** Track official announcements, product launches, hiring pages, and reputable industry news.
7. **Opportunities:** List underserved customer needs and potential differentiators, supported by source links.

### Findings table template
| Area | Evidence to collect | Status |
|---|---|---|
| Product & features | Official product pages / release notes | Needs live data |
| Pricing | Public pricing page | Needs live data |
| SEO & traffic | Authorized SEO data provider | Needs API/source |
| News & launches | Official newsroom / reputable news | Needs live data |
| Customer sentiment | Public review sources | Needs source review |
| Strategic opportunity | Compare verified evidence | Pending evidence |

### Next step
Use the source links and notes panel below to add verified observations. Once official APIs or permitted data sources are connected, this report can be upgraded to automated analysis.
"""
    return report

def save_notes(target, notes):
    if not (notes or "").strip():
        return "Add notes first, then click **Save notes**."
    return f"### Notes saved in this session\n**Topic:** {safe_text(target) or 'General'}\n\n{notes.strip()}\n\n*Note: this starter app does not persist notes after the app process stops.*"

with gr.Blocks(css=CUSTOM_CSS, title=APP_NAME, theme=gr.themes.Soft(primary_hue="pink", neutral_hue="slate")) as demo:
    gr.HTML("""
    <div id="app-header">
      <div class="brand">
        <div class="brand-icon">♛</div>
        <div>
          <div class="brand-title">Krishna <span style="color:#df397d">Competitor Analysis</span></div>
          <div class="brand-sub">AI-powered market intelligence workspace</div>
        </div>
      </div>
    </div>
    """)

    with gr.Row(equal_height=False):
        with gr.Column(scale=7, min_width=300):
            gr.HTML("""
            <div class="hero">
              <div style="font-size:12px;font-weight:800;letter-spacing:.12em;color:#df397d;">YOUR AI RESEARCH WORKSPACE</div>
              <h1>Smarter insights. Better decisions. 🚀</h1>
              <p>Explore competitors, organize market signals, and build a clear research report in one workspace.
              Start with a company name, website, or industry topic.</p>
              <span class="pill">✦ 10 tool categories</span>
              <span class="pill">◉ Competitor comparison</span>
              <span class="pill">↗ Market trends</span>
              <span class="pill">▤ Research reports</span>
            </div>
            """)

            with gr.Group(elem_classes=["section-card"]):
                gr.HTML('<div class="section-title">🔍 Start a Competitor Analysis</div><div class="section-sub">Enter a competitor name or website to create a structured research checklist.</div>')
                competitor = gr.Textbox(
                    label="Competitor name or website",
                    placeholder="e.g. Nike, apple.com, or online grocery delivery",
                    lines=1
                )
                with gr.Row():
                    industry = gr.Textbox(label="Industry (optional)", placeholder="e.g. sportswear, SaaS, retail")
                    tool = gr.Dropdown(
                        choices=["All tools"] + list(TOOLS.keys()),
                        value="All tools",
                        label="Research tool category"
                    )
                focus = gr.Radio(
                    choices=["Overall competitor overview", "Products & pricing", "Marketing & SEO", "News & market trends", "Customer sentiment"],
                    value="Overall competitor overview",
                    label="What do you want to focus on?"
                )
                analyze_btn = gr.Button("✨ Create Analysis Report", variant="primary")
                output = gr.Markdown(
                    "Your report will appear here after you start an analysis.",
                    elem_classes=["section-card"]
                )
                analyze_btn.click(
                    fn=run_analysis,
                    inputs=[competitor, industry, tool, focus],
                    outputs=output
                )
                competitor.submit(
                    fn=run_analysis,
                    inputs=[competitor, industry, tool, focus],
                    outputs=output
                )

            with gr.Row():
                with gr.Column():
                    gr.HTML("""
                    <div class="stat-card">
                      <div class="stat-label">📊 ANALYSIS WORKSPACE</div>
                      <div class="stat-number">Ready</div>
                      <div class="stat-note">Start by entering a competitor above</div>
                    </div>""")
                with gr.Column():
                    gr.HTML("""
                    <div class="stat-card">
                      <div class="stat-label">🧠 RESEARCH APPROACH</div>
                      <div class="stat-number">Evidence-first</div>
                      <div class="stat-note">Separate verified facts from assumptions</div>
                    </div>""")
                with gr.Column():
                    gr.HTML("""
                    <div class="stat-card">
                      <div class="stat-label">📝 REPORT FORMAT</div>
                      <div class="stat-number">Structured</div>
                      <div class="stat-note">Checklist, findings table, next steps</div>
                    </div>""")

            with gr.Group(elem_classes=["section-card"]):
                gr.HTML('<div class="section-title">🗒️ Research Notes</div><div class="section-sub">Keep your observations together while you investigate a competitor.</div>')
                notes_target = gr.Textbox(label="Topic / competitor", placeholder="Company or topic")
                notes = gr.Textbox(label="Notes", placeholder="Add verified facts, source links, questions, and observations...", lines=5)
                notes_btn = gr.Button("Save notes", variant="primary")
                notes_output = gr.Markdown()
                notes_btn.click(save_notes, inputs=[notes_target, notes], outputs=notes_output)

        with gr.Column(scale=3, min_width=260):
            with gr.Group(elem_classes=["section-card"]):
                gr.HTML('<div class="section-title">🧰 10 AI Tool Categories</div><div class="section-sub">Tool names shown as research options; integrations are not connected yet.</div>')
                gr.HTML(make_tool_list())

            with gr.Group(elem_classes=["section-card"]):
                gr.HTML("""
                <div class="section-title">💡 Research best practices</div>
                <div class="tool-card"><div class="tool-name">1. Use reliable sources</div><div class="tool-desc">Prefer official product pages, filings, and reputable news.</div></div>
                <div class="tool-card"><div class="tool-name">2. Add source links</div><div class="tool-desc">Keep a source URL for every important claim.</div></div>
                <div class="tool-card"><div class="tool-name">3. Compare fairly</div><div class="tool-desc">Use the same criteria for each competitor.</div></div>
                <div class="tool-card"><div class="tool-name">4. Refresh findings</div><div class="tool-desc">Record the date and revisit changing information.</div></div>
                """)

            with gr.Group(elem_classes=["section-card"]):
                gr.HTML("""
                <div style="text-align:center;padding:12px 6px;">
                  <div style="font-size:35px;">🤖 🌸</div>
                  <div style="font-size:16px;font-weight:800;margin:8px 0;">Built for smarter research</div>
                  <div class="small-note">Analyze • Compare • Learn • Grow</div>
                </div>
                """)

    gr.HTML("""
    <div style="text-align:center;color:#8a6174;font-size:12px;padding:18px 4px 6px;">
      Krishna Competitor Analysis • Baby Pink + White UI • Starter edition
    </div>
    """)

if __name__ == "__main__":
    demo.launch()
