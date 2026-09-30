import pandas as pd
import streamlit as st
from starter import ZONES, TIME_BLOCKS, COSTS, PROMISE

from rosa_logic import unpack_costs, cost_per_late_order, net_profit, best_promise, late_rate

st.set_page_config(page_title="Rosa's Delivery Promise Finder", page_icon="🍕", layout="centered")
st.title("🍕 Rosa's Delivery Promise Finder")
st.caption("Find the promised delivery time that maximises net profit for each zone and time block.")

default_refund, default_churn, default_margin = unpack_costs(COSTS)

with st.sidebar:
    st.header("1. Segment")
    zone = st.selectbox("Zone", ZONES, index=list(ZONES).index("Far West") if "Far West" in ZONES else 0)
    time_block = st.selectbox("Time block", TIME_BLOCKS,
                              index=list(TIME_BLOCKS).index("Fri/Sat eve") if "Fri/Sat eve" in TIME_BLOCKS else 0)

    st.header("2. Promises to try")
    lo, hi = st.slider("Range of promised times (minutes)", min_value=5, max_value=150, value=(30, 90), step=5)
    step = st.select_slider("Step (minutes)", options=[1, 2, 5, 10], value=5)

    st.header("3. Cost assumptions")
    margin = st.number_input("Profit margin per order ($)", min_value=0.0, value=float(default_margin), step=0.5)
    churn = st.number_input("Future orders lost per late order (churn)", min_value=0.0,
                            value=float(default_churn), step=0.1)
    refund = st.number_input("Refund per late order ($)", min_value=0.0, value=float(default_refund), step=0.5)

    seed = st.number_input("Simulation seed", min_value=0, value=1, step=1,
                           help="Fixes the simulated four weeks so results are reproducible.")

costs = {"refund": refund, "churn": churn, "margin": margin}
promises = list(range(lo, hi + 1, step))

st.write(f"**Segment:** {zone} · {time_block} &nbsp;&nbsp; **Promises tried:** {lo}–{hi} min in steps of {step} "
         f"&nbsp;&nbsp; **Cost per late order:** ${cost_per_late_order(costs):,.2f}")

if st.button("Find best promise", type="primary"):
    with st.spinner("Simulating four weeks of orders for each promise..."):
        out = best_promise(zone, time_block, promises, costs, seed=int(seed))
        current = net_profit(zone, time_block, PROMISE, costs, seed=int(seed))
        lr_best = late_rate(zone, time_block, out["best_promise"], seed=int(seed))

    c1, c2, c3 = st.columns(3)
    c1.metric("Recommended promise", f"{out['best_promise']} min",
              delta=f"{out['best_promise'] - PROMISE:+d} min vs today")
    c2.metric("Net profit (4 weeks)", f"${out['best_profit']:,.0f}",
              delta=f"${out['best_profit'] - current:,.0f} vs {PROMISE}-min promise")
    c3.metric("Late rate at recommendation", f"{lr_best:.1f}%")

    if out["at_edge"]:
        st.warning("The best promise is at the edge of the range you chose. "
                   "The true optimum may lie outside it; widen the range and try again.")

    df = pd.DataFrame(out["results"], columns=["Promise (min)", "Net profit ($)"]).set_index("Promise (min)")
    st.subheader("Net profit by promised time")
    st.line_chart(df)
    with st.expander("Show table"):
        st.dataframe(df.round(0))
else:
    st.info("Choose a segment and assumptions in the sidebar, then click **Find best promise**.")
