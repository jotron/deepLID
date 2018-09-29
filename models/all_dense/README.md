## All_dense_baseline

#### Characteristics

- only dense layers
- Best Model: 5 x [FC 256, Dropout 0.5, l2 0.0001, 'relu'] + [FC 3, softmax]

#### Experiments

| Question                                                     | Exp's                                                        | Result                                                       |
| ------------------------------------------------------------ | ------------------------------------------------------------ | ------------------------------------------------------------ |
| Starting Point (Mel-Spectrogam + 6 layers with 3x 512, 3x 1024) | [e48](https://www.comet.ml/jotron/all-dense/e4810808c2794e7cba47952f4a93c4b1/code) | 33%                                                          |
| No Mel-Spectrogram?                                          | [3d5](https://www.comet.ml/jotron/all-dense/3d58550004ee4833b35c7816e1e959ae/code) | 39%                                                          |
| Use all data + deeper architecture + Dropout                 | [96f](https://www.comet.ml/jotron/all-dense/96fd89020bbb46f3b7d680335a89581b/code) | 32% (acc=100%)                                               |
| Why is acc 100!?                                             | [f95](https://www.comet.ml/jotron/all-dense/f9546cfe1d7c44d3958c0810b33dd639/code), [70e](https://www.comet.ml/jotron/all-dense/70eefae7e6c0406fa413e8a9194bfcea), [a38](https://www.comet.ml/jotron/all-dense/a38845ff58ef4b1999d90393c7b1ad04), [499](https://www.comet.ml/jotron/all-dense/4990e74661b1423aa3d308a4192c1c2f),  [934](https://www.comet.ml/jotron/all-dense/9344756542114f2e9265e25c64eca8f6), [fb7](https://www.comet.ml/jotron/all-dense/fb75ce747d784e9998c4a0fc5adefee2), [502](https://www.comet.ml/jotron/all-dense/50250bebc5c44bf0b07e8e991c2e2963) | BUG! (in Datafeed, solved)                                   |
| How can model 502 be so good? (acc=99% with 2 layers)        | [461](https://www.comet.ml/jotron/all-dense/46147f64af98457dae79142a804fb987) | it already has a lot of weights (80000 * 128), val_acc = 41% |
| Dropout?                                                     | [566](https://www.comet.ml/jotron/all-dense/566ea10c7a7d41398e06c391462f135f), [5be](https://www.comet.ml/jotron/all-dense/5be408df9a9d4c53a5f5faf1f57550dd) | 42.8%                                                        |
| Regularization?                                              | [fae](https://www.comet.ml/jotron/all-dense/faeac593cf1243789bdbbcc6fd08fadb), [9f2](https://www.comet.ml/jotron/all-dense/9f263d47c6844da39135fc9bcb761e67), [e04](https://www.comet.ml/jotron/all-dense/e0454cc07dd24e779ccb9e2c4225b0a2) | helpful but needs more layers                                |
| More Layers?*                                                | [be0](https://www.comet.ml/jotron/all-dense/be07626ad5cf4854aceae0045a4f6c1a), [57a](https://www.comet.ml/jotron/all-dense/57a3364dba584079b6ed239974983713), [3b5](https://www.comet.ml/jotron/all-dense/3b501aceb4154ab896253d4944830145), [5aa](https://www.comet.ml/jotron/all-dense/5aa5a8171c0348379052a4f9b857c384), [db2](https://www.comet.ml/jotron/all-dense/db2669803e3d4b4c9beceb2f27b57ae7), [856](https://www.comet.ml/jotron/all-dense/85682770052343bcaf94b4508ae6af99), [4e0](https://www.comet.ml/jotron/all-dense/4e0848128a3d4c768c8e967114a678be), [8da](https://www.comet.ml/jotron/all-dense/8dab0fa7cf1d4819b78203fdf0f4b5ed), [55a](https://www.comet.ml/jotron/all-dense/55a85ab683054ed7b39e35fd1316a76f) | 45%                                                          |

##### *Workflow:

1. add layers
   - overfitting? → regularize
   - not better? → make bigger layers
2. start again