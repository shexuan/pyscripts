#!/usr/bin/env python3
# coding: utf-8


import pandas as pd
import numpy as np 


from sklearn import model_selection
from sklearn.metrics import recall_score
from sklearn.neural_network import MLPClassifier
from sklearn.externals import joblib


mlp = MLPClassifier(activation='tanh', alpha=0.001, batch_size='auto', beta_1=0.9,beta_2=0.999, early_stopping=False, epsilon=1e-08,hidden_layer_sizes=(30    , 50, 70), learning_rate='constant',learning_rate_init=0.001, max_iter=200, momentum=0.9,nesterovs_momentum=True, power_t=0.5, random_state=None,shuffle=True, solver='a    dam', tol=0.0001, validation_fraction=0.1,verbose=False, warm_start=False)

