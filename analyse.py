import os
import time
import rdflib

query = """
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX ldcm: <https://johanvansoest.nl/ontologies/LinkedDicom/>

SELECT ?patient ?study ?rtStruct ?structureName ?ctSerie ?ctSerieModality ?ctSerieDesc ?ctSerieManufacturerModelName
WHERE {
    ?patient rdf:type ldcm:Patient;
    	ldcm:T00100020 ?patientId;
     	ldcm:has_study ?study.
    ?study ldcm:has_series ?seriesStruct.
    
    ?seriesStruct rdf:type ldcm:Series;
                  ldcm:T00080060 "RTSTRUCT";
    			  ldcm:has_image ?rtStruct.
    
    ?rtStruct rdf:type ldcm:Radiotherapy_Structure_Object;
        ldcm:T30060010 [
        	rdf:type ldcm:Referenced_Frame_of_Reference_Sequence;
            ldcm:has_sequence_item [
        		rdf:type ldcm:Referenced_Frame_of_Reference_Sequence_Item;
                ldcm:T30060012 [
					rdf:type ldcm:Radiotherapy_Referenced_Study_Sequence;
     				ldcm:has_sequence_item [
        				rdf:type ldcm:Radiotherapy_Referenced_Study_Sequence_Item;
        			    ldcm:T30060014 [
        					rdf:type ldcm:Radiotherapy_Referenced_Series_Sequence;
             				ldcm:has_sequence_item [
        						rdf:type ldcm:Radiotherapy_Referenced_Series_Sequence_Item;
              					ldcm:R0020000E ?ctSerie;
    						];
    					];
    				];
            	];
    		];
    	];
    	ldcm:T30060020 [
            rdf:type ldcm:Structure_Set_ROI_Sequence;
            ldcm:has_sequence_item [
        		rdf:type ldcm:Structure_Set_ROI_Sequence_Item;
                ldcm:T30060026 ?structureName;
            ];
        ].
    
    ?ctSerie rdf:type ldcm:Series;
             ldcm:T00080060 ?ctSerieModality.
    OPTIONAL { ?ctSerie ldcm:T0008103E ?ctSerieDesc }.
    OPTIONAL { ?ctSerie ldcm:T00081090 ?ctSerieManufacturerModelName }.
}
"""

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
            print(f'Processing subject: {subject_path}')
            # check if turtle file exists
            if not os.path.exists(os.path.join(subject_path, turtle_file)):
                print(f'Turtle file not found for subject: {subject_label}, skipping...')
                continue

            # start timing
            start_time = time.time()
            g = rdflib.Graph()
            g.parse(os.path.join(subject_path, turtle_file))

            print(f'Graph has {len(g)} statements.')

            results = g.query(query)
            print(f'Query returned {len(results)} results.')
            for row_res in results:
                results_file.write(','.join([str(item) for item in row_res]) + '\n')

            # end timing
            end_time = time.time()
            elapsed_time = end_time - start_time
            print(f'Elapsed time for {subject_label}: {elapsed_time} seconds')

            # write results to csv
            for row in results:
                csv_file.write(f'{subject_label},{elapsed_time}\n')

    csv_file.close()

if __name__ == '__main__':
    main()