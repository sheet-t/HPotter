# HPotter Requests Anomaly Detection
A machine learning algorithm that detects and highlights anomalous requests made against the HPotter honey pot data. 
 
## Training Data Sets
The training data is held in one of the following locations, depending on the type of data (http, shell, or sql):
1. `HPotter/hpotter-app/machine_learning/http_commands/data.tar.gz`
2. `HPotter/hpotter-app/machine_learning/shell_commands/data.tar.gz`
3. `HPotter/hpotter-app/machine_learning/sql_commands/data.tar.gz`

To extract a particular data directory, do one of the following from the parent directory of `HPotter`:
1. `tar -xzvf HPotter/hpotter-app/machine_learning/http_commands/data.tar.gz 
-C HPotter/hpotter-app/machine_learning/http_commands/`
2. `tar -xzvf HPotter/hpotter-app/machine_learning/shell_commands/data.tar.gz 
-C HPotter/hpotter-app/machine_learning/shell_commands/`
3. `tar -xzvf HPotter/hpotter-app/machine_learning/sql_commands/data.tar.gz 
-C HPotter/hpotter-app/machine_learning/sql_commands/`

The data found in these directories has been manually labelled as either benign (data in the benign_requests.txt file)
or nefarious (data in the anomalous_requests.txt file).

## Training
To ensure the necessary packages are installed, run the following command from the `HPotter/hpotter-server` directory:

    pip3 install -r requirements.txt 
 
To train the machine learning algorithm itself, run one of the following commands from the `HPotter/hpotter-app` 
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
This model implements a particular class of Recurrent Neural Networks (RNNs) called a Long Short Term Memory (LSTM) 
network. LSTM networks use a sequence to sequence encoder/decoder of character embeddings (n-grams mapped to integers), 
and are often used for Natural Language Processing (NLP) and classification against text based protocols. Each 
character is encoded into an integer value then fed into the algorithm, where it attempts to predict/reproduce the 
input and anything that does not match is then considered an anomaly. Below demonstrates a high level architecture of 
the algorithm:

![Screen Shot 2019-09-23 at 11 49 45 AM](https://user-images.githubusercontent.com/32188816/65449483-52a9d300-ddf8-11e9-8af0-4d2840a9e167.png)

The model first needs to have start and finish delimiters, which are defined as `<GO>` and `<EOS>`,
respectively. The model will need to compute probabilities of letter occurrences, which is why we need to create
character embeddings that map characters to numeric values. The embedded mapping is defined in 
`HPotter/hpotter-app/machine_learning/general/helpers/vocab.json`. There are also the `<PAD>` and `<UNK>` symbols which are defined to pad short inputs to equal length and to embed unknown characters, respectively.

The model workflow is defined by the following steps:

1. `<GO>` delimiter is appended to the start of each individual payload, and model processing begins on the character 
immediately after the `<GO>` delimiter
2. The model computes the probability of seeing each subsequent character, remembering what characters it has already
processed (hence the 'Long Short Term Memory' name). In the diagram above, the model will compute `P(P)`, or the 
probability of a payload starting with the letter `P`, then given that the model has just seen a `P`, it calculates the
probability of a `P` being followed by an `O`, then an `O` followed by an `S`, and so on until the end of a single
payload is reached.
3. If the resulting probability of seeing a particular letter is low, that indicates a malicious/unexpected character
has been encountered and is likely part of a nefarious payload. 
4. The resulting probabilities for each letter in a single payload are summed up, then compared against a threshold, 
and the prediction confidence, `α`, is calculated from our `100 * (1 - α)` confidence interval. If the model's 
prediction falls within the 91% confidence interval, i.e. `α < 0.09`, the datum sample is deemed as nefarious, 
otherwise the datum sample is considered benign. 

## General Directory Structure
The machine learning algorithm itself lives in the `Hpotter/hpotter-app/machine-learning/general/`
directory, which contains the following files:
* learn.py
    * A script that imports all of the necessary modules and initiates the machine learning algorithm
    training process.
    
    * Hyperparameters (for fine tuning the model's performance)
        * **num_layers** - defines the depth of the neural network (number of layers between the input and output 
        layers)
        * **hidden_size** - defines the number of input neurons to each hidden layer
        * **embedding_size** - defines the size of the embedding matrix (a matrix that maps words into a real-valued 
        matrix)
        * **batch_size** - defines the size of the data chunks fed into the learning algorithm as input
        * **dropout** - defines the amount of input neurons to ignore (crucial to prevent over-fitting) and 
        helps prevent interdependent learning throughout the data
        
    * Other important variables
        * **epochs** - defines the number of times an entire set of data is forward and backward propagated throughout 
        the network
        * **steps** - defines the number of batches needed to complete one epoch
        
* model.py
    * Implementation of the Long Short Term Memory (LSTM) neural network using Tensorflow, and all of the necessary 
    operations used during training.

* trainer.py
    * A script that iterates over the data and feeds it into the model defined in `model.py` until the minimum 
    loss specified is satisfied using Tensorflow. 
    * Hyperparameters
        * **min_loss** - defines the minimum amount of error allowed on a prediction

* predictor.py    
    * Defines a `Predictor` class that utilizes a trained machine learning model read in from one of the `checkpoints`
     directories and prediction data. The `Predictor` class will evaluate and grade the model's performance against 
     a threshold. 
    
* predict.py
    * A simple script that makes use of the `predictor.py` file to make predictions using the data given to it. This
    was written to provide an interface between the front end to provide a data analytics display.
    * The script will read in data from a JSON file provided from the front end, and write the results to a JSON file
    for later parsing by the front end. 

## Helpers Directory Structure
There are a couple of files written to help the with machine learning process's basic functionality
such as reading in data and parsing out payloads, serializing text to numbers, and creating data
generators. This functionality is implemented in the following files:
* helper.py
    * Defines functions for parsing and extracting the actual payloads out of the data files,
    and providing generators containing that data.
    * Since our embeddings need to be a specific length, there is a `padding` function defined 
    to meet that specific length when data is short.
    * Defines functions to help with printing the training progress and creating a checkpoints 
    directory if one doesn't already exist so that the `trainer.py` and `learn.py` scripts can
    write their progress to a saved checkpoint file during training. 

* parser.py
    * Defines classes for reading in the data and provides an interface between the data and the
    machine learning algorithm.
    * Defines functions for producing data generators as well as determining train/test/validation
    data splits.
    
* vocab.json
    * A static mapping of characters to integers.

* vocabulary.py
    * A simple script that translates and serializes characters to integers and integers to 
    characters, using the `vocab.json` file.
    
