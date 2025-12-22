from pathlib import Path
from PIL import Image
import base64
from io import BytesIO
import plotly.graph_objects as go
import streamlit as st

ROOT_PATH = Path(__file__).resolve().parent.parent
IMG_PATH = ROOT_PATH / 'img'

img = Image.open(IMG_PATH / 'mine_diagram.png')
w, h = img.size
ratio = h / w

fig = go.Figure()
fig.add_layout_image(
    source=img,
    x=0, y=0,
    sizex=w, sizey=h,
    xref="x", yref="y",
    sizing="stretch",
    layer="below"
)

fig.update_xaxes(range=[0, w], visible=False)
fig.update_yaxes(range=[h, 0], visible=False, scaleanchor="x")
fig.update_layout(margin=dict(l=0, r=0, t=0, b=0))

st.markdown(
    f"""
    <div style="width:100%; aspect-ratio:{w}/{h};">
    """,
    unsafe_allow_html=True
)

st.plotly_chart(fig, use_container_width=True, config={"responsive": True})

st.markdown("</div>", unsafe_allow_html=True)
