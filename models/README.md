## List of models

A list of hyperparamets can be found [here](potential_hyperparameters.md).

Testset and valset are a mix of youtube and voxforge data.

- #### berlin_net (test_acc=95.1%)

  inspired from *Tom Herold, Thomas Werkmeister Paper; Shallow Architecture* with BN
  
- #### cGAN (failed)
  
  tried to implement: https://pdfs.semanticscholar.org/0505/12496557c439a9b31459b457ea1a57ab7208.pdf

- #### dense_baseline (val_acc=44.2%)

  5 x [FC 256, Dropout 0.5, l2 0.0001, relu] + [FC 3, softmax]
  
- #### conv1d (test_acc=86.9%)

  16, 32, 32, 64, 64, 64, Dense 512
  -> depreciated

- #### conv2d_to_conv1d (val_acc=90%)

  2 x [Conv2D 128 relu + MaxPooling ] + 3 x [Conv1D 128 relu + MaxPooling ]
  → depreciated: a conv2d model should be able to learn just as well if not better

- #### conv2d_deep (test_acc=86.9%)

  (multiple architectures, see in README)
  idea: using dCNN like AlexNet, VGG and Resnet for LID
  → overfits too much

- #### conv2d_to_rnn (test_acc=94.7%)

  (multiple architectures, see in README)
  idea: using dCNN like AlexNet, VGG and Resnet for feature extraction, than a RNN for temporal analysis


