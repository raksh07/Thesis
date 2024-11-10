from owlready2 import *

def merge_and_populate_ontologies(output_file, *input_files):
    # Create a new ontology for merging classes and populating individuals
    merged_ontology = get_ontology("http://example.org/merged_ontology.owl")

    # Dictionary to track merged classes by name
    merged_classes = {}

    # Load each input ontology and merge its classes and individuals
    with merged_ontology:
        for file in input_files:
            print(f"Loading ontology from {file}...")
            try:
                ontology = get_ontology(file).load()
                print(f"Ontology '{file}' loaded successfully.")

                # Merge classes based on name equivalence
                for cls in ontology.classes():
                    if cls.name not in merged_classes:
                        # Create a new class in the merged ontology if it doesn't already exist
                        merged_class = types.new_class(cls.name, (Thing,))
                        merged_classes[cls.name] = merged_class
                        print(f"Class '{cls.name}' added from '{file}'")
                    else:
                        # Use the already merged class if it exists
                        merged_class = merged_classes[cls.name]
                        print(f"Class '{cls.name}' merged with existing class from '{file}'")

                # Populate the merged ontology with individuals from this ontology
                for individual in ontology.individuals():
                    individual_class_name = individual.is_a[0].name if individual.is_a else None
                    merged_class = merged_classes.get(individual_class_name, Thing)

                    if merged_class:
                        # Create the individual in the merged ontology
                        cloned_individual = merged_class(individual.name)

                        # Process properties and relationships
                        for prop, values in individual.get_properties():
                            for value in values:
                                # Skip integer values that could cause issues
                                if isinstance(value, int):
                                    print(f"Skipping integer value '{value}' for property '{prop.name}' in Individual '{individual.name}'")
                                    continue  # Skip this integer value

                                # Safely handle OWL entities that have 'name' and 'namespace'
                                if hasattr(value, "name") and hasattr(value, "namespace"):
                                    setattr(cloned_individual, prop.name, value)
                                    print(f"Assigned OWL entity '{value.name}' to property '{prop.name}'")
                                else:
                                    # Non-entity values, assign them as literals (e.g., strings or floats)
                                    setattr(cloned_individual, prop.name, value)
                                    print(f"Assigned literal '{value}' to property '{prop.name}'")

                        print(f"Copied individual '{individual.name}' from '{file}' under class '{merged_class.name}'")
                    else:
                        print(f"Warning: Could not find a suitable class for individual '{individual.name}' in '{file}'")
            except Exception as e:
                print(f"Error loading or inspecting ontology '{file}': {e}")

    # Save the merged and populated ontology to the output file
    try:
        merged_ontology.save(file=output_file)
        print(f"Merged and populated ontology saved as '{output_file}'.")
    except Exception as e:
        print(f"Error saving ontology to '{output_file}': {e}")

# Input OWL files to merge
file_ontology = "OntologyID(Anonymous-1098663).owl"  # Re-exported merged_biodiversity.owl
file_bco = "bco.owl"
file_taxrank = "taxrank.owl"

# Output file where the merged ontology will be saved
output_file = "merged_populated_ontology.owl"

# Merge and populate the ontologies into a new OWL file
merge_and_populate_ontologies(output_file, file_ontology, file_bco, file_taxrank)
