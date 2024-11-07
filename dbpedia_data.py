import csv
from SPARQLWrapper import SPARQLWrapper, JSON

# SPARQL endpoint for DBpedia
sparql = SPARQLWrapper("https://dbpedia.org/sparql")

# SPARQL query to get data from multiple classes (Organisation, Person, Place, Film, Event)
query = """
SELECT ?id ?title ?text
WHERE {
  {
    ?subject a dbo:Organisation ;
             rdfs:label ?title ;
             dbo:abstract ?text .
    BIND(STR(?subject) AS ?id)
  }
  UNION
  {
    ?subject a dbo:Person ;
             rdfs:label ?title ;
             dbo:abstract ?text .
    BIND(STR(?subject) AS ?id)
  }
  UNION
  {
    ?subject a dbo:Place ;
             rdfs:label ?title ;
             dbo:abstract ?text .
    BIND(STR(?subject) AS ?id)
  }
  UNION
  {
    ?subject a dbo:Film ;
             rdfs:label ?title ;
             dbo:abstract ?text .
    BIND(STR(?subject) AS ?id)
  }  UNION
  {
    ?subject a dbo:Event ;
             rdfs:label ?title ;
             dbo:abstract ?text .
    BIND(STR(?subject) AS ?id)
  }
  FILTER (lang(?text) = "en")
  FILTER (lang(?title) = "en")
  BIND(RAND() AS ?random)
}
ORDER BY ?random
LIMIT 10000
"""

sparql.setQuery(query)
sparql.setReturnFormat(JSON)

results = sparql.query().convert()

with open("dbpedia_results.csv", mode="w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    
    writer.writerow(["ID", "Title", "Text"])
    
    for result in results["results"]["bindings"]:
        # Extract ID, Title, and Text (formerly abstract)
        id_value = result.get("id", {}).get("value", "N/A")
        title_value = result.get("title", {}).get("value", "N/A")
        text_value = result.get("text", {}).get("value", "N/A")
        
        # Write the data to the CSV file
        writer.writerow([id_value, title_value, text_value])

print("Data has been written to 'dbpedia_results.csv'.")
