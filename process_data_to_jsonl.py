import pandas as pd

def combine_features(row):
    """
    Combines the 'text' field into the final 'text' field for Vespa indexing.
    """
    try:
        return row['Text']
    except KeyError as e:
        print(f"Error: Missing key - {e}")
        return ""


def process_dbpedia_csv(input_file, output_file):
    """
    Processes a DBpedia CSV file to create a Vespa-compatible JSON format.

    Args:
        input_file (str): The path to the input CSV file containing DBpedia entity data.
                          Expected columns are 'ID', 'Title', and 'Text'.
        output_file (str): The path to the output JSON file to save the processed data in
                           Vespa-compatible format.
    """
    # Read the DBpedia CSV file
    dbpedia_data = pd.read_csv(input_file)

    # Ensure that missing values in 'ID', 'Title', and 'Text' columns are filled with empty strings
    for f in ['ID', 'Title', 'Text']:
        dbpedia_data[f] = dbpedia_data[f].fillna('')

    # Create 'text' field for Vespa indexing
    dbpedia_data["text"] = dbpedia_data.apply(combine_features, axis=1)

    # Select only the 'ID', 'Title', and 'text' columns
    dbpedia_data = dbpedia_data[['ID', 'Title', 'text']]
    dbpedia_data.rename(columns={'Title': 'doc_id', 'ID': 'title'}, inplace=True)

    # Create 'fields' column as a JSON-like structure of each record
    dbpedia_data['fields'] = dbpedia_data.apply(lambda row: row.to_dict(), axis=1)

    # Create 'put' column based on 'doc_id'
    dbpedia_data['put'] = dbpedia_data['doc_id'].apply(lambda x: f"id:hybrid-search:doc::{x}")

    # Select the 'put' and 'fields' columns to export
    df_result = dbpedia_data[['put', 'fields']]

    # Print the first few rows of the resulting DataFrame for verification
    print(df_result.head())

    # Output the processed data to a JSON file (in line-delimited JSON format)
    df_result.to_json(output_file, orient='records', lines=True)


# Example usage of the function
process_dbpedia_csv("dbpedia_data.csv", "processed_dbpedia.jsonl")
