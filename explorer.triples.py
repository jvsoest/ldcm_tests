# This python file explores the triples in the ./data folder using rdflib.
# It will calculate for every found *.ttl file the number of triples, and the size (in kb) of the file.
# All results will be stored in a CSV file called data_triples_analysis.csv

import os
import rdflib
import csv

def main():
    data_dir = './data'
    results = []

    for subject_label in os.listdir(data_dir):
        subject_path = os.path.join(data_dir, subject_label)
        if os.path.isdir(subject_path):
            for filename in os.listdir(subject_path):
                if filename.endswith('.ttl'):
                    file_path = os.path.join(subject_path, filename)
                    g = rdflib.Graph()
                    g.parse(file_path, format='turtle')
                num_triples = len(g)
                file_size = os.path.getsize(file_path) / 1024  # size in KB
                results.append((subject_label, num_triples, file_size))

    # Write results to CSV
    with open('data_triples_analysis.csv', 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(['Filename', 'Number of Triples', 'File Size (KB)'])
        csvwriter.writerows(results)

if __name__ == '__main__':
    main()