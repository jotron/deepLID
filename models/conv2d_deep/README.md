## Deep Convnets

### Characteristics

- Melspect + Convnet-Architecture

#### Experiments 

| Topcoder_net         | Experiments                                                  | Result [ValAcc]  |
| -------------------- | ------------------------------------------------------------ | ---------------- |
| base                 | [e78](https://www.comet.ml/jotron/conv2d-deep/e78caf2a66774fdf9f242ade1a6f864e), [f9b](https://www.comet.ml/jotron/conv2d-deep/f9b9f73e4acb40c6ae1dfa107568828a/metrics), [b9f](https://www.comet.ml/jotron/conv2d-deep/b9fddc55fe634720a20f776fa476648d/metrics), [0f4](https://www.comet.ml/jotron/conv2d-deep/0f4aa95a456c4c029a9d16fa8d48e5a8/metrics) | 88%              |
| batch_normalizatioin | [297](https://www.comet.ml/jotron/conv2d-deep/2971a9c6d2d84f849caf5e943631674e/code), [598](https://www.comet.ml/jotron/conv2d-deep/59896bf37c04414b9c1ecf650fa6a3b2/metrics) | 86.5% but faster |
| SeparableConv        | [c49](https://www.comet.ml/jotron/conv2d-deep/c49b442bc6084f64a9ad991427966ddd/code) | 59%              |
| AveragePooling       | [4d6](https://www.comet.ml/jotron/conv2d-deep/4d666e5ded1a473e9f55b3643023008a) | 83%              |

| Resnet | Experiments                                                  | Result [ValAcc]                         |
| ------ | ------------------------------------------------------------ | --------------------------------------- |
| base   | [98a](https://www.comet.ml/jotron/conv2d-deep/98a709d7ac064f56830aad146e1f7245/metrics) | 78%, overfits → needs data augmentation |

| Mobilenet | Experiments | Result [ValAcc] |
| --------- | ----------- | --------------- |
| base      | alpha=0.25  | 91% (Overfits)  |

