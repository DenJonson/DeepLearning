import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf

from tkinter import *
import tkinter as tk
import win32gui
from PIL import ImageGrab, Image

# использование обученной полносвязной сети распознаванию рукописных цифр
ARCH_TYPE = 1 #Тип архитектуры нейронной сети: 0 - полносвязная, 1 - сверточная


if(ARCH_TYPE == 0):
    model = tf.keras.models.load_model(r"NumPrediction\num_predict_model_fullyConnected.h5")
elif(ARCH_TYPE == 1):
    model = tf.keras.models.load_model(r"NumPrediction\num_predict_model_Convolutional.h5")


def predict_digit(img):
    # изменение рзмера изобржений на 28x28
    img = img.resize((28,28))
    # конвертируем rgb в grayscale
    img = img.convert('L')
    img = np.array(img)
    # изменение размерности для поддержки модели ввода и нормализации
    img = img.reshape(28,28)
    img = img/255
    img = 1 - img
    # plt.imshow(img, cmap=plt.cm.binary)
    # plt.show()
    img = np.expand_dims(img, axis=0)
    if(ARCH_TYPE==1):
        np.expand_dims(img, axis=3)
    # предсказание цифры
    res = model.predict(img)
    
    return np.argmax(res), max(res[0])
    
class App(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        
        self.x = self.y = 0
        
        # Создание элементов
        self.canvas = tk.Canvas(self, width=280, height=280, bg = "white", cursor="cross")
        self.label = tk.Label(self, text="Думаю..", font=("Helvetica", 48))
        self.classify_btn = tk.Button(self, text = "Распознать", command =         self.classify_handwriting) 
        self.button_clear = tk.Button(self, text = "Очистить", command = self.clear_all)
        
        # Сетка окна
        self.canvas.grid(row=0, column=0, pady=2, sticky=W, )
        self.label.grid(row=0, column=1,pady=2, padx=2)
        self.classify_btn.grid(row=2, column=1, pady=2, padx=2)
        self.button_clear.grid(row=2, column=0, pady=2)
        
        # self.canvas.bind("<Motion>", self.start_pos)
        self.canvas.bind("<B1-Motion>", self.draw_lines)
        
    def clear_all(self):
        self.canvas.delete("all")
        
    def classify_handwriting(self):
        HWND = self.canvas.winfo_id() 
        rect = win32gui.GetWindowRect(HWND) # получаем координату холста
        im = ImageGrab.grab(rect)
        
        digit, acc = predict_digit(im)
        self.label.configure(text= str(digit)+', '+ str(int(acc*100))+'%')
        
    def draw_lines(self, event):
        self.x = event.x
        self.y = event.y
        r=8
        self.canvas.create_oval(self.x-r, self.y-r, self.x + r, self.y + r, fill='black')


app = App()
mainloop()