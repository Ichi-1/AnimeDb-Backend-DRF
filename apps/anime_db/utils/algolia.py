from algoliasearch_django import algolia_engine

anidb_index = 'anidb_Anime'


def get_client():
    return algolia_engine.client


def get_index(index_name):
    client = get_client()
    index = client.init_index(index_name)
    return index


def perform_serach(query, **params):
    """
    1. Getting db index from Algolia
    2. Looking for query and params argument
    By default if both argument is empty or absent,
    the search will match every object in index
    3. Query string is ?search=[YourQuery]&tags=[TagsFrom _tags field]
    4. Look for searchable and tags fields in index.py

    """

    index = get_index(index_name=anidb_index)
    request_options = {}

    if "tags" in params:
        tags = params.pop("tags") or []
        print(tags)
        if len(tags) != 0:
            request_options["tagFilters"] = tags

    result = index.search(query=query, request_options=request_options)
    return result
