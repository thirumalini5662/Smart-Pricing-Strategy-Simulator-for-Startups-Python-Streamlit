import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error


def train_revenue_model(df):

    X = df[
        [
            "Willingness_to_Pay",
            "Churn_Probability"
        ]
    ]

    y = (
        df["Willingness_to_Pay"]
        * (1 - df["Churn_Probability"])
    )

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.20,
        random_state=42
    )

    model = LinearRegression()

    model.fit(X_train, y_train)

    predictions = model.predict(X_test)

    mae = mean_absolute_error(
        y_test,
        predictions
    )

    return model, mae