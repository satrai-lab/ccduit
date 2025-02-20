import time
import random
import Policy_Management_Service as pm

# Script for testing purposes:
def main():
    base_list = ["community", "federation", "policies", "functions"]

    for i in range(0, 100):
        # Ensure 'policies' is always present and immutable
        modifiable_list = [item for item in base_list if item != "policies"]

        # Randomly decide to add or remove elements from the modifiable list
        if random.choice([True, False]):
            # Randomly remove an element (if there are elements to remove)
            if modifiable_list:
                modifiable_list.remove(random.choice(modifiable_list))
        else:
            # Randomly add an element (if not already in the list)
            options_to_add = [item for item in ["community", "federation", "functions"] if item not in modifiable_list]
            if options_to_add:
                modifiable_list.append(random.choice(options_to_add))

        # Re-add 'policies' to ensure it's always included
        modifiable_list.append("policies")
        print(modifiable_list)
        pm.create_publish_policy(
            "Policy1",
            "policy1 test",
            "just testing 100 times",
            "Federation1",
            modifiable_list,  # Updated list for each iteration
            [
                {"Federation2": {"canReceive": "true", "canForward": "true"}},
                {"public": {"canReceive": "true", "canForward": "true"}},
            ],
            "Niemat",
            []
        )

        time.sleep(2)

if __name__ == "__main__":
    main()
