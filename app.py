"""
CyberLens - Streamlit UI
========================
A sleek, interactive web app to convert photos into
black-and-neon stylized images with pixelation controls.
"""

import streamlit as st
import numpy as np
import cv2
from processor import process_image, COLOR_PRESETS

# -- Page config ---------------------------------------------------------------
st.set_page_config(
    page_title="CyberLens",
    page_icon="🔮",
    layout="wide",
    initial_sidebar_state="expanded",
)

# -- Custom CSS for a premium dark cyber aesthetic -----------------------------
st.markdown("""
<style>
    /* -- Import font -- */
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Inter:wght@300;400;500;600&display=swap');

    /* -- Global overrides -- */
    .stApp {
        background: linear-gradient(135deg, #0a0a0a 0%, #0d1117 40%, #161b22 100%);
    }

    /* -- Header styling -- */
    .cyber-header {
        text-align: center;
        padding: 2rem 0 1rem 0;
    }
    .cyber-header h1 {
        font-family: 'Orbitron', monospace;
        font-size: 3.2rem;
        font-weight: 900;
        background: linear-gradient(135deg, #39ff14 0%, #00ffff 50%, #ff69b4 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        text-shadow: none;
        margin-bottom: 0.2rem;
        letter-spacing: 4px;
    }
    .cyber-header p {
        font-family: 'Inter', sans-serif;
        color: #8b949e;
        font-size: 1.05rem;
        font-weight: 300;
        letter-spacing: 1px;
    }

    /* -- Sidebar styling -- */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0d1117 0%, #161b22 100%);
        border-right: 1px solid #21262d;
    }
    section[data-testid="stSidebar"] .stMarkdown h2 {
        font-family: 'Orbitron', monospace;
        color: #39ff14;
        font-size: 1.2rem;
        letter-spacing: 2px;
        border-bottom: 1px solid #21262d;
        padding-bottom: 0.5rem;
    }
    section[data-testid="stSidebar"] .stMarkdown h3 {
        font-family: 'Inter', sans-serif;
        color: #c9d1d9;
        font-size: 0.95rem;
        font-weight: 500;
        margin-top: 1.2rem;
    }

    /* -- Upload area -- */
    section[data-testid="stFileUploader"] {
        border: 2px dashed #30363d;
        border-radius: 12px;
        padding: 0.5rem;
        transition: border-color 0.3s ease;
    }
    section[data-testid="stFileUploader"]:hover {
        border-color: #39ff14;
    }

    /* -- Slider tracks -- */
    .stSlider > div > div > div {
        background: linear-gradient(90deg, #39ff14, #00ffff) !important;
    }

    /* -- Download button -- */
    .stDownloadButton > button {
        font-family: 'Orbitron', monospace;
        background: linear-gradient(135deg, #39ff14 0%, #00e676 100%);
        color: #0a0a0a;
        font-weight: 700;
        letter-spacing: 1px;
        border: none;
        border-radius: 8px;
        padding: 0.6rem 2rem;
        transition: all 0.3s ease;
    }
    .stDownloadButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 20px rgba(57, 255, 20, 0.4);
    }

    /* -- Image captions -- */
    .image-label {
        font-family: 'Orbitron', monospace;
        text-align: center;
        color: #58a6ff;
        font-size: 0.85rem;
        letter-spacing: 2px;
        margin-bottom: 0.5rem;
    }

    /* -- Divider glow -- */
    hr {
        border: none;
        height: 1px;
        background: linear-gradient(90deg, transparent, #39ff14, transparent);
        margin: 1.5rem 0;
    }

    /* -- Hide default Streamlit branding -- */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)


# -- Header -------------------------------------------------------------------
st.markdown("""
<div class="cyber-header">
    <h1>CYBERLENS</h1>
    <p>Transform your photos into black-and-neon cyber art</p>
</div>
""", unsafe_allow_html=True)

st.markdown("---")


# -- Sidebar controls ----------------------------------------------------------
with st.sidebar:
    st.markdown("## CONTROLS")

    st.markdown("### Upload Image")
    uploaded_file = st.file_uploader(
        "Drop your image here",
        type=["jpg", "jpeg", "png", "bmp", "tiff", "webp"],
        label_visibility="collapsed",
    )

    st.markdown("---")

    st.markdown("### Neon Color")
    color_name = st.selectbox(
        "Choose color",
        options=list(COLOR_PRESETS.keys()),
        index=0,
        label_visibility="collapsed",
    )

    # Show a small color preview swatch
    color_bgr = COLOR_PRESETS[color_name]
    color_rgb = (color_bgr[2], color_bgr[1], color_bgr[0])
    hex_color = "#{:02x}{:02x}{:02x}".format(*color_rgb)
    st.markdown(
        f'<div style="width:100%;height:8px;border-radius:4px;'
        f'background:{hex_color};margin-top:-8px;margin-bottom:12px;'
        f'box-shadow:0 0 12px {hex_color};"></div>',
        unsafe_allow_html=True,
    )

    st.markdown("### Threshold")
    threshold = st.slider(
        "Controls black/white cutoff",
        min_value=0,
        max_value=255,
        value=127,
        step=1,
        help="Lower = more neon color, Higher = more black",
    )

    st.markdown("### Pixelation")
    pixel_size = st.slider(
        "Pixel block size",
        min_value=1,
        max_value=32,
        value=1,
        step=1,
        help="1 = no pixelation, higher = blockier retro look",
    )

    st.markdown("---")
    st.markdown(
        '<p style="font-family:Inter;color:#484f58;font-size:0.75rem;'
        'text-align:center;letter-spacing:1px;">CYBERLENS v1.0</p>',
        unsafe_allow_html=True,
    )


# -- Main area -----------------------------------------------------------------
if uploaded_file is not None:
    # Decode the uploaded image
    file_bytes = np.frombuffer(uploaded_file.read(), dtype=np.uint8)
    original = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)

    if original is None:
        st.error("Could not read the uploaded image. Please try a different file.")
    else:
        # Process
        result = process_image(
            original,
            color_name=color_name,
            threshold=threshold,
            pixel_size=pixel_size,
        )

        # Convert BGR -> RGB for Streamlit display
        original_rgb = cv2.cvtColor(original, cv2.COLOR_BGR2RGB)
        result_rgb = cv2.cvtColor(result, cv2.COLOR_BGR2RGB)

        # Side-by-side display
        col1, col2 = st.columns(2)

        with col1:
            st.markdown('<p class="image-label">[ ORIGINAL ]</p>', unsafe_allow_html=True)
            st.image(original_rgb, use_container_width=True)

        with col2:
            st.markdown(
                f'<p class="image-label" style="color:{hex_color};">[ {color_name.upper()} ]</p>',
                unsafe_allow_html=True,
            )
            st.image(result_rgb, use_container_width=True)

        st.markdown("---")

        # Download button -- encode result as PNG bytes
        _, png_buffer = cv2.imencode(".png", result)
        st.download_button(
            label="DOWNLOAD RESULT",
            data=png_buffer.tobytes(),
            file_name=f"cyberlens_{color_name.lower().replace(' ', '_')}.png",
            mime="image/png",
            use_container_width=True,
        )

else:
    # Empty state
    st.markdown(
        '<div style="text-align:center;padding:4rem 2rem;">'
        '<p style="font-family:Orbitron;font-size:1.5rem;color:#30363d;'
        'letter-spacing:3px;">UPLOAD AN IMAGE TO BEGIN</p>'
        '<p style="font-family:Inter;color:#484f58;font-size:0.95rem;'
        'margin-top:0.5rem;">Supports JPG, PNG, BMP, TIFF, WebP</p>'
        '</div>',
        unsafe_allow_html=True,
    )
