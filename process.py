from LinkedDicom import LinkedDicom
import os
import time

def main():
    # set data directory
    data_dir = './data'
    ontology_file = 'LinkedDicom.owl'

    # create csv file for time results
    csv_file = open('./data_processing_times.csv', 'w')
    csv_file.write('subject,elapsed_time\n')

    # Loop over all subjects in the data directory
    for subject_label in os.listdir(data_dir):
        subject_path = os.path.join(data_dir, subject_label)
        if os.path.isdir(subject_path):
            print(f'Processing subject: {subject_path}')
            
            # start timing            
            start_time = time.time()

            linkedDicom = LinkedDicom.LinkedDicom(ontology_file)
            linkedDicom.processFolder(subject_path, persistentStorage=True)

            # Save the linkedDicom object to a file
            output_file = os.path.join(subject_path, "LinkedDicom.ttl")
            linkedDicom.saveResults(output_file)

            # end timing
            end_time = time.time()
            elapsed_time = end_time - start_time
            csv_file.write(f'{subject_label},{elapsed_time}\n')

    csv_file.close()

if __name__ == "__main__":
    main()