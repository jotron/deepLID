# deepLID

Online Demo at *https://jo.guru.xxx/deeplid*

## Problem description

*as in 'Deep learning with Python' Chapter 4.5*

**Input_data:** Audio files from Voxforge, Youtube etc.

**Target:** Language label, either german, french or english

→ **Type:** Multiclass classification

## Repo Structure

- **/data**
  - see [data/README](data/README.md)
  - Scripts to download data
- **/preprocessing**
  - see [preprocessing/README](preprocessing/README.md)
  - Scripts to preprocess data
  - Jupyter notebook with data analysis
- **/models**
  - Description of used models, see [models/README](models/README.md)
  - **Jupyter notebooks with training/evaluation data**
  - Saved models


## Running the Webserver

```bash
git clone https://github.com/jotron/deepLID.git
cd deepLID

pip install pipenv
pipenv install

pipenv run python web-server/webserver.py
```

