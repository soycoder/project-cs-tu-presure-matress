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
    plt.ylabel('y (mmHg)')
 
    # function to show plot
    plt.show()

def linear_regression(coor_x, coor_y, input_x, input_y):
    print("Coor: ", coor_x, coor_y)
    print("Input: ", input_x, input_y)

    # Step 2: Provide data
    x, y = np.array(input_x), np.array(input_y)
    areaMapDict = {
    "x1x5-y2y5": [[1.5*1.0, 1.5*1.0, 1.5*1.0, 1.5*1.0, 1.5*1.0],
                  [1.0*1.0, 1.0*1.0, 1.0*1.0, 1.0*1.0, 1.0*1.0],
                  [1.5*1.0, 1.5*1.0, 1.5*1.0, 1.5*1.0, 1.5*1.0],
                  [1.0*1.0, 1.0*1.0, 1.0*1.0, 1.0*1.0, 1.0*1.0],
                  [1.0*1.0, 1.0*1.0, 1.0*1.0, 1.0*1.0, 1.0*1.0]]
    }
    for i in range(len(y)):
        y[i] = (y[i]/(30.4**2) *areaMapDict["x1x5-y2y5"][coor_x][coor_y]) * 735.55914
    
    # print(y)

    # Step 3: Create a model and fit it
    model = LinearRegression().fit(x, y)
    Pkl_Filename = "./calibrated_sensors/model/x"+str(coor_x+1)+"-y"+str(coor_y+1)+".pkl"  
    


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

# str_weight_list = [0.0]
str_weight_list = [-1.0,0.0,0.5,1.0,1.5,2.0,2.5,3.0,3.5,4.0,4.5,5.0,5.5,6.0,6.5,7.0,7.5,8.0,8.5,9.0]
_range_list = ["x1x5-y2y5"]
# print(areaMapDict["x1x5-y2y5"][0][1])

for r in _range_list:
    _range = r

    x = _range.split("-")[0]
    y = _range.split("-")[1]
    # x - axis
    x1 = int(x.split("x")[1])
    x2 = int(x.split("x")[2])
    # y - axis
    y1 = int(y.split("y")[1])
    y2 = int(y.split("y")[2])

    y_size = y2-(y1-1)
    x_size = x2-(x1-1)

    for axis_y in range(y1-1,y2):
        print("y = ", axis_y - (y1-1) , end="\t")
        for axis_x in range(x1-1,x2):
            print("x = ", axis_x - (x1-1) , end="\t")
            print()
            # p_raw - set p_raw in arr
            p_raw = np.zeros((len(str_weight_list[1:])), dtype=float)
            # Zero - set zeros in arr
            _zero = np.zeros((y_size,x_size), dtype=float)
            _zero_0 = np.zeros((y_size,x_size), dtype=float)

            for w in str_weight_list:
                str_weight = str(w)
                print(" > "+_range+" | "+str_weight)

                if str_weight  == "-1.0":
                    file_name = ("../python/calibrating_file/setWithoutBaseBox/nonConvert-"+_range+"-0.0kg.csv")
                else:
                    file_name = ("../python/calibrating_file/setWithoutBaseBox/nonConvert-"+_range+"-"+str_weight+"kg-box.csv")
                raw_data = pd.read_csv(file_name, header=None)
                # print(raw_data)
                raw_pressure = raw_data[0]
                index = raw_pressure.index
                number_of_rows = len(index)

                # print(number_of_rows)

                
                

                # ZeroNonBox - set zeros in arr
                _zero_non_box = np.zeros((y_size,x_size), dtype=float)

                # Sum - set zeros in arr
                _sum = np.zeros((y_size,x_size), dtype=int)

                # Max - set max in arr
                _max = np.zeros((y_size,x_size), dtype=int)

                # Min - set min in arr
                _min = np.zeros((y_size,x_size), dtype=int)
                _min[0:4,0:5] = 1024

                # Avg - set avg in arr
                _avg = np.zeros((y_size,x_size), dtype=float)

                # Loop
                for n in range(number_of_rows):
                    temp = raw_pressure.iloc[n]
                    each_pressure = np.fromstring(temp[1:-1], dtype=int, sep=' ')
                    
                    # print("lap: ", n)
                    
                    # print(each_pressure.shape)
                    # print(each_pressure)
                    for yi in range(y1-1,y2):
                        # print("y = ", yi - (y1-1) , end="\t")
                        for xi in range(x1-1,x2):
                            # print("x = ", xi - (x1-1) , end="\t")
                            # sum
                            _sum[yi - (y1-1)][xi] = _sum[yi - (y1-1)][xi] + each_pressure[(yi*16)+xi]
                            # max
                            if _max[yi - (y1-1)][xi] < each_pressure[(yi*16)+xi]:
                                _max[yi - (y1-1)][xi] = each_pressure[(yi*16)+xi]
                            # min
                            if _min[yi - (y1-1)][xi] > each_pressure[(yi*16)+xi]:
                                _min[yi - (y1-1)][xi] = each_pressure[(yi*16)+xi]
                            # avg
                            _avg[yi - (y1-1)][xi] = float(_sum[yi - (y1-1)][xi]) / float(number_of_rows)

                            # print each pressure
                            # print(each_pressure[(yi*16)+xi], end="")
                            # print("\t", end="")
                    #     print()
                    # print()

                    # print(_sum)

                # print(_zero)
                # print(_max)
                # print(_min)
                # print(_avg)



                if str_weight == "-1.0":
                    _zero_non_box = _avg
                    # for yi in range(y1-1,y2):
                    #     for xi in range(x1-1,x2):
                    #         if xi==2 and yi==4:
                    #             print(_avg[yi-1][xi])
                elif str_weight == "0.0":
                    _zero = _avg
                    # print(_zero)
                    # for yi in range(y1-1,y2):
                    #     for xi in range(x1-1,x2):
                    #         if xi==2 and yi==4:
                    #             print(_zero[yi-1][xi])
                else:
                    for yi in range(y1-1,y2):
                        for xi in range(x1-1,x2):
                            # if xi==2 and yi==4:
                                # print(str_weight_list.index(w))
                            p_raw[str_weight_list.index(w)-1] = _avg[yi-1][xi] - _zero[yi-1][xi] 
                            # print(p_raw[str_weight_list.index(w)-1] , " = ", _avg[yi-1][xi] ," - ", _zero[yi-1][xi]) 

                        # print()
                            # area_spot = areaMapDict["x1x5-y2y5"][0][0]
                            # print(p_raw/(30.4**2) * area_spot)

            # ! Predict
            # Sample data
            # print(p_raw)
            # print(str_weight_list[1:])
            x = np.array(p_raw[1:]).reshape((-1, 1))
            y = np.array(str_weight_list[2:])


            y_pred, x, y = linear_regression(coor_x=axis_x,coor_y=axis_y,input_x=x, input_y=y)
            # if y_pred[0] < 0.0:
            #     y_pred = y_pred + (y_pred[0] * -1)

            # plotting regression line
            plot_regression_line(y_pred, x, y)




