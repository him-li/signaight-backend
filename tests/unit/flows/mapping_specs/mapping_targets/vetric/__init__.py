from .facebook import Targets as FacebookTargets
from .instagram import Targets as InstagramTargets
from .linkedin import Targets as LinkedinTargets
from .twitter import Targets as TwitterTargets


class Targets(
        FacebookTargets,
        InstagramTargets,
        LinkedinTargets,
        TwitterTargets):
    pass
