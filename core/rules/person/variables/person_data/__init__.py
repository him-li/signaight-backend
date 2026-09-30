from .posts import PostsVariables
from .work import WorkVariables
from .interests import InterestsVariables
from .location import LocationVariables
from .intro import IntroVariables
from .connections import ConnectionsVariables


class PersonDataVariables(PostsVariables,
                          WorkVariables,
                          InterestsVariables,
                          LocationVariables,
                          IntroVariables,
                          ConnectionsVariables
                          ):
    pass
