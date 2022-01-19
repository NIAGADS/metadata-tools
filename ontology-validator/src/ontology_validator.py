'''
utils validating ontology terms against NIAGADS microservices
'''
# pylint: disable=line-too-long,invalid-name,method-hidden

import json
import requests

LOOKUP_TYPES = ['DD', 'OLS', 'HASH']


class OntologyValidator(object):
    ''' utils for ontology validation'''

    def __init__(self, url, lookupType):
        self._requestUrl = url
        self._setType(lookupType)
        self._dict = None

    def setMap(self, map):
        ''' set dict lookup for ontology terms '''
        self._dict = map

    def _setType(self, lookupType):
        ''' set lookup type / throw errror if not exists '''
        if lookupType not in LOOKUP_TYPES:
            raise LookupError("Invalid validation type: " + type)
        self._type = lookupType

    def query(self, term, termSourceId):
        ''' validate term against resource '''
        if self._type == 'DD':
            return self.query_data_dict(term, termSourceId)

        if self._type == 'OLS':
            return self.query_ontology_lookup_service(term, termSourceId)

        if self._type == 'HASH':
            if self._dict is None:
                raise ValueError(
                    "Cannot perform dictionary/hash based validation as dictionary has not been set.")
            return self.query_hash(term, termSourceId)


    def query_ontology_lookup_service(self, term, sourceId):
        ''' query the NIAGADS OLS '''
        raise NotImplementedError("OLS Query not yet implemented")

    def query_hash(self, term, termSourceId):
        ''' query a user-supplied hash '''
        raise NotImplementedError("HASH Query not yet implemented")


    def query_data_dict(self, term, termSourceId):
        ''' query the NIAGADS Data Dictionary '''
        endpoint = "/service/ndd/validate"
        requestUrl = self._requestUrl + endpoint
        payload = {'term': term, 'id': termSourceId}

        try: 
            response = requests.get(requestUrl, params=payload)
            return response.json()

        except requests.exceptions.RequestException as err:  
            raise SystemExit(err)
       