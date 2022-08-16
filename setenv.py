import json


def create_json():
    default = {
        "Name": None,
        "Levels": {
            "Easy":
                (3, 3),
            "Normal":
                (5, 5),
            "Amateur":
                (9, 7),
            "Hard":
                (11, 11),
            "Insane":
                (11, 21),
        }
    }

    with open("config.json", "w") as file:
        json.dump(default, file, indent=4)


if __name__ == "__main__":
    create_json()
