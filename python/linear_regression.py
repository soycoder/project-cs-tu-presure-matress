# Step 1: Import packages
import numpy as np
from sklearn.linear_model import LinearRegression

def linear_regression(input_x, input_y):
    # Step 2: Provide data
    x, y = np.array(input_x), np.array(input_y)

    # Step 3: Create a model and fit it
    model = LinearRegression().fit(x, y)

    # Step 4: Get results
    r_sq = model.score(x, y)
    intercept, coefficients = model.intercept_, model.coef_

    # Step 5: Predict
    y_pred = model.predict(x)
    print('coefficient of determination:', r_sq)
    print('intercept:', intercept)
    print('coefficients:', coefficients, sep='\n')
    print('predicted response:', y_pred, sep='\n')


# Sample data
x = np.array([147.4, 210.9090909090909, 242.4, 252.1, 286.6363636363636, 315.09090909090907, 332.9, 354.0, 370.5, 375.3636363636364, 384.90909090909093, 409.8888888888889, 429.77777777777777, 445.44444444444446, 440.55555555555554, 459.1, 463.75, 482.6363636363636]).reshape((-1, 1))
y = np.array([  0.5,   1.0,               1.5,   2.0,   2.5,               3.0,                3.5,   4.0,   4.5,   5.0,               5.5,                6.0,               6.5,                7.0,                7.5,                8.0,   8.5,    9.0])

linear_regression(input_x=x, input_y=y)
