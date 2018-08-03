from sklearn import model_selection
from sklearn.metrics import recall_score
from sklearn.neural_network import MLPClassifier
from sklearn.externals import joblib

import pandas as pd
import numpy as np
import os


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
                    mlp = MLPClassifier(hidden_layer_sizes=h,
                                        activation=a, solver=s, alpha=alp)
                    models.append(mlp)
    return models

############# my data #################################
# os.chdir('D:/smart-variant-filtering/mymodel/')

# df = pd.read_csv('vcf.info', sep='\t', header=0)
# df = df.fillna(0.)

# df['CLASS'] = df['cls'].apply(lambda x: int(1) if x == 'TP' else int(0))
# df = df.drop(['CHROM', 'POS', 'cls', 'AF', 'AC', 'AN', 'ClippingRankSum',
#               'ExcessHet', 'MLEAC', 'MLEAF', 'DP', 'BaseQRankSum'], axis=1)

# array = df.values
# X = array[:, 0:6]
# Y = array[:, 6]


#################### SVF data #########################
df = pd.read_csv('HG002_oslo_exome_dbsnp_SNVs.table', sep='\t', header=0)
df = df.fillna(0.)
df['CLASS'] = df['HG002.BD'].apply(lambda x: int(1) if x == 'TP' else int(0))
df = df.drop(['CHROM', 'POS', 'TYPE', 'HG002.BD'], axis=1)

array = df.values
X = array[:, 0:7]
Y = array[:, 7]

validation_size = 0.
X_train, X_validation, Y_train, Y_validation = model_selection.train_test_split(
    X, Y, test_size=validation_size, random_state=6)
kfold = model_selection.KFold(n_splits=5, random_state=6)

models = mlp_classifier()
print('model\tstd\tmean')
res = open('model_assess.txt', 'wt', encoding='utf-8')
for idx, model in enumerate(models):
    cv_results = model_selection.cross_val_score(
        model, X_train, Y_train.astype(int), cv=kfold, scoring='accuracy')
    res.write('{idx}\t{std:0.2%}\t{mean:0.2%}\t{model}\n'.format(
        idx=idx, std=cv_results.std(), mean=cv_results.mean(), model=model))


res.close()
print('training over')
