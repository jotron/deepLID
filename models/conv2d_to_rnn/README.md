## Convnet 2d to rnn

#### Characteristics

- MelSpect +  CN Feature Extractor + RNN
- idea: first process frequencies to phonemes and then process timeseries with RNN

#### Early Experiments 

(Later experiments are generally performed with best options so far)

| Simple                                  | Experiments                                                  | Result [ValAcc, ValLoss] |
| --------------------------------------- | ------------------------------------------------------------ | ------------------------ |
| basis                                   | [64b](https://www.comet.ml/jotron/conv-2d-to-rnn/64b617767f6240ecad4df4ca4a6aae89/metrics), [e42](https://www.comet.ml/jotron/conv-2d-to-rnn/e4276d5ea66c4b5d8df584afef625a11), [d17](https://www.comet.ml/jotron/conv-2d-to-rnn/d174d29ed9044791bfad1bbc4a93bbf8/metrics), [988](https://www.comet.ml/jotron/conv-2d-to-rnn/988f0133eb7f4ceca42f87772d7435c0/metrics), [58e](https://www.comet.ml/jotron/conv-2d-to-rnn/58e8a92589314b1d9afce6b153c30c30), [f52](https://www.comet.ml/jotron/conv-2d-to-rnn/f52d120e8d6b4adcbb4b9e79718db67f/code) | 88%                      |
| dropout                                 | [f52](https://www.comet.ml/jotron/conv-2d-to-rnn/f52d120e8d6b4adcbb4b9e79718db67f/code), [d97](https://www.comet.ml/jotron/conv-2d-to-rnn/d97afc212b394b68b11e7c94ec97cc51) | 92.2%                    |
| wider+regularized(1e-4)+strange_reshape | [4b9](https://www.comet.ml/jotron/conv-2d-to-rnn/4b98a37f69fd45ea95bd2f48d79dec86) | 92.9%                    |
| wider+regularized(1e-3)+correct_reshape | [63b](https://www.comet.ml/jotron/conv-2d-to-rnn/63b8c66c0128416891efddb44ab2a3f5) | 94%                      |
| smaller bidirectional                   | [53e](https://www.comet.ml/jotron/conv-2d-to-rnn/53ea59cbb3134accb8a18f743e42a86c) | 92% (slow)               |
| share weights                           | [959](https://www.comet.ml/jotron/conv-2d-to-rnn/9596ed5dde31438893c1a36388f5948f/code) | 91.5%                    |

| Model 2             | Experiments                                                  | Result [ValAcc, ValLoss] |
| ------------------- | ------------------------------------------------------------ | ------------------------ |
| basis               | [a54](https://www.comet.ml/jotron/conv-2d-to-rnn/a548bcd7891547bbb28adc9fbb06335f/code) | 91%                      |
| regularized+dropout | [dde](https://www.comet.ml/jotron/conv-2d-to-rnn/ddefff12a6254356abb6eb93265f4d77/metrics) | 90.4%                    |

| Model 3     | Experiments                                                  | Result [ValAcc, ValLoss] |
| ----------- | ------------------------------------------------------------ | ------------------------ |
| MobileNetV2 | [28f](https://www.comet.ml/jotron/conv-2d-to-rnn/28fab071209b494fb4ce272e8ca3a235) | 92.7% (slow)             |

