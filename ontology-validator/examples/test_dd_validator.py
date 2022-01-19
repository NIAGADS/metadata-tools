''' test NIAGADS Ontology Validator Script against Data Dictionary '''
from sys import path
path.append('../src/') # bring src directory into path so can do the import
from ontology_validator import OntologyValidator

import json

validator = OntologyValidator('https://beta.niagads.org/genomics', 'DD')

response = validator.query('bile acid', 'CHEBI:3098')

print(json.dumps(response, indent=4, sort_keys=True))