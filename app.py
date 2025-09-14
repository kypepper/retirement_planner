import time
import streamlit as st
import plotly.graph_objects as go

# -------------------------------------------------
# Page Config
# -------------------------------------------------
st.set_page_config(page_title="Financial Dashboard", layout="wide")

# -------------------------------------------------
# CSS Styling
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
  background: linear-gradient(145deg, var(--card-grad1), var(--card-grad2));
  border: 1px solid var(--border);
  border-radius: 14px;
  padding: 20px;
  margin-bottom: 22px;
}

.metric-box {
  background: rgba(255,255,255,.03);
  border: 1px solid var(--border);
  border-radius: 12px;
  padding: 16px;
  text-align: center;
  display: flex;
  flex-direction: column;
  justify-content: center;
  /* ✅ Enforce uniform sizing */
  min-height: 140px;   /* adjust as needed */
}

.metric-value {
  font-size: 1.4rem;
  font-weight: 700;
  margin-bottom: 4px;
}

.metric-label {
  font-size: 0.9rem;
  opacity: 0.85;
}

.caption {
  font-size: 0.85rem;
  opacity: 0.7;
  margin-top: 4px;
}

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
        "cash": 25000, "investments": 1000000, "monthly_contributions": 0,
        "annual_return": 5, "retirement_age": 60, "retirement_goal": 3500000,
        "social_security": 3000, "tax_rate": 22, "inflation": 2.5,
        "salary_growth": 3.0,
    }

if "expenses" not in st.session_state:
    st.session_state.expenses = {
        "Housing": 3000, "Utilities": 200, "Food": 1500, "Travel": 500,
        "Insurance": 300, "Entertainment": 250, "Hobbies": 300,
        "Donations": 100, "Emergency Fund": 400,
    }

profile = st.session_state.profile
expenses = st.session_state.expenses

def currency(x): return f"${x:,.0f}"


# =================================================
# 1) FINANCIAL PROFILE
# =================================================
with st.container():
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    ctitle1, ctitle2 = st.columns([0.8, 0.2])
    with ctitle1:
        st.subheader("Financial Profile")
    with ctitle2:
        if st.button(("Close" if st.session_state.edit_profile_open else "Edit"), key="edit_profile_txt"):
            st.session_state.edit_profile_open = not st.session_state.edit_profile_open

    if st.session_state.edit_profile_open:
        with st.form("profile_form", clear_on_submit=False):
            c1, c2, c3, c4 = st.columns(4)
            age = c1.number_input("Age", value=profile["age"], min_value=0, max_value=120)
            status = c2.selectbox("Status", ["working", "retired"], index=0 if profile["status"]=="working" else 1)
            income = c3.number_input("Annual Income", value=profile["income"], step=1000)
            ss = c4.number_input("Social Security / mo", value=profile["social_security"], step=50)

            c5, c6, c7, c8 = st.columns(4)
            cash = c5.number_input("Cash Savings", value=profile["cash"], step=500)
            inv = c6.number_input("Investments", value=profile["investments"], step=1000)
            contr = c7.number_input("Monthly Contributions", value=profile["monthly_contributions"], step=50)
            ret = c8.number_input("Annual Return (%)", value=profile["annual_return"], step=1)

            c9, c10, c11, c12 = st.columns(4)
            tax = c9.number_input("Tax Rate (%)", value=profile["tax_rate"], step=1)
            r_age = c10.number_input("Retirement Age", value=profile["retirement_age"], step=1)
            goal = c11.number_input("Retirement Goal (today $)", value=profile["retirement_goal"], step=50000)
            infl = c12.number_input("Inflation (%)", value=profile["inflation"], step=0.1, format="%.1f")

            c13, _ = st.columns([1,3])
            sal_g = c13.number_input("Annual Salary Growth (%)", value=profile["salary_growth"], step=0.1, format="%.1f")

            save = st.form_submit_button("💾 Save Changes")
            if save:
                profile.update({
                    "age":age,"status":status,"income":income,"social_security":ss,
                    "cash":cash,"investments":inv,"monthly_contributions":contr,
                    "annual_return":ret,"tax_rate":tax,"retirement_age":r_age,"retirement_goal":goal,
                    "inflation": infl,"salary_growth": sal_g
                })
                st.session_state.profile = profile
                st.success("Profile updated.")

    # metrics
    st.markdown("<hr class='div'/>", unsafe_allow_html=True)
    m = st.columns(6)
    m[0].markdown(f"<div class='metric-box'><div class='metric-value text-primary'>{profile['age']}</div><div class='metric-label'>Age</div></div>", unsafe_allow_html=True)
    m[1].markdown(f"<div class='metric-box'><div class='metric-value text-good'>{currency(profile['income'])}</div><div class='metric-label'>Annual Income</div></div>", unsafe_allow_html=True)
    m[2].markdown(f"<div class='metric-box'><div class='metric-value text-purple'>{currency(profile['cash']+profile['investments'])}</div><div class='metric-label'>Total Savings</div></div>", unsafe_allow_html=True)
    m[3].markdown(f"<div class='metric-box'><div class='metric-value text-warn'>{profile['annual_return']}%</div><div class='metric-label'>Expected Return</div></div>", unsafe_allow_html=True)
    m[4].markdown(f"<div class='metric-box'><div class='metric-value text-primary'>{profile['inflation']:.1f}%</div><div class='metric-label'>Inflation</div></div>", unsafe_allow_html=True)
    m[5].markdown(f"<div class='metric-box'><div class='metric-value text-primary'>{profile['salary_growth']:.1f}%</div><div class='metric-label'>Salary Growth</div></div>", unsafe_allow_html=True)
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

    years_to_ret = profile['retirement_age'] - profile['age']
    goal_future = profile['retirement_goal'] * ((1 + profile['inflation']/100) ** years_to_ret)

    ret_index = profile['retirement_age'] - profile['age']
    projected = balances[ret_index] if 0 <= ret_index < len(balances) else balances[-1]
    on_track = projected >= goal_future

    # ✅ Force equal-sized cards
    mm = st.columns(3, gap="large")

    with mm[0]:
        st.markdown(
            f"<div class='metric-box' style='min-height:100px;'>"
            f"<div class='metric-value text-primary'>{currency(projected)}</div>"
            f"<div class='metric-label'>Projected at Retirement</div></div>",
            unsafe_allow_html=True
        )

    with mm[1]:
        st.markdown(
            f"<div class='metric-box' style='min-height:100px;'>"
            f"<div class='metric-value text-purple'>{currency(goal_future)}</div>"
            f"<div class='metric-label'>Inflation-Adjusted Goal</div>"
            f"<div class='caption'>Future value of {currency(profile['retirement_goal'])} in {years_to_ret} yrs.</div></div>",
            unsafe_allow_html=True
        )

    with mm[2]:
        status_class = "text-good" if on_track else "text-bad"
        status_text = "✅ On Track" if on_track else "⚠ Shortfall"
        st.markdown(
            f"<div class='metric-box' style='min-height:100px;'>"
            f"<div class='metric-value {status_class}'>{status_text}</div>"
            f"<div class='metric-label'>Status</div>"
            f"<div class='caption'>Projected vs inflated goal.</div></div>",
            unsafe_allow_html=True
        )

    # Chart
    fig = go.Figure(go.Scatter(x=years, y=balances, mode="lines",
                               line=dict(color="#22c55e", width=3), name="Projected Balance"))
    fig.add_scatter(x=[profile['retirement_age']], y=[projected], mode="markers+text",
                    marker=dict(size=10, color="yellow"), text=["Retirement"],
                    textposition="top center", name="Retirement Age")
    fig.add_hline(y=goal_future, line_dash="dash", line_color="#22d3ee",
                  annotation_text="Inflation-Adjusted Goal", annotation_position="top left")
    fig.update_layout(margin=dict(l=8, r=8, t=8, b=8),
                      paper_bgcolor="rgba(0,0,0,0)",
                      plot_bgcolor="rgba(0,0,0,0)",
                      font=dict(color="white"),
                      height=400,
                      legend=dict(orientation="h", yanchor="bottom", y=1.02,
                                  xanchor="right", x=1))
    st.plotly_chart(fig, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)


# =================================================
# 3) SAVINGS ANALYSIS + 4) EXPENSES
# =================================================
left, right = st.columns([0.9, 1.1])

with left:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("📊 Savings Analysis")

    monthly_income = profile['income']/12
    total_exp = sum(expenses.values())
    contrib = profile['monthly_contributions']
    remaining = monthly_income - total_exp - contrib
    savings_rate = (remaining/monthly_income*100) if monthly_income > 0 else 0

    # Status + alert
    if savings_rate >= 20:
        status_lbl = "<span class='text-good'>🟢 Good</span>"
        alert_html = "<div style='background:#064e3b;color:#a7f3d0;padding:10px;border-radius:10px;'>✅ Great job! You're on track with your savings rate.</div>"
    elif savings_rate >= 10:
        status_lbl = "<span class='text-warn'>🟡 Fair</span>"
        alert_html = "<div style='background:#78350f;color:#fcd34d;padding:10px;border-radius:10px;'>⚠ Consider increasing contributions to reach your goals.</div>"
    else:
        status_lbl = "<span class='text-bad'>🔴 Needs Improvement</span>"
        alert_html = "<div style='background:#7f1d1d;color:#fecaca;padding:10px;border-radius:10px;'>⚠ Critical Action Needed: Reduce expenses or increase income.</div>"

    # Top metric
    st.markdown(
        f"<div class='metric-box'>"
        f"<div class='metric-value text-purple'>{savings_rate:.1f}%</div>"
        f"<div class='metric-label'>Savings Rate</div>"
        f"<div class='caption'>{status_lbl}</div>"
        f"</div>",
        unsafe_allow_html=True
    )

    # Breakdown values
    st.write(f"**Monthly Income:** {currency(monthly_income)}")
    st.write(f"**Monthly Expenses:** {currency(total_exp)}")
    st.write(f"**Contributions:** {currency(contrib)}")
    st.write(f"**Remaining:** {currency(remaining)}")

    # Progress bars
    exp_share = (total_exp/monthly_income*100) if monthly_income else 0
    ctr_share = (contrib/monthly_income*100) if monthly_income else 0
    sav_share = max(0.0, 100 - exp_share - ctr_share) if monthly_income else 0

    for lbl, pct, color in [
        ("Expenses", exp_share, "#ef4444"),
        ("Contributions", ctr_share, "#3b82f6"),
        ("Savings", sav_share, "#10b981")
    ]:
        st.markdown(
            f"<div style='margin-top:8px;'>"
            f"<b>{lbl}</b> — {pct:.1f}%"
            f"<div style='height:10px;background:#374151;border-radius:6px;'>"
            f"<div style='width:{pct:.1f}%;background:{color};height:10px;border-radius:6px;'></div>"
            f"</div></div>",
            unsafe_allow_html=True
        )

    # Status message block
    # ✅ Add spacing before the alert
    st.markdown("<div style='margin-top:20px;'></div>", unsafe_allow_html=True)
    st.markdown(alert_html, unsafe_allow_html=True)


    st.markdown("</div>", unsafe_allow_html=True)

with right:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("💰 Monthly Expenses")

    total_monthly = sum(expenses.values())
    st.markdown(
        f"<div class='metric-value text-warn'>{currency(total_monthly)}</div>"
        f"<div class='metric-label'>Total Monthly Expenses</div>",
        unsafe_allow_html=True
    )

    # ✅ Adjust grid: smaller horizontal gaps
    grid = st.columns(3, gap="small")

    for i, (k, v) in enumerate(expenses.items()):
        p = (v/total_monthly*100) if total_monthly else 0
        with grid[i % 3]:
            st.markdown(
                f"<div class='metric-box' style='margin-bottom:18px;'>"
                f"<div class='metric-value'>{currency(v)}</div>"
                f"<div class='metric-label'>{k}</div>"
                f"<div class='caption'>{p:.1f}% of total</div>"
                f"</div>",
                unsafe_allow_html=True
            )

    st.markdown(
        f"<span class='pill pill-on'>💵 Annual: {currency(total_monthly*12)}</span>",
        unsafe_allow_html=True
    )
    st.markdown("</div>", unsafe_allow_html=True)


# =================================================
# 5) EXPENSE BREAKDOWN + 6) 20-YEAR INVESTMENT SCENARIOS
# =================================================
b_left, b_right = st.columns(2)

with b_left:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("📉 Expense Breakdown")

    labels, values = list(expenses.keys()), list(expenses.values())
    pie = go.Figure(go.Pie(
        labels=labels, values=values, hole=0.55, sort=False,
        hovertemplate="<b>%{label}</b><br>$%{value:,.0f}<br>%{percent}<extra></extra>"
    ))
    pie.update_traces(marker=dict(line=dict(color="#0b1220", width=2)))
    pie.update_layout(showlegend=True, legend=dict(font=dict(color="white")),
                      margin=dict(l=4, r=4, t=4, b=4), paper_bgcolor="rgba(0,0,0,0)")
    st.plotly_chart(pie, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

with b_right:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("📈 20-Year Investment Scenarios")

    def compound(principal, monthly, years, annual_pct):
        r = (annual_pct/100)/12
        n = years*12
        return principal*(1+r)**n + (monthly*((1+r)**n - 1)/r if r else monthly*n)

    principal = profile['cash'] + profile['investments']
    hy = compound(principal, profile['monthly_contributions'], 20, 5)
    sp = compound(principal, profile['monthly_contributions'], 20, 10)

    c = st.columns(2, gap="large")
    c[0].markdown(
        f"<div class='metric-box'><div class='metric-label'>High-Yield Savings</div>"
        f"<div class='caption'>Stable Growth (5% APY)</div>"
        f"<div class='metric-value text-primary'>{currency(hy)}</div>"
        f"<div class='caption'>Projected balance in 20 years.</div></div>",
        unsafe_allow_html=True
    )
    c[1].markdown(
        f"<div class='metric-box'><div class='metric-label'>S&P 500 Index Fund</div>"
        f"<div class='caption'>Market Growth (10% Avg. APY)</div>"
        f"<div class='metric-value text-good'>{currency(sp)}</div>"
        f"<div class='caption'>Projected balance in 20 years.</div></div>",
        unsafe_allow_html=True
    )

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

