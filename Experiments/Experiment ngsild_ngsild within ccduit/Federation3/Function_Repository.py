from rdflib import Graph, Namespace, URIRef, Literal
from rdflib.namespace import RDF, XSD
from datetime import datetime
import json

# Define namespaces
BRICK = Namespace("https://brickschema.org/schema/1.1/Brick#")
EX = Namespace("http://example.com/residential#")

from rdflib import Graph, Literal, RDF, URIRef, Namespace

def convert_ngsi_ld_to_brick(json_data):
    # Create a graph
    g = Graph()

    # Define namespaces
    BRICK = Namespace("https://brickschema.org/schema/1.1/Brick#")
    BLDG = Namespace("http://example.org/building#")
    g.bind("brick", BRICK)
    g.bind("bldg", BLDG)

    # Extract data from JSON
    observation_id = URIRef(BLDG[json_data["id"].split(":")[-1]])
    community_id = URIRef(json_data["Community"]["object"][0])
    date_observed = Literal(json_data["DateObserved"]["value"])
    occupancy_percentage = Literal(json_data["OccupancyPercentage"]["value"])
    occupancy_status = Literal(json_data["OccupancyStatus"]["value"])
    zones_with_high_occupancy = Literal(json_data["ZonesWithHighOccupancy"]["value"])
    name = Literal(json_data["name"]["value"])

    # Add triples to the graph
    g.add((observation_id, RDF.type, BRICK.OccupancyReading))
    g.add((observation_id, BRICK.isPartOf, community_id))
    g.add((observation_id, BRICK.dateObserved, date_observed))
    g.add((observation_id, BRICK.occupancyPercentage, occupancy_percentage))
    g.add((observation_id, BRICK.occupancyStatus, occupancy_status))
    g.add((observation_id, BRICK.zonesWithHighOccupancy, zones_with_high_occupancy))
    g.add((observation_id, BRICK.hasName, name))

    # Serialize graph to TTL format
    ttl_data = g.serialize(format="turtle")
    return ttl_data

# Example JSON data
# json_data = {
#     "id": "urn:ngsild:Community2:Observation:1734240725819384600",
#     "type": "OccupancyReading",
#     "Community": {
#         "type": "Relationship",
#         "object": ["urn:ngsi-ld:Community:Community2"]
#     },
#     "DateObserved": {
#         "type": "Property",
#         "value": "2024-12-15T05:32:05.813902+00:00"
#     },
#     "OccupancyPercentage": {
#         "type": "Property",
#         "value": 94
#     },
#     "OccupancyStatus": {
#         "type": "Property",
#         "value": "high"
#     },
#     "ZonesWithHighOccupancy": {
#         "type": "Property",
#         "value": "ZoneA, ZoneB"
#     },
#     "name": {
#         "type": "Property",
#         "value": "Occupancy Observation"
#     }
# }

# Convert and print TTL
# ttl_result = convert_ngsi_ld_to_brick(json_data)
# print(ttl_result)

# # Define namespaces
# EX = Namespace("http://example.com/weatherObservation#")

# def convert_ngsi_ld_to_brick(ngsi_ld_data):
#     print(json.dumps(ngsi_ld_data, indent=2))
    
#     # Extracting the relevant values from the NGSI-LD data
#     observation_id = ngsi_ld_data["id"]
#     name = ngsi_ld_data.get("name", "Unnamed Observation")  # Default if name not provided
#     community = ngsi_ld_data["Community"]["object"][0]  # Assuming only one community for simplicity
#     date_observed = ngsi_ld_data["DateObserved"]["value"]
#     air_temperature = ngsi_ld_data["AirTemperature"]["value"]
#     diffuse_solar_flux = ngsi_ld_data["DiffuseSolarFlux"]["value"]
#     direct_solar_flux = ngsi_ld_data["DirectSolarFlux"]["value"]
#     global_solar_flux = ngsi_ld_data["GlobalSolarFlux"]["value"]
#     rain = ngsi_ld_data["Rain"]["value"]
#     relative_humidity = ngsi_ld_data["RelativeHumidity"]["value"]
#     wind_speed = ngsi_ld_data["WindSpeed"]["value"]

#     # Convert observation_id to use as a unique identifier in Brick
#     unique_id = observation_id.split(":")[-1]  # Extract the last part for unique ID

#     # Create Turtle representation
#     brick_ttl = f"""
#     @prefix brick1: <https://brickschema.org/schema/1.1/Brick#> .
#     @prefix ex: <http://example.com/weatherObservation#{unique_id}> .
#     @prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

#     ex:weatherObservation_{unique_id} a brick1:WeatherObservation ;
#         brick1:hasName "{name}" ;
#         brick1:hasCommunity <{community}> ;
#         brick1:hasTimestamp "{date_observed}"^^xsd:dateTime ;
#         brick1:hasAirTemperature {air_temperature} ;
#         brick1:hasDiffuseSolarFlux {diffuse_solar_flux} ;
#         brick1:hasDirectSolarFlux {direct_solar_flux} ;
#         brick1:hasGlobalSolarFlux {global_solar_flux} ;
#         brick1:hasRain {rain} ;
#         brick1:hasRelativeHumidity {relative_humidity} ;
#         brick1:hasWindSpeed {wind_speed} .
#     """

#     return brick_ttl.strip()  # Remove leading/trailing whitespace

# # Example usage
# ngsi_ld_data = {
#     "id": "urn:ngsi-ld:Sirta:WeatherObservation:20241112003810",
#     "type": "WeatherObservation",
#     "name": "Weather Observation",
#     "Community": {
#         "type": "Relationship",
#         "object": [
#             "urn:ngsi-ld:Community:WeatherCommunity_001"
#         ]
#     },
#     "DateObserved": {
#         "type": "Property",
#         "value": "2024-11-12T00:38:10"
#     },
#     "AirTemperature": {
#         "type": "Property",
#         "value": 16.577
#     },
#     "RelativeHumidity": {
#         "type": "Property",
#         "value": 55.711
#     },
#     "WindSpeed": {
#         "type": "Property",
#         "value": 0.978
#     },
#     "Rain": {
#         "type": "Property",
#         "value": 0.0
#     },
#     "DirectSolarFlux": {
#         "type": "Property",
#         "value": -0.1725944444444444
#     },
#     "DiffuseSolarFlux": {
#         "type": "Property",
#         "value": -0.8321638888888889
#     },
#     "GlobalSolarFlux": {
#         "type": "Property",
#         "value": -0.8060805555555555
#     }
# }

# # brick_ttl_output = convert_ngsi_ld_to_brick(ngsi_ld_data)
# # print(brick_ttl_output)


from rdflib import Graph, URIRef, Literal, Namespace
import json
import time

# Define namespaces
BRICK = Namespace("https://brickschema.org/schema/1.1/Brick#")
XSD = Namespace("http://www.w3.org/2001/XMLSchema#")
EX = Namespace("http://example.com#")

# Function to parse Brick TTL and convert to NGSI-LD JSON
def convert_brick_to_ngsi_ld(ttl_data):
    # Parse the TTL data into an RDF graph
    g = Graph()
    g.parse(data=ttl_data, format="turtle")

    # Query the graph for relevant data
    query = """
    SELECT ?observation ?dateObserved ?occupancyStatus ?occupancyPercentage ?zonesWithHighOccupancy
    WHERE {
        ?observation a brick:OccupancyReading ;
                     brick:dateObserved ?dateObserved ;
                     brick:occupancyStatus ?occupancyStatus ;
                     brick:occupancyPercentage ?occupancyPercentage .
        OPTIONAL { ?observation brick:zonesWithHighOccupancy ?zonesWithHighOccupancy . }
    }
    """
    results = g.query(query, initNs={"brick": BRICK, "xsd": XSD, "ex": EX})

    # Convert results to NGSI-LD JSON
    ngsild_data = []
    for row in results:
        observation_id = f"urn:ngsild:{str(row['observation'].split('#')[-1])}"
        ngsild_data.append({
            "id": observation_id,
            "type": "OccupancyReading",
            "DateObserved": {
                "type": "Property",
                "value": str(row["dateObserved"])
            },
            "OccupancyStatus": {
                "type": "Property",
                "value": str(row["occupancyStatus"])
            },
            "OccupancyPercentage": {
                "type": "Property",
                "value": float(row["occupancyPercentage"])
            },
            "ZonesWithHighOccupancy": {
                "type": "Property",
                "value": str(row["zonesWithHighOccupancy"]) if row["zonesWithHighOccupancy"] else ""
            }
        })
    
    return ngsild_data