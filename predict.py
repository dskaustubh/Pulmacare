import numpy as np
import pandas as pd
from keras.models import load_model
from keras.preprocessing import image

model = load_model('model.h5')
img = image.load_img('test_3.jpeg', target_size=(100,100))#Pneumonia Image 
x = image.img_to_array(img)
x = np.expand_dims(x, axis=0)
x = x/255.0
pred = print(model.predict_proba(x))