import paho.mqtt.client as mqtt
import json
from multiprocessing import Process
from uuid import uuid4
from datetime import datetime, timezone
import requests
import config as config
import time
import MQTT_Bridge as bridge
import threading
from threading import Event
import time
# MQTT and Context Broker configurations from config.py
FED_BROKER = config.FED_BROKER
FED_PORT = config.FED_PORT
CONTEXT_BROKER_URL = config.CONTEXT_BROKER_URL
FEDERATION_ID = config.FEDERATION_ID

def fetch_request_by_federation_sender(federation_id):
    """
    Fetch collaboration responses where the given federation is the receiver.
    """
    try:
        url = (
            f"{CONTEXT_BROKER_URL}?type=CollaborationRequest"
            f"&q=status==active&q=sender==%22{federation_id}%22"
            f"&attrs=senderAddress&options=keyValues"
        )
        response = requests.get(url, headers={"Content-Type": "application/json"})
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching response for federation receiver: {e}")
        return None


def fetch_response_by_federation_sender(federation_id):
    """
    Fetch collaboration responses where the given federation is the receiver.
    """
    try:
        url = (
                        f"{CONTEXT_BROKER_URL}?type=CollaborationResponse"
                        f"&q=responseStatus==ok&q=sender==%22{federation_id}%22"
                        f"&attrs=senderAddress&options=keyValues"
                    )
        response = requests.get(url, headers={"Content-Type": "application/json"})
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching response for federation receiver: {e}")
        return None

address=fetch_request_by_federation_sender("urn:ngsi-ld:Federation:Federation1")[0].get("senderAddress")
print(address)

address=fetch_response_by_federation_sender("urn:ngsi-ld:Federation:Federation2")
sender_address = address[0].get("senderAddress")
print(sender_address)