import streamlit as st
import feedparser
import requests

st.set_page_config(page_title="RSS Reader", layout="wide")

st.title("📡 RSS Feed Reader")

rss_url = st.text_input("Enter RSS feed URL:")

if st.button("Load Feed"):
    if rss_url:
        try:
            # 🔐 Headers mais completos (simula navegador)
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
                "Accept": "application/rss+xml, application/xml;q=0.9, */*;q=0.8",
                "Accept-Language": "en-US,en;q=0.5",
                "Referer": "https://www.google.com/",
                "Connection": "keep-alive"
            }

            response = requests.get(rss_url, headers=headers, timeout=10)

            # 🚨 Tratamento de erro 403 (muito comum no Lancet)
            if response.status_code == 403:
                st.error("❌ 403 Forbidden: This site is blocking automated access.")
                st.info("💡 Try another RSS feed or use a proxy backend.")
                st.stop()

            response.raise_for_status()

            # 🔍 DEBUG
            st.subheader("🔍 Debug Info")
            st.write("Status Code:", response.status_code)
            st.write("Content-Type:", response.headers.get("Content-Type"))
            st.text(response.text[:500])

            # 🧠 Verifica se é XML válido
            content_type = response.headers.get("Content-Type", "")

            if "xml" not in content_type and "rss" not in content_type:
                st.warning("⚠️ This URL did not return a valid RSS feed (returned HTML).")
                st.stop()

            # 📡 Parse do feed
            feed = feedparser.parse(response.content)

            if feed.bozo:
                st.warning("⚠️ RSS parsed with some issues (non-standard format).")

            st.success(f"Feed loaded: {feed.feed.get('title', 'No title')}")

            # 📰 Exibir artigos
            for entry in feed.entries:
                st.subheader(entry.get("title", "No title"))

                if "published" in entry:
                    st.caption(entry.published)

                if "summary" in entry:
                    st.write(entry.summary)

                if "link" in entry:
                    st.markdown(f"[Read more]({entry.link})")

                st.divider()

        except requests.exceptions.RequestException as e:
            st.error(f"🌐 Request error: {e}")

        except Exception as e:
            st.error(f"⚠️ Unexpected error: {e}")

    else:
        st.warning("Please enter a valid RSS URL.")
