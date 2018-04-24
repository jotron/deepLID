# deepLID

## Problem description

*as in 'Deep learning with Python' Chapter 4.5*

**Input_data:** Audio files from Voxforge, Youtube etc.

**Target:** Language label, either german, french or english

→ **Type:** Multiclass classification

## Repo Structure

- **/data**
  - Script to download training data from Voxforge
  - Jupyter notebook with data analysis
- **/preprocessing**
  - Description of methods, see [preprocessing/README](preprocessing/README.md)
  - Scripts to preprocess data
- **/models**
  - Description of used models, see [models/README](models/README.md)
  - **Jupyter notebooks with training/evaluation data**
  - Saved models

## Dataset 

Number of *.wav* files per languange in datasets.

|              | English | German | French |
| ------------ | ------- | ------ | ------ |
| **Voxforge** | 86'616  | 24'100 | 22'430 |

##### To download files 

```python data/download_data.py <language>```

## Running the Webserver

```bash
# install flask
cd web-server
export FLASK_APP=webserver.py
flask run
```

