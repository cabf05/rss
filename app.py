import streamlit as st
import feedparser

st.set_page_config(page_title="RSS Reader", layout="wide")

st.title("📡 RSS Feed Reader")

# Input do usuário
rss_url = st.text_input("Enter RSS feed URL:")

if st.button("Load Feed"):
    if rss_url:
        feed = feedparser.parse(rss_url)

        if feed.bozo:
            st.error("Invalid RSS feed or error loading it.")
        else:
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
    else:
        st.warning("Please enter a valid RSS URL.")
