ONTOLOGIES=(mondo efo hp uberon)

for ONTOLOGY in "${ONTOLOGIES[@]}"
do
    echo "Processing ${ONTOLOGY}"
    curl -s -F file=@"${ONTOLOGY}.txt" -o ../owl/${ONTOLOGY}.owl http://ontofox.hegroup.org/service.php
done
