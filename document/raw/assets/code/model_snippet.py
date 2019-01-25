# Importieren von Bibliotheken
from keras import models, layers
from kapre.time_frequency import Melspectrogram

# Laden von Daten:
# DataFeed ist eine selbst geschriebene Klasse zum selektiven Laden von Daten.
data_path = '../path/to/data'

# Laden von 50'000 Aufnahmen von Voxforge und Youtube
train_data, train_labels = DataFeed.Dataset.create(data_path,
                           ['train/voxforge','train/youtube'],
                           num=50000)

# Laden von 10'000 Aufnahmen von Voxforge und Youtube
val_data, val_labels = DataFeed.Dataset.create(data_path,
                       ['val/youtube', 'val/voxforge'],
                       num=10000, shuffle=True)

# Definieren des Modells
architecture = [
    Melspectrogram(n_dft=512, input_shape=(1, 5 * 16000,),
                   padding='same', sr=16000, n_mels=28,
                   fmin=0.0, fmax=10000),
    layers.Conv2D(64, (3, 6), activation='relu'),
    layers.MaxPooling2D((2, 2)),
    layers.Conv2D(64, (3, 6), activation='relu'),
    layers.MaxPooling2D((2, 2)),
    layers.Conv2D(128, (3, 6), activation='relu'),
    layers.MaxPooling2D((2, 2)),
    layers.Flatten(),
    layers.Dense(1024, activation='relu'),
    layers.Dense(3, activation='softmax')
]

# Zusammenbauen des Modells
model = models.Sequential(architecture)

# Defninieren des Traininsprozesses: z.b Optimierer, Verlustfunktion
model.compile(optimizer='Rmsprop',
              metrics=['accuracy'],
              loss='categorical_crossentropy')

# Trainieren des Modells
model.fit(train_data, train_labels,
          batch_size=64, # Mit 64 Eingaben auf einmal tranieren (effizienter)
          epochs=9, # Neun mal mit allen Daten trainieren
          validation_data=(val_data, val_labels))
