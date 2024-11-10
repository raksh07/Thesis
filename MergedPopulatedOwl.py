from rdflib import Graph, Namespace, RDF, OWL, RDFS
from difflib import SequenceMatcher

# List of target ontology files
ontology_files = [
    "populated_biodiversity1.owl",
    "populated_biodiversity2.owl",
    "populated_biodiversity3.owl",
    "populated_biodiversity4.owl",
    "populated_biodiversity5.owl",
    "populated_biodiversity6.owl"
]

# Function to match strings based on similarity
def match_strings(str1, str2):
    return SequenceMatcher(None, str1, str2).ratio()

# Function to extract classes, properties, and individuals from a graph
def extract_classes_properties_individuals(graph):
    classes = set()
    properties = set()
    individuals = set()

    for s, p, o in graph.triples((None, RDF.type, OWL.Class)):
        classes.add(s)

    for s, p, o in graph.triples((None, RDF.type, RDF.Property)):
        properties.add(s)

    for s, p, o in graph.triples((None, RDF.type, None)):
        if (s, RDF.type, OWL.Class) not in graph:
            individuals.add(s)

    return classes, properties, individuals

# Function to get the local name of a URI
def get_local_name(uri):
    return uri.split("#")[-1] if "#" in uri else uri.split("/")[-1]

# Initialize an empty graph for the final merged ontology
target_graph = Graph()

# Loop through each ontology file and merge it into the target graph
for ontology_path in ontology_files:
    source_graph = Graph()
    source_graph.parse(ontology_path, format="turtle")

    # Extract classes, properties, and individuals from both graphs
    source_classes, source_properties, source_individuals = extract_classes_properties_individuals(source_graph)
    target_classes, target_properties, target_individuals = extract_classes_properties_individuals(target_graph)

    # Match and populate classes, properties, and individuals
    for source_class in source_classes:
        source_class_name = get_local_name(source_class)
        best_class_match = None
        highest_class_similarity = 0.0

        for target_class in target_classes:
            target_class_name = get_local_name(target_class)
            similarity = match_strings(source_class_name, target_class_name)
            if similarity > highest_class_similarity:
                highest_class_similarity = similarity
                best_class_match = target_class

        # If a match is found, link them with equivalentClass and copy individuals
        if best_class_match and highest_class_similarity > 0.7:  # Adjust threshold as needed
            target_graph.add((source_class, OWL.equivalentClass, best_class_match))
            for s, p, o in source_graph.triples((None, RDF.type, source_class)):
                target_graph.add((s, RDF.type, best_class_match))
                # Copy all properties associated with the individual
                for prop, value in source_graph.predicate_objects(s):
                    target_graph.add((s, prop, value))
        else:
            # If no good match found, add the source class and its individuals to the target graph
            target_graph.add((source_class, RDF.type, OWL.Class))
            for s, p, o in source_graph.triples((None, RDF.type, source_class)):
                target_graph.add((s, RDF.type, source_class))
                # Copy all properties associated with the individual
                for prop, value in source_graph.predicate_objects(s):
                    target_graph.add((s, prop, value))

    # Match and populate properties
    for source_property in source_properties:
        source_property_name = get_local_name(source_property)
        best_property_match = None
        highest_property_similarity = 0.0

        for target_property in target_properties:
            target_property_name = get_local_name(target_property)
            similarity = match_strings(source_property_name, target_property_name)
            if similarity > highest_property_similarity:
                highest_property_similarity = similarity
                best_property_match = target_property

        # If a match is found, link them with equivalentProperty
        if best_property_match and highest_property_similarity > 0.7:  # Adjust threshold as needed
            target_graph.add((source_property, OWL.equivalentProperty, best_property_match))
        else:
            # If no good match found, add the source property to the target graph
            target_graph.add((source_property, RDF.type, RDF.Property))

# Save the final merged ontology
output_path = "merged_biodiversity.owl"
target_graph.serialize(destination=output_path, format="turtle")
