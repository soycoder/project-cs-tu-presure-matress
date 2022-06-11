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


pressure = np.zeros((1,512), dtype=float)
pressure = np.delete(pressure, 0, 0)

_class = np.zeros((1), dtype=int)
_class = np.delete(_class, 0, 0)

for n in range(number_of_rows):
    temp = raw_pressure.iloc[n]
    each_pressure = np.fromstring(temp[1:-1], dtype=float, sep=' ')
    pressure = np.r_[pressure,[each_pressure]]

    temp2 = raw_class.iloc[n]
    _class = np.r_[_class,[temp2]]

# print(number_of_rows)
# print(pressure.shape)
# print(_class)


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

X_train, X_test, y_train, y_test = split_balanced(X, y, test_size=0.20)

# print(X_test[0], y_test[0])

from sklearn.preprocessing import StandardScaler
scaler = StandardScaler()
scaler.fit(X_train)

X_train = scaler.transform(X_train)
X_test = scaler.transform(X_test)

# 1 - Supine
strr = "[  0   0   0   0   0   0   0   0   0   0   0   0   1   0   0   0 119 160 200 281 221 214 364 402 531 381 345  44 214 188 173 176  28  40  50  67  65  61  81  90 103  86  76   9  62  55  42  67  20  28  42  48  50  51  52  63  60  56  50   5  46  44  39  64   7   9  21  23  22  20  18  20  21  19  18   1  16  16  13  25  77 101 116 164 125 135 190 233 237 230 207  24 137 113  98 108 109 147 181 253 211 205 382 353 362 432 327  41 217 177 152 159 107 145 185 260 205 212 333 374 385 362 299  39 246 178 154 155  79 104 131 205 154 142 215 251 249 240 194  26 166 132 114 105 121 161 226 646 245 229 261 307 297 266 244  44 231 282 187 168  58  73 118 261 118 109 125 138 131 126 115  20 112 244  91  88  37  68 123 151  83  82 112 113 116 109 103  13  77 134  69  69  68  94 147 171 126 127 209 225 236 256 204  24 134 130 104 102 149 199 242 342 265 262 455 505 582 466 430  58 280 243 202 212 119 181 217 287 225 224 392 401 404 398 400  48 224 204 177 180  91 147 175 252 188 176 321 287 275 267 271  34 180 197 148 193  42 107 103  82  84  76 105  96  94  89  84  13  81  62 149 106  44  64  76  67  71  68  83  75  74  71  71   9  65  50  88  78  35  55  61  54  57  54  53  48  49  48  48   6  60  39  61  59  38  58  64  69  84  72  72  66  66  67  65   9  73  49  80  85  31  45  54  65  64  63  58  52  53  53  51   7  58  40  61  64  52  45  56  66  89  99  62  64  68  62  60   9  89  47  59  47  81  95 119 140 244 315 134 136 130 131 132  22 229 102 120 104 122 143 182 215 429 445 197 205 199 202 197  37 410 157 160 145  94 116 149 174 408 278 151 156 154 153 144  29 344 126 139 112  83 100 135 144 344 225 135 144 137 140 120  26 295 115 118  98  40  44  54  64  88  66  46  48  51  47  48   8  76  47  44  38  41  53  72 102 143 108  71  76  74  73  75  12 128  81  74  59  71  80 103 278 161 128 119 130 124 117 107  19 136 139  97  90  30  39  66  81  79  72  52  53  53  50  48   8  74  58  58  62  14  24  30  39  34  31  26  24  27  26  25   4  36  30  46  43   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0]"

data_unseen = np.fromstring(strr[1:-1], dtype=int, sep=' ')

from sklearn.neighbors import KNeighborsClassifier
classifier = KNeighborsClassifier(n_neighbors=3)
classifier.fit(X_train, y_train)

y_pred = classifier.predict(X_test)
df = pd.DataFrame({'actual': y_test, 'pred': y_pred})
# print(df)

y_p_u = classifier.predict([data_unseen])
# print("Now, " + str(y_p_u))

# ! Evaluating the Algorithm
from sklearn.metrics import classification_report, confusion_matrix
# print(confusion_matrix(y_test, y_pred))
# print(classification_report(y_test, y_pred))

error = []

import pickle 

# ! Calculating error for K values between 3 and 15
for i in range(3, 16, 2):
    print("k: ", i)
    knn = KNeighborsClassifier(n_neighbors=i)
    knn.fit(X_train, y_train)
    pred_i = knn.predict(X_test)
    error.append(np.mean(pred_i != y_test))
    # ! model save
    # Its important to use binary mode 
    knnPickle = open('./weight/knn_new_n'+str(i), 'wb') 

    # source, destination 
    pickle.dump(knn, knnPickle)  

    # print(confusion_matrix(y_test, pred_i))
    print(classification_report(y_test, pred_i))

# plt.figure(figsize=(12, 6))
# plt.plot(range(3, 16, 2), error, color='red', linestyle='dashed', marker='o',
#          markerfacecolor='blue', markersize=10)
# plt.title('Error Rate K Value')
# plt.xlabel('K Value')
# plt.ylabel('Mean Error')

# plt.show()

# Its important to use binary mode 
# knnPickle = open('knnpickle_file', 'wb') 

# source, destination 
# pickle.dump(knn, knnPickle)                      


# load the model from disk
# loaded_model = pickle.load(open('knnpickle_file', 'rb'))
# result = loaded_model.predict(X_test)
