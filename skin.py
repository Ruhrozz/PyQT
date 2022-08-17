def get_color(name):
    color = {
        "Standard":
            {
                "Window":
                    "background-color: grey;",
                "Restart":
                    "background-color: #a0a0a0",
                "Tiles": [
                    "background-color: #a0a0a0; border-style: inset; border-width: 1px",
                    "background-color: #282828; border-style: outset;",
                ],
            },
        "Desert":
            {
                "Window":
                    "background-color: #fbe1b6;",
                "Restart":
                    "background-color: #daa46d;",
                "Tiles": [
                    "background-color: #daa46d; border-style: inset; border-width: 1px",
                    "background-color: #9c4f20; border-style: outset;",
                ],
            },
        "Cake":
            {
                "Window":
                    "background-color: #e7d6d2;",
                "Restart":
                    "background-color: #b56965;",
                "Tiles": [
                    "background-color: #b56965; border-style: inset; border-width: 1px",
                    "background-color: #613439; border-style: outset;",
                ],
            },
    }
    return color[name]
