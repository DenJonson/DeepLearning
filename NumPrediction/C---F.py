import numpy as np
import matplotlib.pyplot as plt
from tensorflow import keras

#Создание полносвязной нейронной сети для перевода градусов цельсия в градусы Фаренгейта

c = np.array([-40, -10, 0, 8, 15, 22, 38])
f = np.array([-40, 14, 32, 46, 59, 72, 100])

model = keras.Sequential()

model.add(  keras.layers.Dense(units=1, input_shape=(1,), activation='linear' ))

model.compile(loss='mean_squared_error', optimizer=keras.optimizers.Adam(0.1))

history = model.fit(c, f, epochs=500, verbose=0)

plt.plot(history.history['loss'])
plt.grid(True)
plt.show()