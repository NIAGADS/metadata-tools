"""
Metadata Validator
"""

from sys import path
path.append('../../ontology_validator/src') # bring src directory into path so can do the import
from ontology_validator import OntologyValidator

class MetadataValidator(object):
    ''' utils for metadata validation '''

    def __init__(self, serviceUrl):
        self._metadata = None
        self._serviceUrl = serviceUrl
        self._dataDictionary = self._setDataDictionary(serviceUrl)
        
    
    def _setDataDictionary(self, serviceUrl):
        self._dataDictionary = OntologyValidator(serviceUrl, "DD")  
    
    def setMetadata(self, metadata):
        self._metadata = metadata
        
    def _getSheet(self, sheet):
        if sheet in self._metadata:
            return self._metadata[sheet]
        else:
            raise KeyError("Sheet " + sheet + " not found in loaded metadata")
        
    def getMetadata(self, sheet):
        if sheet:
            return self._getSheet(sheet)
        else:
            return self._metadata