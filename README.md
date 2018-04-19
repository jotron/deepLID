# deepLID

## Problem description

*as in 'Deep learning with Python' Chapter 4.5*

### Definition

**Input_data: ** Audio files from Voxforge, Youtube etc.

**Target: ** Language, either german, french or english

→ **Type:** Multiclass classification

### Evaluation 

**Measure of success:** Accuracy (using balanced data)

**Evaluation protocol:** Maintaining a hold-out validation set (data is split in training_data, validation_data and test_data)

### Preprocessing

- Spectrograms?
- Normalization?

### Model ideas

**Last-layer activation: ** softmax (useful for probability, sum(last_layer) = 1)

**Loss function:** categorical_crossentropy

## Dataset 

Number of *.wav* files per languange in datasets.

|              | English | German | French |
| ------------ | ------- | ------ | ------ |
| **Voxforge** | 86'616  | 24'100 | 22'430 |

## Running the Webserver

```bash
# install flask
cd web-server
export FLASK_APP=webserver.py
flask run
```

