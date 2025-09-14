import time
import streamlit as st
import plotly.graph_objects as go

# -------------------------------------------------
# Page Config
# -------------------------------------------------
st.set_page_config(page_title="Financial Dashboard", layout="wide")

# -------------------------------------------------
# CSS — unified palette + card polish + scoped bars
# -------------------------------------------------
st.markdown("""
<style>
:root {
  --primary: #3b82f6;  /* blue */
  --good: #10b981;     /* green */
  --warn: #f59e0b;     /* orange */
  --bad: #ef4444;      /* red */
  --purple: #8b5cf6;   /* purple */
  --card-grad1: #0f172a;
  --card-grad2: #111827;
  --border: #1f2937;
}

.card {
  position: relative;
  padding: 20px;
  margin-bottom: 22px;
  background: linear-gradient(145deg, var(--card-grad1), var(--card-grad2));
  border: 1px solid var(--border);
  border-radius: 14px;
  box-shadow: 0 10px 30px rgba(0,0,0,.35),
              0 2px 0 rgba(255,255,255,.02) inset,
              0 -1px 0 rgba(255,255,255,.02) inset;
  transition: transform .18s ease, box-shadow .18s ease;
}
.card:hover {
  transform: translateY(-2px);
  box-shadow: 0 14px 40px rgba(0,0,0,.45),
              0 2px 0 rgba(255,255,255,.03) inset,
              0 -1px 0 rgba(255,255,255,.03) inset;
}

.metric-box {
  background: rgba(255,255,255,.03);
  border: 1px solid var(--border);
  border-radius: 12px;
  padding: 14px 16px;
  text-align: center;
  transition: box-shadow .2s ease, transform .2s ease;
}
.metric-box:hover {
  box-shadow: 0 6px 18px rgba(0,0,0,.25);
  transform: translateY(-1px);
}

.alert { border-radius: 10px; padding: 12px 14px; border:1px solid var(--border); }
.tip { background: rgba(255,255,255,.03); border: 1px solid var(--border); border-radius: 12px; padding: 14px; }

.text-primary { color: var(--primary) !important; }
.text-good    { color: var(--good) !important; }
.text-warn    { color: var(--warn) !important; }
.text-bad     { color: var(--bad) !important; }
.text-purple  { color: var(--purple) !important; }
</style>
""", unsafe_allow_html=True)

# -------------------------------------------------
# First-load spinner
# -------------------------------------------------
if "loaded" not in st.session_state:
    st.markdown(
        "<div style='height:70vh;display:flex;flex-direction:column;align-items:center;justify-content:center;color:#93a4bf'>"
        "<div style='font-size:40px'>🔄</div><div style='margin-top:8px'>Loading your financial data...</div>"
        "</div>",
        unsafe_allow_html=True,
    )
    time.sleep(1.2)
    st.session_state["loaded"] = True
    st.rerun()

# -------------------------------------------------
# Session state
# -------------------------------------------------
if "profile" not in st.session_state:
    st.session_state.profile = {
        "age": 25, "status": "working", "income": 100000,
        "cash": 25000, "investments": 1000000,
        "monthly_contributions": 0, "annual_return": 5,
        "retirement_age": 60, "retirement_goal": 3500000,
        "social_security": 3000, "tax_rate": 22,
        "inflation": 2.5,
        "salary_growth": 3.0,
    }

if "expenses" not in st.session_state:
    st.session_state.expenses = {
        "Housing": 3000, "Utilities": 200, "Food": 1500,
        "Travel": 500, "Insurance": 300, "Entertainment": 250,
        "Hobbies": 300, "Donations": 100, "Emergency Fund": 400,
    }

if "edit_profile_open" not in st.session_state:
    st.session_state.edit_profile_open = False
if "edit_expenses_open" not in st.session_state:
    st.session_state.edit_expenses_open = False

profile = st.session_state.profile
expenses = st.session_state.expenses

def currency(x): return f"${x:,.0f}"

# =================================================
# 1) FINANCIAL PROFILE
# =================================================
with st.container():
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("Financial Profile")

    m = st.columns(6)
    m[0].markdown(f"<div class='metric-box'><div class='metric-value text-primary'>{profile['age']}</div><div class='metric-label'>Age</div></div>", unsafe_allow_html=True)
    m[1].markdown(f"<div class='metric-box'><div class='metric-value text-good'>{currency(profile['income'])}</div><div class='metric-label'>Annual Income</div></div>", unsafe_allow_html=True)
    m[2].markdown(f"<div class='metric-box'><div class='metric-value text-purple'>{currency(profile['cash']+profile['investments'])}</div><div class='metric-label'>Total Savings</div></div>", unsafe_allow_html=True)
    m[3].markdown(f"<div class='metric-box'><div class='metric-value text-warn'>{profile['annual_return']}%</div><div class='metric-label'>Expected Return</div></div>", unsafe_allow_html=True)
    m[4].markdown(f"<div class='metric-box'><div class='metric-value text-primary'>{profile['inflation']:.1f}%</div><div class='metric-label'>Inflation</div></div>", unsafe_allow_html=True)
    m[5].markdown(f"<div class='metric-box'><div class='metric-value text-primary'>{profile['salary_growth']:.1f}%</div><div class='metric-label'>Salary Growth</div></div>", unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

# =================================================
# 2) RETIREMENT PROJECTION
# =================================================
with st.container():
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("Retirement Projection")

    years = list(range(profile['age'], 91))
    balances = []
    current = profile['cash'] + profile['investments']
    contrib0 = profile['monthly_contributions']
    salary_growth = profile['salary_growth']/100.0
    annual_return = profile['annual_return']/100.0

    for age in years:
        years_since_now = age - profile['age']
        contrib_this_year = contrib0 * ((1 + salary_growth) ** max(0, years_since_now))
        if age < profile['retirement_age']:
            current = current*(1+annual_return) + contrib_this_year*12
        else:
            current = current*(1+annual_return)
        balances.append(current)

    ret_index = profile['retirement_age'] - profile['age']
    projected = balances[ret_index] if 0 <= ret_index < len(balances) else balances[-1]

    years_to_ret = max(0, profile['retirement_age'] - profile['age'])
    goal_future = profile['retirement_goal'] * ((1 + profile['inflation']/100.0) ** years_to_ret)
    on_track = projected >= goal_future

    mm = st.columns(3)
    mm[0].markdown(f"<div class='metric-box'><div class='metric-value text-primary'>{currency(projected)}</div><div class='metric-label'>Projected at Retirement</div></div>", unsafe_allow_html=True)
    mm[1].markdown(f"<div class='metric-box'><div class='metric-value text-purple'>{currency(goal_future)}</div><div class='metric-label'>Inflation-Adjusted Goal</div></div>", unsafe_allow_html=True)
    mm[2].markdown(f"<div class='metric-box'><div class='metric-value {'text-good' if on_track else 'text-bad'}'>{'✅ On Track' if on_track else '⚠ Shortfall'}</div><div class='metric-label'>Status</div></div>", unsafe_allow_html=True)

    fig = go.Figure(go.Scatter(x=years, y=balances, mode="lines",
                               line=dict(color="#22c55e", width=3),
                               name="Projected Balance"))
    fig.add_scatter(x=[profile['retirement_age']], y=[projected],
                    mode="markers+text", marker=dict(size=10, color="yellow"),
                    text=["Retirement"], textposition="top center",
                    name="Retirement Age")
    fig.add_hline(y=goal_future, line_dash="dash", line_color="#22d3ee",
                  annotation_text="Inflation-Adjusted Goal", annotation_position="top left")

    fig.update_layout(margin=dict(l=8,r=8,t=8,b=8),
                      paper_bgcolor="rgba(0,0,0,0)",
                      plot_bgcolor="rgba(0,0,0,0)",
                      font=dict(color="white"),
                      height=320,
                      legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1))
    st.plotly_chart(fig, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

# =================================================
# 3) SAVINGS ANALYSIS
# =================================================
with st.container():
    st.markdown("<div class='card sa'>", unsafe_allow_html=True)
    st.subheader("Savings Analysis")

    monthly_income = profile['income'] / 12 if profile['income'] else 0
    total_exp = sum(expenses.values()) if expenses else 0
    contrib = profile['monthly_contributions'] or 0
    remaining = monthly_income - total_exp - contrib
    savings_rate = (remaining / monthly_income * 100) if monthly_income > 0 else 0

    # Big metric
    st.markdown(f"""
        <div style="text-align:center;margin-bottom:12px">
            <div style="font-size:42px;font-weight:700;color:#8b5cf6">{savings_rate:.1f}%</div>
            <div style="font-size:15px;color:#9ca3af;margin-top:-4px">Savings Rate</div>
        </div>
    """, unsafe_allow_html=True)

    st.write(f"**💸 Monthly Income:** {currency(monthly_income)}")
    st.write(f"**🏠 Monthly Expenses:** {currency(total_exp)}")
    st.write(f"**📈 Contributions:** {currency(contrib)}")
    st.write(f"**💰 Remaining:** {currency(remaining)}")

    exp_share = (total_exp / monthly_income * 100) if monthly_income else 0
    ctr_share = (contrib / monthly_income * 100) if monthly_income else 0
    sav_share = max(0.0, 100 - exp_share - ctr_share) if monthly_income else 0

    bar_html = f"""
    <div style="margin-top:10px">
        <div style="margin-bottom:6px;font-size:13px;color:#d1d5db">Expenses — {exp_share:.1f}%</div>
        <div style="height:10px;border-radius:6px;background:#1f2937">
            <div style="width:{exp_share:.1f}%;height:10px;background:linear-gradient(90deg,#ef4444,#f87171);border-radius:6px"></div>
        </div>
        <div style="margin:10px 0 6px;font-size:13px;color:#d1d5db">Contributions — {ctr_share:.1f}%</div>
        <div style="height:10px;border-radius:6px;background:#1f2937">
            <div style="width:{ctr_share:.1f}%;height:10px;background:linear-gradient(90deg,#3b82f6,#60a5fa);border-radius:6px"></div>
        </div>
        <div style="margin:10px 0 6px;font-size:13px;color:#d1d5db">Savings — {sav_share:.1f}%</div>
        <div style="height:10px;border-radius:6px;background:#1f2937">
            <div style="width:{sav_share:.1f}%;height:10px;background:linear-gradient(90deg,#10b981,#34d399);border-radius:6px"></div>
        </div>
    </div>
    """
    st.markdown(bar_html, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# =================================================
# 4) MONTHLY EXPENSES + PIE SIDE BY SIDE
# =================================================
left, right = st.columns([1.2, 1])

with left:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("Monthly Expenses")
    total_monthly = sum(expenses.values())
    st.markdown(f"<div style='text-align:center;font-size:36px;font-weight:700;color:#facc15'>{currency(total_monthly)}</div>", unsafe_allow_html=True)

    grid = st.columns(3)
    for i,(k,v) in enumerate(expenses.items()):
        p = (v/total_monthly*100) if total_monthly else 0
        with grid[i%3]:
            st.markdown(f"<div class='metric-box'><div class='metric-value'>{currency(v)}</div><div class='metric-label'>{k}</div><div class='caption'>{p:.1f}%</div></div>", unsafe_allow_html=True)
    st.markdown(f"<span class='pill pill-on'>Annual: {currency(total_monthly*12)}</span>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

with right:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("Expense Breakdown")
    labels, values = list(expenses.keys()), list(expenses.values())
    pie = go.Figure(go.Pie(labels=labels, values=values, hole=0.55, sort=False))
    pie.update_traces(marker=dict(line=dict(color="#0b1220", width=2)))
    pie.update_layout(showlegend=True, legend=dict(font=dict(color="white")),
                      margin=dict(l=4,r=4,t=4,b=4), paper_bgcolor="rgba(0,0,0,0)")
    st.plotly_chart(pie, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

# =================================================
# 5) QUICK TIPS
# =================================================
with st.container():
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("Quick Tips")
    t = st.columns(3)
    t[0].markdown("<div class='tip'>🎯 <b>Emergency Fund</b><br>Target 3–6 months of expenses.</div>", unsafe_allow_html=True)
    t[1].markdown("<div class='tip'>📈 <b>Increase Savings Rate</b><br>Aim for 20%+ when possible.</div>", unsafe_allow_html=True)
    t[2].markdown("<div class='tip'>🔄 <b>Review Regularly</b><br>Revisit your plan every 6 months.</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)
