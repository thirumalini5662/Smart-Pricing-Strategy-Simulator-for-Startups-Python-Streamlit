import pandas as pd


def simulate_pricing(
    price,
    churn_rate,
    cost_per_customer,
    customers,
    marketing_spend=0,
    pricing_model="Subscription"
):

    retained_customers = int(
        customers * (1 - churn_rate)
    )

    lost_customers = customers - retained_customers

    if pricing_model == "Subscription":

        revenue = price * retained_customers

    elif pricing_model == "Freemium":

        # 30% of users convert to paid customers
        conversion_rate = 0.30

        paid_customers = int(
            retained_customers * conversion_rate
        )

        revenue = price * paid_customers

    elif pricing_model == "One-time":

        revenue = price * retained_customers

    elif pricing_model == "Tiered":

        basic_customers = int(retained_customers * 0.50)
        standard_customers = int(retained_customers * 0.30)
        premium_customers = (
            retained_customers
            - basic_customers
            - standard_customers
        )

        revenue = (
            basic_customers * price
            + standard_customers * price * 1.5
            + premium_customers * price * 2
        )

    else:
        revenue = 0

    total_cost = (
        customers * cost_per_customer
        + marketing_spend
    )

    profit = revenue - total_cost

    profit_margin = (
        (profit / revenue) * 100
        if revenue > 0 else 0
    )

    monthly_ltv = (
        price / churn_rate
        if churn_rate > 0 else price
    )

    return {
        "Pricing Model": pricing_model,
        "Price": round(price, 2),
        "Customers": customers,
        "Retained Customers": retained_customers,
        "Lost Customers": lost_customers,
        "Revenue": round(revenue, 2),
        "Total Cost": round(total_cost, 2),
        "Profit": round(profit, 2),
        "Profit Margin": round(profit_margin, 2),
        "Estimated LTV": round(monthly_ltv, 2)
    }


def generate_price_comparison(
    min_price,
    max_price,
    step,
    churn_rate,
    cost_per_customer,
    customers,
    marketing_spend,
    pricing_model
):

    results = []

    price = min_price

    while price <= max_price:

        result = simulate_pricing(
            price=price,
            churn_rate=churn_rate,
            cost_per_customer=cost_per_customer,
            customers=customers,
            marketing_spend=marketing_spend,
            pricing_model=pricing_model
        )

        results.append(result)

        price += step

    return pd.DataFrame(results)