from collections import namedtuple

SpriteHit = namedtuple('SpriteHit', ['distance', 'angel', 'casted_ray_index'])
RayCastHit = namedtuple('RayCastHit', ['distance', 'point', 'angel', 'offset'])
