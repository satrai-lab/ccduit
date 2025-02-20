from rdflib import Graph, Namespace, URIRef, Literal
from rdflib.namespace import RDF, XSD
from datetime import datetime
import json

# Define namespaces
BRICK = Namespace("https://brickschema.org/schema/1.1/Brick#")
EX = Namespace("http://example.com/residential#")

def convert_brick_to_ngsi_ld(turtle_data):
    g = Graph()
    g.parse(data=turtle_data, format="turtle")

    ngsi_ld_entities = []

    # Iterate through all occupancy patterns in the Brick data
    for occupancy_pattern in g.subjects(RDF.type, BRICK.Occupancy_Pattern):
        # Extract properties
        occupancy_status = g.value(occupancy_pattern, BRICK.hasOccupancyStatus)
        occupancy_percentage = g.value(occupancy_pattern, BRICK.hasOccupancyPercentage)
        timestamp_literal = g.value(occupancy_pattern, BRICK.hasTimestamp)
        location = g.value(occupancy_pattern, BRICK.hasLocation)
        community = g.value(occupancy_pattern, BRICK.hasCommunity)
        name = g.value(occupancy_pattern, BRICK.hasName)

        # Convert the timestamp from Literal to datetime
        if isinstance(timestamp_literal, Literal) and timestamp_literal.datatype == XSD.dateTime:
            timestamp = datetime.fromisoformat(str(timestamp_literal))
            observation_id = f"urn:ngsild:Residential:Observation:{timestamp.strftime('%Y%m%d%H%M%S')}"
        else:
            timestamp = None
            observation_id = "unknown"

        # Create NGSI-LD entity
        observation = {
            "id": observation_id,
            "type": "Observation",
            "DateObserved": {
                "type": "Property",
                "value": timestamp.isoformat() if timestamp else ""
            },
            "OccupancyStatus": {
                "type": "Property",
                "value": str(occupancy_status) if occupancy_status else ""
            },
            "OccupancyPercentage": {
                "type": "Property",
                "value": float(occupancy_percentage) if occupancy_percentage else 0.0
            },
            "Community": {
                "type": "Relationship",
                "object": str(community)
            },
            "Name": {
                "type": "Property",
                "value": str(name) if name else ""
            }
        }

        ngsi_ld_entities.append(observation)

    return ngsi_ld_entities

# # Example usage
# if __name__ == "__main__":
#     turtle_data = """
#     @prefix brick1: <https://brickschema.org/schema/1.1/Brick#> .
#     @prefix ex: <http://example.com/residential#> .
#     @prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

#     ex:occupancyPattern_20241112012628 a brick1:Occupancy_Pattern ;
#         brick1:hasCommunity "urn:ngsi-ld:Community:Residential_001" ;
#         brick1:hasName "Occupancy Data" ;
#         brick1:hasOccupancyPercentage 88 ;
#         brick1:hasOccupancyStatus "high" ;
#         brick1:hasTimestamp "2024-11-12T01:26:28.512463+00:00"^^xsd:dateTime .
#     """

#     ngsi_ld_data = convert_brick_to_ngsi_ld(turtle_data)
#     print(json.dumps(ngsi_ld_data, indent=4))

from rdflib import Graph, Namespace, URIRef, Literal
from datetime import datetime
import matplotlib.pyplot as plt
import networkx as nx
import json

# Define namespaces
EX = Namespace("http://example.com/weatherObservation#")

def convert_ngsi_ld_to_brick(ngsi_ld_data):
    print(json.dumps(ngsi_ld_data, indent=2))
    
    # Extracting the relevant values from the NGSI-LD data
    observation_id = ngsi_ld_data["id"]
    name = ngsi_ld_data.get("name", "Unnamed Observation")  # Default if name not provided
    community = ngsi_ld_data["Community"]["object"][0]  # Assuming only one community for simplicity
    date_observed = ngsi_ld_data["DateObserved"]["value"]
    air_temperature = ngsi_ld_data["AirTemperature"]["value"]
    diffuse_solar_flux = ngsi_ld_data["DiffuseSolarFlux"]["value"]
    direct_solar_flux = ngsi_ld_data["DirectSolarFlux"]["value"]
    global_solar_flux = ngsi_ld_data["GlobalSolarFlux"]["value"]
    rain = ngsi_ld_data["Rain"]["value"]
    relative_humidity = ngsi_ld_data["RelativeHumidity"]["value"]
    wind_speed = ngsi_ld_data["WindSpeed"]["value"]

    # Convert observation_id to use as a unique identifier in Brick
    unique_id = observation_id.split(":")[-1]  # Extract the last part for unique ID

    # Create Turtle representation
    brick_ttl = f"""
    @prefix brick1: <https://brickschema.org/schema/1.1/Brick#> .
    @prefix ex: <http://example.com/weatherObservation#{unique_id}> .
    @prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

    ex:weatherObservation_{unique_id} a brick1:WeatherObservation ;
        brick1:hasName "{name}" ;
        brick1:hasCommunity <{community}> ;
        brick1:hasTimestamp "{date_observed}"^^xsd:dateTime ;
        brick1:hasAirTemperature {air_temperature} ;
        brick1:hasDiffuseSolarFlux {diffuse_solar_flux} ;
        brick1:hasDirectSolarFlux {direct_solar_flux} ;
        brick1:hasGlobalSolarFlux {global_solar_flux} ;
        brick1:hasRain {rain} ;
        brick1:hasRelativeHumidity {relative_humidity} ;
        brick1:hasWindSpeed {wind_speed} .
    """

    return brick_ttl.strip()  # Remove leading/trailing whitespace

# Example usage
ngsi_ld_data = {
    "id": "urn:ngsi-ld:Sirta:WeatherObservation:20241112003810",
    "type": "WeatherObservation",
    "name": "Weather Observation",
    "Community": {
        "type": "Relationship",
        "object": [
            "urn:ngsi-ld:Community:WeatherCommunity_001"
        ]
    },
    "DateObserved": {
        "type": "Property",
        "value": "2024-11-12T00:38:10"
    },
    "AirTemperature": {
        "type": "Property",
        "value": 16.577
    },
    "RelativeHumidity": {
        "type": "Property",
        "value": 55.711
    },
    "WindSpeed": {
        "type": "Property",
        "value": 0.978
    },
    "Rain": {
        "type": "Property",
        "value": 0.0
    },
    "DirectSolarFlux": {
        "type": "Property",
        "value": -0.1725944444444444
    },
    "DiffuseSolarFlux": {
        "type": "Property",
        "value": -0.8321638888888889
    },
    "GlobalSolarFlux": {
        "type": "Property",
        "value": -0.8060805555555555
    }
}

# brick_ttl_output = convert_ngsi_ld_to_brick(ngsi_ld_data)
# print(brick_ttl_output)
