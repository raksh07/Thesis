import pandas as pd
from rdflib import Graph, Namespace, URIRef, Literal
from rdflib.namespace import RDF, RDFS, OWL, XSD

# Load the CSV file with tab delimiter and error handling for bad lines
csv_file = "DS_6.csv"
try:
    df = pd.read_csv(csv_file, delimiter='\t', on_bad_lines='skip')
except pd.errors.ParserError as e:
    print(f"Error reading CSV file: {e}")

# Print the dataframe and column names to verify
print(df.head())
print(df.columns)

# Assuming the column name is 'gbifID'
# Create a new RDF graph
graph = Graph()

# Define ontology namespaces
BBC_taxo = Namespace("https://github.com/raksh07/BBC#")
ncbi_taxo = Namespace("http://purl.obolibrary.org/obo/NCBITaxon#")

# Bind namespaces to prefixes
graph.bind("bbc", BBC_taxo)
graph.bind("ncbi", ncbi_taxo)

# Define classes
classes = [
    "Kingdom", "Phylum", "Class", "Order", "Family", "Genus", "Species",
    "ScientificName", "GeographicalLocation", "EventDate", "IdentifiedBy",
    "RecordedBy", "TaxonKey", "SpeciesKey"
]
for cls in classes:
    graph.add((BBC_taxo[cls], RDF.type, OWL.Class))

# Define subclass relationships
subclasses = [
    ("Phylum", "Kingdom"), ("Class", "Phylum"), ("Order", "Class"),
    ("Family", "Order"), ("Genus", "Family"), ("Species", "Genus"),
    ("SpeciesKey", "Species"), ("ScientificName", "Species"),
    ("Locality", "GeographicalLocation"), ("DecimalLatitude", "GeographicalLocation"),
    ("DecimalLongitude", "GeographicalLocation")
]
for subclass, superclass in subclasses:
    graph.add((BBC_taxo[subclass], RDFS.subClassOf, BBC_taxo[superclass]))

# Define object properties
properties = [
    "HasPhylum", "HasClass", "HasOrder", "HasFamily", "HasGenus",
    "HasLocation", "InDecimalLatitude", "InDecimalLongitude", "FoundOnEventDate",
    "WasIdentifiedBy", "WasRecordedBy", "HasSpeciesKey", "HasTaxonKey"
]
for prop in properties:
    graph.add((BBC_taxo[prop], RDF.type, OWL.ObjectProperty))

# Map Classes
class_mappings = {
    BBC_taxo.Kingdom: ncbi_taxo.Kingdom,
    BBC_taxo.Phylum: ncbi_taxo.Phylum,
    BBC_taxo.Class: ncbi_taxo.Class,
    BBC_taxo.Order: ncbi_taxo.Order,
    BBC_taxo.Family: ncbi_taxo.Family,
    BBC_taxo.Genus: ncbi_taxo.Genus,
    BBC_taxo.Species: ncbi_taxo.Species,
}
for bbc_class, ncbi_class in class_mappings.items():
    graph.add((bbc_class, BBC_taxo.isMappedTo, ncbi_class))

# Map Object Properties
property_mappings = {
    BBC_taxo.HasPhylum: ncbi_taxo.Phylum,
    BBC_taxo.HasClass: ncbi_taxo.Class,
}
for bbc_property, ncbi_property in property_mappings.items():
    graph.add((bbc_property, BBC_taxo.isMappedTo, ncbi_property))

# Add instances to the graph from the CSV data
for index, row in df.iterrows():
    specimen_uri = URIRef(BBC_taxo + f"specimen_{row['gbifID']}")

    # Add the specimen as an instance of Species
    graph.add((specimen_uri, RDF.type, BBC_taxo.Species))

    # Add properties to the specimen
    if pd.notna(row['kingdom']):
        graph.add((specimen_uri, BBC_taxo.hasPhylum, Literal(row['phylum'], datatype=XSD.string)))
    if pd.notna(row['phylum']):
        graph.add((specimen_uri, BBC_taxo.hasPhylum, Literal(row['phylum'], datatype=XSD.string)))
    if pd.notna(row['class']):
        graph.add((specimen_uri, BBC_taxo.hasClass, Literal(row['class'], datatype=XSD.string)))
    if pd.notna(row['order']):
        graph.add((specimen_uri, BBC_taxo.hasOrder, Literal(row['order'], datatype=XSD.string)))
    if pd.notna(row['family']):
        graph.add((specimen_uri, BBC_taxo.hasFamily, Literal(row['family'], datatype=XSD.string)))
    if pd.notna(row['genus']):
        graph.add((specimen_uri, BBC_taxo.hasGenus, Literal(row['genus'], datatype=XSD.string)))
    if pd.notna(row['species']):
        graph.add((specimen_uri, BBC_taxo.hasSpeciesKey, Literal(row['speciesKey'], datatype=XSD.string)))
    if pd.notna(row['scientificName']):
        graph.add((specimen_uri, BBC_taxo.scientificName, Literal(row['scientificName'], datatype=XSD.string)))
    if pd.notna(row['decimalLatitude']):
        graph.add((specimen_uri, BBC_taxo.decimalLatitude, Literal(row['decimalLatitude'], datatype=XSD.decimal)))
    if pd.notna(row['decimalLongitude']):
        graph.add((specimen_uri, BBC_taxo.decimalLongitude, Literal(row['decimalLongitude'], datatype=XSD.decimal)))
    if pd.notna(row['eventDate']):
        graph.add((specimen_uri, BBC_taxo.foundOnEventDate, Literal(row['eventDate'], datatype=XSD.date)))
    if pd.notna(row['identifiedBy']):
        graph.add((specimen_uri, BBC_taxo.wasIdentifiedBy, Literal(row['identifiedBy'], datatype=XSD.string)))
    if pd.notna(row['recordedBy']):
        graph.add((specimen_uri, BBC_taxo.wasRecordedBy, Literal(row['recordedBy'], datatype=XSD.string)))

# Save the populated RDF graph to a file
graph.serialize("populated_biodiversity6.owl", format="turtle")
