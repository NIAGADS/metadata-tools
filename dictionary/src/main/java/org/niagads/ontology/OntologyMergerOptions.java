package org.niagads.ontology;

import org.kohsuke.args4j.Option;

/**
 *  Process arguments passed from command line for OntologyMerger.java
 * from: https://github.com/VEuPathDB/EbrcWebsiteCommon/blob/bc5dd3077310a46457e95d85f39f341114d644a6/Model/src/main/java/org/eupathdb/common/model/ontology/OntologyMergerOptions.java
 *  @author Jie Zheng
 */
public class OntologyMergerOptions {
    @Option(name="-path", usage ="the directory contains input file and also for saved output file", required = false)
        private String path = "/var/www/PlasmoDB/plasmo.jbrestel/gus_home/lib/wdk/ontology/";

    @Option(name="-inputFilename", usage="OWL file which contains owl import statements", required = false)
    private String inputFilename = "categories.owl";

    @Option(name="-outputFilename", usage="The filename of output OWL file", required = false)
    private String outputFilename = "tmp_merged.owl";

    @Option(name="-ontoIRIstr", usage="IRI of ontology contains term display labels in OWL format", required = false)
    private String ontoIRIstr = "http://purl.obolibrary.org/obo/eupath/external/categories_import.owl";

    public String getPath () {
    	return this.path;
    }

    public String getInputFilename () {
    	return this.inputFilename;
    }

    public String getOutputFilename () {
    	return this.outputFilename;
    }

    public String getOntoIRIstr () {
    	return this.ontoIRIstr;
    }
}
