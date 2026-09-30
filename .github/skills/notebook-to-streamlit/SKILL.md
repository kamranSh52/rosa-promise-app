---
name: notebook-to-streamlit
description: Convert the decision logic in the Rosa's Pizza Jupyter notebook (rosa_assignment1.ipynb) into a Streamlit app. Use when asked to build or update the Streamlit app from the notebook, or to move notebook functions into the app.
---

# Notebook to Streamlit

## Goal
Build a Streamlit app that reuses the logic in `rosa_assignment1.ipynb` so that the app and the notebook always give the same recommendation for the same inputs.

## Rules
1. **Reuse, don't rewrite.** Copy these functions from the notebook into `rosa_logic.py` with the same names, arguments and logic: `unpack_costs`, `cost_per_late_order`, `net_profit`, `best_promise`, and a single-segment `late_rate`. Only remove notebook-only code (prints, plots, `!pip` lines).
2. **Never redefine the starter data.** Import `ZONES`, `TIME_BLOCKS`, `COSTS`, `PROMISE` and `delivery_times` from `starter`. Do not hard-code zone names, time-block names or cost figures.
3. **Keep the definitions.** An order is late if its delivery time is strictly greater than the promise. Net profit = orders x margin - late orders x (refund + churn x margin). Ties go to the shorter promise.
4. **Pass a seed** to `delivery_times` (default 1) so results are reproducible and match the notebook.
5. Put all UI code in `app.py`; keep `rosa_logic.py` free of Streamlit imports.

## Required UI
- Dropdowns (`st.selectbox`) for zone and time block, populated from `ZONES` and `TIME_BLOCKS`.
- Controls for the range of promises to try (min, max, step).
- Inputs for profit margin per order, churn per late order and refund per late order, defaulting to the values in `COSTS`.
- A button; only after it is clicked, show the recommended promise and its net profit (plus the comparison with the current `PROMISE`, and a profit-vs-promise chart).
- Warn if the best promise is at the edge of the range.

## Dependencies and deployment
- `requirements.txt` must include `streamlit`, `numpy`, `pandas` and `git+https://github.com/zhouy185/rosa-starter.git`.
- Test locally with `streamlit run app.py` before pushing. Deploy from the GitHub repo to Streamlit Community Cloud with `app.py` as the entry point.

## Check
With default costs and seed 1, the app's recommendation for Far West / Fri/Sat eve must match the notebook's Part II(b) output.
