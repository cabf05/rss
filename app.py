import streamlit as st
import feedparser
import requests
import xml.etree.ElementTree as ET

st.set_page_config(page_title="RSS Reader", layout="wide")

st.title("📡 RSS Feed Reader (Resilient Mode)")

rss_url = st.text_input("Enter RSS feed URL:")

def extract_links_from_rdf(xml_content):
    links = []
    try:
        root = ET.fromstring(xml_content)

        # namespace RDF
        ns = {
            'rdf': 'http://www.w3.org/1999/02/22-rdf-syntax-ns#'
        }

        for li in root.findall(".//rdf:li", ns):
            link = li.attrib.get('{http://www.w3.org/1999/02/22-rdf-syntax-ns#}resource')
            if link:
                links.append(link)

    except Exception as e:
        st.warning(f"RDF parsing error: {e}")

    return links


if st.button("Load Feed"):
    if rss_url:
        try:
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
                "Accept": "application/rss+xml, application/xml;q=0.9, */*;q=0.8",
                "Accept-Language": "en-US,en;q=0.5",
                "Referer": "https://www.google.com/",
                "Connection": "keep-alive"
            }

            response = requests.get(rss_url, headers=headers, timeout=10)

            if response.status_code == 403:
                st.error("❌ 403 Forbidden: blocked by server")
                st.stop()

            response.raise_for_status()

            st.subheader("🔍 Debug Info")
            st.write("Content-Type:", response.headers.get("Content-Type"))

            content = response.content

            # 🥇 Tentativa 1: feedparser
            feed = feedparser.parse(content)

            if feed.entries:
                st.success("✅ Parsed as standard RSS")

                for entry in feed.entries:
                    st.subheader(entry.get("title", "No title"))

                    if "published" in entry:
                        st.caption(entry.published)

                    if "summary" in entry:
                        st.write(entry.summary)

                    if "link" in entry:
                        st.markdown(f"[Read more]({entry.link})")

                    st.divider()

            else:
                # 🥈 Tentativa 2: RDF manual
                st.warning("⚠️ No standard entries found. Trying RDF parsing...")

                links = extract_links_from_rdf(content)

                if links:
                    st.success(f"✅ Found {len(links)} links via RDF")

                    for link in links[:10]:  # limita pra não travar
                        st.markdown(f"[Open article]({link})")

                else:
                    st.error("❌ Could not extract content from this feed.")

        except Exception as e:
            st.error(f"⚠️ Error: {e}")

    else:
        st.warning("Please enter a valid RSS URL.")
