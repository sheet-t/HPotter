import unittest
import master_db
import hpotter.tables as tables
from hpotter.env import write_db


class TestMasterDB(unittest.TestCase):
    def setUp(self):
        pass

    def test_empty_database(self):
        master = master_db.MasterDB()

        # Add to the connection table
        connection = tables.Connections(
            sourceIP='127.0.0.1',
            sourcePort=35431,
            destPort=23,
            proto=6)
        write_db(connection)

        # Add to the credentials table
        creds = tables.Credentials(username='root', password='lol_wut?', connection=connection)
        write_db(creds)

        # Add to the shell commands table
        command = 'cat /etc/shadow'
        shell = tables.ShellCommands(command=command, connection=connection)
        write_db(shell)

        # Add to the http commands table
        request = 'GET / HTTP/1.1\r\nHost: localhost\r\nUser-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; ' \
                  'rv:68.0) Gecko/20100101 Firefox/68.0\r\nAccept: text/html,application/xhtml+xml,application/xml' \
                  ';q=0.9,*/*;q=0.8\r\nAccept-Language: en-US,en;q=0.5\r\nAccept-Encoding: gzip, deflate\r\n' \
                  'Connection: keep-alive\r\nUpgrade-Insecure-Requests: 1\r\n\r\nGET /favicon.ico HTTP/1.1\r\n' \
                  'Host: localhost\r\nUser-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:68.0) ' \
                  'Gecko/20100101 Firefox/68.0\r\nAccept: image/webp,*/*\r\nAccept-Language: en-US,en;q=0.5' \
                  '\r\nAccept-Encoding: gzip, deflate\r\nConnection: keep-alive\r\n\r\n'
        http = tables.HTTPCommands(request=request, connection=connection)
        write_db(http)

        # Add to the SQL table
        request = '" OR 1=1'
        sql = tables.SQL(request=request, connection=connection)
        write_db(sql)

        table_list = [tables.Connections, tables.HTTPCommands, tables.ShellCommands, tables.Credentials, tables.SQL]
        for table in table_list:
            # Verify there is data in the table before deleting
            self.assertGreaterEqual(len(master.session.query(table).all()), 1)

        master.empty_database()
        for table in table_list:
            # Verify there is no data in the table after deleting
            self.assertEqual(len(master.session.query(table).all()), 0)


