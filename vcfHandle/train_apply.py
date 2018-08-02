#!/usr/bin/env python3
# coding: utf-8


import pandas as pd
import numpy as np
import os
import argparse

from sklearn import model_selection
from sklearn.metrics import recall_score
from sklearn.neural_network import MLPClassifier
from sklearn.externals import joblib


def train(features, model, model_pkl):
    '''
    train models parameters w(weight) and b(bias).  
    '''
    df = pd.read_csv(features, sep='\t', header=0,
                     usecols=(2, 3, 4, 5, 6, 7, 8, 9))
    array = df.values
    X = array[:, :-1]
    Y = array[:, -1]
    X_train, X_validation, Y_train, Y_validation = model_selection.train_test_split(
        X, Y, test_size=0.0, random_state=6)
    model.fit(X_train, Y_train)
    joblib.dump(model, model_pkl)


def apply(features, model_pkl, identified_vcf):
    model = joblib.load(model_pkl)
    vcf_identified = pd.read_csv(
        identified_vcf, sep='\t', header=None, comment='#')
    df = pd.read_csv(features, sep='\t', header=0)
    df_features = df.iloc[:, [2, 3, 4, 5, 6, 7, 8]]
    array = df_features.values
    predictions = model.predict(array)
    df['PREDICTION'] = predictions
    df['PREDICTION'] = df['PREDICTION'].apply(lambda x: int(x))
    tp = df[(df['CLASS'] == 1) & (df['PREDICTION'] == 1)]
    df_filtered = df[df['PREDICTION'] == 1]
    precision = len(tp)/len(df_filtered)
    recall = len(tp)/len(vcf_identified)
    print('Precision:\t{:.2%}'.format(precision))
    print('Recall:\t{:.2%}'.format(recall))
    df.to_csv('predictions.txt', encoding='utf-8', sep='\t', index=False)


def main():
    train(train_features, model, model_pkl)
    apply(predict_features, model_pkl, identified_vcf)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="Train model and Apply.")
    parser.add_argument("--train_features", "-t", type=str,
                        help="Features for training model.")
    parser.add_argument("--predict_features", "-p",
                        type=str, help="Features to predict.")
    parser.add_argument("--identified_vcf", "-id", type=str,
                        help="identified high confidence vcf.")
    args = vars(parser.parse_args())

    train_features = args["train_features"]
    predict_features = args["predict_features"]
    identified_vcf = args["identified_vcf"]
    model = MLPClassifier(activation='tanh',
                          hidden_layer_sizes=500, solver='adam')
    model_pkl = 'mlp_snv.pkl'
    main()
