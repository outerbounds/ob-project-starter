import os
import io
import requests
import streamlit as st

from xkcd_utils import fetch_latest

from metaflow.integrations import ArgoEvent

st.set_page_config(page_title="XKCD Viewer", page_icon="🖼️", layout="centered")

# ---------- Helpers ----------

@st.cache_data(show_spinner=False)
def fetch_xkcd_info(comic_id: int):
    url = f"https://xkcd.com/{comic_id}/info.0.json"
    try:
        r = requests.get(url, timeout=10)
        if r.status_code == 200:
            return r.json()
        return None
    except requests.RequestException:
        return None

@st.cache_data(show_spinner=False)
def fetch_image_bytes(url: str) -> bytes:
    r = requests.get(url, timeout=15)
    r.raise_for_status()
    return r.content

def load_valid_comic(comic_id: int):
    info = fetch_xkcd_info(comic_id)
    if info:
        return comic_id, info
    for delta in range(1, 10):
        for candidate in (comic_id + delta, comic_id - delta):
            if candidate < 1:
                continue
            info = fetch_xkcd_info(candidate)
            if info:
                return candidate, info
    return None, None

# ---------- UI State ----------

START_ID = int(fetch_latest()[0])
if "comic_id" not in st.session_state:
    st.session_state.comic_id = START_ID

# Top nav
left, mid, right = st.columns([1, 3, 1])
with left:
    if st.button("◀ Prev"):
        st.session_state.comic_id = max(1, st.session_state.comic_id - 1)
with right:
    if st.button("Next ▶"):
        st.session_state.comic_id = st.session_state.comic_id + 1

# Load comic
resolved_id, info = load_valid_comic(st.session_state.comic_id)
if info is None:
    st.error("Couldn't load a comic nearby. Try another ID.")
    st.stop()

st.session_state.comic_id = resolved_id

title = info.get("title", f"XKCD {resolved_id}")
alt = info.get("alt", "")
img_url = info.get("img", "")

mid.subheader(f"{resolved_id}: {title}")

# ---------- Comic Image ----------
if img_url:
    try:
        img_bytes = fetch_image_bytes(img_url)
        mid.image(io.BytesIO(img_bytes), caption=alt or "No alt text", width=400)
    except Exception as e:
        st.warning(f"Failed to load image: {e}")
else:
    st.warning("No image found for this comic.")

if mid.button("Trigger analysis", type="primary", use_container_width=True):
    project = os.environ['OB_PROJECT']
    branch = os.environ['OB_BRANCH']
    if branch in ('main', 'master'):
        mf_branch = 'prod'
    else:
        mf_branch = f'test.{branch}'
    event_name = f'metaflow.{project}.{mf_branch}.XKCDData.end'
    ArgoEvent(event_name).publish({'xkcd_url': img_url})
    st.success(f"XKCDExplainer triggered for {st.session_state.comic_id}")

