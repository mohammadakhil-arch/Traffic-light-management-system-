import pandas as pd
import random

def generate_data():
    lights = []

    for i in range(1, 21):
        voltage = random.choice([230, 230, 230, 0])
        current = random.uniform(0, 2)
        temperature = random.randint(30, 90)

        status = "ON" if voltage > 0 else "OFF"

        lights.append([
            f"SL{i:03}",
            voltage,
            round(current, 2),
            temperature,
            status,
            18.5200 + i * 0.001,
            73.8560 + i * 0.001
        ])

    df = pd.DataFrame(lights, columns=[
        "light_id", "voltage", "current", "temperature",
        "status", "latitude", "longitude"
    ])

    df.to_csv("data/street_lights.csv", index=False)

if __name__ == "__main__":
    generate_data()
