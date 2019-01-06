# deepLID

Language identification [French, English, German] with deep learning.

Online Demo at *https://jo.guru.xxx/deeplid*

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

