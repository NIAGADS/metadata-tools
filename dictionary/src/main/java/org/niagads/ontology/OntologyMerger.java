package org.niagads.ontology;

import java.io.File;
import java.util.Set;

import org.apache.log4j.Logger;
import org.kohsuke.args4j.CmdLineException;
import org.kohsuke.args4j.CmdLineParser;
import org.semanticweb.owlapi.apibinding.OWLManager;
import org.semanticweb.owlapi.model.IRI;
import org.semanticweb.owlapi.model.OWLDataFactory;
import org.semanticweb.owlapi.model.OWLImportsDeclaration;
import org.semanticweb.owlapi.model.OWLOntology;
import org.semanticweb.owlapi.model.OWLOntologyManager;
import org.semanticweb.owlapi.model.RemoveImport;
import org.semanticweb.owlapi.util.AutoIRIMapper;

/**
 * Merge all imported OWL files into main OWL file
 * from: https://github.com/VEuPathDB/EbrcWebsiteCommon/blob/bc5dd3077310a46457e95d85f39f341114d644a6/Model/src/main/java/org/eupathdb/common/model/ontology/OntologyMerger.java
 * @author Jie Zheng
 */
public class OntologyMerger {

  private static final Logger LOG = Logger.getLogger(OntologyMerger.class);

  public static void main(String[] args) {
    OntologyMergerOptions bean = new OntologyMergerOptions();
    CmdLineParser parser = new CmdLineParser(bean);

    try {
      parser.parseArgument(args);
    }
    catch (CmdLineException e) {
      System.err.println(e.getMessage());
      parser.printUsage(System.err);
      System.exit(1);
    }

    String path = bean.getPath();
    String inputFilename = path + bean.getInputFilename();
    String outputFilename = path + bean.getOutputFilename();
    // String ontoIRIstr = bean.getOntoIRIstr();

    // Get hold of an ontology manager
    OWLOntologyManager manager = OWLManager.createOWLOntologyManager();

    AutoIRIMapper mapper = new AutoIRIMapper(new File(path), false);
    manager.addIRIMapper(mapper);

    // load ontology
    OWLOntology ont = OntologyManipulator.load(inputFilename, manager);
    if (ont == null) {
      LOG.warn("Could not load ontology using file: " + inputFilename + " and IRI mapper built with " + path);
      System.exit(1);
    }

    OWLDataFactory df = manager.getOWLDataFactory();

    // get all imported ontologies
    Set<OWLOntology> importOnts = ont.getImports();
    Set<OWLImportsDeclaration> importSts = ont.getImportsDeclarations();

    // remove imports statements from the loaded ontology
    for (OWLImportsDeclaration importSt : importSts) {
      IRI importOntIRI = importSt.getIRI();
      System.out.println(importOntIRI.toString());
      RemoveImport ri = new RemoveImport(ont, df.getOWLImportsDeclaration(importOntIRI));
      manager.applyChange(ri);
    }

    // merge the removed imported ontologies to the loaded one
    for (OWLOntology importOnt : importOnts) {
      // IRI importOntIRI = importOnt.getOntologyID().getOntologyIRI();
      // OntologyManipulator.printPrefixNSs(manager, importOnt);
      ont = OntologyManipulator.mergeToTargetOnt(manager, ont, importOnt);
    }

    OntologyManipulator.saveToFile(manager, ont, outputFilename);
  }
}
