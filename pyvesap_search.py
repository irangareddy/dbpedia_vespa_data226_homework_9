#
# https://github.com/vespa-engine/sample-apps/blob/master/news/src/python/user_search.py
# https://docs.vespa.ai/en/tutorials/news-5-recommendation.html
#

# pip install pyvespa
import pandas as pd
from vespa.application import Vespa
from vespa.io import VespaQueryResponse

def display_dbpedia_hits_as_df(response: VespaQueryResponse, fields) -> pd.DataFrame:
    """
    Converts search results from Vespa into a DataFrame format.
    Args:
        response (VespaQueryResponse): The Vespa query response object.
        fields (list): List of fields to extract from each hit (e.g., 'doc_id', 'title', 'text').
    Returns:
        pd.DataFrame: A DataFrame containing the selected fields from the hits.
    """
    records = []
    for hit in response.hits:
        record = {}
        for field in fields:
            record[field] = hit["fields"][field]
        records.append(record)
    return pd.DataFrame(records)

def dbpedia_keyword_search(app, search_query):
    """
    Perform a keyword search on DBpedia data using the 'title' and 'text' fields.
    Args:
        app (Vespa): The Vespa application instance.
        search_query (str): The query string to search for.
    Returns:
        pd.DataFrame: DataFrame containing the results of the keyword search.
    """
    query = {
        "yql": "select * from sources * where userQuery() limit 5",
        "query": search_query,
        "ranking": "bm25",
    }
    response = app.query(query)
    return display_dbpedia_hits_as_df(response, ["doc_id", "title", "text"])

def dbpedia_semantic_search(app, query):
    """
    Perform semantic search on DBpedia using embeddings (requires embedding data).
    Args:
        app (Vespa): The Vespa application instance.
        query (str): The text query to search with.
    Returns:
        pd.DataFrame: DataFrame containing the results of the semantic search.
    """
    query = {
        "yql": "select * from sources * where ({targetHits:100}nearestNeighbor(embedding,e)) limit 5",
        "query": query,
        "ranking": "semantic",
        "input.query(e)": "embed(@query)"
    }
    response = app.query(query)
    return display_dbpedia_hits_as_df(response, ["doc_id", "title", "text"])

# Retrieve the embedding for a specific document from DBpedia (if embeddings exist)
def get_dbpedia_embedding(doc_id):
    """
    Retrieve the embedding of a DBpedia document by doc_id.
    Args:
        doc_id (str): The doc_id of the document for which the embedding is to be fetched.
    Returns:
        dict: The document's embedding data (if available), or None if not found.
    """
    query = {
        "yql": f"select doc_id, title, text, embedding from content.doc where doc_id contains '{doc_id}'",  # Query to fetch embedding for doc_id
        "hits": 1
    }
    result = app.query(query)
    
    if result.hits:
        return result.hits[0]
    return None

# Query DBpedia for documents similar to the given embedding
def query_dbpedia_by_embedding(embedding_vector):
    """
    Search for documents in DBpedia similar to a given embedding vector.
    Args:
        embedding_vector (list): The embedding vector used to search for similar documents.
    Returns:
        VespaQueryResponse: The Vespa query response containing similar documents.
    """
    query = {
        'hits': 5,
        'yql': 'select * from content.doc where ({targetHits:5}nearestNeighbor(embedding, user_embedding))',  # Search using nearest neighbor for embedding
        'ranking.features.query(user_embedding)': str(embedding_vector),  # Use the provided embedding for the search
        'ranking.profile': 'recommendation'  # Use recommendation ranking profile
    }
    return app.query(query)

# Initialize Vespa application with the correct host and port
app = Vespa(url="http://localhost", port=8082)


import pandas as pd
from vespa.application import Vespa
from vespa.io import VespaResponse, VespaQueryResponse

def display_dbpedia_hits_as_df(response: VespaQueryResponse, fields) -> pd.DataFrame:
    """Helper function to display search results as a DataFrame."""
    records = []
    for hit in response.hits:
        record = {}
        for field in fields:
            record[field] = hit["fields"][field]
        records.append(record)
    return pd.DataFrame(records)

def dbpedia_keyword_search(app, search_query):
    """Perform keyword-based search on DBpedia."""
    query = {
        "yql": "select * from sources * where userQuery() limit 5",
        "query": search_query,
        "ranking": "bm25",
    }
    response = app.query(query)
    return display_dbpedia_hits_as_df(response, ["doc_id", "title", "text"])

def dbpedia_semantic_search(app, search_query):
    """Perform semantic search using DBpedia embeddings."""
    query = {
        "yql": "select * from sources * where ({targetHits:100}nearestNeighbor(embedding, e)) limit 5",
        "query": search_query,
        "ranking": "semantic",
        "input.query(e)": "embed(@query)"
    }
    response = app.query(query)
    return display_dbpedia_hits_as_df(response, ["doc_id", "title", "text"])

def get_dbpedia_embedding(query):
    """Fetch embedding for a document using a given query."""
    # Query DBpedia for a document embedding based on the query
    query = {
        "yql": f"select doc_id, title, text, embedding from content.doc where title contains '{query}'",
        "hits": 1
    }
    result = app.query(query)
    if result.hits:
        return result.hits[0]
    return None

def query_dbpedia_by_embedding(embedding_vector):
    """Query DBpedia using an embedding to find similar documents."""
    query = {
        'hits': 5,
        'yql': 'select * from content.doc where ({targetHits:5}nearestNeighbor(embedding, user_embedding))',
        'ranking.features.query(user_embedding)': str(embedding_vector),
        'ranking.profile': 'recommendation'
    }
    return app.query(query)

# Initialize Vespa application instance (replace with your actual Vespa server URL)
app = Vespa(url="http://localhost", port=8082)

# Main query from user
query = "Football player in Europe?"
print(f"\nGeneral search query: {query}")

df_keyword = dbpedia_keyword_search(app, query)
print("\nDBpedia Keyword Search Results:")
print(df_keyword.head())

df_semantic = dbpedia_semantic_search(app, query)
print("\nDBpedia Semantic Search Results:")
print(df_semantic.head())

if not df_semantic.empty:
    doc_id = df_semantic.iloc[0]["doc_id"]
    print(f"\nFetching embedding for doc_id: {doc_id}")

    emb = get_dbpedia_embedding(doc_id)

    # If embedding is found, perform similarity search based on that embedding
    if emb is not None:
        print(f"\nEmbedding for doc_id '{doc_id}': {emb['fields']['embedding']}...")
        
        # Use this embedding to find similar documents
        results = query_dbpedia_by_embedding(emb["fields"]["embedding"])
        df_similar = display_dbpedia_hits_as_df(results, ["doc_id", "title", "text"])
        print("\nSimilar Document Results based on embedding:")
        print(df_similar.head())
    else:
        print(f"\nNo embedding found for doc_id '{doc_id}'. Please check if the document exists or has embeddings.")
else:
    print("\nNo results found from semantic search. Please try again with a different query.")
