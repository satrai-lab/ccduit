from flask import Flask, jsonify

# Creating a Flask app
app = Flask(__name__)

# Sample Brick schema data
brick_data = """
@prefix brick: <https://brickschema.org/schema/1.0.3/Brick#> .
@prefix bf: <https://brickschema.org/schema/1.0.3/BrickFrame#> .
@prefix ex: <https://example.org#> .

# Define building and its components
ex:Building1 a brick:Building .
ex:Floor1 a brick:Floor ;
    bf:isPartOf ex:Building1 .
ex:Room1 a brick:Room ;
    bf:isPartOf ex:Floor1 .
ex:Temperature_Sensor1 a brick:Temperature_Sensor ;
    bf:isLocatedIn ex:Room1 .
ex:Light1 a brick:Lighting_System ;
    bf:isLocatedIn ex:Room1 .

# Define relationships between components
ex:Room1 bf:hasPoint ex:Temperature_Sensor1 .
ex:Room1 bf:hasPoint ex:Light1 .

# Define setpoints and measurements
ex:Temperature_Setpoint1 a brick:Temperature_Setpoint ;
    bf:isPointOf ex:Room1 .
ex:Temperature_Sensor1 bf:measures ex:Temperature_Setpoint1 .
"""

# Creating the /building-data endpoint to serve the Brick schema data
@app.route('/building-data', methods=['GET'])
def get_building_data():
    return jsonify({"data": brick_data}), 200


# Returning the Flask app object for reference
app.run(port=5001)
