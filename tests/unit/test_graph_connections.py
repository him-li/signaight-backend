from core.models.utils.update_connection_graph import (
    GraphBuilder,
    build_dynamic_view,
    nx_to_cytoscape,
    rewrite_relationships,
)
import pytest
import networkx as nx


@pytest.fixture
def builder():
    return GraphBuilder()


@pytest.fixture
def sample_person():
    return {
        "id": "1",
        "personal_details": {
            "name": {
                "first_name": {"f_name": "John"},
                "last_name": {"l_name": "Doe"},
            }
        },
        "risk_score": 0.5,
        "signaight_score": 0.8,
    }


@pytest.fixture
def person_with_interests():
    return {
        "id": "2",
        "interests": {
            "pages": [
                {
                    "fb_page_id": "999",
                    "fb_page_name": "Test Page",
                    "fb_page_url": "https://facebook.com/page",
                }
            ],
            "groups": {
                "telegram_groups": [
                    {"telegram_public_group_id": "tg1", "title": "Telegram Group"}
                ]
            },
        },
    }


@pytest.fixture
def person_with_checkins():
    return {
        "id": "p1",
        "personal_details": {
            "location": {
                "check_ins": {
                    "fb_check_ins": [
                        {
                            "title": "Test Place",
                            "subtitle": "Some subtitle",
                            "url": "https://facebook.com/test",
                            "region": "Test Region",
                            "date": "2024-07-03",
                            "event_image": "https://image.com/test.jpg",
                        }
                    ]
                }
            }
        },
    }


@pytest.fixture
def person_with_hometown():
    return {
        "id": "p1",
        "personal_details": {
            "location": {
                "hometown": {
                    "fb_location_id": "123",
                    "fb_location_picture": "https://image.com/home.jpg",
                    "fb_hometown": "Test City",
                }
            }
        },
    }


# safe_get tests
@pytest.mark.anyio
def test_safe_get_success(builder):
    obj = {"a": {"b": {"c": 10}}}

    result = builder.safe_get(obj, "a", "b", "c", default=None)

    assert result == 10


@pytest.mark.anyio
def test_safe_get_missing(builder):
    obj = {"a": {}}

    result = builder.safe_get(obj, "a", "b", default="fallback")

    assert result == "fallback"


# person node tests
@pytest.mark.anyio
def test_add_person(builder, sample_person):

    node = builder.add_person(sample_person)

    assert node == "person:1"
    assert builder.G.has_node(node)

    data = builder.G.nodes[node]

    assert data["type"] == "person"
    assert data["name"] == "John Doe"
    assert data["risk_score"] == 0.5


# interests tests
@pytest.mark.anyio
def test_add_interests(builder, person_with_interests):

    person_node = builder.add_person(person_with_interests)

    builder.add_interests(person_node, person_with_interests)

    assert builder.G.has_node("fb_page:999")
    assert builder.G.has_edge(person_node, "fb_page:999")

    edge = builder.G[person_node]["fb_page:999"]

    assert edge["relation"] == "likes_page"


@pytest.mark.anyio
def test_add_telegram_group(builder, person_with_interests):

    person_node = builder.add_person(person_with_interests)

    builder.add_interests(person_node, person_with_interests)

    assert builder.G.has_node("telegram_group:tg1")
    assert builder.G.has_edge(person_node, "telegram_group:tg1")

    edge = builder.G[person_node]["telegram_group:tg1"]

    assert edge["relation"] == "member_of_group"


# build graph test
@pytest.mark.anyio
def test_build_graph(builder, sample_person):

    persons = [sample_person]

    G = builder.build(persons)

    assert G.has_node("person:1")
    assert isinstance(G, nx.DiGraph)


# extract_check_ins
def test_extract_check_ins_success(builder, person_with_checkins):

    result = builder.extract_check_ins(person_with_checkins)

    assert len(result) == 1
    assert result[0]["title"] == "Test Place"
    assert result[0]["region"] == "Test Region"
    assert result[0]["date"] == "2024-07-03"
    assert result[0]["picture"] == "https://image.com/test.jpg"


def test_extract_check_ins_empty(builder):

    person = {"personal_details": {"location": {"hometown": None}}}

    result = builder.extract_check_ins(person)

    assert result == []


# add_check_ins
def test_add_check_ins_creates_nodes(builder, person_with_checkins):

    person_node = "person:p1"
    builder.G.add_node(person_node)

    builder.add_check_ins(person_node, person_with_checkins)

    # container node
    assert "checkins:person:p1" in builder.G.nodes

    # check-in node
    checkin_node = "checkin:Test%20Place"
    assert checkin_node in builder.G.nodes

    # edge from person -> container
    assert builder.G.has_edge(person_node, "checkins:person:p1")

    # edge from person -> checkin
    assert builder.G.has_edge(person_node, checkin_node)


def test_add_check_ins_skips_empty(builder):

    person = {"personal_details": {"location": {"check_ins": {"fb_check_ins": None}}}}

    person_node = "person:p1"
    builder.G.add_node(person_node)

    builder.add_check_ins(person_node, person)

    assert len(builder.G.nodes) == 1


# extract_hometown
def test_extract_hometown_success(builder, person_with_hometown):

    result = builder.extract_hometown(person_with_hometown)

    assert result["name"] == "Test City"
    assert result["location_id"] == "123"
    assert result["picture"] == "https://image.com/home.jpg"


def test_extract_hometown_none(builder):

    person = {"personal_details": {"location": {}}}

    result = builder.extract_hometown(person)

    assert result is None


# add_hometown
def test_add_hometown_creates_nodes(builder, person_with_hometown):

    person_node = "person:p1"
    builder.G.add_node(person_node)

    builder.add_hometown(person_node, person_with_hometown)

    hometown_node = "hometown:person:p1"
    container_node = "has_hometown:person:p1"

    assert container_node in builder.G.nodes
    assert hometown_node in builder.G.nodes

    assert builder.G.has_edge(person_node, container_node)
    assert builder.G.has_edge(person_node, hometown_node)


def test_add_hometown_skips_missing(builder):

    person = {"personal_details": {"location": {}}}

    person_node = "person:p1"
    builder.G.add_node(person_node)

    builder.add_hometown(person_node, person)

    # no extra nodes should be added
    assert len(builder.G.nodes) == 1


# rewrite_relationships tests
@pytest.mark.anyio
def test_bidirectional_follow():

    G = nx.DiGraph()

    G.add_node("a", type="candidate")
    G.add_node("b", type="candidate")

    G.add_node("c", type="person")
    G.add_node("d", type="person")

    G.add_edge("a", "b", relation="follows")
    G.add_edge("b", "a", relation="follows")
    G.add_edge("c", "d", relation="follows")
    G.add_edge("d", "c", relation="follows")

    H = rewrite_relationships(G)

    edges = list(H.edges(data=True))

    assert len(edges) == 1
    assert edges[0][2]["relation"] == "bidirectional"


@pytest.mark.anyio
def test_unidirectional_follow():

    G = nx.DiGraph()

    G.add_node("a", type="candidate")
    G.add_node("b", type="candidate")

    G.add_edge("a", "b", relation="follows")

    H = rewrite_relationships(G, connection_type=["unidirectional"], min_degree=0)

    edges = list(H.edges(data=True))

    assert edges[0][2]["relation"] == "unidirectional"


# dynamic view test
@pytest.mark.anyio
def test_build_dynamic_view():

    G = nx.DiGraph()

    G.add_node("person:1", type="person")
    G.add_node("company:1", type="company")

    G.add_edge("person:1", "company:1", relation="worked_at")

    H = build_dynamic_view(G, {"person", "company"}, {"worked_at"})

    assert H.has_node("person:1")
    assert H.has_node("company:1")
    assert H.has_edge("person:1", "company:1")


# cytoscape export
@pytest.mark.anyio
def test_nx_to_cytoscape():

    G = nx.DiGraph()

    G.add_node("n1", type="person")
    G.add_node("n2", type="company")

    G.add_edge("n1", "n2", relation="worked_at")

    elements = nx_to_cytoscape(G)

    nodes = [e for e in elements if "source" not in e["data"]]
    edges = [e for e in elements if "source" in e["data"]]

    assert len(nodes) == 2
    assert len(edges) == 1

    edge = edges[0]["data"]

    assert edge["source"] == "n1"
    assert edge["target"] == "n2"


def test_builder_include_likes_only(builder, person_with_interests):
    graph = builder.build([person_with_interests], from_database=False)
    H = rewrite_relationships(graph, connection_type=["likes"], min_degree=1)

    edges = list(H.edges(data=True))

    assert len(edges) == 1

    u, v, data = edges[0]
    assert data["label"] == "like"
    assert data["relation"] == "unidirectional"
    assert v == "fb_page:999"


def test_builder_exclude_likes(builder, person_with_interests):
    graph = builder.build([person_with_interests], from_database=False)
    H = rewrite_relationships(graph, connection_type=["groups"], min_degree=1)

    labels = [data["label"] for _, _, data in H.edges(data=True)]

    assert "like" not in labels


def test_builder_include_groups_only(builder, person_with_interests):
    graph = builder.build([person_with_interests], from_database=False)
    H = rewrite_relationships(graph, connection_type=["groups"], min_degree=1)

    edges = list(H.edges(data=True))

    assert len(edges) == 1

    u, v, data = edges[0]
    assert data["label"] == "membership"
    assert data["relation"] == "unidirectional"
    assert v == "telegram_group:tg1"


def test_builder_exclude_groups(builder, person_with_interests):
    graph = builder.build([person_with_interests], from_database=False)
    H = rewrite_relationships(graph, connection_type=["likes"], min_degree=1)

    labels = [data["label"] for _, _, data in H.edges(data=True)]

    assert "membership" not in labels


def test_builder_likes_and_groups(builder, person_with_interests):
    graph = builder.build([person_with_interests], from_database=False)
    H = rewrite_relationships(graph, connection_type=["likes", "groups"], min_degree=1)

    labels = [data["label"] for _, _, data in H.edges(data=True)]

    assert "like" in labels
    assert "membership" in labels
    assert len(labels) == 2


def test_builder_all_includes_everything(builder, person_with_interests):
    graph = builder.build([person_with_interests], from_database=False)
    H = rewrite_relationships(graph, connection_type=["all"], min_degree=1)

    labels = [data["label"] for _, _, data in H.edges(data=True)]

    assert "like" in labels
    assert "membership" in labels


def test_builder_likes_skipped_if_bidirectional(builder):
    G = nx.DiGraph()

    G.add_node("p1", type="person", person="p1")
    G.add_node("p2", type="person", person="p2")
    G.add_node("page1", type="page")

    # bidirectional
    G.add_edge("p1", "p2", relation="follows")
    G.add_edge("p2", "p1", relation="follows")

    # likes (should be skipped)
    G.add_edge("p1", "page1", relation="likes_page")

    H = rewrite_relationships(G, connection_type=["all"])

    labels = [data["label"] for _, _, data in H.edges(data=True)]

    assert "like" not in labels
    assert any(l in labels for l in ["mutual follow", "friendship"])


# ---------------------------------------------------------------------------
# Helpers for cross-platform tests
# ---------------------------------------------------------------------------

def _ig_contact(user_id, username="", full_name=""):
    return {
        "instagram_user_id": user_id,
        "instagram_username": username or user_id,
        "instagram_full_name": full_name or user_id,
        "instagram_profile_picture": None,
    }


def _fb_contact(user_id, full_name=""):
    return {
        "facebook_user_id": user_id,
        "facebook_full_name": full_name or user_id,
        "facebook_profile_url": f"https://facebook.com/{user_id}",
        "facebook_profile_picture": None,
    }


def _make_person_dict(person_id, platforms: dict, connections: dict | None = None):
    """
    platforms: e.g. {"facebook": "fb_123"} or {"instagram": "ig_456"} or both.
    connections: e.g. {"followers": {"instagram": [...]}, "following": {...}, "friends": {...}}
    """
    matched_profiles = {}
    for platform, profile_id in platforms.items():
        matched_profiles[platform] = {
            "primary_candidate": {
                "p0": {
                    "profile_id": profile_id,
                    "profile_username": f"{profile_id}_user",
                    "profile_url": f"https://{platform}.com/{profile_id}",
                    "profile_picture": None,
                    "full_name": f"Person {person_id}",
                }
            }
        }
    return {
        "id": person_id,
        "personal_details": {
            "name": {
                "first_name": {"f_name": f"Person{person_id}"},
                "last_name": {"l_name": ""},
            }
        },
        "network_signature": {"matched_profiles": matched_profiles},
        "connections": connections or {},
    }


def _build_graph(*persons):
    b = GraphBuilder()
    b.get_presigned_link_picture = lambda _: None
    return b.build(list(persons))


# ---------------------------------------------------------------------------
# _get_follow_candidates
# ---------------------------------------------------------------------------

def test_get_follow_candidates_returns_platform_match(builder):
    builder.G.add_node(
        "person:A", type="person",
        matched_profiles={"instagram:A_ig": True, "facebook:A_fb": True},
    )
    result = builder._get_follow_candidates("person:A")
    assert result == ["instagram:A_ig", "facebook:A_fb"]


def test_get_follow_candidates_fallback_when_no_platform_match(builder):
    builder.G.add_node("person:A", type="person", matched_profiles={"facebook:A_fb": True})
    result = builder._get_follow_candidates("person:A")
    assert result == ["facebook:A_fb"]


def test_get_follow_candidates_empty_when_no_profiles(builder):
    builder.G.add_node("person:A", type="person")
    result = builder._get_follow_candidates("person:A")
    assert result == []


def test_get_follow_candidates_fallback_returns_all_platforms(builder):
    builder.G.add_node(
        "person:A", type="person",
        matched_profiles={"facebook:A_fb": True, "linkedin:A_li": True},
    )
    result = builder._get_follow_candidates("person:A")
    assert set(result) == {"facebook:A_fb", "linkedin:A_li"}


# ---------------------------------------------------------------------------
# add_connections — cross-platform edge creation
# ---------------------------------------------------------------------------

def test_instagram_follower_edge_to_instagram_primary():
    person = _make_person_dict("A", {"instagram": "A_ig"}, connections={
        "followers": {"instagram": [_ig_contact("B_ig")]}
    })
    G = _build_graph(person)
    assert G.has_edge("instagram:B_ig", "instagram:A_ig")
    assert G["instagram:B_ig"]["instagram:A_ig"]["relation"] == "follows"


def test_instagram_follower_fallback_to_facebook_primary():
    """Person A has only Facebook primary — instagram follower edge must use facebook candidate."""
    person = _make_person_dict("A", {"facebook": "A_fb"}, connections={
        "followers": {"instagram": [_ig_contact("B_ig")]}
    })
    G = _build_graph(person)
    assert G.has_edge("instagram:B_ig", "facebook:A_fb"), (
        "instagram follower should link to facebook primary when no instagram candidate exists"
    )
    assert G["instagram:B_ig"]["facebook:A_fb"]["relation"] == "follows"


def test_instagram_following_fallback_to_facebook_primary():
    """Person A has only Facebook primary — instagram following edge must use facebook candidate."""
    person = _make_person_dict("A", {"facebook": "A_fb"}, connections={
        "following": {"instagram": [_ig_contact("B_ig")]}
    })
    G = _build_graph(person)
    assert G.has_edge("facebook:A_fb", "instagram:B_ig"), (
        "instagram following should link from facebook primary when no instagram candidate exists"
    )
    assert G["facebook:A_fb"]["instagram:B_ig"]["relation"] == "follows"


def test_facebook_follower_fallback_to_instagram_primary():
    """Person A has only Instagram primary — facebook follower edge falls back to instagram candidate."""
    person = _make_person_dict("A", {"instagram": "A_ig"}, connections={
        "followers": {"facebook": [_fb_contact("B_fb")]}
    })
    G = _build_graph(person)
    assert G.has_edge("facebook:B_fb", "instagram:A_ig")
    assert G["facebook:B_fb"]["instagram:A_ig"]["relation"] == "follows"


def test_facebook_following_fallback_to_instagram_primary():
    """Person A has only Instagram primary — facebook following edge falls back to instagram candidate."""
    person = _make_person_dict("A", {"instagram": "A_ig"}, connections={
        "following": {"facebook": [_fb_contact("B_fb")]}
    })
    G = _build_graph(person)
    assert G.has_edge("instagram:A_ig", "facebook:B_fb")


def test_friend_edge_fallback_to_instagram_primary():
    """Facebook friends data when person only has Instagram primary — uses instagram candidate."""
    person = _make_person_dict("A", {"instagram": "A_ig"}, connections={
        "friends": {"facebook": [_fb_contact("B_fb")]}
    })
    G = _build_graph(person)
    assert G.has_edge("instagram:A_ig", "facebook:B_fb")
    assert G["instagram:A_ig"]["facebook:B_fb"]["relation"] == "friend"


# ---------------------------------------------------------------------------
# rewrite_relationships — cross-platform mutual follow
# ---------------------------------------------------------------------------

def test_same_platform_mutual_follow_bidirectional():
    """Both persons on Instagram and follow each other → bidirectional mutual follow."""
    person_a = _make_person_dict("A", {"instagram": "A_ig"}, connections={
        "following": {"instagram": [_ig_contact("B_ig")]}
    })
    person_b = _make_person_dict("B", {"instagram": "B_ig"}, connections={
        "following": {"instagram": [_ig_contact("A_ig")]}
    })
    G = _build_graph(person_a, person_b)
    H = rewrite_relationships(G)

    edge = H.get_edge_data("person:A", "person:B") or H.get_edge_data("person:B", "person:A")
    assert edge is not None
    assert edge["relation"] == "bidirectional"
    assert edge["label"] == "mutual follow"


def test_cross_platform_mutual_follow_fb_primary_ig_data():
    """
    Person A: Facebook primary only, has Instagram follower/following data for B.
    Person B: Instagram primary.

    Raw graph edges created via cross-platform fallback:
      instagram:B_ig → facebook:A_fb  (B follows A — from A's instagram followers)
      facebook:A_fb  → instagram:B_ig  (A follows B — from A's instagram following)

    rewrite_relationships must detect this as a mutual follow between person:A and person:B.
    """
    person_a = _make_person_dict("A", {"facebook": "A_fb"}, connections={
        "followers": {"instagram": [_ig_contact("B_ig")]},
        "following": {"instagram": [_ig_contact("B_ig")]},
    })
    person_b = _make_person_dict("B", {"instagram": "B_ig"})
    G = _build_graph(person_a, person_b)

    assert G.has_edge("instagram:B_ig", "facebook:A_fb"), "cross-platform B→A edge missing"
    assert G.has_edge("facebook:A_fb", "instagram:B_ig"), "cross-platform A→B edge missing"

    H = rewrite_relationships(G)
    edge = H.get_edge_data("person:A", "person:B") or H.get_edge_data("person:B", "person:A")
    assert edge is not None, "no edge between person:A and person:B"
    assert edge["relation"] == "bidirectional"
    assert edge["label"] == "mutual follow"


def test_cross_platform_mutual_follow_different_platforms_each_direction():
    """
    Person A: Facebook + Instagram primary.
    Person B: Facebook + Instagram primary.
    A follows B on Instagram; B follows A on Facebook (different platforms each direction).
    """
    person_a = _make_person_dict("A", {"facebook": "A_fb", "instagram": "A_ig"}, connections={
        "following": {"instagram": [_ig_contact("B_ig")]}
    })
    person_b = _make_person_dict("B", {"facebook": "B_fb", "instagram": "B_ig"}, connections={
        "following": {"facebook": [_fb_contact("A_fb")]}
    })
    G = _build_graph(person_a, person_b)
    H = rewrite_relationships(G)

    edge = H.get_edge_data("person:A", "person:B") or H.get_edge_data("person:B", "person:A")
    assert edge is not None, "no edge between person:A and person:B"
    assert edge["relation"] == "bidirectional"
    assert edge["label"] == "mutual follow"


def test_cross_platform_unidirectional_not_detected_as_mutual():
    """A follows B via cross-platform fallback but B does not follow A → not mutual."""
    person_a = _make_person_dict("A", {"facebook": "A_fb"}, connections={
        "following": {"instagram": [_ig_contact("B_ig")]}
    })
    person_b = _make_person_dict("B", {"instagram": "B_ig"})
    G = _build_graph(person_a, person_b)
    H = rewrite_relationships(G)

    edge = H.get_edge_data("person:A", "person:B") or H.get_edge_data("person:B", "person:A")
    assert edge is None or edge.get("relation") != "bidirectional"


# ---------------------------------------------------------------------------
# rewrite_relationships — cross-platform friendship
# ---------------------------------------------------------------------------

def test_facebook_friends_bidirectional_friendship():
    """A and B are Facebook friends → bidirectional friendship edge."""
    person_a = _make_person_dict("A", {"facebook": "A_fb"}, connections={
        "friends": {"facebook": [_fb_contact("B_fb")]}
    })
    person_b = _make_person_dict("B", {"facebook": "B_fb"}, connections={
        "friends": {"facebook": [_fb_contact("A_fb")]}
    })
    G = _build_graph(person_a, person_b)
    H = rewrite_relationships(G)

    edge = H.get_edge_data("person:A", "person:B") or H.get_edge_data("person:B", "person:A")
    assert edge is not None
    assert edge["relation"] == "bidirectional"
    assert edge["label"] == "friendship"


def test_cross_platform_friend_uses_fallback_candidate():
    """A has Instagram primary but Facebook friends data — friend edge created via fallback."""
    person_a = _make_person_dict("A", {"instagram": "A_ig"}, connections={
        "friends": {"facebook": [_fb_contact("B_fb")]}
    })
    person_b = _make_person_dict("B", {"facebook": "B_fb"}, connections={
        "friends": {"facebook": [_fb_contact("A_ig")]}
    })
    G = _build_graph(person_a, person_b)

    assert G.has_edge("instagram:A_ig", "facebook:B_fb"), (
        "friend edge should be created from instagram primary when no facebook candidate"
    )

    H = rewrite_relationships(G)
    edge = H.get_edge_data("person:A", "person:B") or H.get_edge_data("person:B", "person:A")
    assert edge is not None
    assert edge["relation"] == "bidirectional"
