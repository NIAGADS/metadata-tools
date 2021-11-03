ONTOLOGIES=(cl clo doid efo hancestro hp mondo ncit obi pr uberon ero chebi chmo)

for ONTOLOGY in "${ONTOLOGIES[@]}"
do
    echo "Processing ${ONTOLOGY}"
    curl -s -F file=@"../ontofox/${ONTOLOGY}.txt" -o ../owl/${ONTOLOGY}.owl http://ontofox.hegroup.org/service.php
done
