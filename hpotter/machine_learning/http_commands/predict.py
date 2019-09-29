import numpy as np

from hpotter.machine_learning.http_commands.helpers.parser import Data
from hpotter.machine_learning.http_commands.helpers.vocabulary import Vocabulary
from hpotter.machine_learning.http_commands.model import BASE_PATH
from hpotter.machine_learning.http_commands.predictor import Predictor

d = Data(path=BASE_PATH + 'data/benign_requests.txt')
predictor = Predictor(checkpoint_path=BASE_PATH + "checkpoints/", std_factor=49.0, vocab=Vocabulary())
validation_generator = d.validation_gen()
predictor.set_threshold(data_generator=validation_generator)

test_generator = d.test_gen()
valid_predictions, valid_losses = predictor.predict(data_generator=test_generator, visual=False)
fps = np.sum(valid_predictions)
num_samples = len(valid_predictions)
print("\r\nNumber of False Positives: ", fps)
print("Number of Samples: ", num_samples)
print("False Positive Rate: ", (fps / num_samples))

predicted_data = Data(path=BASE_PATH + 'data/anomalous_requests.txt', predict=True)
predicted_generator = predicted_data.predict_gen()
anomalous_predictions, anomaly_losses = predictor.predict(data_generator=predicted_generator)
tps = np.sum(anomalous_predictions)
num_samples = len(anomalous_predictions)
print("\r\nNumber of True Positives: ", tps)
print("Number of Samples: ", num_samples)
print("True Positive Rate: ", (tps / num_samples))

print("\r\n\r\nLogits: ", predictor.logits)
