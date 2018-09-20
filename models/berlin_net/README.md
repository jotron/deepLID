## Berlin_net_shallow

#### Characteristics

- MelSpect + 3 CONV + 2 FC
- heavily inspired by [iLID](https://github.com/twerkmeister/iLID/blob/master/Deep%20Audio%20Paper%20Thomas%20Werkmeister%2C%20Tom%20Herold.pdf)

#### Experiments 

(Later experiments are generally performed with best options so far)

| Question                             | Experiments                                                  | Result [ValAcc, ValLoss]      |
| ------------------------------------ | ------------------------------------------------------------ | ----------------------------- |
| Same Accuracy with same Parameters?  | [Exp1](https://www.comet.ml/jotron/berlinnetmelbn/6ca1a10554844b6b8b7a21e1d82c46c2), [Exp2](https://www.comet.ml/jotron/berlinnetmelbn/f8af7798be0c4201a912a027a1ecea1e), [Exp3](https://www.comet.ml/jotron/berlinnetmelbn/40b5f03a9b8d449b905d64386700ed20), [Exp4](https://www.comet.ml/jotron/berlinnetmelbn/6accc8b7fd574b1d8d2491bdbe12b998) | → better set np.random.seed() |
| Starting Point                       | [1fd](https://www.comet.ml/jotron/berlinnetmelbn/1fd8b827f1a34c308bb50d175a2915d0/metrics) | 89%, 0.335                    |
| Selu Activations?                    | [0ee](https://www.comet.ml/jotron/berlinnetmelbn/0ee5f7ec57e34dcca86f657bb9212508) | not compatible                |
| Batch normalisation?                 | [d0f](https://www.comet.ml/jotron/berlinnetmelbn/d0f0ee3c8c4c4bb7b88ef183772088ab) | 88%, 0.505                    |
| No Pooling Stride?                   | [6ac](https://www.comet.ml/jotron/berlinnetmelbn/6accc8b7fd574b1d8d2491bdbe12b998/code) | 90.3%, 0.303                  |
| Different Depth of Conv Filter Map?  | [cfc](https://www.comet.ml/jotron/berlinnetmelbn/cfc9bd04407f4cdf9c84166de9ea8e95), [69b](https://www.comet.ml/jotron/berlinnetmelbn/69bdad23d4214b838a6f74e9dcad88be) | ~88%, 0.33                    |
| Sigmoid Activations?                 | [50b](https://www.comet.ml/jotron/berlinnetmelbn/50b1d48742c149d185e147616935ea6c) | not compatible                |
| Power Melgram?                       | [3f4](https://www.comet.ml/jotron/berlinnetmelbn/3f4752f0d99e4e73afa781983042747a) | 81%, 0.526                    |
| Decibel Melgram?                     | [b21](https://www.comet.ml/jotron/berlinnetmelbn/b21b6cc1e6e64b2183bc2f6093c85e89) | not compatible?               |
| change ndft?                         | [2eb](https://www.comet.ml/jotron/berlinnetmelbn/2eb8f3c428cb4a7da873e4984fcb6456), [afd](https://www.comet.ml/jotron/berlinnetmelbn/afd3615e04964543810c342bbd9de92f) | 83-88%, 0.44-0.34             |
| Dense neurons? KernelRegularization? | [182](https://www.comet.ml/jotron/berlinnetmelbn/1812c47216ea415881bfcd93b7bfc795/chart), [c6e](https://www.comet.ml/jotron/berlinnetmelbn/c6e63b0a32dc4b4cb4e3e7e39b4121f4), [53e](https://www.comet.ml/jotron/berlinnetmelbn/53e50f5cb2974a14962644d7b2a4ade2/code), [9da](https://www.comet.ml/jotron/berlinnetmelbn/9dab18428d504f40b4cbe3e8d3e692cf/metrics), [691](https://www.comet.ml/jotron/berlinnetmelbn/691c7ceb14bd433ab7b5e47cd4d357e9), [f86](https://www.comet.ml/jotron/berlinnetmelbn/f865b0956d5b4c4090be4667409c309f) | → Best: 1024 without reg.     |
| Only Voxforge Validation?            | [a29](https://www.comet.ml/jotron/berlinnetmelbn/a29686bfcdd34d289bb164f23b8459bc) | 89.5%, 0.295 → as should be   |
|                                      |                                                              |                               |
|                                      |                                                              |                               |

