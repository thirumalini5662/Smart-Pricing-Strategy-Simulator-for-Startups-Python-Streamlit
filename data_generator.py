import pandas as pd
import numpy as np


def generate_customer_data(n_customers=1000, random_state=42):

    np.random.seed(random_state)

    df = pd.DataFrame({
        "CustomerID": range(1, n_customers + 1),

        "Willingness_to_Pay": np.random.randint(
            5, 101, n_customers
        ),

        "Churn_Probability": np.round(
            np.random.uniform(0.02, 0.40, n_customers),
            3
        ),

        "Subscription_Duration_Months": np.random.randint(
            1, 37, n_customers
        )
    })

    # Customer segments
    conditions = [
        df["Willingness_to_Pay"] < 35,
        (df["Willingness_to_Pay"] >= 35) &
        (df["Willingness_to_Pay"] < 70),
        df["Willingness_to_Pay"] >= 70
    ]

    choices = [
        "Price Sensitive",
        "Standard",
        "Premium"
    ]

    df["Segment"] = np.select(
        conditions,
        choices,
        default="Standard"
    )

    return df