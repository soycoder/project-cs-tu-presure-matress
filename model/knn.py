import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# ! Read Dataset and Re-format
file_name = ("../python/dataset.csv")
raw_data = pd.read_csv(file_name, header=None)
# print(raw_data)
raw_pressure = raw_data[1]
raw_class = raw_data[2]
index = raw_pressure.index
number_of_rows = len(index)


pressure = np.zeros((1,512), dtype=int)
pressure = np.delete(pressure, 0, 0)

_class = np.zeros((1), dtype=int)
_class = np.delete(_class, 0, 0)

for n in range(number_of_rows):
    temp = raw_pressure.iloc[n]
    each_pressure = np.fromstring(temp[1:-1], dtype=int, sep=' ')
    pressure = np.r_[pressure,[each_pressure]]

    temp2 = raw_class.iloc[n]
    _class = np.r_[_class,[temp2]]

# print(number_of_rows)
# print(pressure.shape)
# print(_class.shape)


# ! 
X = pressure
y = _class

from sklearn.model_selection import train_test_split
def split_balanced(data, target, test_size=0.2):

    classes = np.unique(target)
    # can give test_size as fraction of input data size of number of samples
    if test_size<1:
        n_test = np.round(len(target)*test_size)
    else:
        n_test = test_size
    n_train = max(0,len(target)-n_test)
    n_train_per_class = max(1,int(np.floor(n_train/len(classes))))
    n_test_per_class = max(1,int(np.floor(n_test/len(classes))))

    ixs = []
    for cl in classes:
        if (n_train_per_class+n_test_per_class) > np.sum(target==cl):
            # if data has too few samples for this class, do upsampling
            # split the data to training and testing before sampling so data points won't be
            #  shared among training and test data
            splitix = int(np.ceil(n_train_per_class/(n_train_per_class+n_test_per_class)*np.sum(target==cl)))
            ixs.append(np.r_[np.random.choice(np.nonzero(target==cl)[0][:splitix], n_train_per_class),
                np.random.choice(np.nonzero(target==cl)[0][splitix:], n_test_per_class)])
        else:
            ixs.append(np.random.choice(np.nonzero(target==cl)[0], n_train_per_class+n_test_per_class,
                replace=False))

    # take same num of samples from all classes
    ix_train = np.concatenate([x[:n_train_per_class] for x in ixs])
    ix_test = np.concatenate([x[n_train_per_class:(n_train_per_class+n_test_per_class)] for x in ixs])

    X_train = data[ix_train,:]
    X_test = data[ix_test,:]
    y_train = target[ix_train]
    y_test = target[ix_test]

    return X_train, X_test, y_train, y_test

X_train, X_test, y_train, y_test = split_balanced(X, y, test_size=0.30)

from sklearn.preprocessing import StandardScaler
scaler = StandardScaler()
scaler.fit(X_train)

X_train = scaler.transform(X_train)
X_test = scaler.transform(X_test)

# 1 - Supine
strr = "[  0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0 157 254   0   0   0   0   0   0 152   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0 189 205 209 239 192   0   0   0   0   0   0   0   0   0 161 153 254 242 229 225 200   0 160   0   0   0   0   0   0   0   0   0 157 182 179 177 152   0   0   0   0   0   0   0   0   0 162   0 156 206 183 174 157   0 160   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0 165 156 241 254 254 254 252   0 166   0 165   0   0   0   0   0 160 151 225 245 254 254 254   0 165   0 179   0   0   0   0   0   0   0 216 229 196 200 187   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0 223 228   0   0   0   0   0   0 233   0   0   0   0   0   0   0 214 178   0   0   0   0   0   0 201   0   0   0   0   0   0   0 212   0   0   0   0   0   0   0 181   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0 174   0   0   0   0   0   0   0 254   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0]"

data_unseen = np.fromstring(strr[1:-1], dtype=int, sep=' ')

from sklearn.neighbors import KNeighborsClassifier
classifier = KNeighborsClassifier(n_neighbors=3)
classifier.fit(X_train, y_train)

y_pred = classifier.predict(X_test)
df = pd.DataFrame({'actual': y_test, 'pred': y_pred})
print(df.head())

y_p_u = classifier.predict([data_unseen])
print("Now, " + str(y_p_u))

# # ! Evaluating the Algorithm
# from sklearn.metrics import classification_report, confusion_matrix
# # print(confusion_matrix(y_test, y_pred))
# # print(classification_report(y_test, y_pred))

error = []

import pickle 

# ! Calculating error for K values between 1 and 40
for i in range(1, 15):
    knn = KNeighborsClassifier(n_neighbors=i)
    knn.fit(X_train, y_train)
    pred_i = knn.predict(X_test)
    error.append(np.mean(pred_i != y_test))
    # ! model save
    # Its important to use binary mode 
    knnPickle = open('./weight/knn_n'+str(i), 'wb') 

    # source, destination 
    pickle.dump(knn, knnPickle)  

plt.figure(figsize=(12, 6))
plt.plot(range(1, 15), error, color='red', linestyle='dashed', marker='o',
         markerfacecolor='blue', markersize=10)
plt.title('Error Rate K Value')
plt.xlabel('K Value')
plt.ylabel('Mean Error')

plt.show()

# Its important to use binary mode 
knnPickle = open('knnpickle_file', 'wb') 

# source, destination 
pickle.dump(knn, knnPickle)                      


# load the model from disk
# loaded_model = pickle.load(open('knnpickle_file', 'rb'))
# result = loaded_model.predict(X_test)
