#!/usr/bin/env/python3
# coding:utf-8


import matplotlib.pyplot as plt
import numpy as np
import itertools
from sklearn.metrics import confusion_matrix
from sklearn.utils.multiclass import unique_labels


def plot_confusion_matrix(cm, classes, normalize=False,
                          title='Confusion matrix',
                          cmap=plt.cm.Blues):
    """
    This function prints and plots the confusion matrix. 
    Normalization can be applied by setting `normalize=True`. 
    """
    if normalize:
        cm_norm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
        print("Normalized confusion matrix")
    else:
        print('Confusion matrix, without normalization')
        # print(cm)
    plt.figure(figsize=(20, 20), dpi=100)
    plt.imshow(cm, interpolation='nearest', cmap=cmap)
    plt.title(title, fontsize=20)
    plt.colorbar()
    labels = []
    if isinstance(classes, dict):
        for idx, label in sorted(classes.items(), key=lambda x: x[0]):
            labels.append(label)
    else:
        labels = classes
    tick_marks = np.arange(len(labels))
    plt.xticks(tick_marks, labels, rotation=90, fontsize=18)
    plt.yticks(tick_marks, labels, fontsize=18)
    plt.ylim(tick_marks[-1]+0.5, tick_marks[0]-0.5)
    fmt = '.2f' if normalize else 'd'
    thresh = cm.max() / 2.
    print(thresh)
    for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
        plt.text(j, i, format(cm[i, j], 'd')+'\n'+format(cm_norm[i, j], '.2f'),
                 horizontalalignment="center",
                 color="pink" if cm[i, j] > thresh else "black",
                 fontsize=16)
    plt.tight_layout()
    plt.ylabel('True label', fontsize=20)
    plt.xlabel('Predicted label', fontsize=20)


if __name__ == '__main__':
    df = {'label': np.random.randint(2, size=100),
          'prediction': np.random.randint(2, size=100)}

    cf_matrix = confusion_matrix(y_true=df['label'], y_pred=df['prediction'])
    classes = {0: 'dog', 1: 'cat'}
    plot_confusion_matrix(cf_matrix, classes, normalize=True)
