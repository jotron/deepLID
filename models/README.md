## List of models

A list of hyperparamets can be found [here](potential_hyperparameters.md).

- #### berlin_net (val_acc=92%)

  inspired from *Tom Herold, Thomas Werkmeister Paper; Shallow Architecture* with BN

- #### dense_baseline (val_acc=45%)

  5 x [FC 256, Dropout 0.5, l2 0.0001, relu] + [FC 3, softmax]

- #### conv2d_to_conv1d (val_acc=90%)

  2 x [Conv2D 128 relu + MaxPooling ] + 3 x [Conv1D 128 relu + MaxPooling ]
  → depreciated: a conv2d model should be able to learn just as well if not better

- #### conv2d_deep (val_acc=87%)

  (multiple architectures, see in README)
  idea: using dCNN like AlexNet, VGG and Resnet for LID
  → overfits too much

- #### conv2d_to_rnn (val_acc=92.2%)

  (multiple architectures, see in README)
  idea: using dCNN like AlexNet, VGG and Resnet for feature extraction, than a RNN for temporal analysis


