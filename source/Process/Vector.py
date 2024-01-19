from math import sqrt, pi, sin, cos


# Some maths to work out the unit vector between two positions
def unit_vector(pos1: tuple[float, float] | list[int], pos2: tuple[float, float] | list[int]) -> tuple[float, float]:
    pos1, pos2 = tuple[float, float](pos1), tuple[float, float](pos2)
    # Find the vector itself
    vector: tuple[float, float] = __vector_from_pos(pos1, pos2)
    # Then find the magnitude of that vector
    vector_mag: float = __magnitude(vector)
    # Then divide each part of the vector by the magnitude, and return it
    #   (as a float tuple)
    return tuple[float, float](map(lambda x: x/vector_mag, vector))


def unit_vector_from_angle(normalised_angle: float) -> tuple[float, float]:
    angle = normalised_angle*0.5*pi
    x: float = -cos(angle) if normalised_angle < 0 else cos(angle)
    y: float = sin(angle) if normalised_angle < 0 else -sin(angle)
    return x, y


def distance(pos1: tuple[float, float], pos2: tuple[float, float]) -> float:
    # First find the vector itself
    vector: tuple[float, float] = __vector_from_pos(pos1, pos2)
    # Then find the Euclidean distance between the two points
    return __magnitude(vector)


def __magnitude(vector: tuple[float, float]) -> float:
    # Find the Euclidean distance between the two points
    return sqrt(vector[0]**2 + vector[1]**2)


def __vector_from_pos(pos1: tuple[float, float], pos2: tuple[float, float]) -> tuple[float, float]:
    return pos1[0]-pos2[0], pos1[1]-pos2[1]
