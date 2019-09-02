import configparser
import itertools
import boto3
from hpotter.tables import Connections, HTTPCommands, ShellCommands, Credentials, SQL
from hpotter.env import session


class MasterDB:
    """
    Input: The SQLite 'main.db' file
    Output: True if 'main.db' is successfully written to AWS postgeSQL, False otherwise
    """

    def __init__(self):
        self.session = session
        self.config = configparser.ConfigParser()
        self.config.read('.aws/credentials.ini')
        self.access_key = self.config['default']['aws_access_key_id']
        self.secret_key = self.config['default']['aws_secret_access_key']
        self.session_token = self.config['default']['aws_session_token']

        self.client = boto3.client('rds-data', 'us-east-1', aws_access_key_id=self.access_key,
                                   aws_secret_access_key=self.secret_key,
                                   aws_session_token=self.session_token)

    def upload_connections(self):
        pass

    def upload_httpcommands(self):
        pass

    def upload_shellcommands(self):
        pass

    def upload_credentials(self):
        pass

    def upload_sql(self):
        pass

    def empty_database(self):
        table_list = [Connections, HTTPCommands, ShellCommands, Credentials, SQL]
        for table in table_list:
            for row in self.session.query(table).all():
                self.session.delete(row)
        self.session.commit()
