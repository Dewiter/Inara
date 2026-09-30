import json
import zlib

import zmq

EDDN_URL = "tcp://eddn.edcd.io:9500"


def listen():
    context = zmq.Context()
    socket = context.socket(zmq.SUB)
    socket.connect(EDDN_URL)
    socket.setsockopt_string(zmq.SUBSCRIBE, "")
    print("Connected to EDDN")

    while True:
        message = socket.recv()
        try:
            decompressed = zlib.decompress(message)
            data = json.loads(decompressed)
        except (zlib.error, json.JSONDecodeError) as error:
            print(f"Could not decode EDDN message: {error}")
            continue

        schema = data.get("$schemaRef", "")

        if "commodity" in schema:
            print(json.dumps(data, indent=2))


if __name__ == "__main__":
    listen()
