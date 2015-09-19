import json
import io
from os.path import join as pjoin
from config import CONVERSIONS, SIMULATIONS_PATH


def parse_map(name):
    """ parses a map from a file. The first line contains the map width
    and the second line contains the corresponding height, followed
    by the actual map data.

    See the example below for a simple map and config.CONVERSIONS for
    the representation. Note: Only quadratic maps are currently supported.

        WWWW
        W  W
        W  W
        WWWW

    name -- file name regarding the map (located in SIMULATIONS_PATH)
    """

    with io.open(pjoin(SIMULATIONS_PATH, name)) as map_stream:
        lines = map_stream.read().splitlines()
        width = int(lines[0])
        height = int(lines[1])

        rows = []
        for i, l in enumerate(lines[2:]):
            if len(l) != width:
                raise ValueError("Line %d  has invalid length: %d, should be %d according to header" % (i, len(l), width))
            rows.append(list(map(lambda x: int(CONVERSIONS[x]), l)))

        if len(rows) != height:
            raise ValueError(
                "parseMap: Read invalid number of lines: %d should be %d according to header" % (len(rows), height))

        return rows, width, height


def parse_simulation_params(name, additional_params):
    with io.open(pjoin(SIMULATIONS_PATH, name)) as sim_stream:
        params = json.load(sim_stream)

        #Override some parameters from additional_params which are given explicitly from the console
        for param in additional_params:
            k, v = param.split("=")
            params[k.strip()] = int(v.strip())

        return params

