import time
from rdflib import Graph, Namespace
import json
# Define namespaces
BRICK = Namespace("https://brickschema.org/schema/1.1/Brick#")
EX = Namespace("http://example.com#")

def convert_brick_to_ngsi_ld(ttl_data):
    # start = time.time_ns()
    g = Graph()
    
    # Faster Turtle Parsing
    g.parse(data=ttl_data, format="turtle", publicID="")

    ngsild_data = []

    # Fetch all triples once and store in a dictionary (avoiding multiple lookups)
    observations = {
        obs: {
            "dateObserved": g.value(obs, BRICK["dateObserved"]),
            "occupancyStatus": g.value(obs, BRICK["occupancyStatus"]),
            "occupancyPercentage": g.value(obs, BRICK["occupancyPercentage"]),
            "zonesWithHighOccupancy": g.value(obs, BRICK["zonesWithHighOccupancy"])
        }
        for obs in g.subjects(predicate=None, object=BRICK["OccupancyReading"])
    }

    # Process Observations Efficiently
    for obs, data in observations.items():
        observation_id = f"urn:ngsild:OccupancyReading:{obs.split(':')[-1]}"  # Faster ID extraction
        ngsild_data.append({
            "id": observation_id,
            "type": "OccupancyReading",
            "DateObserved": {"type": "Property", "value": str(data["dateObserved"])},
            "OccupancyStatus": {"type": "Property", "value": str(data["occupancyStatus"])},
            "OccupancyPercentage": {"type": "Property", "value": float(data["occupancyPercentage"]) if data["occupancyPercentage"] else None},
            "ZonesWithHighOccupancy": {"type": "Property", "value": str(data["zonesWithHighOccupancy"]) if data["zonesWithHighOccupancy"] else ""}
        })

    return ngsild_data

# # Example Data
# brick_ttl = """
# @prefix brick: <https://brickschema.org/schema/1.1/Brick#> .
# @prefix ex: <http://example.com#> .
# @prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

# ex:Community1:Observation:1738236177893584788790 a brick:OccupancyReading ;
#     brick:dateObserved "2025-01-30T11:22:52.935847+00:00"^^xsd:dateTime ;
#     brick:occupancyStatus "low" ;
#     brick:occupancyPercentage "22"^^xsd:float ;
#     brick:zonesWithHighOccupancy "" .
# """
# import requests
# # Run Benchmark
# ngsild_json = convert_brick_to_ngsi_ld(brick_ttl)
# print(json.dumps(ngsild_json[0], indent=2))
# community_context_url=r" http://localhost:1032/ngsi-ld/v1/entities"
# headers = {
#                 "Content-Type": "application/json",
# #                 "Accept": "application/json"
#             }
# before_posting=time.time_ns()
# # print(f"conversion_time: {conversion_time}")
# response = requests.post(community_context_url,json=ngsild_json[0],headers=headers)
# if response.status_code in [200, 201]:
#     end_time = time.time_ns()
#     delay_ms = (end_time - before_posting) / 1_000_000
#     print(f"{delay_ms}")
# else:
#     print(f"End time: {time.time_ns()}")
#     print(f"Failed to send data via HTTP. Status code: {response.status_code}")