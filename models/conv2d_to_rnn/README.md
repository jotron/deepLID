## Convnet 2d to rnn

#### Characteristics

- MelSpect +  CN Feature Extractor + RNN
- idea: first process frequencies to phonemes and then process timeseries with RNN

#### Experiments 

(Later experiments are generally performed with best options so far)

| Simple  | Experiments                                                  | Result [ValAcc, ValLoss] |
| ------- | ------------------------------------------------------------ | ------------------------ |
| basis   | [64b](https://www.comet.ml/jotron/conv-2d-to-rnn/64b617767f6240ecad4df4ca4a6aae89/metrics), [e42](https://www.comet.ml/jotron/conv-2d-to-rnn/e4276d5ea66c4b5d8df584afef625a11), [d17](https://www.comet.ml/jotron/conv-2d-to-rnn/d174d29ed9044791bfad1bbc4a93bbf8/metrics), [988](https://www.comet.ml/jotron/conv-2d-to-rnn/988f0133eb7f4ceca42f87772d7435c0/metrics), [58e](https://www.comet.ml/jotron/conv-2d-to-rnn/58e8a92589314b1d9afce6b153c30c30), [f52](https://www.comet.ml/jotron/conv-2d-to-rnn/f52d120e8d6b4adcbb4b9e79718db67f/code) | 88%                      |
| dropout | [f52](https://www.comet.ml/jotron/conv-2d-to-rnn/f52d120e8d6b4adcbb4b9e79718db67f/code), [d97](https://www.comet.ml/jotron/conv-2d-to-rnn/d97afc212b394b68b11e7c94ec97cc51) | 92.2%                    |

| Model 2 | Experiments | Result [ValAcc, ValLoss] |
| ------- | ----------- | ------------------------ |
| basis   |             |                          |

| Model 3 | Experiments | Result [ValAcc, ValLoss] |
| ------- | ----------- | ------------------------ |
| basis   |             |                          |

