import numpy as np
import base64
import zlib


from object import object_kinds
from constants import GROUND_HEIGHT


def parse_level_string(txt: str):
    object_strings = txt.split(';')

    objects = []

    for objstr in object_strings:
        raw_properties = objstr.split(',')
        properties = {}
        for i in range(len(raw_properties) // 2):
            properties[raw_properties[2 * i]] = raw_properties[2 * i + 1]

        objects.append(properties)

    # TODO: handle level start object
    objects = objects[1:]

    level_objects = []
    for obj in objects:
        if ('1' not in obj.keys()) or (int(obj['1']) not in object_kinds.keys()):
            continue

        kind = object_kinds[int(obj['1'])]
        x = float(obj.get('2', '0.0'))
        y = float(obj.get('3', '0.0'))+GROUND_HEIGHT
        hflip = bool(obj.get('4', False))
        vflip = bool(obj.get('5', False))
        rotation = float(obj.get('6', 0.0))

        level_objects.append(kind.new(
            position=np.array([x, y]),
            hflip=hflip,
            vflip=vflip,
            rotation=rotation,
        ))

    return level_objects


def parse_level(path: str):
    with open(path) as f:
        base64_decoded = base64.urlsafe_b64decode(f.read().encode())
        # window_bits = 15 | 32 will autodetect gzip or not
        decompressed = zlib.decompress(base64_decoded, 15 | 32)
        return parse_level_string(decompressed.decode())
