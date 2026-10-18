%%writefile /content/app.py
import streamlit as st
import pandas as pd
import plotly.express as px
import requests
import trafilatura
import feedparser
from google import genai
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4
from io import BytesIO
from urllib.parse import quote
from datetime import datetime

st.set_page_config(
    page_title="Krishna Competitor Analysis",
    page_icon="📊",
    layout="wide"
)

st.markdown("""
<style>
.stApp {
    background: #fff9fc;
    color: #202020;
}
[data-testid="stSidebar"] {
    background: #ffe4ef;
}
.main-title {
    background: linear-gradient(90deg, #ffc1dc, #fff0f7);
    padding: 25px;
    border-radius: 18px;
    text-align: center;
    color: #222222;
    margin-bottom: 20px;
}
div.stButton > button {
    background: #f3a6ca;
    color: #222222;
    border: 0;
    border-radius: 10px;
    padding: 10px 20px;
    font-weight: bold;
}
div.stButton > button:hover {
    background: #ed8fbd;
    color: #111111;
}
[data-testid="stMetric"] {
    background: white;
    padding: 16px;
    border-radius: 12px;
    border: 1px solid #f4c7dc;
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="main-title">
<h1>📊 Krishna Competitor Analysis</h1>
<p>AI-Powered Market Intelligence & Competitor Research</p>
</div>
""", unsafe_allow_html=True)

TOOLS = [
    "Klue",
    "Crayon",
    "Kompyte",
    "AlphaSense",
    "Semrush",
    "Contify",
    "Valona Intelligence",
    "Softly",
    "Feedly AI",
    "AI PhaseSense"
]

with st.sidebar:
    st.header("⚙️ Analysis Settings")
    api_key = st.text_input(
        "Gemini API Key",
        type="password",
        help="Enter your own Google Gemini API key."
    )
    model_name = st.text_input(
        "Gemini Model",
        value="gemini-2.5-flash"
    )
    st.divider()
    st.subheader("Analysis Modules")
    st.write("✅ Company Research")
    st.write("✅ Website Content")
    st.write("✅ Market News")
    st.write("✅ AI Insights")
    st.write("✅ Competitor Comparison")
    st.write("✅ Charts and PDF Report")

tab1, tab2, tab3 = st.tabs([
    "🔎 Competitor Analysis",
    "📰 Market News",
    "🧰 Intelligence Tools"
])

with tab1:
    st.subheader("Company Research")

    col1, col2 = st.columns(2)

    with col1:
        company = st.text_input(
            "Main Company",
            placeholder="Example: Zoho"
        )
        website = st.text_input(
            "Company Website",
            placeholder="https://www.example.com"
        )

    with col2:
        competitors_text = st.text_area(
            "Competitors (one company per line)",
            placeholder="Freshworks\nSalesforce\nHubSpot"
        )

    run_analysis = st.button(
        "🚀 Create Analysis Report",
        use_container_width=True
    )

    if run_analysis:
        if not company.strip():
            st.error("Please enter the main company name.")
            st.stop()

        competitor_list = [
            x.strip()
            for x in competitors_text.splitlines()
            if x.strip()
        ]

        website_text = ""
        news_items = []

        with st.spinner("Collecting available public information..."):
            if website.strip():
                try:
                    downloaded = trafilatura.fetch_url(website.strip())
                    if downloaded:
                        website_text = (
                            trafilatura.extract(downloaded) or ""
                        )[:12000]
                except Exception as e:
                    st.warning(f"Website retrieval failed: {e}")

            try:
                news_url = (
                    "https://news.google.com/rss/search?q="
                    + quote(company + " company market")
                    + "&hl=en-IN&gl=IN&ceid=IN:en"
                )
                feed = feedparser.parse(news_url)

                for item in feed.entries[:10]:
                    news_items.append({
                        "Title": item.get("title", ""),
                        "Published": item.get("published", ""),
                        "Source": item.get("source", {}).get(
                            "title", "News source"
                        ),
                        "Link": item.get("link", "")
                    })
            except Exception as e:
                st.warning(f"News retrieval failed: {e}")

        news_df = pd.DataFrame(news_items)

        st.session_state["company"] = company
        st.session_state["competitors"] = competitor_list
        st.session_state["website_text"] = website_text
        st.session_state["news_df"] = news_df

        st.markdown("### 📌 Research Overview")

        m1, m2, m3 = st.columns(3)
        m1.metric("Main Company", company)
        m2.metric("Competitors Entered", len(competitor_list))
        m3.metric("News Items Retrieved", len(news_items))

        st.markdown("### 🌐 Website Research")

        if website_text:
            st.success("Website text retrieved successfully.")
            with st.expander("View retrieved website content"):
                st.write(website_text)
        elif website.strip():
            st.warning(
                "Website content could not be retrieved. "
                "The site may block automated access."
            )
        else:
            st.info("Enter a company website to retrieve its content.")

        st.markdown("### 📰 Recent Market News")

        if not news_df.empty:
            st.dataframe(
                news_df,
                use_container_width=True,
                hide_index=True
            )
        else:
            st.info("No news items were retrieved.")

        st.markdown("### 🤖 AI Analysis")

        if not api_key:
            st.warning(
                "Enter a Gemini API key in the sidebar to generate "
                "AI-powered analysis. Website and news retrieval can "
                "still work without a Gemini key."
            )
            report_text = (
                f"Competitor Analysis Report: {company}\n\n"
                f"Competitors entered: {', '.join(competitor_list) or 'None'}\n\n"
                f"Website content retrieved: {'Yes' if website_text else 'No'}\n\n"
                f"News articles retrieved: {len(news_items)}\n\n"
                "AI analysis was not generated because no API key was provided."
            )
        else:
            prompt = f"""
You are a careful market research assistant.

Prepare a structured competitor research report for: {company}

Competitors supplied by the user:
{competitor_list}

Company website text actually retrieved:
{website_text[:9000] if website_text else "No website text was retrieved."}

Recent news actually retrieved:
{news_df.head(10).to_string(index=False) if not news_df.empty else "No news retrieved."}

Include:
1. Company overview based only on available evidence.
2. Product/service positioning.
3. Competitor comparison.
4. Strengths and weaknesses supported by evidence.
5. Market opportunities and threats.
6. Recent news implications.
7. Practical recommendations.
8. Missing information and limitations.

Rules:
- Never invent facts, financial numbers, market shares, or research findings.
- Clearly label assumptions and unknown information.
- Do not claim you directly accessed paid tools.
- If evidence is missing, say so.
- Do not imply the competitor websites were researched unless evidence is provided.

Format the answer with clear headings and bullet points.
"""
            try:
                with st.spinner("Generating AI report..."):
                    client = genai.Client(api_key=api_key)
                    response = client.models.generate_content(
                        model=model_name.strip(),
                        contents=prompt
                    )
                    report_text = response.text or (
                        "The AI returned no text."
                    )
                st.markdown(report_text)
            except Exception as e:
                report_text = (
                    "AI report generation failed.\n\n"
                    f"Error: {e}"
                )
                st.error(
                    "AI request failed. Check the API key, model name, "
                    "internet connection, and API quota."
                )
                st.code(str(e))

        st.session_state["report_text"] = report_text

        st.markdown("### 📊 Competitor Research Coverage")

        comparison_rows = [{
            "Company": company,
            "Website Content Retrieved": bool(website_text),
            "News Articles Retrieved": len(news_items)
        }]

        for competitor in competitor_list:
            comparison_rows.append({
                "Company": competitor,
                "Website Content Retrieved": False,
                "News Articles Retrieved": 0
            })

        comparison_df = pd.DataFrame(comparison_rows)
        st.dataframe(
            comparison_df,
            use_container_width=True,
            hide_index=True
        )

        st.caption(
            "Competitor entries are not automatically researched in this "
            "prototype. Their website and news coverage is not verified "
            "until those sources are separately retrieved."
        )

        chart_df = pd.DataFrame({
            "Company": [company] + competitor_list,
            "Research Coverage": (
                [1 if website_text else 0]
                + [0] * len(competitor_list)
            )
        })

        fig = px.bar(
            chart_df,
            x="Company",
            y="Research Coverage",
            title="Retrieved Website Evidence (1 = retrieved, 0 = unavailable)",
            color="Company"
        )
        st.plotly_chart(fig, use_container_width=True)

        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4)
        styles = getSampleStyleSheet()
        story = [
            Paragraph("Krishna Competitor Analysis", styles["Title"]),
            Spacer(1, 12),
            Paragraph(
                f"Company: {company}",
                styles["Heading2"]
            ),
            Paragraph(
                f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}",
                styles["Normal"]
            ),
            Spacer(1, 12)
        ]

        for line in report_text.splitlines():
            safe_line = (
                line.replace("&", "&amp;")
                    .replace("<", "&lt;")
                    .replace(">", "&gt;")
            )
            if safe_line.strip():
                story.append(Paragraph(safe_line, styles["BodyText"]))
                story.append(Spacer(1, 5))

        doc.build(story)
        buffer.seek(0)

        st.download_button(
            "📄 Download PDF Report",
            data=buffer.getvalue(),
            file_name="krishna_competitor_analysis.pdf",
            mime="application/pdf",
            use_container_width=True
        )

with tab2:
    st.subheader("📰 Market News Research")
    st.write(
        "Enter a company name to search publicly available Google News RSS."
    )

    news_company = st.text_input(
        "Company or Topic",
        key="news_company"
    )

    if st.button("Search News"):
        if not news_company.strip():
            st.warning("Enter a company or topic first.")
        else:
            try:
                url = (
                    "https://news.google.com/rss/search?q="
                    + quote(news_company)
                    + "&hl=en-IN&gl=IN&ceid=IN:en"
                )
                feed = feedparser.parse(url)
                rows = []

                for item in feed.entries[:20]:
                    rows.append({
                        "Title": item.get("title", ""),
                        "Published": item.get("published", ""),
                        "Link": item.get("link", "")
                    })

                if rows:
                    st.dataframe(
                        pd.DataFrame(rows),
                        use_container_width=True,
                        hide_index=True
                    )
                else:
                    st.info("No news articles were found.")
            except Exception as e:
                st.error(f"News search failed: {e}")

with tab3:
    st.subheader("🧰 Competitive Intelligence Tools")

    st.info(
        "These are tool categories for future integrations. "
        "This prototype does not connect to their paid APIs."
    )

    tools_df = pd.DataFrame({
        "Tool": TOOLS,
        "Integration Status": [
            "Not connected" for _ in TOOLS
        ],
        "Notes": [
            "Requires separate data source or API integration"
            for _ in TOOLS
        ]
    })

    st.dataframe(
        tools_df,
        use_container_width=True,
        hide_index=True
    )

st.divider()
st.caption(
    "Krishna Competitor Analysis | Public-source research prototype. "
    "Verify important business decisions against original sources."
)
