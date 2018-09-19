import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix
import numpy as np
import IPython.display as ipd

def history_plot(history_dict, metrics=['acc', 'loss']):
    
    epochs = range(1, len(history_dict[metrics[0]])+1)
    plt.figure(figsize=(15, 6*(len(metrics)/2)))
    
    for i in range(len(metrics)):
        # get data
        data = history_dict[metrics[i]]
        val_data = history_dict['val_' + metrics[i]]
        
        # plot
        plt.subplot(1, 2, i+1)
        plt.title(metrics[i])
        plt.plot(epochs, data, 'og', label="Training")
        plt.plot(epochs, val_data, 'b', label="Validation")
        plt.legend()
        
def confusion_matrix_plot(one_hot_y_pred, one_hot_y_tar,
                          classes=['EN', 'FR', 'DE'],
                          title='Confusion matrix',
                          cmap=plt.cm.Blues):
    #http://scikit-learn.org/stable/auto_examples/model_selection
    #/plot_confusion_matrix.html#sphx-glr-auto-examples-model-selection-plot-confusion-matrix-py
    
    plt.figure(figsize=(10, 5))
    def plot(cnf_matrix, i, classes=classes, title=title, cmap=cmap, fmt='.2f'):
        plt.subplot(1, 2, i)
        plt.imshow(cnf_matrix, interpolation='nearest', cmap=cmap)
        plt.title(title)
        plt.colorbar()
        tick_marks = np.arange(len(classes))
        plt.xticks(tick_marks, classes, rotation=45)
        plt.yticks(tick_marks, classes)

        thresh = cnf_matrix.max() / 2.
        for i in range(cnf_matrix.shape[0]): 
            for j in range(cnf_matrix.shape[1]):
                plt.text(j, i, format(cnf_matrix[i, j], fmt),
                         horizontalalignment="center",
                         color="white" if cnf_matrix[i, j] > thresh else "black")

        plt.tight_layout()
        plt.ylabel('True label')
        plt.xlabel('Predicted label')

    
    cnf_matrix_abs = confusion_matrix(np.argmax(one_hot_y_tar, axis=1), np.argmax(one_hot_y_pred, axis=1))
    cnf_matrix_norm = cnf_matrix_abs.astype('float') / cnf_matrix_abs.sum(axis=1)[:, np.newaxis]
    plot(cnf_matrix_abs, 1, fmt='d')
    plot(cnf_matrix_norm, 2, title="Normalized " + title, fmt='.2f')
    
def random_listening(data, labels, pred=-1, size=5, classes=["FR", "EN", "DE"]):
    pred = np.zeros((len(data), len(classes)))
    choice = np.random.choice(len(data), size)
    for i in choice:
        sample = data[i]
        p = np.argmax(pred[i], axis=0)
        l = np.argmax(labels[i], axis=0)
        
        print("{}  Label: {}({}),    Pred: {}({})".format(p==l, classes[l], l, classes[p], p), end='')
        ipd.display(ipd.Audio(sample, rate=16000,))
    
    