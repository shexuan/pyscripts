#!/usr/bin/env python3
# coding: utf-8

from sklearn import model_selection
from sklearn.metrics import recall_score
from sklearn.neural_network import MLPClassifier
from sklearn.externals import joblib
from sklearn import preprocessing

import pandas as pd
import numpy as np
import os
import argparse
from functools import wraps


def timethis(func):
    ''' Decorator that reports the execution time.'''
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(func.__name__, end-start)
        return result
    return wrapper


@timethis
def mlp_classifier():
    '''
    Generating MLPClassifiers with parameters combinations.
    '''
    models = []
    hidden_layer_sizes = [50, 100, 150, 250, 500,
                          (10, 10), (20, 25), (30, 50), (10, 10, 10), (20, 30, 40), (30, 50, 70)]
    activation = ['identity', 'logistic', 'tanh', 'relu']
    solver = ['lbfgs', 'sgd', 'adam']
    alpha = [0.00001, 0.0001, 0.001]
    for h in hidden_layer_sizes:
        for a in activation:
            for s in solver:
                for alp in alpha:
                    mlp = MLPClassifier(hidden_layer_sizes=h, activation=a, solver=s, alpha=alp)
                    models.append(mlp)
    return models


@timethis
def preprocessing_features(array, method):
    '''
    features scaling using MinMaxScaler.
    '''
    X = array[:, :-1]
    Y = array[:, -1].astype(int)

    if method == 'Standardization':
        # 标准化，对特征进行缩放使其具有零均值和标准方差
        X = preprocessing.StandardScaler().fit_transform(X)
    if method == 'MinMaxScaler':
        # 归一化
        min_max_scaler = preprocessing.MinMaxScaler()
        X = min_max_scaler.fit_transform(X)
    X_train, X_validation, Y_train, Y_validation = model_selection.train_test_split(X, Y, test_size=0.0, random_state=6)
    return X_train, X_validation, Y_train, Y_validation


@timethis
def test_model(features, tmp, prep_method):
    '''
    Testing model with different parameters.
    '''
    df = pd.read_csv(features, header=0, sep='\t', usecols=(2, 3, 4, 5, 6, 7, 8, 9))
    array = df.values
    X_train, X_validation, Y_train, Y_validation = preprocessing_features(array=array, method=prep_method)
    kfold = model_selection.KFold(n_splits=10, random_state=6)

    models = mlp_classifier()
    res = open(tmp, 'wt', encoding='utf-8')
    res.write('idx\tstd\tmean\tmodel\n')
    for idx, model in enumerate(models):
        cv_results = model_selection.cross_val_score(
            model, X_train, Y_train.astype(int), cv=kfold, scoring='accuracy')
        res.write('{idx}\t{std:0.2%}\t{mean:0.2%}\t{model}\n'.format(
            idx=idx, std=cv_results.std(), mean=cv_results.mean(), model=model))
    res.close()


@timethis
def sort_model(tmp, reslut):
    '''
    Sorting the model with different parameters according to accuracy.
    '''
    with open(tmp, 'r', encoding='utf-8') as f, open('tmp2', 'wt', encoding='utf-8') as tmp_f:
        tmp_f.write(next(f))
        try:
            while True:
                line = ''
                for i in range(7):
                    line += next(f).strip()
                tmp_f.write(line+'\n')
        except StopIteration:
            pass
    df = pd.read_csv('tmp2', header=0, sep='\t')
    df = df.sort_values(by=['mean', 'std'], axis=0, ascending=False)
    df.to_csv(result, sep='\t', index=0)
    os.remove('tmp2')


@timethis
def main():
    test_model(features, tmp, prep_method)
    sort_model(tmp, result)
    os.remove(tmp)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Train mlp parameters.")
    parser.add_argument("--train_features", "-tf", type=str, help="Features tables used for trainning model.")
    parser.add_argument("--outdir", '-o', type=str, help="Output directory.")
    parser.add_argument("--param_prefix", "-pref", type=str, help="Model stat file name prefix.")
    parser.add_argument("--preprocessing_features", "-prep", type=str, default="MinMaxScaler", choices=["Standardization", "MinMaxScaler"],
                        help="Preprocessing features method.")
    args = vars(parser.parse_args())

    outdir = args['outdir']
    prefix = args['param_prefix']
    features = args['train_features']
    prep_method = args['preprocessing_features']
    if not os.path.exists(outdir):
        os.mkdir(outdir)
    tmp = outdir+'/'+'model_assess.tmp'
    result = outdir+'/'+prefix+'_model_assess.txt'

    main()
