## Convnet 2d to 1d

#### Characteristics

- MelSpect +  2 CONV2D + 3 CONV1D + FC
- idea: first process frequencies to phonemes and then process timeseries with conv1d

#### Experiments 

(Later experiments are generally performed with best options so far)

| Question                        | Experiments                                                  | Result [ValAcc, ValLoss]        |
| ------------------------------- | ------------------------------------------------------------ | ------------------------------- |
| Is it even possible (workflow)? | [7de](https://www.comet.ml/jotron/conv-2d-to-1d/7de660f8f9764eefac4f4c5abf9a31cd), [c74](https://www.comet.ml/jotron/conv-2d-to-1d/c74f3ed0705a46c7baed87abef516f8c), [f69](https://www.comet.ml/jotron/conv-2d-to-1d/f693c47ce04f409bb1215a11b31c43b7), [026](https://www.comet.ml/jotron/conv-2d-to-1d/026931aee46c4806b9629c5bb6bf1c4a), [0a7](https://www.comet.ml/jotron/conv-2d-to-1d/0a79e5b451e74eecb11bd0e1edf9b5e9), [1c0](https://www.comet.ml/jotron/conv-2d-to-1d/1c0c81eef3094a0e82d712a68db1691d) | 33% ): → was because of decibel |
| repeat                          | [e5b](https://www.comet.ml/jotron/conv-2d-to-1d/e5b88a8649c649828b5cc4246e42bbfc), [30a](https://www.comet.ml/jotron/conv-2d-to-1d/30ad6d24de634ca188818b509fa485fa/code), [98c](https://www.comet.ml/jotron/conv-2d-to-1d/98c2cbcba59946e99843b61a42bc1b04), [52e](https://www.comet.ml/jotron/conv-2d-to-1d/52e2be55b9b34084969fc6df8f770a98), [c1a](https://www.comet.ml/jotron/conv-2d-to-1d/c1aaa7fd207a49b1a752c320e58caa53), [0bc](https://www.comet.ml/jotron/conv-2d-to-1d/0bca92db40124707ad3d72f1ff32acef), [df8](https://www.comet.ml/jotron/conv-2d-to-1d/df8f204e536249b2891ee0c2fece419a) | 90.4%, 0.26                     |
| SeparableConv?                  | [337](https://www.comet.ml/jotron/conv-2d-to-1d/337516459df14cf18365b314a248d07b), [377](https://www.comet.ml/jotron/conv-2d-to-1d/3779e8c09ada40caa9739cacbe0c7800) | too slow to train?              |

