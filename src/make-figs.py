def main():
    predictions = load_data("results/03_knn-test-predict.csv")
    flight_test = load_data("data/processed/02_flight-test.csv").reset_index()

    flight_test_predict = pd.concat([flight_test, predictions], axis=1)

    flight_test_predict["MONTH"] = flight_test_predict["MONTH"].replace({1: "Jan", 2: "Feb", 3: "Mar", 4: "Apr", 5: "May", 6: "Jun", 7: "Jul", 8: "Aug", 9: "Sep", 10: "Oct", 11: "Nov", 12: "Dec"})

    flight_test_predict["DAY_OF_WEEK"] = flight_test_predict["DAY_OF_WEEK"].replace({2: "Mon", 3: "Tue", 4: "Wed", 5: "Thu", 6: "Fri", 7: "Sat", 8: "Sun"})
    flight_test_predict["prediction"] = flight_test_predict["prediction"].replace({0: "not delayed", 1: "delayed"})
    flight_test_predict["DEP_DEL15"] = flight_test_predict["DEP_DEL15"].replace({0: "not delayed", 1: "delayed"})

    plot1(flight_test_predict)
    plot2(flight_test_predict)
    plot3(flight_test_predict)
    plot4(flight_test_predict)

def plot1(data):
    month_vs_prediction = alt.Chart(data, width=300, height=200, title="Month and Predicted Flight Delay"
                                    ).mark_bar().encode(
                                        x=alt.X("MONTH", title="Month", axis=alt.Axis(labelAngle=0),
                                                sort=["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]),
                                        xOffset="prediction",
                                        y=alt.Y("count()", title="Number of Flights"),
                                        color=alt.Color("prediction", title="Model Prediction"),
                                        tooltip=alt.Tooltip(["count()", "MONTH"])
                                    )

    month_vs_real = alt.Chart(data, width=300, height=200, title="Month and Actual Flight Delay"
                                    ).mark_bar().encode(
                                        x=alt.X("MONTH", title="Month", axis=alt.Axis(labelAngle=0),
                                                sort=["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]),
                                        xOffset="DEP_DEL15",
                                        y=alt.Y("count()", title="Number of Flights"),
                                        color=alt.Color("DEP_DEL15", title="Actual"),
                                        tooltip=alt.Tooltip(["count()", "MONTH"])
                                    )

    plt = (month_vs_prediction | month_vs_real).resolve_scale(color='independent')

    plt.save("results/04_fig_month-vs-prediction-actual.png")

def plot2(data):
    day_vs_prediction = alt.Chart(data, width=300, height=250, title="Day of the Week and Predicted Flight Delay"
                                    ).mark_bar().encode(
                                        x=alt.X("DAY_OF_WEEK", title="Day of the Week", axis=alt.Axis(labelAngle=0),
                                                sort=["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]),
                                        xOffset="prediction",
                                        y=alt.Y("count()", title="Number of Flights"),
                                        color=alt.Color("prediction", title="Model Prediction"),
                                        tooltip=alt.Tooltip(["count()", "DAY_OF_WEEK"])
                                    )

    day_vs_real = alt.Chart(data, width=300, height=250, title="Day of the Week and Actual Flight Delay"
                                    ).mark_bar().encode(
                                        x=alt.X("DAY_OF_WEEK", title="Day of the Week", axis=alt.Axis(labelAngle=0),
                                                sort=["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]),
                                        xOffset="DEP_DEL15",
                                        y=alt.Y("count()", title="Number of Flights"),
                                        color=alt.Color("DEP_DEL15", title="Actual"),
                                        tooltip=alt.Tooltip(["count()", "DAY_OF_WEEK"])
                                    )

    plt2 = (day_vs_prediction | day_vs_real).resolve_scale(color='independent')

    plt2.save("results/05_fig_day-vs-prediction-actual.png")

def plot3(data):
    carrier_vs_prediction = alt.Chart(data, width=400, height=300, title="Flight Carriers and Predicted Flight Delay"
                                        ).mark_bar().encode(
                                            x=alt.X("CARRIER_NAME", title="Airline Carrier", axis=alt.Axis(labelAngle=-45)),
                                            xOffset="prediction",
                                            y=alt.Y("count()", title="Number of Flights"),
                                            color=alt.Color("prediction", title="Model Prediction"),
                                            tooltip=alt.Tooltip(["count()", "CARRIER_NAME"])
                                        )

    carrier_vs_real = alt.Chart(data, width=400, height=300, title="Flight Carriers and Actual Flight Delay"
                                        ).mark_bar().encode(
                                            x=alt.X("CARRIER_NAME", title="Airline Carrier", axis=alt.Axis(labelAngle=-45)),
                                            xOffset="DEP_DEL15",
                                            y=alt.Y("count()", title="Number of Flights"),
                                            color=alt.Color("DEP_DEL15", title="Actual"),
                                            tooltip=alt.Tooltip(["count()", "CARRIER_NAME"])
                                        )

    plt3 = (carrier_vs_prediction | carrier_vs_real).resolve_scale(color='independent')

    plt3.save("results/06_fig_carrier-vs-prediction-actual.png")

def plot4(data):
    alt.data_transformers.disable_max_rows()

    melt_flight_predict = data.melt(id_vars=['MONTH', 'DAY_OF_WEEK', 'DEP_DEL15', 'CARRIER_NAME', 'prediction', 'index'])

    dropdown_options = ['CONCURRENT_FLIGHTS', 'FLT_ATTENDANTS_PER_PASS', 'GROUND_SERV_PER_PASS', 'PLANE_AGE', 'SNOW', 'AWND']
    dropdown_numeric_variable = alt.binding_select(options=dropdown_options, name='Y-axis feature')
    selection = alt.selection_point(fields=['variable'], bind=dropdown_numeric_variable)

    drop_down_chart = alt.Chart(melt_flight_predict, width=1000, height=400
                                    ).mark_circle(opacity=0.4).encode(
                                        y=alt.X('value:Q', title=""),
                                        x=alt.Y('MONTH', title="Month", sort=["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]),
                                        color=alt.Color('prediction', title="Model Prediction")
                                    ).add_params(selection).transform_filter(selection)

    drop_down_chart.save("results/07_fig_numeric-feats-interactive-viz.html")

if __name__ == "__main__":
    main()
