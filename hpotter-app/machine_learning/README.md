# HPotter Requests Anomaly Detection
A machine learning algorithm that detects and highlights anomalous requests made against the HPotter honey pot data. 
 
## Training Datasets
The training data is held in one of the following paths:
1. `HPotter/hpotter-app/machine_learning/http_commands/data.tar.gz`
2. `HPotter/hpotter-app/machine_learning/shell_commands/data.tar.gz`
3. `HPotter/hpotter-app/machine_learning/sql_commands/data.tar.gz`

To extract the data directory, do one of the following:
1. `tar -xzvf HPotter/hpotter-app/machine_learning/http_commands/data.tar.gz -C HPotter/hpotter-app/machine_learning/http_commands/`
2. `tar -xzvf HPotter/hpotter-app/machine_learning/shell_commands/data.tar.gz -C HPotter/hpotter-app/machine_learning/shell_commands/`
3. `tar -xzvf HPotter/hpotter-app/machine_learning/sql_commands/data.tar.gz -C HPotter/hpotter-app/machine_learning/sql_commands/`

## Training
To ensure the necessary packages are installed, do the following command from the `HPotter/hpotter-app` directory:

    pip3 install -r requirements.txt 
 
To train the machine learning algorithm itself, run on of the following commands from the `HPotter/hpotter-app` 
directory to specify the data to train on:

1. `python3 -m machine_learning.general.learn --data-path machine_learning/http_commands/data`
2. `python3 -m machine_learning.general.learn --data-path machine_learning/shell_commands/data`
3. `python3 -m machine_learning.general.learn --data-path machine_learning/sql_commands/data`

## Saved Model
Checkpoints of the model's training progress are saved if adjustments need to be made or for future training/prediction
 purposes. These checkpoints are stored in one of the following directories:
1. `machine_learning/http_commands/checkpoints` 
2. `machine_learning/shell_commands/checkpoints` 
3. `machine_learning/sql_commands/checkpoints` 

## Model
The algorithm used to classify anomalous commands is a Long Short Term Memory (LSTM) Recurrent Neural Network 
(RNN) that uses a sequence to sequence encoder/decoder of character embeddings. Each character is encoded into an 
integer value then fed into the algorithm, where it attempts to predict/reproduce the input and anything that
does not match is then considered an anomaly. Below demonstrates a high level architecture of the algorithm:

![Screen Shot 2019-09-23 at 11 49 45 AM](https://user-images.githubusercontent.com/32188816/65449483-52a9d300-ddf8-11e9-8af0-4d2840a9e167.png)