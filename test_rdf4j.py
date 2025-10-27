# This file reads the ./data folder for *.ttl files and loads them into a local RDF4J repository.
# Import necessary libraries
import os
import requests
import time

def create_repository():
        # Create the repository if it doesn't exist
    repo_url = "http://localhost:8080/rdf4j-server/repositories/ldcm_native"
    repo_config = """
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#>.
@prefix rep: <http://www.openrdf.org/config/repository#>.
@prefix sr: <http://www.openrdf.org/config/repository/sail#>.
@prefix sail: <http://www.openrdf.org/config/sail#>.
@prefix ns: <http://www.openrdf.org/config/sail/native#>.

[] a rep:Repository ;
   rep:repositoryID "ldcm_native" ;
   rdfs:label "LinkedDicom Native Store" ;
   rep:repositoryImpl [
      rep:repositoryType "openrdf:SailRepository" ;
      sr:sailImpl [
         sail:sailType "openrdf:NativeStore" ;
         ns:tripleIndexes "spoc,posc,cspo"
      ]
   ].
"""
    headers = {"Content-Type": "text/turtle"}
    response = requests.put(repo_url, headers=headers, data=repo_config.encode('utf-8'))
    if response.status_code == 204:
        print("Successfully created RDF4J repository 'ldcm_native'")
    else:
        print(f"Failed to create RDF4J repository: {response.status_code} - {response.content}")
        # Try to continue anyway in case repository already exists
        print("Attempting to load data anyway...")

def load_data():
    time_start = time.time()

    # Define the RDF4J repository URL
    rdf4j_url = "http://localhost:8080/rdf4j-server/repositories/ldcm_native/statements"
    
    # Iterate over all files in the ./data directory
    for filename in os.listdir("./data"):
        # print(f"Found file: {filename}")
        ttl_file_path = os.path.join("./data", filename, "LinkedDicom.ttl")
        if os.path.isfile(ttl_file_path):
            # print(f"Loading {filename} into RDF4J...")
            # Load the TTL file into the RDF4J repository
            with open(ttl_file_path, "rb") as f:
                headers = {"Content-Type": "text/turtle"}
                response = requests.post(rdf4j_url, headers=headers, data=f)
                if response.status_code == 204:
                    # print(f"Successfully loaded {filename} into RDF4J")
                    continue
                else:
                    print(f"Failed to load {filename} into RDF4J: {response.content}")
    
    time_end = time.time()
    elapsed_time = time_end - time_start
    print(f"Elapsed time for loading data into RDF4J: {elapsed_time} seconds")

# read query from file
with open('query.sparql', 'r') as f:
    query = f.read()

def run_query():
    rdf4j_url = "http://localhost:8080/rdf4j-server/repositories/ldcm_native"
    headers = {"Accept": "application/sparql-results+json"}
    # measure time of the post request
    start_time = time.time()
    response = requests.post(rdf4j_url, headers=headers, data={"query": query})
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Elapsed time for SPARQL query: {elapsed_time} seconds")
    
    del end_time
    del start_time
    del elapsed_time

    start_time = time.time()
    #store results in a csv file
    with open('./data_analysis_results_rdf4j.csv', 'w') as results_file:
        results_file.write('patient,study,rtStruct,structureName,ctSerie,ctSerieModality,ctSerieDesc,ctSerieManufacturerModelName\n')
        if response.status_code == 200:
            results = response.json()
            for binding in results["results"]["bindings"]:
                row = [
                    binding.get("patient", {}).get("value", ""),
                    binding.get("study", {}).get("value", ""),
                    binding.get("rtStruct", {}).get("value", ""),
                    binding.get("structureName", {}).get("value", ""),
                    binding.get("ctSerie", {}).get("value", ""),
                    binding.get("ctSerieModality", {}).get("value", ""),
                    binding.get("ctSerieDesc", {}).get("value", ""),
                    binding.get("ctSerieManufacturerModelName", {}).get("value", "")
                ]
                results_file.write(','.join(row) + '\n')
        else:
            print(f"Failed to execute SPARQL query: {response.status_code} - {response.content}")
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Elapsed time for writing results to CSV: {elapsed_time} seconds")

def main():
    create_repository()
    load_data()
    run_query()

if __name__ == "__main__":
    main()