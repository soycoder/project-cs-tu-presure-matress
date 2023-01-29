import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt

import pickle

def plot_regression_line(y_pred, x, y):
    # plotting the actual points as scatter plot
    plt.scatter(x, y, color = "m",
               marker = "o", s = 30)
 
 
    # plotting the regression line
    plt.plot(x, y_pred, color = "g")
 
    # putting labels
    plt.xlabel('x')
    plt.ylabel('y - kg')
 
    # function to show plot
    plt.show()

def linear_regression(coor_x, coor_y, input_x, input_y):
    print("Coor: ", coor_x, coor_y)
    print("Input: ", input_x, input_y)

    # Step 2: Provide data
    x, y = np.array(input_x), np.array(input_y)

    for i in range(len(y)):
        y[i] = (y[i]/(15**2) * 1.0) * 735.55914
    
    # print(y)

    # Step 3: Create a model and fit it
    model = LinearRegression().fit(x, y)
    Pkl_Filename = "./calibrated_sensors/model/x"+str(coor_x)+"-y"+str(coor_y)+".pkl"  
    


    with open(Pkl_Filename, 'wb') as file:  
        pickle.dump(model, file)

    # Step 4: Get results
    r_sq = model.score(x, y)
    intercept, coefficients = model.intercept_, model.coef_

    # Step 5: Predict
    y_pred = model.predict(x)
    # print('coefficient of determination:', r_sq)
    # print('intercept:', intercept)
    # print('coefficients:', coefficients, sep='\n')
    # print('predicted response:', y_pred, sep='\n')

    return y_pred, x, y

str_weight_list = [-1.1, 10.0]
# str_weight_list = [0.0, 0.5, 1.0, 1.5, 2.0]
# str_weight_list = [0.0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.5, 7.0, 7.5, 8.0, 8.5, 9.0, 9.5, 10.0]
height = 10
width = 10
# ----------------------------------------------------------------------------------------------
y_size = 10
x_size = 10

for axis_y in range(height):
    # axis_y = 1
    print("y = ", axis_y, end="\t")
    for axis_x in range(width):
        # axis_x = 0
        print("x = ", axis_x, end="\t")
        print()
        # p_raw - set p_raw in arr
        p_raw = np.zeros((len(str_weight_list)), dtype=float)
        # Zero - set zeros in arr
        _zero = np.zeros((height,width), dtype=float)

        for w in str_weight_list:
            str_weight = str(w)
            print(" > | "+str_weight)

            file_name = ("./calibrating/data_collecting-"+str_weight+".csv")
            raw_data = pd.read_csv(file_name, header=None)
            # print(raw_data)
            raw_pressure = raw_data[1]
            index = raw_pressure.index
            number_of_rows = len(index)

            # print(number_of_rows)

            # Sum - set zeros in arr
            _sum = np.zeros((y_size,x_size), dtype=int)

            # Max - set max in arr
            _max = np.zeros((y_size,x_size), dtype=int)

            # Min - set min in arr
            _min = np.zeros((y_size,x_size), dtype=int)
            _min[0:height-1,0:width-1] = 1024

            # Avg - set avg in arr
            _avg = np.zeros((y_size,x_size), dtype=float)

            # Loop
            for n in range(number_of_rows):
                # print("number_of_rows : " ,n)
                temp = raw_pressure.iloc[n]
                each_pressure = np.fromstring(temp[1:-1], dtype=float, sep=' ')
                
                # print("lap: ", n)
                
                # print(each_pressure.shape)
                # print(each_pressure[10])
                for yi in range(height):
                    # print("y = ", yi - (y1-1) , end="\t")
                    for xi in range(width):
                        # print("x = ", xi - (x1-1) , end="\t")
                        # sum
                        _sum[yi][xi] = _sum[yi][xi] + each_pressure[(yi*10)+xi]
                        # max
                        if _max[yi][xi] < each_pressure[(yi*10)+xi]:
                            _max[yi][xi] = each_pressure[(yi*10)+xi]
                        # min
                        if _min[yi][xi] > each_pressure[(yi*10)+xi]:
                            _min[yi][xi] = each_pressure[(yi*10)+xi]
                        # avg
                        _avg[yi][xi] = float(_sum[yi][xi]) / float(number_of_rows)

                        # if yi == 1 and xi == 0:
                        #     print(">>>>> " ,_avg[yi][xi])
                        # print each pressure
                        # print(each_pressure[(yi*10)+xi], end="")
                        # print("\t", end="")
                #     print()
                # print()

                # print(_sum)

            # print(_zero)
            # print(_max)
            # print(_min)
            # print(_avg)



            # if str_weight == "0.0":
            #     _zero = _avg
                # print(_zero)
                # for yi in range(y1-1,y2):
                #     for xi in range(x1-1,x2):
                #         if xi==2 and yi==4:
                #             print(_zero[yi-1][xi])
            # else:
            for yi in range(height):
                for xi in range(width):
                    if yi == axis_y and xi == axis_x:
                        # print(str_weight_list.index(w))
                        p_raw[str_weight_list.index(w)] = _avg[yi][xi] 
                        # if yi == 1 and xi == 0:
                        #         print(">>>>> ", _avg[yi][xi])
                        #         print(">>>>> ", p_raw[str_weight_list.index(w)])



        # ! Predict
        # Sample data
        # print(p_raw)
        # print(str_weight_list[1:])
        # if axis_y == 1 and axis_x == 0:
        #     print(">>>>> ", p_raw)

        x = np.array(p_raw).reshape((-1, 1))
        y = np.array(str_weight_list)


        y_pred, x, y = linear_regression(coor_x=axis_x, coor_y=axis_y, input_x=x, input_y=y+1.1)
        # if y_pred[0] < 0.0:
        #     y_pred = y_pred + (y_pred[0] * -1)

        # plotting regression line
        # plot_regression_line(y_pred, x, y)