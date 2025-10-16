docker run -d --name rdf4j --rm \
    -p 8080:8080 \
    -e JAVA_OPTS="-Xms1g -Xmx8g" \
    -v data:/var/rdf4j -v logs:/usr/local/tomcat/logs \
    eclipse/rdf4j-workbench:latest
