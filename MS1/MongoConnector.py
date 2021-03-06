__author__ = 'Nimrod Ben-Em'
from pymongo import MongoClient
import logging


class CMongoConnector(object):
    def __init__(self):
        logging.debug('CMongoConnector::Init MongoConnector Class')
        self.mongo_client = None
        self.db = None
        self.db_collection = None
        self.connection_status = False

    def init_connection(self, ip, port, user=None, password=None):
        # connect to DB server
        logging.debug('CMongoConnector::Connect to MongoDB at:%s:%s' % (ip, port))
        self.mongo_client = MongoClient(ip, port)
        if self.mongo_client is None:
            logging.error('CMongoConnector::Failed to connect DB Server...')
            return False

        #Authenticate to Server
        if (user is not None) and (password is not None):
            logging.debug('CMongoConnector::Authenticating...')
            auth_succeeded = self.mongo_client.ClouDNS.authenticate(user, password)
            if auth_succeeded is False:
                logging.error('CMongoConnector::Authentication Failed...')
                return False

        # Select ClouDNS DB
        logging.debug('CMongoConnector::Get ClouDNS DB...')
        self.db = self.mongo_client['ClouDNS']
        if self.db is None:
            logging.error('CMongoConnector::Failed to get DB ClouDNS')
            return False

        # Select DNS Queries Collection
        logging.debug('CMongoConnector::Get ClouDNS_Queries Collection...')
        self.db_collection = self.db['ClouDNS_Queries']
        if self.db_collection is None:
            logging.error('CMongoConnector::Failed to get DB Collection ClouDNS_Queries')
            return False

        self.connection_status = True
        return self.connection_status

    def insert_dns_query(self, dns_query):
        logging.debug('CMongoConnector::Inserting: %s' % dns_query)
        query_id = self.db_collection.insert(dns_query)
        return query_id

    def is_alive(self):
        return self.mongo_client.alive()
