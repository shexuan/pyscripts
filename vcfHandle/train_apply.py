#!/usr/bin/env python3
# coding: utf-8


from sklearn import model_selection
from sklearn import preprocessing
from sklearn.metrics import recall_score
from sklearn.neural_network import MLPClassifier
from sklearn.externals import joblib

import pandas as pd
import numpy as np
import os
import argparse
from functools import wraps
import time


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
def preprocessing_features(training_array, predict_array, method):
    '''
    features scaling using MinMaxScaler.
    '''
    if method == 'Standardization':
        # 标准化，对特征进行缩放使其具有零均值和标准方差
        scaler = preprocessing.StandardScaler()
        training_array_scale = scaler.fit_transform(training_array)
        predict_array_scale = scaler.fit_transform(predict_array)
    if method == 'MinMaxScaler':
        # 归一化
        min_max_scaler = preprocessing.MinMaxScaler()
        training_array_scale = min_max_scaler.fit_transform(training_array)
        predict_array_scale = min_max_scaler.fit_transform(predict_array)
    return training_array_scale, predict_array_scale


@timethis
def train_apply(train_features, predict_features, prepro_method, model, model_pkl, result):
    '''
    train models parameters w(weight) and b(bias) and predictions.
    '''
    # trainning mlp models
    # load training data
    df_train = pd.read_csv(train_features, sep='\t', header=0, usecols=(2, 3, 4, 5, 6, 7, 8, 9))
    X_train = df_train.values[:, :-1]
    Y_train = (df_train.values[:, -1]).astype(int)
    # load predicted data
    df = pd.read_csv(predict_features, sep='\t', header=0)
    df_predict = df.iloc[:, [2, 3, 4, 5, 6, 7, 8]]
    array_predict = df_predict.values
    # fit: training model
    X_train_scale, X_predict_scale = preprocessing_features(X_train, array_predict, prepro_method)
    model.fit(X_train_scale, Y_train)
    # predicting with trained models
    predictions = model.predict(X_predict_scale)
    df['PREDICTION'] = predictions
    df['PREDICTION'] = df['PREDICTION'].apply(lambda x: int(x))
    df.to_csv(result, encoding='utf-8', sep='\t', index=False)
    joblib.dump(model, model_pkl)


@timethis
def stat(result, stats):
    '''
    stat the Raw recall, precision and after mlp filtered.
    '''
    vcf_identified = pd.read_csv(identified_vcf, sep='\t', header=None, comment='#')
    #vcf_raw=pd.read_csv(predict_features, header=0, sep='\t')
    res = open(stats, 'wt', encoding='utf-8')
    df = pd.read_csv(result, sep='\t', header=0)
    # True positive snvs before filter
    origin_tp = df[(df['CLASS'] == 1)]
    # mlp Classifier predicted True positive
    mlp_t = df[df['PREDICTION'] == 1]
    # True positive snvs after mlp filter
    mlp_tp = df[(df['PREDICTION'] == 1) & (df['CLASS'] == 1)]
    # mlp Classifier predicted False positive
    mlp_f = df[df['PREDICTION'] == 0]
    # mlp Classifier mis-filtered snvs
    mlp_misf = df[(df['CLASS'] == 1) & (df['PREDICTION'] == 0)]
    # real Flase positive snv numbers of mlp filtered
    mlp_rfp = df[(df['CLASS'] == 0) & (df['PREDICTION'] == 0)]
    # recall and precison after mlp filtered
    precision = len(mlp_tp)/len(mlp_t)
    recall = len(mlp_tp)/len(vcf_identified)
    res.write('RAW SNV Numbers:\t{}\n'.format(len(df)))
    res.write('RAW TP:\t'+str(len(origin_tp))+'\n')
    res.write('RAW reacall:\t{:.2%}\n'.format(len(origin_tp)/len(vcf_identified)))
    res.write('RAW precision:\t{:.2%}\n'.format(len(origin_tp)/len(df)))
    res.write('Total SNV Numbers remained after mlp filtered:\t{}\n'.format(len(mlp_t)))
    res.write('Precision after mlp filtered:\t{:.2%}\n'.format(precision))
    res.write('Recall after mlp filtered:\t{:.2%}\n'.format(recall))
    res.write('Total SNV Numers of mlp filtered :\t'+str(len(mlp_f))+'\n')
    res.write('TP of mlp filtered:\t'+str(len(mlp_misf))+'\n')
    res.write('FP of mlp filtered:\t'+str(len(mlp_rfp))+'\n')
    res.close()


@timethis
def main():
    train_apply(train_features, predict_features, prepro_method, model, model_pkl, result)
    stat(result, stats)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Trainning model and Apply predictions.")
    parser.add_argument("--train_features", "-tf", type=str,
                        help="Features for training model.")
    parser.add_argument("--predict_features", "-pf", type=str,
                        help="Features to predict.")
    parser.add_argument("--identified_vcf", "-id", type=str,
                        help="identified high confidence vcf.")
    parser.add_argument("--outdir", "-o", type=str, default='.',
                        help="Output directory.")
    parser.add_argument("--prefix", "-pref", type=str,
                        help="Output Result prefix")
    parser.add_argument("--preprocessing_features", "-prep", type=str, default="MinMaxScaler", choices=["Standardization", "MinMaxScaler"],
                        help="Preprocessing features method.")
    parser.add_argument("--alg_param", "-ap", type=str, default="tanh:0.001:10,10,10:lbfgs",
                        help="Comma seperated list of MLPClassifier algorithm parameters. Default 'tanh:0.001:10,10,10:lbfgs'")
    args = vars(parser.parse_args())

    train_features = args["train_features"]
    predict_features = args["predict_features"]
    identified_vcf = args["identified_vcf"]
    prepro_method = args['preprocessing_features']
    outdir = args["outdir"]
    result = outdir+'/'+args["prefix"]+'.mlp_filterd'
    stats = outdir+'/'+args["prefix"]+'.stat'
    if not os.path.exists(outdir):
        os.mkdir(outdir)

    model_pkl = 'mlp_snv.pkl'
    # mlp parameters
    params = args['alg_param'].split(':')
    activation, solver = params[0], params[-1]
    alpha = float(params[1])
    hidden_layer_sizes = tuple(map(lambda x: int(x), params[2].split(',')))
    model = MLPClassifier(activation=activation, alpha=alpha, hidden_layer_sizes=hidden_layer_sizes, solver=solver)

    main()
