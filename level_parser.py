import numpy as np

from obj_kinds import obj_kinds
from constants import *

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
        if ('1' not in obj.keys()) or (int(obj['1']) not in obj_kinds.keys()):
            continue

        kind = obj_kinds[int(obj['1'])]
        x = float(obj.get('2', '0.0'))
        y = float(obj.get('3', '0.0'))+GROUND_HEIGHT

        level_objects.append(kind.new(np.array([x, y])))

    return level_objects


def parse_level(path: str):
    with open(path) as f:
        return parse_level_string(f.read())
