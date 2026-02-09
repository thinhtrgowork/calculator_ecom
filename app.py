import streamlit as st
import pandas as pd
st.markdown("""
<style>
/* ===== BASE ===== */
body { background:#f5f7fb; color:#111827; }
.block-container { padding-top:2rem; }
.section-title { font-size: 24px; font-weight:700; margin-bottom:12px; }

/* ===== RESULT CARD ===== */
.result-card {
    position:relative;
    background:#fff;
    padding:22px;
    border-radius:18px;
    border:1px solid #e5e7eb;
    box-shadow:0 10px 20px rgba(0,0,0,.05);
    transition:.25s;
    overflow:hidden;
}
.result-card:hover {
    transform:translateY(-4px);
    box-shadow:0 18px 36px rgba(0,0,0,.08);
}
.result-card::before {
    content:"";
    position:absolute;
    left:0; top:0;
    width:6px; height:100%;
}

/* ===== RESULT CONTENT ===== */
.result-header {
    display:flex;
    justify-content:space-between;
    margin-bottom:12px;
}
.result-title {
    font-size:13px;
    font-weight:600;
    color:#6b7280;
    letter-spacing:.04em;
    text-transform:uppercase;
}
.result-icon {
    width:36px; height:36px;
    border-radius:50%;
    display:flex;
    align-items:center;
    justify-content:center;
    font-size:18px;
}
.result-value {
    font-size:30px;
    font-weight:800;
    margin-bottom:4px;
}
.sub-note { font-size:12px; color:#6b7280; }

/* ===== COLOR VARIANTS ===== */
.profit-positive { color:#16a34a; }
.profit-negative { color:#dc2626; }
.margin-color { color:#2563eb; }
.cost-color { color:#f59e0b; }

.card-profit::before { background:linear-gradient(#22c55e,#16a34a); }
.card-margin::before { background:linear-gradient(#3b82f6,#2563eb); }
.card-cost::before { background:linear-gradient(#fbbf24,#f59e0b); }

.card-profit .result-icon { background:rgba(34,197,94,.12); }
.card-margin .result-icon { background:rgba(59,130,246,.12); }
.card-cost .result-icon { background:rgba(251,191,36,.18); }

/* ===== SIDEBAR ===== */
section[data-testid="stSidebar"] {
    background:linear-gradient(#fff,#fafafa);
    border-right:1px solid #e5e7eb;
}
section[data-testid="stSidebar"] .block-container {
    padding:1.25rem;
}

/* ===== BADGE & FEE ===== */
.badge {
    display:inline-block;
    padding:3px 10px;
    border-radius:999px;
    font-size:11px;
    font-weight:600;
}
.badge-normal { background:#dcfce7; color:#166534; }
.badge-mall { background:#fee2e2; color:#991b1b; }

.fee-highlight {
    margin-top:10px;
    padding:10px 12px;
    border-radius:12px;
    background:#f8fafc;
    border:1px dashed #e5e7eb;
    font-size:13px;
}
            /* ---------- SHOP TYPE PILLS ---------- */
.shop-pill-group {
    display:flex;
    gap:12px;
}

.shop-pill {
    flex:1;
    text-align:center;
    padding:12px 0;
    border-radius:14px;
    font-size:14px;
    font-weight:700;
    cursor:pointer;
    border:1px solid #e5e7eb;
    background:#f8fafc;
    color:#475569;
}

.shop-pill.active-normal {
    background:#e0f2fe;
    border-color:#38bdf8;
    color:#0369a1;
}

.shop-pill.active-mall {
    background:#ffe4e6;
    border-color:#fb7185;
    color:#be123c;
}

.shop-desc {
    font-size:12px;
    color:#64748b;
    margin-top:6px;
    text-align:center;
}
            /* Sidebar container */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #f8f9fc, #eef1f6);
}


/* Hover */
div[role="radiogroup"] > label:hover {
    border-color: #d0d5dd;
}

/* Selected */
div[role="radiogroup"] > label[data-checked="true"] {
    border-color: #6366f1;
    background: #eef2ff;
}
</style>
""", unsafe_allow_html=True)


# ======================
# PAGE CONFIG
# ======================
st.set_page_config(
    page_title="TikTok Profit Calculator",
    layout="centered"
)
st.markdown("""
<style>
.platform-btn {
    width: 100%;
    padding: 14px 0;
    border-radius: 16px;
    border: 1px solid #e5e7eb;
    font-size: 16px;
    font-weight: 800;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 10px;
    cursor: pointer;
    background: #ffffff;
    transition: all 0.25s ease;
}

.platform-btn img {
    height: 22px;
}

.platform-btn:hover {
    transform: translateY(-2px);
    box-shadow: 0 10px 24px rgba(0,0,0,0.08);
}

/* TikTok */
.platform-tiktok.active {
    background: linear-gradient(90deg, #ff0050, #00f2ea);
    color: white;
    border: none;
}

/* Shopee */
.platform-shopee.active {
    background: linear-gradient(90deg, #ee4d2d, #ff7337);
    color: white;
    border: none;
}
</style>
""", unsafe_allow_html=True)

with st.sidebar:
    st.markdown("### 🛒 Nền tảng")

    if "platform" not in st.session_state:
        st.session_state.platform = "TikTok"

    col1, col2 = st.columns(2)

    with col1:
        if st.button("➡️ TikTok",  width="stretch"):
            st.session_state.platform = "TikTok"

    with col2:
        if st.button("➡️ Shopee",  width="stretch"):
            st.session_state.platform = "Shopee"

    platform = st.session_state.platform

df_shopee = pd.DataFrame({
    "Order ID": ["SP001", "SP002"],
    "Doanh thu": [900000, 1200000],
    "Trạng thái": ["Hoàn tất", "Đã hủy"]
})

if platform == "TikTok":
    # ======================
    # DATA NGÀNH HÀNG
    # ======================
    categories = pd.DataFrame([
        {"category": "Tương & hỗn hợp gia vị nấu ăn", "fee": 0.0884},
        {"category": "Thời trang", "fee": 0.0982},
        {"category": "Giày", "fee": 0.108},
        {"category": "Kẹo", "fee": 0.0884},
        {"category": "Bàn phím & Chuột", "fee": 0.0785},
        {"category": "Thực phẩm bổ sung sức khỏe", "fee": 0.1129},
        {"category": "Sách", "fee": 0.108},
       

    ])

    st.markdown("""
    <style>
    /* ---------- HEADER ---------- */
    .app-header {
        display:flex;
        flex-direction:column;
        align-items:center;
        gap:10px;
        margin-bottom:28px;
    }

    .app-title {
        font-size: 48px;
        font-weight: 900;
        margin: 0;

        background: linear-gradient(
            90deg,
            #000000,   /* TikTok black */
            #ff0050,   /* TikTok pink */
            #00f2ea    /* TikTok cyan */
        );

        -webkit-background-clip: text;
        background-clip: text;
        color: transparent;
    }

    .app-subtitle {
        display:inline-flex;
        align-items:center;
        gap:8px;
        background:#f1f5f9;
        padding:6px 16px;
        border-radius:999px;
        font-size:13px;
        color:#475569;
        font-weight:500;
    }

    /* ---------- BADGE ---------- */
    .badge {
        display:inline-block;
        margin-top:10px;
        padding:4px 12px;
        border-radius:999px;
        font-size:12px;
        font-weight:700;
    }

    .badge-normal {
        background:#e0f2fe;
        color:#0369a1;
    }

    .badge-mall {
        background:#ffe4e6;
        color:#be123c;
    }

    /* ---------- FEE ---------- */
    .fee-highlight {
        margin-top:10px;
        background:#f8fafc;
        border:1px dashed #cbd5e1;
        padding:10px 12px;
        border-radius:12px;
        font-size:13px;
        color:#334155;
    }

    /* ---------- RADIO & SELECT ---------- */
    div[data-baseweb="radio"] label {
        font-size:14px;
        font-weight:500;
    }

    div[data-baseweb="select"] > div {
        border-radius:12px;
    }
    </style>
    """, unsafe_allow_html=True)

    # ======================
    # HEADER
    # ======================
    st.markdown("""
    <style>
    .shop-card {
        border-radius: 16px;
        padding: 18px;
        cursor: pointer;
        border: 2px solid transparent;
        background: #f8fafc;
        transition: all 0.25s ease;
        height: 100%;
    }

    .shop-card:hover {
        transform: translateY(-2px);
        background: #f1f5f9;
    }

    .shop-card.active-normal {
        border-color: #ff0050;
        background: #fff1f5;
    }

    .shop-card.active-mall {
        border-color: #2563eb;
        background: #eff6ff;
    }

    .shop-title {
        font-weight: 700;
        font-size: 16px;
        margin-bottom: 4px;
    }

    .shop-desc {
        font-size: 13px;
        color: #64748b;
    }

    .shop-badge {
        display: inline-block;
        margin-top: 10px;
        padding: 4px 10px;
        border-radius: 999px;
        font-size: 12px;
        font-weight: 600;
    }

    .badge-normal {
        background: #ff0050;
        color: white;
    }

    .badge-mall {
        background: #2563eb;
        color: white;
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="app-header">
        <div class="app-title">TikTok Profit Calculator</div>
        <div class="app-subtitle">📊 Công cụ tính lợi nhuận TikTok Shop</div>
    </div>
    """, unsafe_allow_html=True)
    # ======================
    # INPUT SECTION
    # ======================
    st.markdown('<div class="section-title">📦 Ngành hàng</div>',
                unsafe_allow_html=True)
    st.write("")
    selected_category = st.selectbox(
        label="Chọn ngành hàng",
        options=categories,
        index=0,
        label_visibility="collapsed"
    )

    fee_rate = categories.loc[
        categories["category"] == selected_category, "fee"
    ].values[0]

    st.markdown(
        f"""
        <div class="fee-highlight">
            💰 Phí nền tảng: <b>{fee_rate*100:.2f}%</b>
        </div>
        """,
        unsafe_allow_html=True
    )
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("""
    <style>
    /* ===== TITLE ===== */
    .price-title {
        font-size: 24px;
        font-weight: 700;
        color: #111827;
        display: flex;
        align-items: center;
        gap: 8px;
        margin-bottom: 4px;
    }

    /* ===== HINT ===== */
    .price-hint {
        font-size: 12px;
        color: #6b7280;
        margin-bottom: 10px;
    }

    /* ===== NUMBER INPUT STYLE ===== */
    div[data-baseweb="input"] {
        border-radius: 14px !important;
        border: 1px solid #e5e7eb !important;
        background: #ffffff !important;
        box-shadow: inset 0 1px 2px rgba(0,0,0,0.04);
    }

    /* Focus */
    div[data-baseweb="input"]:focus-within {
        border-color: #ff0050 !important;
        box-shadow: 0 0 0 3px rgba(255,0,80,0.15) !important;
    }

    /* Input text */
    input[type="number"] {
        font-size: 16px !important;
        font-weight: 700 !important;
        color: #111827 !important;
        padding: 10px 12px !important;
    }
    </style>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
    <div class="">
        <div class="price-title">💸 Giá nhập</div>
        <div class="price-hint">Chi phí nhập 1 sản phẩm</div>
    """, unsafe_allow_html=True)

        cost_price = st.number_input(
            "Giá nhập (VNĐ)",
            min_value=0.0,
            value=41000.0,
            step=1000.0,
            label_visibility="collapsed"
        )

        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        st.markdown("""
    <div class="">
        <div class="price-title">🏷️ Giá bán</div>
        <div class="price-hint">Giá niêm yết trên TikTok</div>
    """, unsafe_allow_html=True)

        sell_price = st.number_input(
            "Giá bán (VNĐ)",
            min_value=0.0,
            value=75000.0,
            step=1000.0,
            label_visibility="collapsed"
        )

        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown('<div class="section-title">Thiết lập chi phí</div>',
                unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)

    with c1:
        affiliate_fee = st.number_input(
            "✏️ Affiliate (%)",
            min_value=0.0,
            max_value=50.0,
            value=7.0,
            step=0.1
        ) / 100
        transaction_fee_rate = st.number_input(
            "Transaction fee (%)",
            min_value=0.0,
            max_value=50.0,
            value=5.0,      # ✅ mặc định 5%
            step=0.5
        ) / 100

        voucher_fee = st.number_input(
            "Voucher (VNĐ)",
            min_value=0,
            value=0,
            step=1000
        )

    with c2:

        ads_fee = st.number_input(
            "✏️ Quảng cáo (%)",
            min_value=0.0,
            max_value=50.0,
            value=0.0,
            step=0.5
        ) / 100
        extra_voucher_rate = st.number_input(
            "Voucher Extra (%)",
            min_value=0.0,
            max_value=50.0,
            value=3.0,      # ✅ mặc định 3%
            step=0.5
        ) / 100
        SFR_service_fee = st.number_input(
            "Phí SFR service (VNĐ)",
            min_value=0,
            value=1620,
            step=500
        )

    with c3:
        packing_fee = st.number_input(
            "✏️ Phí đóng gói (VNĐ)",
            min_value=0,
            value=1500,
            step=500
        )

        handling_fee = st.number_input(
            "Phí xử lý đơn (VNĐ)",
            min_value=0,
            value=3000,
            step=500
        )

        tax_fee = st.number_input(
            "Thuế (%)",
            min_value=0.0,
            max_value=20.0,
            value=1.5,
            step=0.1
        ) / 100

    # ======================
    # CALCULATION
    # ======================
    platform_fee = sell_price * fee_rate
    affiliate_cost = sell_price * affiliate_fee
    ads_cost = sell_price * ads_fee
    tax_cost = sell_price * tax_fee
    extra_voucher = sell_price * extra_voucher_rate
    transaction_fee = sell_price * transaction_fee_rate

    total_fee = (
        platform_fee
        + affiliate_cost
        + ads_cost
        + tax_cost
        + voucher_fee
        + extra_voucher
        + transaction_fee
        + packing_fee
        + handling_fee
        + SFR_service_fee
    )

    profit = sell_price - cost_price - total_fee
    margin = profit / sell_price if sell_price > 0 else 0

    # ======================
    # RESULT CARDS
    # ======================
    st.markdown('<div class="section-title">Kết quả</div>',
                unsafe_allow_html=True)
    r1, r2, r3 = st.columns(3)
    profit_class = "profit-positive" if profit >= 0 else "profit-negative"

    # --- LỢI NHUẬN ---
    r1.markdown(f"""
    <div class="result-card card-profit">
        <div class="result-header">
            <div class="result-title">Lợi nhuận</div>
            <div class="result-icon">💰</div>
        </div>
        <div class="result-value {profit_class}">
            {profit:,.0f} VNĐ
        </div>
        <div class="sub-note">
            Sau tất cả chi phí
        </div>
    </div>
    """, unsafe_allow_html=True)

    # --- BIÊN LỢI NHUẬN ---
    r2.markdown(f"""
    <div class="result-card card-margin">
        <div class="result-header">
            <div class="result-title">Biên lợi nhuận</div>
            <div class="result-icon">📈</div>
        </div>
        <div class="result-value margin-color">
            {margin:.2%}
        </div>
        <div class="sub-note">
            Lợi nhuận / Giá bán
        </div>
    </div>
    """, unsafe_allow_html=True)

    # --- TỔNG CHI PHÍ ---
    r3.markdown(f"""
    <div class="result-card card-cost">
        <div class="result-header">
            <div class="result-title">Tổng chi phí</div>
            <div class="result-icon">🧾</div>
        </div>
        <div class="result-value cost-color">
            {total_fee:,.0f} VNĐ
        </div>
        <div class="sub-note">
            Phí + Thuế + Voucher
        </div>
    </div>
    """, unsafe_allow_html=True)
    # ======================
    # DETAIL TABLE
    # ======================
    st.write("")
    st.markdown('<div class="section-title">Chi tiết chi phí</div>',
                unsafe_allow_html=True)

    fee_table = pd.DataFrame({
        "Loại phí": [
            "Phí nền tảng",
            "Phí giao dịch",
            "Affiliate",
            "Quảng cáo",
            "Thuế",
            "Voucher",
            "Voucher Extra",
            "Đóng gói",
            "Xử lý đơn"
        ],
        "Số tiền (VNĐ)": [
            platform_fee,
            transaction_fee,
            affiliate_cost,
            ads_cost,
            tax_cost,
            voucher_fee,
            extra_voucher,
            packing_fee,
            handling_fee
        ]
    })

    st.dataframe(
        fee_table.style.format({"Số tiền (VNĐ)": "{:,.0f}"}),
        width="stretch"
    )


elif platform == "Shopee":
    # ======================
    # DATA NGÀNH HÀNG
    # ======================
    categories_sp = pd.DataFrame([
        {"category": "Gia vị & Hương liệu", "fee": 0.11},
        {"category": "Áo", "fee": 0.135},
        {"category": "Giày thể thao/ Sneakers", "fee": 0.125},
        {"category": "Kẹo", "fee": 0.11},
        {"category": "Bàn phím máy tính", "fee": 0.1},
        {"category": "Thực phẩm bổ sung sức khỏe", "fee": 0.1129},
        {"category": "Sách", "fee": 0.12},
        {"category": "Sở thích & Sưu tầm", "fee": 0.13},

    ])

    st.markdown("""
    <style>
    /* ---------- HEADER ---------- */
    .app-header {
        display:flex;
        flex-direction:column;
        align-items:center;
        gap:10px;
        margin-bottom:28px;
    }

    .app-title-sp {
        font-size: 48px;
        font-weight: 900;
        margin: 0;

        background: linear-gradient(
            90deg,
            #ff6a00,   /* Shopee orange */
            #ee4d2d    /* Shopee red-orange */
        );

        -webkit-background-clip: text;
        background-clip: text;
        color: transparent;
    }


    .app-subtitle {
        display:inline-flex;
        align-items:center;
        gap:8px;
        background:#f1f5f9;
        padding:6px 16px;
        border-radius:999px;
        font-size:13px;
        color:#475569;
        font-weight:500;
    }

    /* ---------- BADGE ---------- */
    .badge {
        display:inline-block;
        margin-top:10px;
        padding:4px 12px;
        border-radius:999px;
        font-size:12px;
        font-weight:700;
    }

    .badge-normal {
        background:#e0f2fe;
        color:#0369a1;
    }

    .badge-mall {
        background:#ffe4e6;
        color:#be123c;
    }

    /* ---------- FEE ---------- */
    .fee-highlight {
        margin-top:10px;
        background:#f8fafc;
        border:1px dashed #cbd5e1;
        padding:10px 12px;
        border-radius:12px;
        font-size:13px;
        color:#334155;
    }

    /* ---------- RADIO & SELECT ---------- */
    div[data-baseweb="radio"] label {
        font-size:14px;
        font-weight:500;
    }

    div[data-baseweb="select"] > div {
        border-radius:12px;
    }
    </style>
    """, unsafe_allow_html=True)

    # ======================
    # HEADER
    # ======================
    st.markdown("""
    <style>
    .shop-card {
        border-radius: 16px;
        padding: 18px;
        cursor: pointer;
        border: 2px solid transparent;
        background: #f8fafc;
        transition: all 0.25s ease;
        height: 100%;
    }

    .shop-card:hover {
        transform: translateY(-2px);
        background: #f1f5f9;
    }

    .shop-card.active-normal {
        border-color: #ff0050;
        background: #fff1f5;
    }

    .shop-card.active-mall {
        border-color: #2563eb;
        background: #eff6ff;
    }

    .shop-title {
        font-weight: 700;
        font-size: 16px;
        margin-bottom: 4px;
    }

    .shop-desc {
        font-size: 13px;
        color: #64748b;
    }

    .shop-badge {
        display: inline-block;
        margin-top: 10px;
        padding: 4px 10px;
        border-radius: 999px;
        font-size: 12px;
        font-weight: 600;
    }

    .badge-normal {
        background: #ff0050;
        color: white;
    }

    .badge-mall {
        background: #2563eb;
        color: white;
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="app-header">
        <div class="app-title-sp">Shopee Profit Calculator</div>
        <div class="app-subtitle">📊 Công cụ tính lợi nhuận Shopee Shop</div>
    </div>
    """, unsafe_allow_html=True)
    # ======================
    # INPUT SECTION
    # ======================
    st.markdown('<div class="section-title">📦 Ngành hàng</div>',
                unsafe_allow_html=True)
    st.write("")

    selected_category = st.selectbox(
        label="Chọn ngành hàng",
        options=categories_sp,
        index=0,
        label_visibility="collapsed"
    )

    fee_rate_sp = categories_sp.loc[
        categories_sp["category"] == selected_category, "fee"
    ].values[0]

    st.markdown(
        f"""
        <div class="fee-highlight">
            💰 Phí nền tảng: <b>{fee_rate_sp*100:.2f}%</b>
        </div>
        """,
        unsafe_allow_html=True
    )
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("""
    <style>
    /* ===== TITLE ===== */
    .price-title {
        font-size: 24px;
        font-weight: 700;
        color: #111827;
        display: flex;
        align-items: center;
        gap: 8px;
        margin-bottom: 4px;
    }

    /* ===== HINT ===== */
    .price-hint {
        font-size: 12px;
        color: #6b7280;
        margin-bottom: 10px;
    }

    /* ===== NUMBER INPUT STYLE ===== */
    div[data-baseweb="input"] {
        border-radius: 14px !important;
        border: 1px solid #e5e7eb !important;
        background: #ffffff !important;
        box-shadow: inset 0 1px 2px rgba(0,0,0,0.04);
    }

    /* Focus */
    div[data-baseweb="input"]:focus-within {
        border-color: #ff0050 !important;
        box-shadow: 0 0 0 3px rgba(255,0,80,0.15) !important;
    }

    /* Input text */
    input[type="number"] {
        font-size: 16px !important;
        font-weight: 700 !important;
        color: #111827 !important;
        padding: 10px 12px !important;
    }
    </style>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
    <div class="">
        <div class="price-title">💸 Giá nhập</div>
        <div class="price-hint">Chi phí nhập 1 sản phẩm</div>
    """, unsafe_allow_html=True)

        cost_price_sp = st.number_input(
            "Giá nhập (VNĐ)",
            min_value=0.0,
            value=41000.0,
            step=1000.0,
            label_visibility="collapsed"
        )

        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        st.markdown("""
    <div class="">
        <div class="price-title">🏷️ Giá bán</div>
        <div class="price-hint">Giá niêm yết trên TikTok</div>
    """, unsafe_allow_html=True)

        sell_price_sp = st.number_input(
            "Giá bán (VNĐ)",
            min_value=0.0,
            value=75000.0,
            step=1000.0,
            label_visibility="collapsed"
        )

        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown('<div class="section-title">Thiết lập chi phí</div>',
                unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)

    with c1:
        affiliate_fee_sp = st.number_input(
            "✏️ Affiliate (%)",
            min_value=0.0,
            max_value=50.0,
            value=7.0,
            step=0.5
        ) / 100

        transaction_fee_rate_sp = st.number_input(
            "Transaction fee (%)",
            min_value=0.0,
            max_value=50.0,
            value=4.91,      # ✅ mặc định 4.91%
            step=0.5
        ) / 100
        voucher_fee_sp = st.number_input(
            "Voucher (VNĐ)",
            min_value=0,
            value=0,
            step=1000
        )

    with c2:

        ads_fee_sp = st.number_input(
            "✏️ Quảng cáo (%)",
            min_value=0.0,
            max_value=50.0,
            value=0.0,
            step=0.5
        ) / 100

        extra_voucher_rate_sp = st.number_input(
            "Voucher Extra (%)",
            min_value=0.0,
            max_value=50.0,
            value=4.0,      # ✅ mặc định 4%
            step=0.5
        ) / 100
        Pi_Ship_fee = st.number_input(
            "Phí Pi Ship (VNĐ)",
            min_value=0,
            value=1620,
            step=500
        )

    with c3:
        packing_fee_sp = st.number_input(
            "✏️ Phí đóng gói (VNĐ)",
            min_value=0,
            value=1500,
            step=500
        )

        HT_fee_sp = st.number_input(
            "Phí hạ tầng (VNĐ)",
            min_value=0,
            value=3000,
            step=500
        )

        tax_fee_sp = st.number_input(
            "Thuế (%)",
            min_value=0.0,
            max_value=20.0,
            value=1.5,
            step=0.1
        ) / 100

    # ======================
    # CALCULATION
    # ======================
    platform_fee_sp = sell_price_sp * fee_rate_sp
    affiliate_cost_sp = sell_price_sp * affiliate_fee_sp
    ads_cost_sp = sell_price_sp * ads_fee_sp
    tax_cost_sp = sell_price_sp * tax_fee_sp
    extra_voucher_sp = sell_price_sp * extra_voucher_rate_sp
    transaction_fee_sp = sell_price_sp * transaction_fee_rate_sp

    total_fee = (
        platform_fee_sp
        + affiliate_cost_sp
        + ads_cost_sp
        + tax_cost_sp
        + voucher_fee_sp
        + extra_voucher_sp
        + transaction_fee_sp
        + packing_fee_sp
        + HT_fee_sp
        + Pi_Ship_fee
    )

    profit_sp = sell_price_sp - cost_price_sp - total_fee
    margin_sp = profit_sp / sell_price_sp if sell_price_sp > 0 else 0

    # ======================
    # RESULT CARDS
    # ======================
    st.markdown('<div class="section-title">Kết quả</div>',
                unsafe_allow_html=True)
    r1, r2, r3 = st.columns(3)
    profit_class = "profit-positive" if profit_sp >= 0 else "profit-negative"

    # --- LỢI NHUẬN ---
    r1.markdown(f"""
    <div class="result-card card-profit">
        <div class="result-header">
            <div class="result-title">Lợi nhuận</div>
            <div class="result-icon">💰</div>
        </div>
        <div class="result-value {profit_class}">
            {profit_sp:,.0f} VNĐ
        </div>
        <div class="sub-note">
            Sau tất cả chi phí
        </div>
    </div>
    """, unsafe_allow_html=True)

    # --- BIÊN LỢI NHUẬN ---
    r2.markdown(f"""
    <div class="result-card card-margin">
        <div class="result-header">
            <div class="result-title">Biên lợi nhuận</div>
            <div class="result-icon">📈</div>
        </div>
        <div class="result-value margin-color">
            {margin_sp:.2%}
        </div>
        <div class="sub-note">
            Lợi nhuận / Giá bán
        </div>
    </div>
    """, unsafe_allow_html=True)

    # --- TỔNG CHI PHÍ ---
    r3.markdown(f"""
    <div class="result-card card-cost">
        <div class="result-header">
            <div class="result-title">Tổng chi phí</div>
            <div class="result-icon">🧾</div>
        </div>
        <div class="result-value cost-color">
            {total_fee:,.0f} VNĐ
        </div>
        <div class="sub-note">
            Phí + Thuế + Voucher
        </div>
    </div>
    """, unsafe_allow_html=True)
    # ======================
    # DETAIL TABLE
    # ======================
    st.write("")
    st.markdown('<div class="section-title">Chi tiết chi phí</div>',
                unsafe_allow_html=True)

    fee_table = pd.DataFrame({
        "Loại phí": [
            "Phí nền tảng",
            "Phí giao dịch",
            "Affiliate",
            "Quảng cáo",
            "Voucher",
            "Voucher Extra",
            "Phí hạ tầng",
            "Thuế",
            "Phí Pi Ship",
            "Đóng gói"
        ],
        "Số tiền (VNĐ)": [
            platform_fee_sp,
            transaction_fee_sp,
            affiliate_cost_sp,
            ads_cost_sp,
            voucher_fee_sp,
            extra_voucher_sp,
            HT_fee_sp,
            tax_cost_sp,
            Pi_Ship_fee,
            packing_fee_sp,
        ]
    })

    st.dataframe(
        fee_table.style.format({"Số tiền (VNĐ)": "{:,.0f}"}),
        width="stretch"
    )


