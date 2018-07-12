## List of models

A list of hyperparamets can be found [here](potential_hyperparameters.md).

- #### berlin_net_mel_bn: *Tom Herold, Thomas Werkmeister Paper; Shallow Architecture* with BN

  Activations = ReLU
  Loss = categorical_crossentropy
  Input = Mel-filter images

  1. CONV(kernel=6x6, stride=1)  + MAXPOOL(kernel=2x2, stride=2) + BN
  2. CONV(kernel=6x6, stride=1) + MAXPOOL(kernel=2x2, stride=2) + BN
  3. CONV(kernel=6x6, stride=1) + MAXPOOL(kernel=2x2, stride=2) + BN
  4. FC(1024)
  5. FC(3, act=softmax)

- 

