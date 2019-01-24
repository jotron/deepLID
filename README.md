# deepLID

Language identification [French, English, German] with deep learning.

Online Demo at *https://jo.guru.xxx/deeplid*

## Repo Structure

- **/data**
  - see [data/README](data/README.md)
  - Scripts to download data
- **/document**
  - Latex source files
- **/models**
  - see [models/README](models/README.md)
  - Different Keras models
  - Jupyter notebooks with training/evaluation data
  - Saved models
- **/preprocessing**
  - see [preprocessing/README](preprocessing/README.md)
  - Scripts to preprocess data
  - Jupyter notebooks with data analysis
- **/webserver**
  - see [preprocessing/README](web-server/README.md)
  - Minimalistic Flask Webserver


## Running the Webserver

```bash
git clone https://github.com/jotron/deepLID.git
cd deepLID

pip install pipenv
pipenv install

pipenv run python web-server/webserver.py
```

