import streamlit as st
import feedparser
import requests

st.set_page_config(page_title="RSS Reader", layout="wide")

st.title("📡 RSS Feed Reader")

rss_url = st.text_input("Enter RSS feed URL:")

if st.button("Load Feed"):
    if rss_url:
        try:
            headers = {
                "User-Agent": "Mozilla/5.0"
            }

            response = requests.get(rss_url, headers=headers, timeout=10)
            response.raise_for_status()

            # 🔍 DEBUG: ver o que o servidor retornou
            st.subheader("🔍 Debug Info")
            st.write("Content-Type:", response.headers.get("Content-Type"))
            st.text(response.text[:500])

            # Se não for XML, alerta
            content_type = response.headers.get("Content-Type", "")
            if "xml" not in content_type and "rss" not in content_type:
                st.warning("⚠️ This URL did not return a valid RSS feed (it returned HTML instead).")
                st.stop()

            # Parse do RSS
            feed = feedparser.parse(response.content)

            if feed.bozo:
                st.warning("RSS parsed with some issues (non-standard format).")

            st.success(f"Feed loaded: {feed.feed.get('title', 'No title')}")

            # Mostrar itens
            for entry in feed.entries:
                st.subheader(entry.get("title", "No title"))

                if "published" in entry:
                    st.caption(entry.published)

                if "summary" in entry:
                    st.write(entry.summary)

                if "link" in entry:
                    st.markdown(f"[Read more]({entry.link})")

                st.divider()

        except Exception as e:
            st.error(f"Error loading feed: {e}")
    else:
        st.warning("Please enter a valid RSS URL.")
