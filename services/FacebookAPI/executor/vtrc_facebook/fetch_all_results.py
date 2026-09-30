from core.fields import S3Path
from glom import glom
from core.clients.vetric.facebook import api, VtrcFbSpecs
from core.documents.base import SearchRequestDoc
from ..config import settings

async def fetch_users_with_retry(body, no_cache=False, depth=0):
    if depth > 1:
        return [], {}

    print(f"Running search (no_cache={no_cache}, depth={depth})")

    response = await api.async_search.users(body=body, no_cache=no_cache)
    response_body = response.body
    page_info = response_body.get("page_info", {})

    edges_spec = VtrcFbSpecs.search_edges_spec
    mapped_edges = glom(response_body, edges_spec)

    if mapped_edges:
        first_picture = next(
            (item.get("profile_picture") for item in mapped_edges if item.get("profile_picture")),
            None
        )
        print("Validating profile pictures...", first_picture)
        if first_picture is None and not no_cache:
            return await fetch_users_with_retry(body, no_cache=True, depth=depth + 1)
        valid = S3Path.validate(first_picture)
        print("Validating profile pictures final", valid)

        if valid is None and not no_cache:
            return await fetch_users_with_retry(body, no_cache=True, depth=depth + 1)

        return mapped_edges, page_info

    if not no_cache:
        return await fetch_users_with_retry(body, no_cache=True, depth=depth + 1)

    return [], {}


async def fetch_all_results(
    doc: SearchRequestDoc,
    limit=100
):
    all_results = {}
    end_cursor = None
    request_count = 0
    has_next_page = True
    candidates_count = len(list(all_results.values()))
    while (has_next_page and
          (candidates_count <
                settings.VETRIC_FACEBOOK_API_CANDIDATES_LIMIT or request_count < 15)):
        body = {
            "typed_query": getattr(doc, "query", None) or getattr(doc, "name", None),
            "transform": True,
        }
        if end_cursor:
            body["end_cursor"] = end_cursor
        try:
            mapped_edges, page_info =  await fetch_users_with_retry(body)
            for item in mapped_edges:
                all_results[item["id"]] = item
            has_next_page = page_info.get("has_next_page", False)
            if not has_next_page:
                break
            end_cursor = page_info.get("end_cursor")
        except Exception as e:
            print(str(e))
            has_next_page = False
        finally:
            candidates_count = len(list(all_results.values()))
            request_count += 1

    result = list(all_results.values())
    return result[:limit] if len(result) > limit else result
