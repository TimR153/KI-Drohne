import os
import tensorflow as tf
from mediapipe_model_maker import gesture_recognizer
assert tf.__version__.startswith('2')

dataset_path = "/Users/timrentrop/Desktop/KI Drohne/Lernjob2-8/trainingData"
print(dataset_path)
labels = []
for i in os.listdir(dataset_path):
    if os.path.isdir(os.path.join(dataset_path, i)):
        if i != ".ipynb_checkpoints":
            labels.append(i)
print(labels)

data = gesture_recognizer.Dataset.from_folder(dirname=dataset_path,
                                              hparams=gesture_recognizer.HandDataPreprocessingParams())
train_data, rest_data = data.split(0.8)
validation_data, test_data = rest_data.split(0.5)

hparams = gesture_recognizer.HParams(export_dir="exported_model")
options = gesture_recognizer.GestureRecognizerOptions(hparams=hparams)
model = gesture_recognizer.GestureRecognizer.create(train_data=train_data,
                                                    validation_data=validation_data,
                                                    options=options)

loss, acc = model.evaluate(test_data, batch_size=1)
print(f"Test loss:{loss}, Test accuracy:{acc}")

model.export_model()
print(os.listdir("exported_model"))
