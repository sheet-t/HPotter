from machine_learning.general.helpers.helper import create_checkpoints_dir
from machine_learning.general.helpers.parser import Data
from machine_learning.general.helpers.vocabulary import Vocabulary
from machine_learning.general.model import Model
from machine_learning.general.trainer import Trainer
import argparse


parser = argparse.ArgumentParser()
parser.add_argument('--data-path', required=True, type=str, help='Path from hpotter-app to a child data directory. \r\n'
                                                                 'EX: --data-path machine_learning/http_commands/data')
args = parser.parse_args()
data_path = args.data_path
checkpoints_path = '/'.join(data_path.split('/')[0:2]) + '/checkpoints/'
create_checkpoints_dir(checkpoints_path)
d = Data(path=data_path + '/benign_requests.txt')
rnn = Model(num_layers=2, hidden_size=64, vocab=Vocabulary(), embedding_size=64)
trainer = Trainer(batch_size=128, checkpoints_path=checkpoints_path, dropout=0.6)
steps = 10 ** 6
epochs = 1000
train_gen = d.train_gen(batch_size=128, num_epochs=epochs)
train_size = d.train_size
trainer.train(model=rnn, training_data=train_gen, training_data_size=train_size,
              num_steps=steps, num_epochs=epochs)
