import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import warnings
warnings.filterwarnings('ignore')

st.set_page_config(
    page_title="Iran War Oil Price Analysis",
    page_icon="🛢️",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
    .hero-banner {
        background: linear-gradient(135deg, #0a0e1a 0%, #1a1f35 40%, #0d2137 100%);
        border: 1px solid #1e3a5f; border-radius: 16px;
        padding: 36px 40px; margin-bottom: 28px;
    }
    .hero-title { font-size: 2.2rem; font-weight: 700; color: #f0f4ff; margin: 0 0 8px 0; }
    .hero-subtitle { font-size: 1rem; color: #7a8ba0; margin: 0; }
    .hero-badge {
        display: inline-block; background: rgba(255,80,0,0.15);
        border: 1px solid rgba(255,80,0,0.3); color: #ff6030;
        padding: 4px 12px; border-radius: 20px; font-size: 0.75rem;
        font-weight: 600; margin-bottom: 12px; text-transform: uppercase;
    }
    .metric-card {
        background: linear-gradient(145deg, #111827, #1a2235);
        border: 1px solid #1e3a5f; border-radius: 12px;
        padding: 20px 22px; margin-bottom: 12px;
    }
    .metric-label { font-size: 0.78rem; color: #6b7a99; font-weight: 500; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 6px; }
    .metric-value { font-size: 1.8rem; font-weight: 700; color: #e8f0fe; line-height: 1; }
    .metric-delta { font-size: 0.82rem; margin-top: 6px; }
    .delta-up { color: #ff5722; }
    .delta-down { color: #4caf50; }
    .section-header {
        font-size: 1.15rem; font-weight: 600; color: #c8d8f0;
        border-left: 3px solid #1e6fff; padding-left: 12px; margin: 24px 0 16px 0;
    }
    .ai-chat-container {
        background: linear-gradient(145deg, #0d1525, #111827);
        border: 1px solid #1e3a5f; border-radius: 16px; padding: 24px; margin-top: 8px;
    }
    .user-bubble {
        background: linear-gradient(135deg, #1e3a6e, #1a2f5a);
        border: 1px solid #2a4f8a; border-radius: 12px 12px 4px 12px;
        padding: 12px 16px; margin: 10px 0; margin-left: 15%;
        color: #d0e0ff; font-size: 0.9rem;
    }
    .ai-bubble {
        background: linear-gradient(135deg, #111827, #1a2235);
        border: 1px solid #1e3a5f; border-radius: 4px 12px 12px 12px;
        padding: 14px 18px; margin: 10px 0; margin-right: 5%;
        color: #c8d8f0; font-size: 0.9rem; line-height: 1.6;
    }
    .insight-box {
        background: linear-gradient(135deg, #0a1628, #0d1f35);
        border: 1px solid #1a4060; border-radius: 10px;
        padding: 16px 20px; margin: 8px 0;
        font-size: 0.88rem; color: #9ab0cc; line-height: 1.6;
    }
    .insight-box b { color: #64b5f6; }
    footer { visibility: hidden; }
    #MainMenu { visibility: hidden; }
    .stDeployButton { display: none; }
</style>
""", unsafe_allow_html=True)

# ─── Load Data ──────────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    df = pd.read_csv("iran_war_oil_prices_daily_2026.csv")
    df['date'] = pd.to_datetime(df['date'])
    df['price_spread'] = df['brent_usd_barrel'] - df['wti_usd_barrel']
    return df

df = load_data()

# FIX: get war start date as a proper string to avoid numpy datetime64 issue
war_start_str = str(df[df['war_day'] == 1]['date'].iloc[0])[:10]

PHASE_COLORS = {
    "Pre-War Tensions":                          "#64b5f6",
    "Week 1 Shock (Feb 28 - Mar 6)":             "#ffb74d",
    "Week 2 Escalation (Mar 7-13)":              "#ff7043",
    "Week 3 Infrastructure Strikes (Mar 14-21)": "#ef5350",
}

# ─── Sidebar ─────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### 🛢️ Iran War Oil Analysis")
    st.markdown("---")
    page = st.radio("Navigation", [
        "📊 Dashboard",
        "📈 Price Charts",
        "🔍 Data Explorer",
        "📋 Project Summary",
    ])
    st.markdown("---")
    st.markdown("**Dataset Info**")
    st.markdown(f"- 📅 Rows: `{len(df)}`")
    st.markdown(f"- 📊 Columns: `{len(df.columns)}`")
    st.markdown(f"- 🗓️ Period: `Feb 9 – Mar 20, 2026`")
    st.markdown(f"- 📡 Source: AAA/CNBC/Reuters")

# ─── HERO ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero-banner">
  <div class="hero-badge">🔴 LIVE ANALYSIS · MARCH 2026</div>
  <div class="hero-title">🛢️ Iran War Oil Price Intelligence</div>
  <div class="hero-subtitle">
    Real-time data analysis of global crude oil markets during the US-Israel-Iran conflict &nbsp;·&nbsp;
    Brent · WTI · Dubai · US Fuel Prices · Strait of Hormuz · Iran Production
  </div>
</div>
""", unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════════════════
# PAGE 1: DASHBOARD
# ════════════════════════════════════════════════════════════════════════════
if page == "📊 Dashboard":

    latest = df.iloc[-1]
    c1, c2, c3, c4, c5 = st.columns(5)
    with c1:
        st.markdown(f"""<div class="metric-card">
          <div class="metric-label">Brent Crude</div>
          <div class="metric-value">${latest['brent_usd_barrel']:.2f}</div>
          <div class="metric-delta delta-up">▲ {latest['brent_vs_prewar_pct']:.1f}% vs pre-war</div>
        </div>""", unsafe_allow_html=True)
    with c2:
        st.markdown(f"""<div class="metric-card">
          <div class="metric-label">WTI Crude</div>
          <div class="metric-value">${latest['wti_usd_barrel']:.2f}</div>
          <div class="metric-delta delta-up">▲ All-time high</div>
        </div>""", unsafe_allow_html=True)
    with c3:
        st.markdown(f"""<div class="metric-card">
          <div class="metric-label">US Gas Avg/Gal</div>
          <div class="metric-value">${latest['us_gas_avg_gallon']:.2f}</div>
          <div class="metric-delta delta-up">▲ +{latest['gas_vs_prewar_pct']:.1f}% vs pre-war</div>
        </div>""", unsafe_allow_html=True)
    with c4:
        st.markdown(f"""<div class="metric-card">
          <div class="metric-label">Hormuz Ships/Day</div>
          <div class="metric-value">{latest['strait_hormuz_daily_ships']}</div>
          <div class="metric-delta delta-down">▼ Was 138 pre-war</div>
        </div>""", unsafe_allow_html=True)
    with c5:
        st.markdown(f"""<div class="metric-card">
          <div class="metric-label">Iran Production</div>
          <div class="metric-value">{latest['iran_production_mbpd']} <span style="font-size:1rem">mbpd</span></div>
          <div class="metric-delta delta-down">▼ Was 3.3 pre-war</div>
        </div>""", unsafe_allow_html=True)

    col_left, col_right = st.columns([3, 1])

    with col_left:
        st.markdown('<div class="section-header">Oil Price Timeline — All Benchmarks</div>', unsafe_allow_html=True)
        fig = go.Figure()

        # Phase background bands
        for phase, color in PHASE_COLORS.items():
            sub = df[df['phase'] == phase]
            if sub.empty:
                continue
            fig.add_vrect(
                x0=str(sub['date'].min())[:10],
                x1=str(sub['date'].max())[:10],
                fillcolor=color, opacity=0.06, layer="below", line_width=0
            )

        for bm, color, dash, name in [
            ('brent_usd_barrel', '#4fc3f7', 'solid', 'Brent'),
            ('wti_usd_barrel',   '#ffb74d', 'dash',  'WTI'),
            ('dubai_usd_barrel', '#81c784', 'dot',   'Dubai'),
        ]:
            fig.add_trace(go.Scatter(
                x=df['date'].dt.strftime('%Y-%m-%d'),
                y=df[bm],
                mode='lines+markers', name=name,
                line=dict(color=color, width=2.5, dash=dash),
                marker=dict(size=5),
                hovertemplate=f"<b>%{{x}}</b><br>{name}: $%{{y:.2f}}<extra></extra>"
            ))

        # FIX: pass string date to add_vline
        fig.add_vline(
            x=pd.Timestamp(war_start_str),
            line_dash="dash",
            line_color="#ff5722"
        )

        fig.update_layout(
            template="plotly_dark", height=380,
            paper_bgcolor="#0d1525", plot_bgcolor="#0a0e1a",
            legend=dict(orientation="h", yanchor="bottom", y=1.01),
            margin=dict(l=0, r=0, t=40, b=0),
            xaxis=dict(gridcolor="#1a2a40"),
            yaxis=dict(gridcolor="#1a2a40", title="USD / Barrel"),
        )
        st.plotly_chart(fig, use_container_width=True)

    with col_right:
        st.markdown('<div class="section-header">Phase Summary</div>', unsafe_allow_html=True)
        phase_stats = df.groupby('phase').agg(
            avg_brent=('brent_usd_barrel', 'mean'),
            max_brent=('brent_usd_barrel', 'max'),
            days=('date', 'count')
        ).reset_index()
        phase_order_map = {
            "Pre-War Tensions": 0,
            "Week 1 Shock (Feb 28 - Mar 6)": 1,
            "Week 2 Escalation (Mar 7-13)": 2,
            "Week 3 Infrastructure Strikes (Mar 14-21)": 3
        }
        phase_stats['order'] = phase_stats['phase'].map(phase_order_map)
        phase_stats = phase_stats.sort_values('order')
        for _, row in phase_stats.iterrows():
            color = PHASE_COLORS.get(row['phase'], '#64b5f6')
            short = row['phase'].split('(')[0].strip()
            st.markdown(f"""
            <div style="background:#0d1525;border-left:3px solid {color};padding:10px 12px;border-radius:0 8px 8px 0;margin:6px 0">
              <div style="font-size:0.75rem;color:{color};font-weight:600">{short}</div>
              <div style="font-size:0.88rem;color:#c8d8f0;margin-top:4px">Avg: <b>${row['avg_brent']:.1f}</b> · Max: <b>${row['max_brent']:.1f}</b></div>
              <div style="font-size:0.75rem;color:#6b7a99">{int(row['days'])} data points</div>
            </div>""", unsafe_allow_html=True)

    st.markdown('<div class="section-header">Fuel Prices · Hormuz Shipping · Iran Production</div>', unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)

    date_strs = df['date'].dt.strftime('%Y-%m-%d')

    with c1:
        fig2 = go.Figure()
        fig2.add_trace(go.Scatter(x=date_strs, y=df['us_gas_avg_gallon'],
            name="Gas", line=dict(color="#4fc3f7", width=2),
            fill='tozeroy', fillcolor='rgba(79,195,247,0.08)'))
        fig2.add_trace(go.Scatter(x=date_strs, y=df['us_diesel_avg_gallon'],
            name="Diesel", line=dict(color="#ff7043", width=2),
            fill='tozeroy', fillcolor='rgba(255,112,67,0.08)'))
        fig2.update_layout(template="plotly_dark", height=250,
            paper_bgcolor="#0d1525", plot_bgcolor="#0a0e1a",
            margin=dict(l=0,r=0,t=30,b=0), title="US Fuel Prices ($/gal)",
            legend=dict(orientation="h", y=1.1),
            xaxis=dict(gridcolor="#1a2a40"), yaxis=dict(gridcolor="#1a2a40"))
        st.plotly_chart(fig2, use_container_width=True)

    with c2:
        fig3 = go.Figure()
        fig3.add_trace(go.Bar(x=date_strs, y=df['strait_hormuz_daily_ships'],
            marker=dict(color=df['strait_hormuz_daily_ships'],
                        colorscale='RdYlGn', showscale=False),
            name="Ships/Day"))
        fig3.update_layout(template="plotly_dark", height=250,
            paper_bgcolor="#0d1525", plot_bgcolor="#0a0e1a",
            margin=dict(l=0,r=0,t=30,b=0), title="Strait of Hormuz Ships/Day",
            xaxis=dict(gridcolor="#1a2a40"), yaxis=dict(gridcolor="#1a2a40"))
        st.plotly_chart(fig3, use_container_width=True)

    with c3:
        fig4 = go.Figure()
        fig4.add_trace(go.Scatter(x=date_strs, y=df['iran_production_mbpd'],
            mode='lines+markers', line=dict(color="#ef5350", width=2.5),
            fill='tozeroy', fillcolor='rgba(239,83,80,0.1)', name="Iran Output"))
        fig4.update_layout(template="plotly_dark", height=250,
            paper_bgcolor="#0d1525", plot_bgcolor="#0a0e1a",
            margin=dict(l=0,r=0,t=30,b=0), title="Iran Oil Production (mbpd)",
            xaxis=dict(gridcolor="#1a2a40"), yaxis=dict(gridcolor="#1a2a40"))
        st.plotly_chart(fig4, use_container_width=True)

    st.markdown('<div class="section-header">⚡ Key War Events Timeline</div>', unsafe_allow_html=True)
    war_df = df[df['war_day'] > 0].copy()
    for _, row in war_df.iterrows():
        phase_color = PHASE_COLORS.get(row['phase'], '#64b5f6')
        event_short = row['key_event'][:120] + ("…" if len(row['key_event']) > 120 else "")
        st.markdown(f"""
        <div style="background:#0a0e1a;border-left:3px solid {phase_color};padding:10px 16px;margin:5px 0;border-radius:0 8px 8px 0;display:flex;align-items:flex-start;gap:12px">
          <span style="background:{phase_color}22;color:{phase_color};padding:2px 8px;border-radius:8px;font-size:0.75rem;font-weight:700;white-space:nowrap">Day {int(row['war_day'])}</span>
          <span style="font-size:0.82rem;color:#9ab0cc">{event_short} &nbsp;<span style="color:{phase_color}">Brent: ${row['brent_usd_barrel']}</span></span>
        </div>""", unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════════════════
# PAGE 2: PRICE CHARTS
# ════════════════════════════════════════════════════════════════════════════
elif page == "📈 Price Charts":
    st.markdown('<div class="section-header">Interactive Price Charts</div>', unsafe_allow_html=True)

    chart_type = st.selectbox("Select Chart", [
        "Brent vs WTI vs Dubai (Line)",
        "% Change vs Pre-War Level",
        "Price Spread (Brent − WTI)",
        "Average Brent by Phase (Bar)",
        "Correlation Heatmap",
        "Scatter: Oil vs Gas Price",
        "Boxplot: Brent by Phase",
        "Iran Production vs Brent",
    ])

    date_strs = df['date'].dt.strftime('%Y-%m-%d')

    if chart_type == "Brent vs WTI vs Dubai (Line)":
        fig = go.Figure()
        for col, color, name in [
            ('brent_usd_barrel', '#4fc3f7', 'Brent'),
            ('wti_usd_barrel',   '#ffb74d', 'WTI'),
            ('dubai_usd_barrel', '#81c784', 'Dubai'),
        ]:
            fig.add_trace(go.Scatter(x=date_strs, y=df[col],
                mode='lines+markers', name=name,
                line=dict(color=color, width=2)))
        # FIX: string date for add_vline
        fig.add_vline(
                      x=pd.Timestamp(war_start_str),
                      line_dash="dash",
                      line_color="#ff5722")
        fig.update_layout(template="plotly_dark", height=480,
            paper_bgcolor="#0d1525", plot_bgcolor="#0a0e1a",
            title="Global Oil Benchmarks — Feb to Mar 2026",
            xaxis=dict(gridcolor="#1a2a40"), yaxis=dict(gridcolor="#1a2a40", title="USD/Barrel"))
        st.plotly_chart(fig, use_container_width=True)

    elif chart_type == "% Change vs Pre-War Level":
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=date_strs, y=df['brent_vs_prewar_pct'],
            name="Brent %", line=dict(color="#ff7043", width=2)))
        fig.add_trace(go.Scatter(x=date_strs, y=df['gas_vs_prewar_pct'],
            name="Gas %", line=dict(color="#4fc3f7", width=2)))
        fig.add_hline(y=0, line_dash="dash", line_color="#ffffff44")
        fig.update_layout(template="plotly_dark", height=480,
            paper_bgcolor="#0d1525", plot_bgcolor="#0a0e1a",
            title="% Change vs Pre-War Level",
            xaxis=dict(gridcolor="#1a2a40"), yaxis=dict(gridcolor="#1a2a40", title="% Change"))
        st.plotly_chart(fig, use_container_width=True)

    elif chart_type == "Price Spread (Brent − WTI)":
        fig = go.Figure()
        fig.add_trace(go.Bar(x=date_strs, y=df['price_spread'],
            marker=dict(color=df['price_spread'], colorscale='Plasma', showscale=True)))
        fig.update_layout(template="plotly_dark", height=480,
            paper_bgcolor="#0d1525", plot_bgcolor="#0a0e1a",
            title="Brent − WTI Price Spread (USD)",
            xaxis=dict(gridcolor="#1a2a40"), yaxis=dict(gridcolor="#1a2a40"))
        st.plotly_chart(fig, use_container_width=True)

    elif chart_type == "Average Brent by Phase (Bar)":
        phase_avg = df.groupby('phase')['brent_usd_barrel'].mean().reset_index()
        phase_order_map = {
            "Pre-War Tensions": 0,
            "Week 1 Shock (Feb 28 - Mar 6)": 1,
            "Week 2 Escalation (Mar 7-13)": 2,
            "Week 3 Infrastructure Strikes (Mar 14-21)": 3
        }
        phase_avg['order'] = phase_avg['phase'].map(phase_order_map)
        phase_avg = phase_avg.sort_values('order')
        fig = px.bar(phase_avg, x='phase', y='brent_usd_barrel',
            color='phase', color_discrete_map=PHASE_COLORS,
            template="plotly_dark",
            title="Average Brent Crude Price by War Phase",
            labels={'brent_usd_barrel': 'Avg Brent ($/bbl)', 'phase': 'Phase'})
        fig.update_layout(paper_bgcolor="#0d1525", plot_bgcolor="#0a0e1a",
            height=480, showlegend=False)
        st.plotly_chart(fig, use_container_width=True)

    elif chart_type == "Correlation Heatmap":
        num_cols = ['brent_usd_barrel','wti_usd_barrel','dubai_usd_barrel',
                    'us_gas_avg_gallon','us_diesel_avg_gallon',
                    'strait_hormuz_daily_ships','iran_production_mbpd','price_spread']
        corr = df[num_cols].corr()
        fig, ax = plt.subplots(figsize=(9, 6))
        fig.patch.set_facecolor('#0d1525')
        ax.set_facecolor('#0a0e1a')
        sns.heatmap(corr, annot=True, fmt=".2f", cmap='coolwarm',
                    linewidths=0.5, linecolor='#1e3a5f', ax=ax,
                    annot_kws={"size": 9, "color": "white"})
        ax.tick_params(colors='#9ab0cc', labelsize=8)
        plt.title("Correlation Matrix", color='#c8d8f0', fontsize=12)
        st.pyplot(fig)
        plt.close()

    elif chart_type == "Scatter: Oil vs Gas Price":
        fig = px.scatter(df, x='brent_usd_barrel', y='us_gas_avg_gallon',
            color='phase', size='strait_hormuz_daily_ships',
            color_discrete_map=PHASE_COLORS,
            template="plotly_dark",
            hover_data={'date': True, 'key_event': True},
            title="Brent Oil Price vs US Gas Price (bubble = Hormuz ships)",
            labels={'brent_usd_barrel': 'Brent ($/bbl)', 'us_gas_avg_gallon': 'US Gas ($/gal)'})
        fig.update_layout(paper_bgcolor="#0d1525", plot_bgcolor="#0a0e1a", height=480)
        st.plotly_chart(fig, use_container_width=True)

    elif chart_type == "Boxplot: Brent by Phase":
        phase_order_list = [
            "Pre-War Tensions",
            "Week 1 Shock (Feb 28 - Mar 6)",
            "Week 2 Escalation (Mar 7-13)",
            "Week 3 Infrastructure Strikes (Mar 14-21)"
        ]
        fig = px.box(df, x='phase', y='brent_usd_barrel',
            color='phase', color_discrete_map=PHASE_COLORS,
            template="plotly_dark",
            category_orders={"phase": phase_order_list},
            title="Distribution of Brent Crude Prices by War Phase",
            labels={'brent_usd_barrel': 'Brent ($/bbl)', 'phase': 'Phase'})
        fig.update_layout(paper_bgcolor="#0d1525", plot_bgcolor="#0a0e1a",
            height=480, showlegend=False, xaxis_tickangle=-20)
        st.plotly_chart(fig, use_container_width=True)

    elif chart_type == "Iran Production vs Brent":
        fig = make_subplots(specs=[[{"secondary_y": True}]])
        fig.add_trace(go.Scatter(x=date_strs, y=df['brent_usd_barrel'],
            name="Brent", line=dict(color="#4fc3f7", width=2)), secondary_y=False)
        fig.add_trace(go.Scatter(x=date_strs, y=df['iran_production_mbpd'],
            name="Iran Production", line=dict(color="#ef5350", width=2, dash='dash')), secondary_y=True)
        fig.update_layout(template="plotly_dark", paper_bgcolor="#0d1525", plot_bgcolor="#0a0e1a",
            title="Brent Crude vs Iran Oil Production", height=480)
        fig.update_yaxes(title_text="Brent ($/bbl)", secondary_y=False, gridcolor="#1a2a40")
        fig.update_yaxes(title_text="Production (mbpd)", secondary_y=True)
        st.plotly_chart(fig, use_container_width=True)

# ════════════════════════════════════════════════════════════════════════════
# PAGE 3: DATA EXPLORER
# ════════════════════════════════════════════════════════════════════════════
elif page == "🔍 Data Explorer":
    st.markdown('<div class="section-header">Dataset Explorer</div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        phase_filter = st.multiselect("Filter by Phase",
            options=df['phase'].unique().tolist(),
            default=df['phase'].unique().tolist())
    with col2:
        brent_range = st.slider("Brent Price Range ($/bbl)",
            float(df['brent_usd_barrel'].min()), float(df['brent_usd_barrel'].max()),
            (float(df['brent_usd_barrel'].min()), float(df['brent_usd_barrel'].max())))

    filtered = df[
        (df['phase'].isin(phase_filter)) &
        (df['brent_usd_barrel'] >= brent_range[0]) &
        (df['brent_usd_barrel'] <= brent_range[1])
    ]

    st.markdown(f"**{len(filtered)} rows matched**")
    display_cols = ['date', 'brent_usd_barrel', 'wti_usd_barrel', 'dubai_usd_barrel',
                    'us_gas_avg_gallon', 'us_diesel_avg_gallon', 'strait_hormuz_daily_ships',
                    'iran_production_mbpd', 'war_day', 'phase', 'price_spread']
    st.dataframe(
        filtered[display_cols].style
            .format({
                'brent_usd_barrel':  '${:.2f}',
                'wti_usd_barrel':    '${:.2f}',
                'dubai_usd_barrel':  '${:.2f}',
                'us_gas_avg_gallon': '${:.2f}',
                'us_diesel_avg_gallon': '${:.2f}',
                'price_spread':      '${:.2f}',
                'iran_production_mbpd': '{:.1f}'
            })
            .background_gradient(subset=['brent_usd_barrel'], cmap='YlOrRd'),
        use_container_width=True, height=400
    )

    st.markdown('<div class="section-header">Descriptive Statistics</div>', unsafe_allow_html=True)
    num_cols = ['brent_usd_barrel','wti_usd_barrel','dubai_usd_barrel',
                'us_gas_avg_gallon','us_diesel_avg_gallon',
                'strait_hormuz_daily_ships','iran_production_mbpd','price_spread']
    st.dataframe(filtered[num_cols].describe().round(3), use_container_width=True)

    st.markdown('<div class="section-header">GroupBy Aggregation</div>', unsafe_allow_html=True)
    agg_col = st.selectbox("Aggregate Column", [
        'brent_usd_barrel','wti_usd_barrel','us_gas_avg_gallon',
        'us_diesel_avg_gallon','iran_production_mbpd'])
    agg_df = filtered.groupby('phase')[agg_col].agg(['mean','min','max','std']).round(3)
    st.dataframe(agg_df, use_container_width=True)

# ════════════════════════════════════════════════════════════════════════════
# PAGE 4: AI QUERY ASSISTANT
# ════════════════════════════════════════════════════════════════════════════
# ════════════════════════════════════════════════════════════════════════════
# PAGE 4: PROJECT SUMMARY
# ════════════════════════════════════════════════════════════════════════════
elif page == "📋 Project Summary":
    st.markdown('<div class="section-header">📋 Project Overview</div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        <div class="insight-box">
          <b>📦 Dataset</b><br>
          50-State US pump price data + global crude benchmarks during the Iran War 2026.
          24 daily observations from Feb 9 to Mar 20, 2026.
          Verified by AAA, CNBC, Reuters, NPR, CBS, Euronews.
        </div>
        <div class="insight-box" style="margin-top:10px">
          <b>🐍 Python Libraries Used</b><br>
          NumPy · Pandas · Matplotlib · Seaborn · Plotly · Streamlit
        </div>
        <div class="insight-box" style="margin-top:10px">
          <b>📊 Visualizations</b><br>
          Line charts · Bar charts · Histograms · Subplots · Pie charts ·
          Scatter plots · Box plots · Violin plots · Heatmaps
        </div>""", unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="insight-box">
          <b>🔑 Key Findings</b><br>
          • Brent surged <b>+50.9%</b> from pre-war levels by Day 21<br>
          • US gas prices rose <b>+31.5%</b> (+$0.94/gal)<br>
          • Strait of Hormuz: 138 → just 4 ships/day (−97%)<br>
          • Iran production halved: 3.3 → 1.6 mbpd (−52%)<br>
          • Brent–WTI spread widened from $5.30 to $14.10<br>
          • Diesel hit $5.10/gal — highest since 2022
        </div>
        <div class="insight-box" style="margin-top:10px">
          <b>📉 Conclusion</b><br>
          The analysis demonstrates the direct impact of geopolitical events on oil markets.
          Oil prices increased continuously across all four conflict phases.
          The Strait of Hormuz closure acted as a key supply shock amplifier,
          while declining Iran production compounded upward price pressure.
        </div>""", unsafe_allow_html=True)

    st.markdown('<div class="section-header">Phase Distribution</div>', unsafe_allow_html=True)
    phase_counts = df['phase'].value_counts()
    fig_pie = px.pie(
        values=phase_counts.values, names=phase_counts.index,
        color=phase_counts.index, color_discrete_map=PHASE_COLORS,
        template="plotly_dark", title="Distribution of War Phases")
    fig_pie.update_layout(paper_bgcolor="#0d1525", height=350)
    st.plotly_chart(fig_pie, use_container_width=True)
