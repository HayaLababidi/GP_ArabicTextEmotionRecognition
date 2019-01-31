import keras
import random
from keras.models import Sequential

_dropout_rate = 0.2
_dropout_rate_softmax = 0.5
_number_of_inputs = 100 #max number of words /characters
_input_size = 300
_batch_size = 100
_kernal_size= 5 #An integer or tuple/list of a single integer
_pool_size = 3
_noise_shape = (_batch_size,1,_number_of_inputs)

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