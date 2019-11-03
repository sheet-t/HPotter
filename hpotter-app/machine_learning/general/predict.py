# import json
#
# import numpy as np
#
# from machine_learning.general.helpers.parser import Data
# from machine_learning.general.helpers.vocabulary import Vocabulary
# from machine_learning.general.predictor import Predictor
#
#
# def predict(json_file, num_samples, path):
#     with open(json_file, 'r') as json_handle, \
#             open(path + '/samples.txt', 'a+') as text_handle:
#         data = json.load(json_handle)
#         start = 'START\r\n----------\r\n'
#         end = '\r\n----------\r\nEND\r\n\r\n'
#         try:
#             for i, request_dict in enumerate(data['data']['requests']):
#                 if i < num_samples:
#                     text_handle.write(start + request_dict['request'].strip() + end)
#                 else:
#                     break
#         except KeyError as err:
#             raise Exception('Key Error, Expecting JSON in the Following Format: ' +
#                             json.dumps({'data': {'requests': [{'id': 'id_goes_here', 'request': 'data_goes_here',
#                                                                'requestType': 'Web/SQL/Shell'}]}}, indent=4))
#
#     predictor = Predictor(checkpoint_path="machine_learning/http_commands/checkpoints/",
#                           std_factor=25.0, vocab=Vocabulary())
#     predicted_data = Data(path='machine_learning/http_commands/data/samples.txt')
#     predicted_generator = predicted_data.predict_gen()
#     anomalous_predictions, anomaly_losses = predictor.predict(data_generator=predicted_generator)
#     tps = np.sum(anomalous_predictions)
#     num_samples = len(anomalous_predictions)
#     print("\r\nNumber of True Positives: ", tps)
#     print("Number of Samples: ", num_samples)
#     print("True Positive Rate: ", (tps / num_samples))
#     print("Prediction Accuracy: %.6f%%" % (tps / num_samples))


import numpy as np

from machine_learning.general.helpers.parser import Data
from machine_learning.general.helpers.vocabulary import Vocabulary
from machine_learning.general.predictor import Predictor

data = Data(path='machine_learning/sql_commands/data/anomalous_requests.txt')
predictor = Predictor(checkpoint_path="machine_learning/sql_commands/checkpoints/",
                      std_factor=0.006, vocab=Vocabulary())
validation_generator = data.validation_gen()
predictor.set_threshold(data_generator=validation_generator)

test_generator = data.test_gen()
valid_predictions, valid_losses = predictor.predict(data_generator=test_generator, visual=False)
fps = np.sum(valid_predictions)
num_samples = len(valid_predictions)
print("\r\nNumber of False Positives: ", fps)
print("Number of Samples: ", num_samples)
print("False Positive Rate: ", (fps / num_samples))

predicted_data = Data(path='machine_learning/sql_commands/data/anomalous_requests.txt')
predicted_generator = predicted_data.predict_gen()
predictor.write_header(title='SQL')
anomalous_predictions, anomaly_losses = predictor.predict(data_generator=predicted_generator,
                                                          num_to_display=1000, visual=True)
tps = np.sum(anomalous_predictions)
num_samples = len(anomalous_predictions)
print("\r\nNumber of True Positives: ", tps)
print("Number of Samples: ", num_samples)
print("True Positive Rate: ", (tps / num_samples))
print("Prediction Accuracy: %.6f%%" % (tps / num_samples))