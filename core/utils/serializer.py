import json

class Serializer:
    # Serialize an object to a JSON string
    @staticmethod
    def serialize(obj) -> str:
        if hasattr(obj, "to_dict"):
            obj = obj.to_dict()

        return json.dumps(
            obj,
            sort_keys=True,
            separators=(',', ':'))