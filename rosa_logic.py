"""Decision logic for Rosa's delivery promise, carried over from rosa_assignment1.ipynb (Part II)."""
import numpy as np
from starter import delivery_times


def unpack_costs(costs):
    """Return (refund, churn, margin) from a costs dictionary, matching keys by name."""
    def find(*words):
        for key, value in costs.items():
            if any(w in key.lower() for w in words):
                return float(value)
        raise KeyError(f"No key containing {words} in {list(costs)}")
    return find("refund"), find("churn"), find("margin", "profit")


def cost_per_late_order(costs):
    """Refund + (future orders lost x profit margin per order)."""
    refund, churn, margin = unpack_costs(costs)
    return refund + churn * margin


def net_profit(zone, time_block, promise, costs, seed=1):
    """Net profit over four simulated weeks: orders x margin - late orders x cost per late order."""
    refund, churn, margin = unpack_costs(costs)
    times = delivery_times(zone, time_block, promise, seed=seed)
    n_orders = len(times)
    n_late = int(np.sum(times > promise))
    return n_orders * margin - n_late * (refund + churn * margin)


def best_promise(zone, time_block, promises, costs, seed=1):
    """Try every promise and return the most profitable one (ties go to the shorter promise)."""
    promises = sorted(set(promises))
    results = []
    for p in promises:
        try:
            results.append((p, net_profit(zone, time_block, p, costs, seed)))
        except ValueError:
            continue
    if not results:
        raise ValueError("None of the promises could be evaluated.")
    best_p, best_np = max(results, key=lambda r: r[1])
    tried = [p for p, _ in results]
    return {"best_promise": best_p, "best_profit": best_np,
            "results": results, "at_edge": best_p in (tried[0], tried[-1])}


def late_rate(zone, time_block, promise, seed=1):
    """Percentage of orders delivered after the promise."""
    times = delivery_times(zone, time_block, promise, seed=seed)
    return float("nan") if len(times) == 0 else 100 * float(np.mean(times > promise))
