from  Interaction_Handling_Service import create_Interaction

def main():
    print("Creating interaction ...")
    interaction_id, pid = create_Interaction(
        "Federation1", "Community2", "Community1", "community", "active",
        "NGSI-LD", "Brick", "/?type=OccupancyReading", "community2/occupancy"
    )
    print(f"Interaction created with ID: {interaction_id} and PID: {pid}")

if __name__ == '__main__':
    main()