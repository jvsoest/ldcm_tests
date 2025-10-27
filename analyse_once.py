import os
import time
import rdflib

# read query from file
with open('query.sparql', 'r') as f:
    query = f.read()

def main(i_max):
    # set data directory
    data_dir = './data'
    turtle_file = 'LinkedDicom.ttl'

    start_time = time.time()
    g = rdflib.Graph()

    i = 0

    # Loop over all subjects in the data directory
    for subject_label in os.listdir(data_dir):
        subject_path = os.path.join(data_dir, subject_label)
        if os.path.isdir(subject_path):
            # print(f'Processing subject: {subject_path}')
            # check if turtle file exists
            if not os.path.exists(os.path.join(subject_path, turtle_file)):
                print(f'Turtle file not found for subject: {subject_label}, skipping...')
                continue

            # parse turtle file
            g.parse(os.path.join(subject_path, turtle_file))

            i += 1
            if i >= i_max:
                print("================================================")
                print(f"Loaded {i} patient(s)")
                break

            #print(f'Graph has {len(g)} statements.')
    
    # end timing
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f'Elapsed time for loading data: {elapsed_time} seconds')

    # remove variables end and start time to avoid confusion
    del end_time
    del start_time
    del elapsed_time

    start_time = time.time()
    results = g.query(query)
    # end timing
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f'Elapsed time for running query: {elapsed_time} seconds')

    # remove variables end and start time to avoid confusion
    del end_time
    del start_time
    del elapsed_time

    start_time = time.time()
    results.serialize(destination='./data_analysis_results_once.csv', format='csv')
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f'Elapsed time for writing results to CSV: {elapsed_time} seconds')

    print(f"Number of rows in results: {len(results)}")

if __name__ == '__main__':
    #get first input argument as integer
    import sys
    if len(sys.argv) > 1:
        i_max = int(sys.argv[1])
    else:
        i_max = 1  # default value
    main(i_max)