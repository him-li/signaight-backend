from .schemas import SearchEventCreate


async def register_search(context):
    """Register new search event in database

    Parameters
    ----------
    context : str
        Context where is run search

    Returns
    -------
    string
        string which represents identificator to search event in database
    """
    search_event = SearchEventCreate(context=context)
    await search_event.insert()
    return str(search_event.id)
