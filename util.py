from config import DIR_VEC_MAPPING


def is_even(num):
    return num & 1


def decode_rot(direction):
    """Decodes a rotation from a direction"""
    inv_dict = {v: k for k, v in DIR_VEC_MAPPING.items()}
    return inv_dict[direction]


def encode_rot(x, y):
    """Encodes a rotation into a direction"""
    return DIR_VEC_MAPPING[(x, y)]


def rotate(direction, degrees):
    """
    rotates a direction.
    degrees must be one of +-[45,90]
    """

    if abs(degrees) == 45:
        res = direction + 1 if degrees > 0 else direction - 1
    elif abs(degrees) == 90:
        res = direction + 2 if degrees > 0 else direction - 2
    else:
        raise ValueError("Invalid value for degrees: %d" % degrees)

    # make sure that the values are in range [1,8]
    possible_results = {0: 8, -1: 7, 9: 1, 10: 2}
    return possible_results.get(res, res)
