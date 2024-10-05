#!/bin/bash

if [ $# -eq 0 ]; then
    echo "Usage: $0 <number_of_requests>"
    exit 1
fi

REQUESTS=$1

URL_MICROSERVICIOS_USER="https://user.eden.localhost/api/v1/all"
URL_MICROSERVICIOS_CABIN="https://cabin.eden.localhost/api/v1/all"

OUTPUT_DIR="results"
mkdir -p $OUTPUT_DIR

function run_vegeta {
    local url=$1
    local output_prefix=$2

    echo "GET ${url}" | vegeta attack -insecure -rate=${REQUESTS} -duration=10s -max-workers=10 -connections=100 > "${OUTPUT_DIR}/${output_prefix}_results.bin"
    
    vegeta report < "${OUTPUT_DIR}/${output_prefix}_results.bin" > "${OUTPUT_DIR}/${output_prefix}_report.txt"
    
    vegeta plot < "${OUTPUT_DIR}/${output_prefix}_results.bin" > "${OUTPUT_DIR}/${output_prefix}_report.html"
    
    echo "HTML report for ${url} generated at ${OUTPUT_DIR}/${output_prefix}_report.html"
}

run_vegeta "${URL_MICROSERVICIOS_USER}" "user"

run_vegeta "${URL_MICROSERVICIOS_CABIN}" "cabin"
