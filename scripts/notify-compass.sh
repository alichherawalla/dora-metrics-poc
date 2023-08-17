#!/bin/bash

TARGET_YAML=metrics/data.yaml

# Set common req payload values
USER_EMAIL=$COMPASS_USER_EMAIL
USER_API_KEY=$COMPASS_USER_API_KEY
URL=$COMPASS_METRICS_BASE_URL
COMMON_METIRCS_ID="ari:cloud:compass:e8e03695-06ef-4cb5-8c6b-1779f03bb72c:metric-source/f35e9589-f113-4456-84b4-8d515c2bf2d8"

# Convert current UTC time to IST
TIMESTAMP=$(TZ="Asia/Kolkata" date +'%Y-%m-%dT%H:%M:%SZ')


# hotfix to release ratio
METRICS=$(yq eval '.last_release.hotfix_to_release_ratio' ${TARGET_YAML} | tr -d '%')
METRIC_SOURCE_ID=""${COMMON_METIRCS_ID}"/f1f70a55-c349-485a-845f-f5c4e9cf161a"
PAYLOAD="{\"metricSourceId\": \"$METRIC_SOURCE_ID\", \"value\": "$METRICS", \"timestamp\": \"$TIMESTAMP\"}"

curl --request POST \
--url $URL \
--user "$USER_EMAIL:$USER_API_KEY" \
--header "Accept: application/json" \
--header "Content-Type: application/json" \
--data "$PAYLOAD"


# failures to total previous tickets ratio
METRICS=$(yq eval '.last_release.failures_to_total_previous_tickets_ratio' ${TARGET_YAML} | tr -d '%')
METRIC_SOURCE_ID=""${COMMON_METIRCS_ID}"/973658f8-1c1b-4c02-a1a6-8bf64aaf585d"
PAYLOAD="{\"metricSourceId\": \"$METRIC_SOURCE_ID\", \"value\": "$METRICS", \"timestamp\": \"$TIMESTAMP\"}"

curl --request POST \
--url $URL \
--user "$USER_EMAIL:$USER_API_KEY" \
--header "Accept: application/json" \
--header "Content-Type: application/json" \
--data "$PAYLOAD"


# feature to bug ratio
METRICS=$(yq eval '.last_release.feature_to_bug_ratio' ${TARGET_YAML} | tr -d '%')
METRIC_SOURCE_ID=""${COMMON_METIRCS_ID}"/c6161d5a-4bf3-49f2-8e8a-da5edc9afd87"
PAYLOAD="{\"metricSourceId\": \"$METRIC_SOURCE_ID\", \"value\": "$METRICS", \"timestamp\": \"$TIMESTAMP\"}"

curl --request POST \
--url $URL \
--user "$USER_EMAIL:$USER_API_KEY" \
--header "Accept: application/json" \
--header "Content-Type: application/json" \
--data "$PAYLOAD"

# release without bugs ratio
METRICS=$(yq eval '.last_release.release_without_bugs_ratio' ${TARGET_YAML} | tr -d '%')
METRIC_SOURCE_ID=""${COMMON_METIRCS_ID}"/b42f4c2a-0025-469b-a9ca-45a6c70eeb3b"
PAYLOAD="{\"metricSourceId\": \"$METRIC_SOURCE_ID\", \"value\": "$METRICS", \"timestamp\": \"$TIMESTAMP\"}"

curl --request POST \
--url $URL \
--user "$USER_EMAIL:$USER_API_KEY" \
--header "Accept: application/json" \
--header "Content-Type: application/json" \
--data "$PAYLOAD"

