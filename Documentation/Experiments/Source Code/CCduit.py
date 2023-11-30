# CCduit Python Interface
# This script provides the declarations for managing interactions between IoT federations using CCduit.

from pickle import NONE
from tinydb import TinyDB, Query
from tinydb import where
import json
from rdflib import Graph
from pyld import jsonld
from flask import Flask, request, jsonify
import uuid
import multiprocessing
import paho.mqtt.client as mqtt
import requests
import time
import hashlib
import sqlite3
from flask_cors import CORS
import os
import signal


app = Flask(__name__)
CORS(app)


#---------------------------
#Init stuff here
#---------------------------------------
# Initialize the database

#db = TinyDB('database.json')

#mappings_table = db.table('Mappings')


#DB_NAME = 'ccduit.db'


custom_converters = {}

ccduit_version=0.03




def sanitize_column_name(name):
    # Replace special characters with underscores
    # You can extend this as needed
    return name.replace("@", "_")

def serialize_value(value):
    if isinstance(value, (list, dict)):
        return json.dumps(value)
    return value

def deserialize_value(value, datatype):
    if datatype in ("LIST", "DICT"):
        return json.loads(value)
    return value

class SQLiteDB:
    def __init__(self, dbname):
        self.conn = sqlite3.connect(dbname, check_same_thread=False)

    def table(self, table_name):
        return SQLiteTable(self.conn, table_name)

    def close(self):
        self.conn.close()

class SQLiteTable:
    def __init__(self, conn, table_name):
        self.conn = conn
        self.table_name = table_name
        self.columns_initialized = False

    def ensure_table_columns(self, data):
        if not self.columns_initialized:
            columns = self.conn.execute(f'PRAGMA table_info({self.table_name})').fetchall()
            if not columns:
                sanitized_columns = [sanitize_column_name(key) for key in data.keys()]
                datatypes = ["TEXT" if not isinstance(value, list) else "LIST" for value in data.values()]
                datatypes = ["DICT" if isinstance(value, dict) else datatype for value, datatype in zip(data.values(), datatypes)]
                columns_str = ', '.join([f"{col} {datatype}" for col, datatype in zip(sanitized_columns, datatypes)])
                self.conn.execute(f'CREATE TABLE IF NOT EXISTS {self.table_name} ({columns_str})')
            self.columns_initialized = True

    def insert(self, data):
        self.ensure_table_columns(data)
        sanitized_columns = [sanitize_column_name(key) for key in data.keys()]
        placeholders = ', '.join(['?'] * len(data))
        serialized_values = [serialize_value(value) for value in data.values()]
        
        sql = f"INSERT INTO {self.table_name} ({', '.join(sanitized_columns)}) VALUES ({placeholders})"
        self.conn.execute(sql, tuple(serialized_values))
        self.conn.commit()

    def remove(self, column_name, value):
        """
        Removes rows where the given column matches the given value.
        
        Returns:
            int: The number of rows removed.
        """
        sql = f"DELETE FROM {self.table_name} WHERE {column_name} = ?"
        cursor = self.conn.execute(sql, (value,))
        self.conn.commit()
        
        return cursor.rowcount
    def all(self):
        rows = self.conn.execute(f'SELECT * FROM {self.table_name}').fetchall()
        deserialized_rows = []
        for row in rows:
            deserialized_row = {}
            for idx, col in enumerate(self.conn.execute(f'PRAGMA table_info({self.table_name})')):
                column_name = col[1]
                column_type = col[2]
                value = row[idx]
                if column_type in ["LIST", "DICT"]:
                    value = json.loads(value)
                    # Additional deserialization for nested serialized values
                    if isinstance(value, dict):
                        for k, v in value.items():
                            if isinstance(v, str) and (v.startswith('{') or v.startswith('[')):
                                try:
                                    value[k] = json.loads(v)
                                except json.JSONDecodeError:
                                    pass
                deserialized_row[column_name] = value
            deserialized_rows.append(deserialized_row)
        return deserialized_rows



    def search(self, column, value):
        # This is a simple example of searching for rows based on a column's value
        # and then deserializing the result.
        sql = f"SELECT data FROM {self.table_name} WHERE {column} = ?"
        rows = self.conn.execute(sql, (value,)).fetchall()
        return [json.loads(row[0]) for row in rows]

    def get(self, column, value):
        sql = f"SELECT * FROM {self.table_name} WHERE {column} = ?"
        row = self.conn.execute(sql, (value,)).fetchone()
        if not row:
            return None
        
        deserialized_row = {}
        for idx, col in enumerate(self.conn.execute(f'PRAGMA table_info({self.table_name})')):
            column_name = col[1]
            column_type = col[2]
            value = row[idx]
            if column_type in ["LIST", "DICT"]:
                value = json.loads(value)
                # Additional deserialization for nested serialized values
                if isinstance(value, dict):
                    for k, v in value.items():
                        if isinstance(v, str) and (v.startswith('{') or v.startswith('[')):
                            try:
                                value[k] = json.loads(v)
                            except json.JSONDecodeError:
                                pass
            deserialized_row[column_name] = value
        return deserialized_row

    # To add more methods as needed to emulate TinyDB's API


db = SQLiteDB('mydatabase.db')
mappings_table = db.table('Mappings')

#--------------------------------------
#Convertor and mapping related stuff
#---------------------------------------
def table_exists(conn, table_name):
    """
    Check if a table exists in the SQLite database.
    
    Args:
    - conn: SQLite database connection
    - table_name: The name of the table to check

    Returns:
    - bool: True if the table exists, False otherwise
    """
    cursor = conn.execute(f"SELECT count(name) FROM sqlite_master WHERE type='table' AND name='{table_name}'")
    count = cursor.fetchone()[0]
    return count > 0

def remove_converter(converter_name):
    """
    Deletes a converter based on its name.
    
    Logic:
    - Find and delete the converter by name
    """
    converters_table = db.table('Converters')
    
    removed = converters_table.remove('name',converter_name)
    
    if removed:
        print(f"Converter {converter_name} removed successfully!")
    else:
        print(f"No converter found with the name {converter_name}")



def register_converter(name, converter_function_str):
    """
    Allow developers to register their custom converter functions.
    """
    
    converters_table = db.table('Converters')    
    converters_table.insert({
        "name": name,
        "function": converter_function_str
    })

def get_converter_function(converter_name):
    """
    Fetches the converter function from the database.
    """
    converters_table = db.table('Converters')  
    converter = converters_table.get("name", converter_name)
    if converter:
        # Assuming converter_code is Python code, using exec is a security risk.
        # You should have checks in place to ensure only safe code is executed.
        exec_globals = {}
        exec(converter["code"], exec_globals)
        return exec_globals.get(converter_name)
    return None

def check_mapping_exists(source_model, dest_model):
    """
    Check if a mapping exists for the given source and destination models.
    """
    if not table_exists(mappings_table.conn, mappings_table.table_name):
        print(f"Table {mappings_table.table_name} does not exist!")
        return None

    mapping = mappings_table.get("source", source_model)
    if mapping and mapping.get("destination") == dest_model:
        return mapping
    return None

def convert_data(data, source_model, dest_model):
    """
    Convert data from source model to destination model.
    """
    mapping = check_mapping_exists(source_model, dest_model)
    
    if not mapping:
        print("Mapping doesn't exist. Please provide a mapping.")
        prompt_user_for_converter_name()
        return None

    converter_name = mapping['converter']
    converters_table = db.table('Converters') 
    converter_record = converters_table.get("name", converter_name)
    if not converter_record:
        print(f"Converter {converter_name} not registered.")
        return None

    converter_func_str = converter_record["function"]
    # Execute the function string to get the function object
    exec(converter_func_str, globals())
    converter_func = globals().get(converter_name)
        
    if callable(converter_func):
        converted_data = converter_func(data)
        return converted_data
    else:
        print(f"Error: Couldn't retrieve converter function for {converter_name}.")
        return None

def prompt_user_for_converter_name():
    """
    Prompt the user to specify the name of the converter.
    """
    print("Use the endpoint to store a converter in the mapping table ")
    

def save_mapping(source_model, dest_model, converter_name):
    """
    Save the new mapping to the mappings table.
    """
    mappings_table.insert({
        "source": source_model,
        "destination": dest_model,
        "converter": converter_name
    })

def list_converters():
    """
    Retrieves a list of all registered converters.
    """
    # Get the 'Converters' table from the database
    converters_table = db.table('Converters')
    # Fetch all converters from the Converters table
    converters = converters_table.all()
    return converters

#-------------------------------------
#Converter functions 
#-------------------------------------

def rdf_to_ngsi_ld(rdf_data):
    # Parse RDF data
    g = Graph()
    g.parse(data=rdf_data, format='xml')
    
    # Convert RDF to JSON-LD (assuming you have a context defined)
    json_ld_data = g.serialize(format='json-ld', context={"@context": "your_context_url_or_dict_here"})
    
    return json_ld_data

def ngsi_ld_to_rdf(ngsi_ld_data):
    # Convert JSON-LD to RDF
    expanded = jsonld.expand(ngsi_ld_data)
    compacted = jsonld.compact(expanded, {"@context": "your_context_url_or_dict_here"})
    
    # Convert to RDF (assuming you want RDF/XML format)
    g = Graph().parse(data=json.dumps(compacted), format='json-ld')
    rdf_data = g.serialize(format='xml')
    
    return rdf_data



# ------------------------------------------------------------------------------
# Community Management API
# ------------------------------------------------------------------------------

def register_Community(community_Id, name, connection_Details, origin, role_In_Federation,
                       geographical_Location, has_Data_Models, part_Of_Federation, last_Updated):
    """
    Enables the integration of a new community into the IoT federation.
    """
    # Construct the Community entity in NGSI-LD format
    community_entity = {
        "id": community_Id,
        "type": "Community",
        "name": {"type": "Property", "value": name},
        "connectionDetails": {"type": "Property", "value": connection_Details},
        "origin": {"type": "Property", "value": origin},
        "roleInFederation": {"type": "Property", "value": role_In_Federation},
        "geographicalLocation": {"type": "Property", "value": geographical_Location},
        "hasDataModels": {"type": "Relationship", "object": has_Data_Models},
        "partOfFederation": {"type": "Relationship", "object": part_Of_Federation},
        "lastUpdated": {"type": "Property", "value": last_Updated},
        "@context": [
            "https://raw.githubusercontent.com/SAMSGBLab/CCduit/main/Data%20Models/Community/context.json",
            "https://uri.etsi.org/ngsi-ld/v1/ngsi-ld-core-context.jsonld"
        ]
    }
    
    # Get the 'Communities' table from the database
    communities_table = db.table('Communities')
    
    # Insert the entity into the 'Communities' table
    communities_table.insert(community_entity)
    print(f"Community {community_Id} Registered Successfully!")

def update_Community(community_Id, **kwargs):
    """
    Update the community with the given community_Id using the provided fields.
    """
    communities_table = db.table('Communities')
    
    # Construct the update data
    update_data = {}
    for key, value in kwargs.items():
        if value:  # Only add non-empty values
            update_data[key] = value

    # Update the community entity in the database
    communities_table.update(update_data, where('id') == community_Id)


def remove_Community(community_Id):
    """
    Facilitates the deletion of a community based on its unique identifier.
    """
    # Get the 'Communities' table from the database
    communities_table = db.table('Communities')
    
    # Remove the community with the specified ID from the Communities table
    removed = communities_table.remove('id',community_Id)
    
    if removed:
        print(f"Community {community_Id} Removed Successfully!")
    else:
        print(f"No Community found with ID {community_Id}")

def query_Community(community_Id):
    """
    Retrieves information about a specific community.
    """
    # Get the 'Communities' table from the database
    communities_table = db.table('Communities')
    
    # Query the Communities table for the specified ID
    community = communities_table.get('id', community_Id)
    
    return community

def list_Communities(federation_id=None):
    """
    Retrieves a list of all communities or those within a specific federation.
    """
    # Get the 'Communities' table from the database
    communities_table = db.table('Communities')
    
    if federation_id:
        # List communities within the specified federation
        communities = communities_table.search(where('partOfFederation')["object"] == federation_id)
    else:
        # Fetch all communities from the Communities table
        communities = communities_table.all()
    return communities


# ------------------------------------------------------------------------------
# Federation Management API
# ------------------------------------------------------------------------------

def register_Federation(federationId, name, topology, structure, areaCovered, number_Of_Nodes,
                        part_Of_Federation, includes_Communities, uses_Interactions, data_Sharing_Policy):
    federation_entity = {
        "id": federationId,
        "type": "Federation",
        "name": {"type": "Property", "value": name},
        "topology": {"type": "Property", "value": topology},
        "structure": {"type": "Property", "value": structure},
        "areaCovered": {"type": "Property", "value": areaCovered},
        "numberOfNodes": {"type": "Property", "value": number_Of_Nodes},
        "partOfFederation": {"type": "Relationship", "object": part_Of_Federation},
        "includesCommunities": {"type": "Relationship", "object": includes_Communities},
        "usesConnections": {"type": "Relationship", "object": uses_Interactions},
        "dataSharingPolicy": {"type": "Property", "value": data_Sharing_Policy},
        "@context": [
            "https://raw.githubusercontent.com/SAMSGBLab/CCduit/main/Data%20Models/Federation/context.json",
            "https://uri.etsi.org/ngsi-ld/v1/ngsi-ld-core-context.jsonld"
        ]
    }
    
    federations_table = db.table('Federations')
    federations_table.insert(federation_entity)
    print(f"Federation {federationId} Registered Successfully!")

def update_Federation(federation_Id, new_Topology, new_Structure, new_Number_Of_Nodes,
                      new_IncludesCommunities, new_Uses_Connections, new_Data_Sharing_Policy):
    federations_table = db.table('Federations')
    Federation = Query()
    federation = federations_table.get('id', federation_Id)
    if federation:
        federation['topology'] = new_Topology
        federation['structure'] = new_Structure
        federation['numberOfNodes'] = new_Number_Of_Nodes
        federation['includesCommunities'] = new_IncludesCommunities
        federation['usesConnections'] = new_Uses_Connections
        federation['dataSharingPolicy'] = new_Data_Sharing_Policy
        federations_table.update(federation, Federation.id == federation_Id)
        print(f"Federation {federation_Id} Updated Successfully!")
    else:
        print(f"Federation {federation_Id} Not Found!")

def remove_Federation(federation_Id):
    federations_table = db.table('Federations')
    removed = federations_table.remove('id',federation_Id)
    if removed:
        print(f"Federation {federation_Id} Removed Successfully!")
    else:
        print(f"Federation {federation_Id} Not Found!")

def query_Federation(federation_Id):
    federations_table = db.table('Federations')
    Federation = Query()
    federation = federations_table.get('id', federation_Id)
    return federation

def list_Federations():
    federations_table = db.table('Federations')
    federations = federations_table.all()
    return federations

# Implementing the query_community_federation function

def query_community_federation(community_id):
    """
    Given a community ID, return the federation to which the community belongs.
    """
    communities_table = db.table('Communities')
    Community = Query()
    community = communities_table.get('id', community_id)
    
    if community:
        return community.get('part_Of_Federation', None)
    else:
        return None
# ------------------------------------------------------------------------------
# Community Interaction API
# ------------------------------------------------------------------------------
def get_endpoint_url(community_id):
    """
    Fetch the endpoint URL for the given community from the database.
    """
    communities_table = db.table('Communities')
    community = communities_table.get('id', community_id)

    print("HERE IS AN ENDPOINT!!!!!!!!!!!!")
    print(community)
    
    if community and 'connectionDetails' in community:
        connection_details = community['connectionDetails'].get('value', {})
        if 'endpoint' in connection_details:
            return connection_details['endpoint']
    return None



def get_protocol(community_id):
    """
    Fetch the protocol for the given community from the database.
    """
    communities_table = db.table('Communities')
    community = communities_table.get('id', community_id)

    print("HERE IS AN ENDPOINT!!!!!!!!!!!!")
    print(community)
    
    if community and 'connectionDetails' in community:
        connection_details = community['connectionDetails'].get('value', {})
        if 'protocol' in connection_details:
            return connection_details['protocol']
    return None

def get_interaction_status(interaction_id):
    """
    Fetch the current status of the interaction.
    """
    interactions_table = db.table('CommunityInteractions')
    Interaction = Query()
    interaction = interactions_table.get('id', interaction_id)
    
    if interaction and 'connectionStatus' in interaction and 'value' in interaction['connectionStatus']:
        return interaction['connectionStatus']['value']
    else:
        return None

def compute_data_hash(data):
    """
    Compute the MD5 hash of the given data.
    """
    return hashlib.md5(str(data).encode()).hexdigest()

# Callback when a message is received
import functools

def on_message(client, userdata, message, target_data_model, dest_mqtt_client, destpath, destination_protocol, destination_endpoint):
    """
    This function will be invoked when a message is received on a subscribed topic.
    """
    print(f"Received message: {message.payload.decode('utf-8')} on topic {message.topic}")
    
    # Convert the received data using the data model mapping
    source_data = message.payload.decode('utf-8')
    converted_data = convert_data(source_data, userdata['source_data_model'], target_data_model)
    
    # Send the converted data to the destination based on its protocol
    if destination_protocol == "HTTP":
        destination_endpoint_with_path = str(destination_endpoint) + str(destpath)
        requests.post(destination_endpoint_with_path, json=converted_data)
    elif destination_protocol == "MQTT" and dest_mqtt_client:
        try:
            dest_mqtt_client.publish(str(destpath), converted_data)
        except Exception as e:
            print(f"Failed to publish to MQTT broker. Error: {e}")


def interaction_process(interaction_id, source_community, destination_community, Interaction_Type, 
                        source_data_model, target_data_model, sourcepath, destpath):
    """
    Process the interaction between source and destination communities.
    """
    print("TRYING TO SETUP INTERACTION")
    source_endpoint = get_endpoint_url(source_community)
    destination_endpoint = get_endpoint_url(destination_community)
    source_protocol = get_protocol(source_community)
    destination_protocol = get_protocol(destination_community)
    print("HERE IS WHAT I FOUND" + str(source_endpoint) + str(source_protocol) + str(destination_endpoint) + str(destination_protocol))
    
    previous_data_hash = None  # Store the hash of the previously fetched data
    dest_mqtt_client = None
    
    if source_protocol == "MQTT":
        source_mqtt_client = mqtt.Client(userdata={'source_data_model': source_data_model})
        customized_on_message = functools.partial(on_message, 
                                                  target_data_model=target_data_model, 
                                                  dest_mqtt_client=dest_mqtt_client, 
                                                  destpath=destpath, 
                                                  destination_protocol=destination_protocol, 
                                                  destination_endpoint=destination_endpoint)
        source_mqtt_client.on_message = customized_on_message
        source_mqtt_client.connect(source_endpoint)
        source_mqtt_client.subscribe(sourcepath)
        source_mqtt_client.loop_start()
    
    if destination_protocol == "MQTT":
        dest_mqtt_client = mqtt.Client()
        host, port = destination_endpoint.split(":")
        port = int(port)
        dest_mqtt_client.connect(host, port, 60)
        dest_mqtt_client.loop_start()
    
    while True:  # Continuous loop for checking interaction status
          # Sleep for a short duration
        interaction_status = get_interaction_status(interaction_id)
        
        if interaction_status == "Paused":
            print("I am paused")
            time.sleep(5)
            continue
        
        if source_protocol == "HTTP":
            time.sleep(5)
            source_endpoint_with_path = str(source_endpoint) + str(sourcepath)
            response = requests.get(source_endpoint_with_path)
            print(response)
            if response.status_code == 200 and response.content:
                source_data = response.json()
                print(source_data)
                if not source_data:
                    continue
                
                # Check if the fetched data has changed since the last iteration
                current_data_hash = compute_data_hash(source_data)
                print(current_data_hash)
                if current_data_hash == previous_data_hash:
                    continue  # Skip this iteration if the data hasn't changed

                previous_data_hash = current_data_hash

                converted_data = convert_data(source_data, source_data_model, target_data_model)
                
                # Send the converted data to the destination based on its protocol
                if destination_protocol == "HTTP":
                    destination_endpoint_with_path = str(destination_endpoint) + str(destpath)
                    requests.post(destination_endpoint_with_path, json=converted_data)
                elif destination_protocol == "MQTT" and dest_mqtt_client:
                    try:
                        dest_mqtt_client.publish(str(destpath), converted_data)
                    except Exception as e:
                        print(f"Failed to publish to MQTT broker. Error: {e}")
            else:
                print(f"Failed to fetch data from {source_endpoint_with_path}. Status code: {response.status_code}")


# Returning the modified function
#interaction_process




def create_Interaction(initiated_By, from_community, towards,Interaction_Type, Interaction_Status,source_data_model, target_data_model,sourcepath,destpath):
    """
    Enables the establishment of interactions between communities.
    """
    # 1. Create and Store the NGSI-LD Representation
    # Generate a unique identifier for the interaction
    unique_id = str(uuid.uuid4())[:8]  # Taking the first 8 characters for brevity

    # Construct the ID for the CommunityInteraction entity
    interaction_id = f"urn:ngsi-ld:CommunityInteraction:{from_community}:{towards}:{unique_id}"

    # Construct the CommunityInteraction entity in NGSI-LD format
    interaction_entity = {
        "id": interaction_id,
        "type": "CommunityInteraction",
        "initiatedBy": {"type": "Property", "value": initiated_By},
        "fromC": {"type": "Property", "value": from_community},
        "towardsC": {"type": "Property", "value": towards},
        "SourceSpecificPath": {"type": "Property", "value": sourcepath},
        "TargetSpecificPath": {"type": "Property", "value": destpath},
        "source_data_model": {"type": "Property", "value": source_data_model},
        "target_data_model": {"type": "Property", "value": target_data_model},
        "connectionType": {"type": "Property", "value": Interaction_Type},
        "connectionStatus": {"type": "Property", "value": Interaction_Status},
        "@context": [
            "https://raw.githubusercontent.com/SAMSGBLab/CCduit/main/Data%20Models/CommunityInteraction/context.json",
            "https://uri.etsi.org/ngsi-ld/v1/ngsi-ld-core-context.jsonld"
        ]
    }
    
    # Get the 'CommunityInteractions' table from the database
    interactions_table = db.table('CommunityInteractions')
    
    # 2. Validate the Interaction
    if not validate_Interaction(interaction_id):
        print("Interaction validation failed!")
        return

    # 3. Check if Communities are Part of a Federation
    from_community_federation = query_community_federation(from_community)
    towards_community_federation = query_community_federation(towards)

    # 4. Integration of Communities or Federations
    if not from_community_federation:
        integrate_Community(from_community, "FederationID", "Position")
    if not towards_community_federation:
        integrate_Community(towards, "FederationID", "Position")
    if from_community_federation and towards_community_federation:
        integrate_Federation(from_community_federation, towards_community_federation, "Position")

    # Spawn a new process for the interaction based on its type
    process = multiprocessing.Process(target=interaction_process, args=(interaction_id,from_community,towards,Interaction_Type,source_data_model,target_data_model,sourcepath,destpath))
    process.start()

    # Store the process ID (PID) in the interaction's NGSI-LD data
    interaction_entity["processId"] = {"type": "Property", "value": process.pid}

    # Insert the entity into the 'CommunityInteractions' table
    interactions_table.insert(interaction_entity)

    print(f"Interaction from {from_community} to {towards} Created Successfully!")


def query_Interaction(interaction_id):
    """
    Retrieves information about a specific interaction.
    """
    interactions_table = db.table('CommunityInteractions')
    Interaction = Query()
    interaction = interactions_table.get('id', interaction_id)
    return interaction

def validate_Interaction(interaction_id):
    """
    Ensures interactions adhere to set policies and data models.
    """
    #its fake for now
    return True
    # For the sake of this example, let's assume a simple validation
    interaction = query_Interaction(interaction_id)
    if interaction:
        # Check compatibility of data models (this is a placeholder and should be replaced with actual logic)
        compatible_data_models = True
        # Validate against set policies (this is a placeholder and should be replaced with actual logic)
        valid_policies = True
        
        return compatible_data_models and valid_policies
    #its fake for now
    return False

def monitor_Interaction(interaction_id):
    """
    Provides real-time information about the data flow in an interaction.
    """
    # This function would typically interface with a monitoring system or tool.
    # return a placeholder response for now.
    return {"dataFlow": "Normal", "status": "Active"}

def pause_Interaction(interaction_id):
    """
    Pauses an ongoing interaction.
    """
    interactions_table = db.table('CommunityInteractions')
    Interaction = Query()
    updated = interactions_table.update({"connectionStatus": {"type": "Property", "value": "Paused"}}, Interaction.id == interaction_id)
    if updated:
        print(f"Interaction {interaction_id} Paused Successfully!")
    else:
        print(f"Failed to Pause Interaction {interaction_id}")

def resume_Interaction(interaction_id):
    """
    Resumes a paused interaction.
    """
    interactions_table = db.table('CommunityInteractions')
    Interaction = Query()
    updated = interactions_table.update({"connectionStatus": {"type": "Property", "value": "Active"}}, Interaction.id == interaction_id)
    if updated:
        print(f"Interaction {interaction_id} Resumed Successfully!")
    else:
        print(f"Failed to Resume Interaction {interaction_id}")

def terminate_Interaction(interaction_id):
    # Retrieve the interaction's data from the database
    interaction_data = query_Interaction(interaction_id)
    pid = interaction_data["processId"]["value"]

    # Terminate the process
    try:
        os.kill(pid, signal.SIGTERM)  # Sends the SIGTERM signal to the process
    except ProcessLookupError:
        print(f"No process with PID {pid} found.")
    except PermissionError:
        print(f"Permission denied to terminate PID {pid}.")   

def list_Interactions():
    """
    Retrieves a list of all interactions.
    """
    interactions_table = db.table('CommunityInteractions')
    return interactions_table.all()



def remove_Interaction(interaction_id):
    """
    Deletes an interaction based on its unique identifier.
    
    Logic:
    - Find and delete the interaction by ID
    """
    terminate_Interaction(interaction_id)  
    interactions_table = db.table('CommunityInteractions')
    Interaction = Query()
    removed = interactions_table.remove('id',interaction_id)
    
    if removed:
        print(f"Interaction {interaction_id} Removed Successfully!")
    else:
        print(f"No Interaction found with ID {interaction_id}")
      

# ------------------------------------------------------------------------------
# Integration API
# ------------------------------------------------------------------------------

def integrate_Community(community_Id, federation_Id, position=None):
    """
    Integrates a community into a federation.
    
    Logic:
    - Validate community and federation IDs
    - Add community to federation at provided/automatic position
    """
    pass


def integrate_Federation(federation1_Id, federation2_Id, position=None):
    """
    Integrates one federation into another.
    
    Logic:
    - Validate federation IDs
    - Integrate federations at provided/automatic position
    """
    pass


# ------------------------------------------------------------------------------
# Data Model Management API
# ------------------------------------------------------------------------------

def register_DataModel(dataModel_Id, name, description, model_Format, specific_Ontology,
                       ontology_Version, ontology_URL, associated_Communities, dataSharing_Policy):
    # Construct the NGSI-LD entity
    data_model_entity = {
        "id": dataModel_Id,
        "type": "DataModel",
        "name": {"type": "Property", "value": name},
        "description": {"type": "Property", "value": description},
        "modelFormat": {"type": "Property", "value": model_Format},
        "ontology": {"type": "Property", "value": specific_Ontology},
        "ontologyVersion": {"type": "Property", "value": ontology_Version},
        "ontologyURL": {"type": "Property", "value": ontology_URL},
        "associatedCommunities": {"type": "Relationship", "object": associated_Communities},
        "dataSharingPolicy": {"type": "Property", "value": dataSharing_Policy},
        "@context": [
            "https://raw.githubusercontent.com/SAMSGBLab/CCduit/main/Data%20Models/DataModel/context.json",
            "https://uri.etsi.org/ngsi-ld/v1/ngsi-ld-core-context.jsonld"
        ]
    }
    
    # Get the 'DataModels' table from the database
    data_models_table = db.table('DataModels')
    
    # Insert the entity into the 'DataModels' table
    data_models_table.insert(data_model_entity)
    print(f"Data Model {dataModel_Id} Registered Successfully!")


def update_Data_Model(dataModel_Id, new_Description, new_Model_Format, new_Specific_Ontology, 
                      new_Ontology_Version, new_Ontology_URL, new_Associated_Communities, new_DataSharing_Policy):
    """
    Allows for the modification of data model information.
    
    Logic:
    - Find the data model by ID
    - Update the provided attributes
    """
    
    # Define a table for data models in the database
    data_models_table = db.table('DataModels')
    
    # Query object for TinyDB
    DataModel = Query()
    
    # Check if the data model exists
    existing_data_model = data_models_table.get('id', dataModel_Id)
    
    if existing_data_model:
        # Update the attributes
        data_models_table.update({
            "description": {"type": "Property", "value": new_Description},
            "modelFormat": {"type": "Property", "value": new_Model_Format},
            "ontology": {"type": "Property", "value": new_Specific_Ontology},
            "ontologyVersion": {"type": "Property", "value": new_Ontology_Version},
            "ontologyURL": {"type": "Property", "value": new_Ontology_URL},
            "associatedCommunities": {"type": "Relationship", "object": new_Associated_Communities},
            "dataSharingPolicy": {"type": "Property", "value": new_DataSharing_Policy}
        }, DataModel.id == dataModel_Id)
        
        print(f"Data Model {dataModel_Id} Updated Successfully!")
    else:
        print(f"No Data Model found with ID {dataModel_Id}")


def remove_DataModel(data_Model_Id):
    # Define a table for data models in the database
    data_models_table = db.table('DataModels')
    
    # Remove the data model with the specified ID from the DataModels table
    removed = data_models_table.remove('id',data_Model_Id)
    
    # Check if a data model was removed and display the appropriate message
    if removed:
        print(f"Data Model {data_Model_Id} Removed Successfully!")
        #dpg.set_value('Logging Text', f"Data Model {data_Model_Id} Removed Successfully!")
    else:
        print(f"No Data Model found with ID {data_Model_Id}")
        #dpg.set_value('Logging Text', f"No Data Model found with ID {data_Model_Id}")


def query_DataModel(data_model_id):
    # Define a table for data models in the database
    data_models_table = db.table('DataModels')
    
    # Query the DataModels table for the specified ID
    DataModel = Query()
    data_model = data_models_table.get('id', data_model_id)
    
    return data_model


def list_DataModels():
    # Define a table for data models in the database
    data_models_table = db.table('DataModels')
    
    # Fetch all data models from the DataModels table
    data_models = data_models_table.all()
    
    # Display the data models in the GUI
    return data_models




def validate_DataModel(dataModel_Id):
    """
    Checks the integrity and correctness of a data model.
    
    Logic:
    - Validate data model structure and contents
    """
    pass


def convert_DataModel(source_DataModel_Id, target_DataModel_Id, mapping):
    """
    Converts one data model into another.
    
    Logic:
    - Use provided mapping to convert source data model to target model
    """
    pass

# Additional prototype functions

def usage():
    """
    Provides the usage information for the CCduit API.
    
    Logic:
    - Print out information and examples of using the API 
    """
    pass




#------------------------------------------------------
#FLASK API FUNCTIONS
#---------------------------------------------------------
@app.route('/register_data_model', methods=['POST'])
def register_data_model_api():
    data = request.json
    register_DataModel(data['dataModel_Id'], data['name'], data['description'], data['model_Format'], 
                       data['specific_Ontology'], data['ontology_Version'], data['ontology_URL'], 
                       data['associated_Communities'], data['dataSharing_Policy'])
    return jsonify({"message": f"Data Model {data['dataModel_Id']} Registered Successfully!"})

@app.route('/update_data_model', methods=['PUT'])
def update_data_model_api():
    data = request.json
    update_Data_Model(data['dataModel_Id'], data['new_Description'], data['new_Model_Format'], 
                      data['new_Specific_Ontology'], data['new_Ontology_Version'], data['new_Ontology_URL'], 
                      data['new_Associated_Communities'], data['new_DataSharing_Policy'])
    return jsonify({"message": f"Data Model {data['dataModel_Id']} Updated Successfully!"})

@app.route('/remove_data_model/<data_Model_Id>', methods=['DELETE'])
def remove_data_model_api(data_Model_Id):
    remove_DataModel(data_Model_Id)
    return jsonify({"message": f"Data Model {data_Model_Id} Removed Successfully!"})

@app.route('/query_data_model/<data_model_id>', methods=['GET'])
def query_data_model_api(data_model_id):
    data_model = query_DataModel(data_model_id)
    if data_model:
        return jsonify(data_model)
    else:
        return jsonify({"message": f"No Data Model Found for ID: {data_model_id}"}), 404

@app.route('/list_data_models', methods=['GET'])
def list_data_models_api():
    data_models = list_DataModels()
    return jsonify(data_models)


@app.route('/register_community', methods=['POST'])
def register_community_endpoint():
    data = request.json
    register_Community(
        data['community_Id'],
        data['name'],
        data['connection_Details'],
        data['origin'],
        data['role_In_Federation'],
        data['geographical_Location'],
        data['has_Data_Models'],
        data['part_Of_Federation'],
        data['last_Updated']
    )
    return jsonify({"message": "Community registered successfully!"}), 201

@app.route('/update_community/<community_Id>', methods=['PUT'])
def update_community_endpoint(community_Id):
    data = request.json
    update_Community(
        community_Id,
        data['new_Data_Models'],
        data['new_Last_Updated']
    )
    return jsonify({"message": "Community updated successfully!"})

@app.route('/remove_community/<community_Id>', methods=['DELETE'])
def remove_community_endpoint(community_Id):
    remove_Community(community_Id)
    return jsonify({"message": "Community removed successfully!"})

@app.route('/query_community/<community_Id>', methods=['GET'])
def query_community_endpoint(community_Id):
    community = query_Community(community_Id)
    if community:
        return jsonify(community)
    else:
        return jsonify({"message": "Community not found!"}), 404

@app.route('/list_communities', methods=['GET'])
def list_communities_endpoint():
    federation_id = request.args.get('federation_id')
    communities = list_Communities(federation_id)
    return jsonify(communities)

@app.route('/register_federation', methods=['POST'])
def register_federation_endpoint():
    data = request.json
    register_Federation(
        data['federationId'],
        data['name'],
        data['topology'],
        data['structure'],
        data['areaCovered'],
        data['number_Of_Nodes'],
        data['part_Of_Federation'],
        data['includes_Communities'],
        data['uses_Interactions'],
        data['data_Sharing_Policy']
    )
    return jsonify({"message": "Federation registered successfully!"}), 201

@app.route('/update_federation/<federation_Id>', methods=['PUT'])
def update_federation_endpoint(federation_Id):
    data = request.json
    update_Federation(
        federation_Id,
        data['new_Topology'],
        data['new_Structure'],
        data['new_Number_Of_Nodes'],
        data['new_IncludesCommunities'],
        data['new_Uses_Connections'],
        data['new_Data_Sharing_Policy']
    )
    return jsonify({"message": "Federation updated successfully!"})

@app.route('/remove_federation/<federation_Id>', methods=['DELETE'])
def remove_federation_endpoint(federation_Id):
    remove_Federation(federation_Id)
    return jsonify({"message": "Federation removed successfully!"})

@app.route('/query_federation/<federation_Id>', methods=['GET'])
def query_federation_endpoint(federation_Id):
    federation = query_Federation(federation_Id)
    if federation:
        return jsonify(federation)
    else:
        return jsonify({"message": "Federation not found!"}), 404

@app.route('/list_federations', methods=['GET'])
def list_federations_endpoint():
    federations = list_Federations()
    return jsonify(federations)

@app.route('/create_interaction', methods=['POST'])
def create_interaction_endpoint():
    data = request.json
    create_Interaction(
        data['initiated_By'],
        data['from_community'],
        data['towards'],
        data['interaction_Type'],
        data['interaction_Status'],
        data['source_data_model'],
        data['target_data_model'],
        data['source_path'],
        data['dest_path']
    )
    return jsonify({"message": "Interaction created successfully!"})


@app.route('/query_interaction/<interaction_id>', methods=['GET'])
def query_interaction_endpoint(interaction_id):
    interaction = query_Interaction(interaction_id)
    return jsonify(interaction)

@app.route('/validate_interaction/<interaction_id>', methods=['GET'])
def validate_interaction_endpoint(interaction_id):
    validation_result = validate_Interaction(interaction_id)
    return jsonify({"validation": validation_result})

@app.route('/monitor_interaction/<interaction_id>', methods=['GET'])
def monitor_interaction_endpoint(interaction_id):
    monitoring_data = monitor_Interaction(interaction_id)
    return jsonify(monitoring_data)

@app.route('/pause_interaction/<interaction_id>', methods=['PUT'])
def pause_interaction_endpoint(interaction_id):
    pause_Interaction(interaction_id)
    return jsonify({"message": "Interaction paused successfully!"})

@app.route('/resume_interaction/<interaction_id>', methods=['PUT'])
def resume_interaction_endpoint(interaction_id):
    resume_Interaction(interaction_id)
    return jsonify({"message": "Interaction resumed successfully!"})
    
@app.route('/list_interactions', methods=['GET'])
def list_interactions_endpoint():
    interactions = list_Interactions()
    return jsonify(interactions)

@app.route('/remove_interaction/<interaction_Id>', methods=['DELETE'])
def remove_interaction_endpoint(interaction_Id):
    remove_Interaction(interaction_Id)
    return jsonify({"message": "interaction removed successfully!"})


@app.route('/save_mapping', methods=['POST'])
def save_mapping_endpoint():
    try:
        data = request.json
        
        # Extract the required parameters from the JSON data
        source_model = data["source_model"]
        dest_model = data["dest_model"]
        converter_name = data["converter_name"]
        
        # Insert the mapping into the table
        mappings_table.insert({
            "source": source_model,
            "destination": dest_model,
            "converter": converter_name
        })

        return jsonify({"message": "Mapping saved successfully!"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/register_converter', methods=['POST'])
def register_converter_endpoint():
    data = request.get_json()

    # Extract name and function from the request data
    name = data.get('name')
    function_str = data.get('function')

    # Validate received data
    if not name or not function_str:
        return jsonify({'error': 'Both "name" and "function" fields are required!'}), 400

    # Save the function string in the database
    register_converter(name, function_str)

    return jsonify({'message': 'Converter function registered successfully!'}), 201

@app.route('/remove_converter/<converter_name>', methods=['DELETE'])
def remove_converter_endpoint(converter_name):
    remove_converter(converter_name)
    return jsonify({"message": f"Converter {converter_name} removed successfully!"})

@app.route('/list_converters', methods=['GET'])
def list_converters_endpoint():
    converters = list_converters()
    return jsonify({"converters": converters})


if __name__ == "__main__":
    app.run(debug=True)


