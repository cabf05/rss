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

            feed = feedparser.parse(response.content)

            if feed.bozo:
                st.warning("RSS parsed with some issues (non-standard format).")

            st.success(f"Feed loaded: {feed.feed.get('title', 'No title')}")

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
