import keras
import random
from keras.models import Sequential
import csv
import read_data
_dropout_rate = 0.2
_dropout_rate_softmax = 0.5
_number_of_inputs = 100 #max number of words /characters
_input_size = 100
_batch_size = 100
_kernal_size= 5 #An integer or tuple/list of a single integer
_pool_size = 3
_noise_shape = (_batch_size,1,_number_of_inputs)
_epochs = 25
print("fjrfj")
'''
#X list of list of arrays
X_train, X_test, y_train, y_test = read_data.read_dataset()
try:
    with open("Embedded_trainX.csv",'w') as f:
        writer = csv.writer(f,delimiter=',')
        writer.writerows(X_train)
    with open("Embedded_testX.csv",'w') as f:
        writer = csv.writer(f,delimiter=',')
        writer.writerows(X_test)
    with open("Embedded_trainY.csv",'w') as f:
        writer = csv.writer(f,delimiter=',')
        writer.writerows(y_train)
    with open("Embedded_testY.csv",'w') as f:
        writer = csv.writer(f,delimiter=',')
        writer.writerows(y_test)
except:
    print("error saving")
'''
X_train = list(csv.reader(open("Embedded_trainX.csv")))
y_train = list(csv.reader(open("Embedded_trainY.csv")))
X_test = list(csv.reader(open("Embedded_testX.csv")))
y_test = list(csv.reader(open("Embedded_testY.csv")))

print("done input embedding")
model = Sequential()

#input
#model.add(keras.layers.Input(shape=(_number_of_inputs,_input_size)))

#Dropout
model.add(keras.layers.Dropout(rate=_dropout_rate,input_shape=(_number_of_inputs,_input_size)))#,noise_shape,random.randint(0,number_of_inputs)))

#Convolution
model.add(keras.layers.Conv1D(filters=_number_of_inputs, kernel_size=_kernal_size, strides=1, padding='same', activation="relu"))
model.add(keras.layers.Conv1D(filters=_number_of_inputs, kernel_size=_kernal_size, strides=1, padding='same', activation="relu"))
model.add(keras.layers.MaxPooling1D(pool_size = _pool_size, padding='same'))

#Dropout
model.add(keras.layers.Dropout(_dropout_rate_softmax))#,noise_shape,random.randint(0,number_of_inputs)))

#output
model.add(keras.layers.Dense(8, activation="softmax"))

model.compile(
    loss='categorical_crossentropy',
    optimizer='adam',
    metrics=['accuracy']
)

model.summary()

# Train the model
model.fit(
    X_train,
    y_train,
    batch_size=_batch_size,
    epochs=_epochs,
    validation_data=(X_test, y_test),
    shuffle=True
)