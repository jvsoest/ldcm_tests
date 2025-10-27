bash run_rdf4j.sh

echo "================================================="
echo "RDF4J test on data folder"
echo "Creates data_analysis_results_rdf4j.csv"
/usr/bin/time -v python test_rdf4j.py

docker stop rdf4j
docker volume rm rdf4j-data

echo ""

echo "================================================="
echo "RDFLib test on data folder (loading per-patient)"
echo "Creates data_analysis_times.csv and data_analysis_results.csv"
/usr/bin/time -v python analyse.py

echo ""

echo "================================================="
echo "RDFLib test on data folder (loading all patients at once, capped at 1 patient)"
echo "Creates data_analysis_results_once.csv"
/usr/bin/time -v python analyse_once.py 1

echo ""

echo "================================================="
echo "RDFLib test on data folder (loading all patients at once, capped at 2 patients)"
echo "Creates data_analysis_results_once.csv"
/usr/bin/time -v python analyse_once.py 2

echo ""

echo "================================================="
echo "RDFLib test on data folder (loading all patients at once, capped at 3 patients)"
echo "Creates data_analysis_results_once.csv"
/usr/bin/time -v python analyse_once.py 3