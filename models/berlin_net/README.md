## Berlin_net_shallow

#### Characteristics

- MelSpect + 3 CONV + 2 FC
- heavily inspired by [iLID](https://github.com/twerkmeister/iLID/blob/master/Deep%20Audio%20Paper%20Thomas%20Werkmeister%2C%20Tom%20Herold.pdf)

#### Experiments

| Question                            | Experiments                                                  | Result [ValAcc, ValLoss]      |
| ----------------------------------- | ------------------------------------------------------------ | ----------------------------- |
| Same Accuracy with same Parameters? | [Exp1](https://www.comet.ml/jotron/berlinnetmelbn/6ca1a10554844b6b8b7a21e1d82c46c2), [Exp2](https://www.comet.ml/jotron/berlinnetmelbn/f8af7798be0c4201a912a027a1ecea1e), [Exp3](https://www.comet.ml/jotron/berlinnetmelbn/40b5f03a9b8d449b905d64386700ed20), [Exp4](https://www.comet.ml/jotron/berlinnetmelbn/6accc8b7fd574b1d8d2491bdbe12b998) | → better set np.random.seed() |
| Starting Point                      | [Exp](https://www.comet.ml/jotron/berlinnetmelbn/6accc8b7fd574b1d8d2491bdbe12b998) | 89%, 0.335                    |
| Selu Activations?                   | [Exp](https://www.comet.ml/jotron/berlinnetmelbn/0ee5f7ec57e34dcca86f657bb9212508) | 33%, 10.744                   |
| Batch normalisation?                | [Exp](https://www.comet.ml/jotron/berlinnetmelbn/d0f0ee3c8c4c4bb7b88ef183772088ab) | 88%, 0.505                    |
| No Pooling Stride?                  |                                                              |                               |
| Different Kernel Size?              |                                                              |                               |

