import streamlit as st
import pandas as pd
import plotly.express as px
import random
import os

from id3_core import build_id3, predict, tree_to_text, rules_from_tree

# ==========================
# CONFIG
# ==========================
st.set_page_config(
    page_title="Dashboard ID3 - Data Pelanggan Property",
    layout="wide",
    page_icon="📊",
    initial_sidebar_state="expanded",
)

# ==========================
# CSS (FINAL) — FIX INPUT PUTIH (TERMASUK TEXT_INPUT) + GANTI "DISABLED" JADI READONLY CARD
# ==========================
st.markdown(
    """
<style>
@keyframes fadeIn {
  from {opacity: 0; transform: translateY(12px);}
  to {opacity: 1; transform: translateY(0);}
}

/* HEADER TRANSPARAN */
header[data-testid="stHeader"]{
  background: transparent !important;
  box-shadow: none !important;
}
div[data-testid="stToolbar"]{ visibility: hidden; }
#MainMenu { visibility: hidden; }
footer { visibility: hidden; }

/* BACKGROUND */
.stApp{
  background:
    radial-gradient(900px 500px at 12% 10%, rgba(56,189,248,0.22), transparent 55%),
    radial-gradient(900px 500px at 88% 18%, rgba(45,212,191,0.18), transparent 55%),
    radial-gradient(900px 500px at 55% 92%, rgba(99,102,241,0.14), transparent 55%),
    linear-gradient(180deg, #0b1220 0%, #0a1020 55%, #07101b 100%);
  color: #e5e7eb;
}
.block-container{ padding-top: 1.1rem; padding-bottom: 90px !important; }

:root{
  --sb-bg: rgba(255,255,255,0.08);
  --sb-bg2: rgba(255,255,255,0.12);
  --sb-bd: rgba(255,255,255,0.18);
  --sb-bd2: rgba(255,255,255,0.34);
  --sb-text: rgba(229,231,235,0.92);
  --sb-ph: rgba(229,231,235,0.55);
}

/* SIDEBAR */
[data-testid="stSidebar"]{
  background: linear-gradient(180deg, #0f1b2d, #0b1220) !important;
  border-right: 1px solid rgba(255,255,255,0.08);
}
[data-testid="stSidebar"] * { color: #e5e7eb !important; }

/* LOGO */
.logo-wrap{
  margin: -12px -12px 10px -12px;
  padding: 0;
  background: transparent;
  border: none;
}
.logo-wrap img{
  background: transparent !important;
  border-radius: 0 !important;
  padding: 0 !important;
  box-shadow: none !important;
}

/* ==========================
   FIX UTAMA: TEXT INPUT / NUMBER / SELECT DI SIDEBAR (ANTI PUTIH)
   - nembak wrapper + nembak langsung <input>
========================== */

/* wrapper baseweb */
section[data-testid="stSidebar"] div[data-baseweb="base-input"],
section[data-testid="stSidebar"] div[data-baseweb="input"],
section[data-testid="stSidebar"] div[data-baseweb="textarea"],
section[data-testid="stSidebar"] div[data-baseweb="select"]{
  background: transparent !important;
}

/* wrapper box yang sering jadi putih */
section[data-testid="stSidebar"] div[data-baseweb="base-input"] > div,
section[data-testid="stSidebar"] div[data-baseweb="input"] > div,
section[data-testid="stSidebar"] div[data-baseweb="textarea"] > div,
section[data-testid="stSidebar"] div[data-baseweb="select"] > div{
  background: var(--sb-bg) !important;
  border: 1px solid var(--sb-bd) !important;
  border-radius: 14px !important;
  box-shadow: none !important;
}

/* focus */
section[data-testid="stSidebar"] div[data-baseweb="base-input"] > div:focus-within,
section[data-testid="stSidebar"] div[data-baseweb="input"] > div:focus-within,
section[data-testid="stSidebar"] div[data-baseweb="textarea"] > div:focus-within,
section[data-testid="stSidebar"] div[data-baseweb="select"] > div:focus-within{
  background: var(--sb-bg2) !important;
  border: 1px solid var(--sb-bd2) !important;
  box-shadow: 0 0 0 3px rgba(99,102,241,0.18) !important;
}

/* 🔥 INI KUNCI: tembak langsung input biar ga putih */
section[data-testid="stSidebar"] input,
section[data-testid="stSidebar"] textarea{
  background-color: rgba(255,255,255,0.04) !important;
  color: var(--sb-text) !important;
  -webkit-text-fill-color: var(--sb-text) !important;
  caret-color: var(--sb-text) !important;
  border: 0 !important;
  outline: none !important;
}

/* placeholder */
section[data-testid="stSidebar"] input::placeholder,
section[data-testid="stSidebar"] textarea::placeholder{
  color: var(--sb-ph) !important;
}

/* tags multiselect */
section[data-testid="stSidebar"] span[data-baseweb="tag"]{
  background: rgba(255,255,255,0.12) !important;
  border: 1px solid rgba(255,255,255,0.14) !important;
}

/* ==========================
   FILE UPLOADER DARK MODE
========================== */
section[data-testid="stSidebar"] div[data-testid="stFileUploader"]{
  background: rgba(255,255,255,0.06) !important;
  border: 1px solid rgba(255,255,255,0.18) !important;
  border-radius: 16px !important;
  padding: 12px !important;
}
section[data-testid="stSidebar"] div[data-testid="stFileUploader"] section{
  background: rgba(255,255,255,0.08) !important;
  border: 1px dashed rgba(255,255,255,0.35) !important;
  border-radius: 14px !important;
}
section[data-testid="stSidebar"] div[data-testid="stFileUploader"] *{
  color: rgba(229,231,235,0.92) !important;
}
section[data-testid="stSidebar"] div[data-testid="stFileUploader"] button{
  background: rgba(255,255,255,0.12) !important;
  color: rgba(229,231,235,0.95) !important;
  border: 1px solid rgba(255,255,255,0.28) !important;
  border-radius: 12px !important;
}
section[data-testid="stSidebar"] div[data-testid="stFileUploader"] button:hover{
  background: rgba(255,255,255,0.20) !important;
  border: 1px solid rgba(255,255,255,0.45) !important;
}

/* dropdown menu dark */
div[data-baseweb="popover"] > div{
  background: rgba(15,23,42,0.98) !important;
  border: 1px solid rgba(255,255,255,0.14) !important;
}
div[data-baseweb="popover"] ul{
  min-width: 520px !important;
  background: transparent !important;
}
div[data-baseweb="popover"] li{
  white-space: nowrap !important;
  color: rgba(229,231,235,0.92) !important;
}
div[data-baseweb="popover"] li:hover{
  background: rgba(255,255,255,0.08) !important;
}

/* READONLY CARD (ganti text_input disabled biar ga putih) */
.readonly{
  padding: 10px 12px;
  border-radius: 14px;
  background: rgba(255,255,255,0.08);
  border: 1px solid rgba(255,255,255,0.18);
  color: rgba(229,231,235,0.78);
  font-weight: 700;
}
.readonly small{
  display:block;
  margin-top:4px;
  color: rgba(229,231,235,0.60);
  font-weight: 600;
}

/* HERO */
.hero{
  background: rgba(255,255,255,0.06);
  border: 1px solid rgba(255,255,255,0.10);
  border-radius: 20px;
  padding: 18px 18px 16px 18px;
  backdrop-filter: blur(8px);
  animation: fadeIn .6s ease-in-out;
}
.hero h1{ margin: 0; font-size: 2.05rem; font-weight: 950; letter-spacing: .2px; }
.hero p{ margin: 6px 0 0 0; color: rgba(229,231,235,.75); }

/* KPI GRID */
.stats-grid{
  display: grid;
  grid-template-columns: repeat(4, minmax(220px, 1fr));
  gap: 18px;
  margin-top: 16px;
}
.kpi{
  border-radius: 22px;
  padding: 18px 18px;
  height: 180px;
  display:flex;
  flex-direction:column;
  justify-content:center;
  text-align:left;
  background: rgba(255,255,255,0.06);
  border: 1px solid rgba(255,255,255,0.11);
  backdrop-filter: blur(10px);
  animation: fadeIn .7s ease-in-out;
  transition: all .25s ease;
}
.kpi:hover{
  transform: translateY(-4px);
  box-shadow: 0 16px 40px rgba(0,0,0,.35);
}
.kpi .label{ font-size: 1.02rem; color: rgba(229,231,235,.75); font-weight: 800; margin-bottom: 8px; }
.kpi .value{ font-size: 3.0rem; font-weight: 950; line-height: 1; }
.kpi .tag{ margin-top: 10px; font-size: .86rem; color: rgba(229,231,235,.70); }
.kpi.blue { border-left: 6px solid rgba(56,189,248,0.9); }
.kpi.green{ border-left: 6px solid rgba(34,197,94,0.9); }
.kpi.red  { border-left: 6px solid rgba(239,68,68,0.9); }
.kpi.amber{ border-left: 6px solid rgba(245,158,11,0.95); }

/* GLASS SECTION */
.glass{
  background: rgba(255,255,255,0.06);
  border: 1px solid rgba(255,255,255,0.10);
  border-radius: 18px;
  padding: 16px;
  backdrop-filter: blur(10px);
  animation: fadeIn .7s ease-in-out;
}

/* DATAFRAME DARK MODE */
div[data-testid="stDataFrame"]{
  border-radius:16px;
  overflow:hidden;
  border: 1px solid rgba(255,255,255,0.12);
  background: rgba(10,16,32,0.55) !important;
}

/* Buttons */
.stButton>button{
  border-radius: 14px;
  padding: 10px 14px;
  border: 1px solid rgba(255,255,255,0.16);
  background: rgba(255,255,255,0.08);
  color: #e5e7eb;
}
.stButton>button:hover{
  border: 1px solid rgba(255,255,255,0.30);
  background: rgba(255,255,255,0.14);
}

/* FOOTER */
.app-footer{
  position: fixed;
  left: 0;
  bottom: 0;
  width: 100%;
  text-align: center;
  padding: 12px 0;
  color: rgba(229,231,235,.70);
  background: rgba(7,16,27,0.55);
  border-top: 1px solid rgba(255,255,255,0.10);
  backdrop-filter: blur(10px);
  z-index: 9999;
}
</style>
""",
    unsafe_allow_html=True,
)

# ==========================
# HELPERS: LABEL ANGKA
# ==========================
def fmt_rp(n: int) -> str:
    return f"{n:,.0f}".replace(",", ".")

INCOME_DISPLAY = {
    "Rendah": f"Rendah (≤ {fmt_rp(5_000_000)})",
    "Sedang": f"Sedang ({fmt_rp(5_000_000)}–{fmt_rp(10_000_000)})",
    "Tinggi": f"Tinggi (≥ {fmt_rp(10_000_000)})",
}
AGE_DISPLAY = {
    "Remaja": "Remaja (≤ 17)",
    "Dewasa": "Dewasa (18-60)",
    "Lansia": "Lansia (≥ 60)",
}

def format_penghasilan(v) -> str:
    s = str(v).strip()
    return INCOME_DISPLAY.get(s, s)

def format_usia(v) -> str:
    s = str(v).strip()
    return AGE_DISPLAY.get(s, s)

# ==========================
# LOAD DATA (UPLOAD)
# ==========================
@st.cache_data
def load_data(source) -> pd.DataFrame:
    try:
        df_ = pd.read_csv(source, encoding="utf-8-sig", sep=";")
    except Exception:
        df_ = pd.read_csv(source, encoding="utf-8-sig", sep=",")

    df_.columns = [str(c).strip() for c in df_.columns]
    df_ = df_.fillna("").applymap(lambda x: str(x).strip())
    return df_

# ==========================
# SIDEBAR
# ==========================
with st.sidebar:
    st.markdown('<div class="logo-wrap">', unsafe_allow_html=True)
    if os.path.exists("logo.png"):
        st.image("logo.png", use_container_width=True)
    else:
        st.markdown("### 🏷️ Logo belum ada")
        st.caption("Taruh file **logo.png** di folder project.")
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("**Mulana Property**")
    st.caption("Klasifikasi Data Pelanggan (ID3)")

    st.markdown("## ⚙️ Pengaturan")

    uploaded_csv = st.file_uploader("📤 Upload CSV", type=["csv"])

    # ✅ GANTI: jangan text_input disabled (biar ga putih)
    st.markdown("**Nama file CSV**")
    st.markdown(
        """
        <div class="readonly">
          <small>file wajib upload</small>
        </div>
        """,
        unsafe_allow_html=True,
    )

    target_col = st.text_input("Kolom Target", value="Keputusan", key="target_col_cfg")

    st.markdown("---")
    st.markdown("### 🔍 Filter Data")

# ==========================
# WAJIB UPLOAD DULU
# ==========================
if uploaded_csv is None:
    st.markdown(
        """
    <div class="hero">
      <h1>📤 Upload CSV dulu ya</h1>
      <p>Silakan upload file CSV di sidebar untuk menampilkan data, visualisasi, dan prediksi ID3.</p>
    </div>
    """,
        unsafe_allow_html=True,
    )
    st.stop()

# ==========================
# LOAD DF
# ==========================
try:
    df = load_data(uploaded_csv)
    st.sidebar.success(f"Memakai file upload: {uploaded_csv.name}")
except Exception as e:
    st.error(f"Gagal membaca CSV upload.\n\nDetail: {e}")
    st.stop()

# Drop kolom No kalau ada
if "No" in df.columns:
    df = df.drop(columns=["No"])

required = ["Nama", "Penghasilan", "Usia", "Pekerjaan", "Kredit", target_col]
missing = [c for c in required if c not in df.columns]
if missing:
    st.error(f"Kolom kurang: {missing}\nKolom yang ada: {list(df.columns)}")
    st.stop()

# ==========================
# FILTERS
# ==========================
with st.sidebar:
    pekerjaan = st.multiselect(
        "Pilih Pekerjaan",
        options=sorted(df["Pekerjaan"].unique()),
        default=sorted(df["Pekerjaan"].unique()),
        key="pekerjaan_filter",
    )
    kredit = st.multiselect(
        "Kondisi Kredit",
        options=sorted(df["Kredit"].unique()),
        default=sorted(df["Kredit"].unique()),
        key="kredit_filter",
    )
    keputusan = st.selectbox(
        "Keputusan",
        options=["Semua"] + sorted(df[target_col].unique()),
        key="keputusan_filter",
    )

    st.markdown("---")
    st.markdown("### 🧪 Evaluasi")
    test_size = st.slider("Test size", 0.1, 0.5, 0.2, 0.05, key="test_size")
    seed = st.number_input("Random seed", min_value=0, max_value=9999, value=42, step=1, key="seed")

# ==========================
# FILTER LOGIC
# ==========================
df_filtered = df[(df["Pekerjaan"].isin(pekerjaan)) & (df["Kredit"].isin(kredit))]
if keputusan != "Semua":
    df_filtered = df_filtered[df_filtered[target_col].str.lower() == keputusan.lower()]

display_df = df_filtered.copy()
display_df.insert(0, "No", range(1, len(display_df) + 1))

display_df_view = display_df.copy()
display_df_view["Penghasilan"] = display_df_view["Penghasilan"].apply(format_penghasilan)
display_df_view["Usia"] = display_df_view["Usia"].apply(format_usia)

# ==========================
# HERO
# ==========================
st.markdown(
    """
<div class="hero">
  <h1>📊 Data Pelanggan Mulana Property</h1>
  <p>Visualisasi interaktif + Information</p>
</div>
""",
    unsafe_allow_html=True,
)

# ==========================
# KPI
# ==========================
total = len(df_filtered)
iya = (df_filtered[target_col].str.lower() == "iya").sum()
tidak = (df_filtered[target_col].str.lower() == "tidak").sum()
persen = (iya / total * 100) if total > 0 else 0

st.markdown(
    f"""
<div class="stats-grid">
  <div class="kpi blue">
    <div class="label">Total Data</div>
    <div class="value">{total}</div>
    <div class="tag">Jumlah baris setelah filter</div>
  </div>
  <div class="kpi green">
    <div class="label">Iya</div>
    <div class="value">{iya}</div>
    <div class="tag">Total keputusan = Iya</div>
  </div>
  <div class="kpi red">
    <div class="label">Tidak</div>
    <div class="value">{tidak}</div>
    <div class="tag">Total keputusan = Tidak</div>
  </div>
  <div class="kpi amber">
    <div class="label">Persentase Iya</div>
    <div class="value">{persen:.0f}%</div>
    <div class="tag">Total Persentase</div>
  </div>
</div>
""",
    unsafe_allow_html=True,
)

st.write("")

# ==========================
# TRAIN ID3
# ==========================
features = ["Penghasilan", "Usia", "Pekerjaan", "Kredit"]

def train_test_split(df_in: pd.DataFrame, test_size: float, seed: int):
    idx = list(range(len(df_in)))
    random.Random(seed).shuffle(idx)
    cut = int(len(idx) * (1 - test_size))
    train_idx = idx[:cut]
    test_idx = idx[cut:]
    return df_in.iloc[train_idx].reset_index(drop=True), df_in.iloc[test_idx].reset_index(drop=True)

df_for_model = df_filtered.copy()
if len(df_for_model) < 5:
    df_for_model = df.copy()

train_df, test_df = train_test_split(df_for_model, float(test_size), int(seed))
tree = build_id3(train_df.to_dict(orient="records"), features, target_col)

y_true = test_df[target_col].tolist()
y_pred = [predict(tree, row) for row in test_df[features].to_dict(orient="records")]
acc = sum(1 for t, p in zip(y_true, y_pred) if t == p) / max(1, len(y_true))

# ==========================
# CHART STYLE
# ==========================
CHART_BG = "rgba(255,255,255,0.07)"
PAPER_BG = "rgba(0,0,0,0)"
GRID_CLR = "rgba(255,255,255,0.10)"
FONT_CLR = "rgba(229,231,235,0.90)"

def style_fig(fig):
    fig.update_layout(
        plot_bgcolor=CHART_BG,
        paper_bgcolor=PAPER_BG,
        font=dict(color=FONT_CLR, size=14),
        legend=dict(bgcolor="rgba(0,0,0,0)"),
        margin=dict(l=10, r=10, t=55, b=10),
    )
    fig.update_xaxes(showgrid=False, color=FONT_CLR)
    fig.update_yaxes(showgrid=True, gridcolor=GRID_CLR, zeroline=False, color=FONT_CLR)
    return fig

# ==========================
# TABS
# ==========================
tab1, tab2, tab3 = st.tabs(["📈 Visualisasi", "🌳 Model ID3", "🔮 Prediksi"])

with tab1:
    st.markdown('<div class="glass">', unsafe_allow_html=True)

    st.subheader("🧾 Data (Setelah Difilter)")
    st.dataframe(display_df_view, use_container_width=True, hide_index=True)

    csv = df_filtered.to_csv(index=False)
    st.download_button("📥 Download Data Filtered (CSV)", csv, "data_pelanggan_filtered.csv", "text/csv")

    st.divider()
    st.subheader("📈 Visualisasi Data Pelanggan")

    fig1 = px.bar(
        df_filtered,
        x="Pekerjaan",
        color=target_col,
        barmode="group",
        title="Jumlah Keputusan Berdasarkan Pekerjaan",
        color_discrete_sequence=["#38bdf8", "#a78bfa", "#34d399", "#fb7185"],
    )
    fig1 = style_fig(fig1)
    fig1.update_traces(marker_line_width=0)
    st.plotly_chart(fig1, use_container_width=True)

    # ✅ PIE BARU: IYA vs TIDAK
    decision_counts = (
        df_filtered[target_col]
        .astype(str)
        .str.strip()
        .str.lower()
        .replace({"iya": "Iya", "tidak": "Tidak"})
        .value_counts()
        .reindex(["Iya", "Tidak"])
        .fillna(0)
        .reset_index()
    )
    decision_counts.columns = ["Keputusan", "Jumlah"]

    fig2 = px.pie(
        decision_counts,
        names="Keputusan",
        values="Jumlah",
        title="Proporsi Potensi Keputusan (Iya vs Tidak)",
        hole=0.55,
        color="Keputusan",
        color_discrete_map={"Iya": "#34d399", "Tidak": "#60a5fa"},
    )
    fig2 = style_fig(fig2)
    fig2.update_traces(textfont_color=FONT_CLR)
    st.plotly_chart(fig2, use_container_width=True)

    st.markdown("</div>", unsafe_allow_html=True)

with tab2:
    st.markdown('<div class="glass">', unsafe_allow_html=True)
    st.subheader("🌳 Model ID3 (Decision Tree)")
    st.info(f"Akurasi evaluasi (split): **{acc*100:.2f}%**  (train={len(train_df)} | test={len(test_df)})")
    st.code(tree_to_text(tree), language="text")

    st.subheader("📜 Rules (IF–THEN)")
    rules = rules_from_tree(tree)

    rules_lines = []
    for i, (cond, label) in enumerate(rules, start=1):
        st.write(f"**{i}.** IF `{cond}` THEN **{target_col} = {label}**")
        rules_lines.append(f"{i}. IF {cond} THEN {target_col} = {label}")

    st.download_button("⬇️ Download Rules (.txt)", "\n".join(rules_lines), "rules_id3.txt", "text/plain")
    st.markdown("</div>", unsafe_allow_html=True)

# ==========================
# TAB PREDIKSI
# ==========================
def _apply_name_to_inputs():
    nama = st.session_state.get("pred_nama", "")
    if not nama or nama == "(Manual)":
        return

    rows = df[df.get("Nama", "").astype(str) == str(nama)]
    if rows.empty:
        return

    r = rows.iloc[0]
    st.session_state["pred_penghasilan"] = str(r["Penghasilan"])
    st.session_state["pred_usia"] = str(r["Usia"])
    st.session_state["pred_pekerjaan"] = str(r["Pekerjaan"])
    st.session_state["pred_kredit"] = str(r["Kredit"])

with tab3:
    st.markdown('<div class="glass">', unsafe_allow_html=True)
    st.subheader("🔮 Prediksi Keputusan (ID3)")

    nama_list = ["(Manual)"]
    if "Nama" in df.columns:
        nama_vals = [x for x in sorted(df["Nama"].astype(str).unique()) if x.strip() != ""]
        nama_list += nama_vals

    c0, c1, c2, c3, c4 = st.columns([1.4, 2.2, 1.6, 1.2, 1.2])
    sample = {}

    with c0:
        st.selectbox("Nama", options=nama_list, key="pred_nama", on_change=_apply_name_to_inputs)

    with c1:
        sample["Penghasilan"] = st.selectbox(
            "Penghasilan",
            sorted(df["Penghasilan"].unique()),
            key="pred_penghasilan",
            format_func=format_penghasilan,
        )

    with c2:
        sample["Usia"] = st.selectbox(
            "Usia",
            sorted(df["Usia"].unique()),
            key="pred_usia",
            format_func=format_usia,
        )

    with c3:
        sample["Pekerjaan"] = st.selectbox("Pekerjaan", sorted(df["Pekerjaan"].unique()), key="pred_pekerjaan")

    with c4:
        sample["Kredit"] = st.selectbox("Kredit", sorted(df["Kredit"].unique()), key="pred_kredit")

    if st.button("✅ Prediksi Sekarang", key="btn_pred"):
        hasil = predict(tree, sample)
        st.success(f"Hasil Prediksi Keputusan: **{hasil}**")

    st.markdown("</div>", unsafe_allow_html=True)

# ==========================
# FOOTER
# ==========================
st.markdown(
    """
<div class="app-footer">
  © 2025 Dashboard Data Pelanggan | Mulana Property
</div>
""",
    unsafe_allow_html=True,
)
