import pandas as pd

from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score


def sales_forecast(df, periods):

    data = df.copy()

    # ---------------------------------------
    # Prepare Data
    # ---------------------------------------

    data["Order Date"] = pd.to_datetime(data["Order Date"])

    monthly = (
        data.groupby(
            pd.Grouper(
                key="Order Date",
                freq="ME"
            )
        )["Sales"]
        .sum()
        .reset_index()
    )

    monthly["Month_Index"] = range(len(monthly))

    # ---------------------------------------
    # Train Model
    # ---------------------------------------

    X = monthly[["Month_Index"]]
    y = monthly["Sales"]

    model = LinearRegression()

    model.fit(X, y)

    predictions = model.predict(X)

    accuracy = r2_score(y, predictions)

    # ---------------------------------------
    # Future Forecast
    # ---------------------------------------

    future_index = list(
        range(
            len(monthly),
            len(monthly) + periods
        )
    )

    future = pd.DataFrame(
        {
            "Month_Index": future_index
        }
    )

    future["Forecast Sales"] = model.predict(future)

    future["Order Date"] = pd.date_range(
        start=monthly["Order Date"].iloc[-1]
        + pd.offsets.MonthEnd(1),
        periods=periods,
        freq="ME"
    )

    future = future[
        [
            "Order Date",
            "Forecast Sales"
        ]
    ]

    return monthly, future, accuracy