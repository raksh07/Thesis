import geopandas as gpd
import matplotlib.pyplot as plt
from rdflib import Graph, Namespace
from shapely.geometry import Point
import contextily as ctx
from rdflib.namespace import RDF

# Load the RDF graph
graph = Graph()
graph.parse("BBC.owl", format="xml")  # Change format to "xml"

# Define the namespace
BBC_taxo = Namespace("https://github.com/raksh07/BBC#")

# Extract species, their families, and their corresponding locations
species_locations = []

for specimen in graph.subjects(RDF.type, BBC_taxo.Species):
    species = str(graph.value(specimen, BBC_taxo.hasSpeciesKey))
    family = str(graph.value(specimen, BBC_taxo.hasFamily))  # Assuming 'hasFamily' is the property for family
    latitude = graph.value(specimen, BBC_taxo.decimalLatitude)
    longitude = graph.value(specimen, BBC_taxo.decimalLongitude)

    if latitude and longitude and family:
        species_locations.append((species, family, float(latitude), float(longitude)))

# Convert to GeoDataFrame
gdf = gpd.GeoDataFrame(species_locations, columns=["Species", "Family", "Latitude", "Longitude"])
gdf['geometry'] = gdf.apply(lambda x: Point((x.Longitude, x.Latitude)), axis=1)

# Set the Coordinate Reference System (CRS) to WGS84 (EPSG:4326)
gdf.crs = 'epsg:4326'

# Generate different maps by family
families = gdf['Family'].unique()

for i, family in enumerate(families):
    # Subset the species for the current family
    gdf_subset = gdf[gdf['Family'] == family]

    # Plot the ecological range map for the current family
    fig, ax = plt.subplots(figsize=(15, 10))

    # Plot species occurrences in red
    gdf_subset.plot(ax=ax, marker='o', color='red', markersize=50, alpha=0.7)

    # Zoom in to the area where the points are located
    minx, miny, maxx, maxy = gdf_subset.total_bounds
    ax.set_xlim([minx - 1, maxx + 1])
    ax.set_ylim([miny - 1, maxy + 1])

    # Add the tile basemap
    ctx.add_basemap(ax, crs=gdf_subset.crs.to_string(), source=ctx.providers.OpenStreetMap.Mapnik)

    # Enhance the map appearance
    plt.title(f'Ecological Range Map of {family} Family Occurrences', fontsize=20)
    plt.xlabel('Longitude', fontsize=15)
    plt.ylabel('Latitude', fontsize=15)
    plt.grid(True, linestyle='--', alpha=0.5)

    # Display the map
    plt.show()
