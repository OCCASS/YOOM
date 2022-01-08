from collections import namedtuple

SpriteHit = namedtuple('SpriteHit', ['sprite_index', 'distance', 'angel', 'casted_ray_index', 'texture'])
RayCastHit = namedtuple('RayCastHit', ['distance', 'point', 'angel', 'offset'])
