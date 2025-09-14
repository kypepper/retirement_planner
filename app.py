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

/* ================================
   CARD + METRIC BOXES
   ================================ */
.card {
  position: relative;
  padding: 20px;
  margin-bottom: 22px;
  background: linear-gradient(145deg, var(--card-grad1), var(--card-grad2));
  border: 1px solid var(--border);
  border-radius: 14px;
  box-shadow:
    0 10px 30px rgba(0,0,0,.35),
    0 2px 0 rgba(255,255,255,.02) inset,
    0 -1px 0 rgba(255,255,255,.02) inset;
  transition: transform .18s ease, box-shadow .18s ease;
}
.card:hover {
  transform: translateY(-2px);
  box-shadow:
    0 14px 40px rgba(0,0,0,.45),
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

/* Alerts, tips, pills */
.alert { border-radius: 10px; padding: 12px 14px; border:1px solid var(--border); }
.tip { background: rgba(255,255,255,.03); border: 1px solid var(--border); border-radius: 12px; padding: 14px; }

/* ================================
   EDIT / CLOSE BUTTONS
   ================================ */
button[kind="secondary"] {
  background: #374151;
  color: #f9fafb !important;
  border-radius: 6px;
  padding: 2px 10px;
  font-weight: 600;
  border: none;
  text-decoration: none !important;
  transition: background 0.2s ease;
}
[data-theme="light"] button[kind="secondary"] {
  background: #e5e7eb;
  color: #111827 !important;
  border: 1px solid #d1d5db;
}
button[kind="secondary"]:hover {
  filter: brightness(0.9);
}

/* ================================
   TEXT COLOR ACCENTS
   ================================ */
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
# Session state (data + edit toggles)
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
    ctitle1, ctitle2 = st.columns([0.8, 0.2])
    with ctitle1: st.subheader("Financial Profile")
    with ctitle2:
        if st.button(("Close" if st.session_state.edit_profile_open else "Edit"), key="edit_profile_txt"):
            st.session_state.edit_profile_open = not st.session_state.edit_profile_open

    if st.session_state.edit_profile_open:
        with st.form("profile_form", clear_on_submit=False):
            c1, c2, c3, c4 = st.columns(4)
            age   = c1.number_input("Age", value=profile["age"], min_value=0, max_value=120)
            status= c2.selectbox("Status", ["working", "retired"], index=0 if profile["status"]=="working" else 1)
            income= c3.number_input("Annual Income", value=profile["income"], step=1000)
            ss    = c4.number_input("Social Security / mo", value=profile["social_security"], step=50)

            c5, c6, c7, c8 = st.columns(4)
            cash  = c5.number_input("Cash Savings", value=profile["cash"], step=500)
            inv   = c6.number_input("Investments", value=profile["investments"], step=1000)
            contr = c7.number_input("Monthly Contributions", value=profile["monthly_contributions"], step=50)
            ret   = c8.number_input("Annual Return (%)", value=profile["annual_return"], step=1)

            c9, c10, c11, c12 = st.columns(4)
            tax   = c9.number_input("Tax Rate (%)", value=profile["tax_rate"], step=1)
            r_age = c10.number_input("Retirement Age", value=profile["retirement_age"], step=1)
            goal  = c11.number_input("Retirement Goal (today $)", value=profile["retirement_goal"], step=50000)
            infl  = c12.number_input("Inflation (%)", value=profile["inflation"], step=0.1, format="%.1f")

            c13, _ = st.columns([1,3])
            sal_g = c13.number_input("Annual Salary Growth (%)", value=profile["salary_growth"], step=0.1, format="%.1f")

            save = st.form_submit_button("💾 Save Changes")
            if save:
                profile.update({
                    "age":age,"status":status,"income":income,"social_security":ss,
                    "cash":cash,"investments":inv,"monthly_contributions":contr,
                    "annual_return":ret,"tax_rate":tax,"retirement_age":r_age,"retirement_goal":goal,
                    "inflation": infl, "salary_growth": sal_g
                })
                st.session_state.profile = profile
                st.success("Profile updated.")

        st.markdown("<hr class='div'/>", unsafe_allow_html=True)

    m = st.columns(6)
    m[0].markdown(f"<div class='metric-box'><div class='metric-value text-primary'>{profile['age']}</div><div class='metric-label'>Age</div><div class='caption'>Your current age.</div></div>", unsafe_allow_html=True)
    m[1].markdown(f"<div class='metric-box'><div class='metric-value text-good'>{currency(profile['income'])}</div><div class='metric-label'>Annual Income</div><div class='caption'>Before taxes.</div></div>", unsafe_allow_html=True)
    m[2].markdown(f"<div class='metric-box'><div class='metric-value text-purple'>{currency(profile['cash']+profile['investments'])}</div><div class='metric-label'>Total Savings</div><div class='caption'>Cash + investments.</div></div>", unsafe_allow_html=True)
    m[3].markdown(f"<div class='metric-box'><div class='metric-value text-warn'>{profile['annual_return']}%</div><div class='metric-label'>Expected Return</div><div class='caption'>Long-run average.</div></div>", unsafe_allow_html=True)
    m[4].markdown(f"<div class='metric-box'><div class='metric-value text-primary'>{profile['inflation']:.1f}%</div><div class='metric-label'>Inflation</div><div class='caption'>Assumed CPI per year.</div></div>", unsafe_allow_html=True)
    m[5].markdown(f"<div class='metric-box'><div class='metric-value text-primary'>{profile['salary_growth']:.1f}%</div><div class='metric-label'>Salary Growth</div><div class='caption'>Grows contributions yearly.</div></div>", unsafe_allow_html=True)

    st.markdown(f"<span class='pill pill-on'>{profile['status'].capitalize()}</span>", unsafe_allow_html=True)
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
      
    # Balance at retirement age (instead of final age 90)
    ret_index = profile['retirement_age'] - profile['age']
    projected = balances[ret_index] if 0 <= ret_index < len(balances) else balances[-1]
    on_track = projected >= goal_future

    mm = st.columns(3)
    mm[0].markdown(f"<div class='metric-box'><div class='metric-value text-primary'>{currency(projected)}</div><div class='metric-label'>Projected at Retirement</div><div class='caption'>Nominal dollars at retirement.</div></div>", unsafe_allow_html=True)
    mm[1].markdown(f"<div class='metric-box'><div class='metric-value text-purple'>{currency(goal_future)}</div><div class='metric-label'>Inflation-Adjusted Goal</div><div class='caption'>Future value of {currency(profile['retirement_goal'])} in {years_to_ret} yrs.</div></div>", unsafe_allow_html=True)

    status_class = "text-good" if on_track else "text-bad"
    status_text = "✅ On Track" if on_track else "⚠ Shortfall"
    mm[2].markdown(
        f"<div class='metric-box'>"
        f"<div class='metric-value {status_class}'>{status_text}</div>"
        f"<div class='metric-label'>Status</div>"
        f"<div class='caption'>Projected vs inflated goal.</div>"
        f"</div>",
        unsafe_allow_html=True,
    )

    fig = go.Figure(go.Scatter(x=years, y=balances, mode="lines",
                               line=dict(color="#22c55e", width=3),
                               name="Projected Balance"))
    # Add a marker at retirement age
    fig.add_scatter(
        x=[profile['retirement_age']],
        y=[projected],
        mode="markers+text",
        marker=dict(size=10, color="yellow"),
        text=["Retirement"],
        textposition="top center",
        name="Retirement Age"
    )
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
left, right = st.columns(2)

with left:
    st.markdown("<div class='card sa'>", unsafe_allow_html=True)
    st.subheader("Savings Analysis")

    monthly_income = profile['income']/12
    total_exp = sum(expenses.values())
    contrib = profile['monthly_contributions']
    remaining = monthly_income - total_exp - contrib
    savings_rate = (remaining/monthly_income*100) if monthly_income > 0 else 0

    if savings_rate >= 20:
        status_lbl = "<span class='text-good'>🟢 Good</span>"
        alert_html = "<div class='alert alert-good'>Great job! You're on track with your savings rate.</div>"
    elif savings_rate >= 10:
        status_lbl = "<span class='text-warn'>🟡 Fair</span>"
        alert_html = "<div class='alert alert-warn'>Consider increasing contributions to reach your long-term goals.</div>"
    else:
        status_lbl = "<span class='text-bad'>🔴 Poor</span>"
        alert_html = "<div class='alert alert-bad'>Critical Action Needed: Reduce expenses or increase income.</div>"

    st.markdown(f"<div class='metric-value text-purple'>{savings_rate:.1f}%</div><div class='metric-label'>Savings Rate</div><div class='caption'>{status_lbl}</div>", unsafe_allow_html=True)
    st.write(f"Monthly Income: {currency(monthly_income)}")
    st.write(f"Monthly Expenses: {currency(total_exp)}")
    st.write(f"Contributions: {currency(contrib)}")
    st.write(f"Remaining: {currency(remaining)}")

    exp_share = (total_exp/monthly_income*100) if monthly_income else 0
    ctr_share = (contrib/monthly_income*100) if monthly_income else 0
    sav_share = max(0.0, 100 - exp_share - ctr_share) if monthly_income else 0

    for lbl, pct, klass in [
        ("Expenses Share", exp_share, "bar-exp"),
        ("Contributions Share", ctr_share, "bar-ctr"),
        ("Savings Share", sav_share, "bar-sav")
    ]:
        st.markdown(f"<div class='bar-wrap'><div class='bar-label'>{lbl} — {pct:.1f}%</div><div class='progress'><span class='{klass}' style='width:{min(max(pct,0),100)}%'></span></div></div>", unsafe_allow_html=True)

    st.markdown(alert_html, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# =================================================
# 4) MONTHLY EXPENSES
# =================================================
with right:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    header_l, header_r = st.columns([0.8,0.2])
    with header_l: st.subheader("Monthly Expenses")
    with header_r:
        if st.button(("Close" if st.session_state.edit_expenses_open else "Edit"), key="edit_expenses_txt"):
            st.session_state.edit_expenses_open = not st.session_state.edit_expenses_open

    if st.session_state.edit_expenses_open:
        with st.form("expenses_form", clear_on_submit=False):
            new = {}
            c1, c2, c3 = st.columns(3)
            keys = list(expenses.keys())
            for i, k in enumerate(keys):
                col = [c1,c2,c3][i%3]
                with col:
                    new[k] = st.number_input(k, value=expenses[k], step=25, min_value=0)
            if st.form_submit_button("💾 Save Changes"):
                st.session_state.expenses = new
                expenses = new
                st.success("Expenses updated.")

        st.markdown("<hr class='div'/>", unsafe_allow_html=True)

    total_monthly = sum(expenses.values())
    st.markdown(f"<div class='metric-value text-warn'>{currency(total_monthly)}</div><div class='metric-label'>Total Monthly Expenses</div>", unsafe_allow_html=True)

    grid = st.columns(3)
    for i,(k,v) in enumerate(expenses.items()):
        p = (v/total_monthly*100) if total_monthly else 0
        with grid[i%3]:
            st.markdown(f"<div class='metric-box'><div class='metric-value'>{currency(v)}</div><div class='metric-label'>{k}</div><div class='caption'>{p:.1f}% of total</div></div>", unsafe_allow_html=True)

    st.markdown(f"<span class='pill pill-on'>💵 Annual: {currency(total_monthly*12)}</span>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# =================================================
# 5) EXPENSE BREAKDOWN
# 6) 20-YEAR INVESTMENT SCENARIOS
# =================================================
b_left, b_right = st.columns(2)

with b_left:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("Expense Breakdown")
    labels, values = list(expenses.keys()), list(expenses.values())
    pie = go.Figure(go.Pie(
        labels=labels, values=values, hole=0.55, sort=False,
        hovertemplate="<b>%{label}</b><br>$%{value:,.0f}<br>%{percent}<extra></extra>"
    ))
    pie.update_traces(marker=dict(line=dict(color="#0b1220", width=2)))
    pie.update_layout(showlegend=True,
                      legend=dict(font=dict(color="white")),
                      margin=dict(l=4,r=4,t=4,b=4),
                      paper_bgcolor="rgba(0,0,0,0)")
    st.plotly_chart(pie, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

with b_right:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("20-Year Investment Scenarios")

    def compound(principal, monthly, years, annual_pct):
        r = (annual_pct/100)/12
        n = years*12
        return principal*(1+r)**n + (monthly*((1+r)**n - 1)/r if r else monthly*n)

    principal = profile['cash'] + profile['investments']
    hy = compound(principal, profile['monthly_contributions'], 20, 5)
    sp = compound(principal, profile['monthly_contributions'], 20, 10)

    c = st.columns(2)
    c[0].markdown(f"<div class='metric-box'><div class='metric-value text-primary'>{currency(hy)}</div><div class='metric-label'>High-Yield Savings</div><div class='caption'>Stable growth (~5% APY)</div></div>", unsafe_allow_html=True)
    c[1].markdown(f"<div class='metric-box'><div class='metric-value text-good'>{currency(sp)}</div><div class='metric-label'>S&P 500 Index</div><div class='caption'>Market growth (~10% Avg.)</div></div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# =================================================
# 7) QUICK TIPS
# =================================================
with st.container():
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("Quick Tips")
    t = st.columns(3)
    t[0].markdown("<div class='tip'>🎯 <b>Emergency Fund</b><br><span class='small'>Target 3–6 months of expenses in cash or high-yield savings.</span></div>", unsafe_allow_html=True)
    t[1].markdown("<div class='tip'>📈 <b>Increase Savings Rate</b><br><span class='small'>Automate transfers and aim for 20%+ of income when possible.</span></div>", unsafe_allow_html=True)
    t[2].markdown("<div class='tip'>🔄 <b>Review Regularly</b><br><span class='small'>Revisit your plan every 6 months and adjust for life changes.</span></div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)
