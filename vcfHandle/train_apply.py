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
    df = pd.read_csv(features, sep='\t', header=0, usecols=(2, 3, 4, 5, 6, 7, 8, 9))
    array = df.values
    X = array[:, :-1]
    Y = array[:, -1]
    X_train, X_validation, Y_train, Y_validation = model_selection.train_test_split(X, Y, test_size=0.0, random_state=6)
    model.fit(X_train, Y_train)
    joblib.dump(model, model_pkl)


def apply(features, model_pkl, reslut):
    '''
    Classified samples by trained models.
    '''
    model = joblib.load(model_pkl)
    df = pd.read_csv(features, sep='\t', header=0)
    df_features = df.iloc[:, [2, 3, 4, 5, 6, 7, 8]]
    array = df_features.values
    predictions = model.predict(array)
    df['PREDICTION'] = predictions
    df['PREDICTION'] = df['PREDICTION'].apply(lambda x: int(x))
    df.to_csv(reslut, encoding='utf-8', sep='\t', index=False)


def stat(reslut):
    '''
    stat the Raw recall, precision and after mlp filtered.
    '''
    vcf_identified = pd.read_csv(identified_vcf, sep='\t', header=None, comment='#')
    #vcf_raw=pd.read_csv(predict_features, header=0, sep='\t')
    res = open(result, 'wt', encoding='utf-8')
    df = pd.read_csv(reslut, sep='\t', header=0)
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
    recall = len(tp)/len(vcf_identified)
    res.write('RAW SNV Numbers:\t{}\n'.format(len(df)))
    res.write('RAW TP:\t'+str(len(origin_tp))+'\n')
    res.write('RAW reacall:\t{:.2%}\n'.format(len(origin_tp)/len(len(vcf_identified))))
    res.write('RAW precision:\t{:.2%}\n'.format(len(origin_tp)/len(res)))
    res.write('Total SNV Numbers remained after mlp filtered:\t{}\n'.format(mlp_t))
    res.write('Precision after mlp filtered:\t{:.2%}\n'.format(precision))
    res.write('Recall after mlp filtered:\t{:.2%}\n'.format(recall))
    res.write('Total SNV Numers of mlp filtered :\t'+str(len(mlp_f))+'\n')
    res.write('TP of mlp filtered:\t'+str(len(mlp_misf))+'\n')
    res.write('FP of mlp filtered:\t'+str(len(mlp_rfp))+'\n')
    res.close()


def main():
    train(train_features, model, model_pkl)
    apply(predict_features, model_pkl, identified_vcf)
    stat()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Train model and Apply.")
    parser.add_argument("--train_features", "-t", type=str,
                        help="Features for training model.")
    parser.add_argument("--predict_features", "-p", type=str,
                        help="Features to predict.")
    parser.add_argument("--identified_vcf", "-id", type=str,
                        help="identified high confidence vcf.")
    parser.add_argument("--outdir", "-o", , type=str, default='.'
                        help="Output directory.")
    parser.add_argument("--prefix", "-pref", type=str,
                        help="Output Result prefix")
    args = vars(parser.parse_args())

    train_features = args["train_features"]
    predict_features = args["predict_features"]
    identified_vcf = args["identified_vcf"]
    result = outdir+'/'+args["prefix"]+'.mlp_filterd'
    outdir = args["outdir"]
    if not os.path.exists(outdir):
        os.mkdir(outdir)
    model = MLPClassifier(activation='tanh', hidden_layer_sizes=500, solver='adam')
    model_pkl = 'mlp_snv.pkl'

    main()
