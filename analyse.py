import os
import time
import rdflib

# read query from file
with open('query.sparql', 'r') as f:
    query = f.read()

def main():
    # set data directory
    data_dir = './data'
    turtle_file = 'LinkedDicom.ttl'

    # create csv file for time results
    csv_file = open('./data_analysis_times.csv', 'w')
    csv_file.write('subject,elapsed_time\n')

    # create a csv file for query results
    results_file = open('./data_analysis_results.csv', 'w')
    results_file.write('patient,study,rtStruct,structureName,ctSerie,ctSerieModality,ctSerieDesc,ctSerieManufacturerModelName\n')

    # Loop over all subjects in the data directory
    for subject_label in os.listdir(data_dir):
        subject_path = os.path.join(data_dir, subject_label)
        if os.path.isdir(subject_path):
            #print(f'Processing subject: {subject_path}')
            # check if turtle file exists
            if not os.path.exists(os.path.join(subject_path, turtle_file)):
                print(f'Turtle file not found for subject: {subject_label}, skipping...')
                continue

            # start timing
            start_time = time.time()
            g = rdflib.Graph()
            g.parse(os.path.join(subject_path, turtle_file))

            #print(f'Graph has {len(g)} statements.')

            results = g.query(query)
            #print(f'Query returned {len(results)} results.')
            for row_res in results:
                results_file.write(','.join([str(item) for item in row_res]) + '\n')

            # end timing
            end_time = time.time()
            elapsed_time = end_time - start_time
            #print(f'Elapsed time for {subject_label}: {elapsed_time} seconds')

            # write results to csv
            for row in results:
                csv_file.write(f'{subject_label},{elapsed_time}\n')

    csv_file.close()

if __name__ == '__main__':
    main()
