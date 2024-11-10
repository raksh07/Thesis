from owlready2 import get_ontology
import networkx as nx
import matplotlib.pyplot as plt

# Load the ontology
ontology_path = "merged_populated_ontology.owl"
onto = get_ontology(ontology_path).load()

# Create a directed graph
G = nx.DiGraph()

# Extract classes and their relationships from the ontology
for cls in onto.classes():
    # Add the class as a node
    G.add_node(cls.name)

    # Add relationships (subclass_of) as edges
    for parent in cls.is_a:
        if hasattr(parent, 'name'):
            G.add_edge(cls.name, parent.name)

# Plot the knowledge graph
plt.figure(figsize=(12, 12))
pos = nx.spring_layout(G, k=0.5, iterations=50)
nx.draw(G, pos, with_labels=True, node_color='lightblue', font_size=8, node_size=500, edge_color='gray')
plt.title("Knowledge Graph of the Ontology", size=16)
plt.show()
