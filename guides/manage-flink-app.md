# Manage Flink application

## Start the application

```bash
aws kinesisanalyticsv1 start-application --profile $AWS_PROFILE --cli-input-json "{
  \"ApplicationName\": \"apache-flink-example\",
  \"RunConfiguration\": {
    \"ApplicationRestoreConfiguration\": {
      \"ApplicationRestoreType\": \"RESTORE_FROM_LATEST_SNAPSHOT\"
    }
  }
}"
```

## Stop the application

```bash
aws kinesisanalyticsv1 stop-application --cli-input-json "{
  \"ApplicationName\": \"apache-flink-example\"
}"
```

## Update environment properties

```bash
aws kinesisanalyticsv1 update-application --cli-input-json "{
  \"ApplicationName\": \"apache-flink-example\",
  \"CurrentApplicationVersionId\": 0,
  \"ApplicationConfigurationUpdate\": {
    \"EnvironmentPropertyUpdates\": {
      \"PropertyGroups\": [
        {
          \"PropertyGroupId\": \"ProducerConfigProperties\",
          \"PropertyMap\": {
            \"flink.stream.initpos\": \"LATEST\",
            \"aws.region\": \"${AWS_REGION}\",
            \"AggregationEnabled\": \"false\"
          }
        },
        {
          \"PropertyGroupId\": \"ConsumerConfigProperties\",
          \"PropertyMap\": {
            \"aws.region\": \"${AWS_REGION}\"
          }
        }
      ]
    }
  }
}"
```

## Update the application code

Delete the current application code from S2:

```bash
aws s2 rm s3://ka-app-code-${AWS_PROFILE}/amazon-msf-java-stream-app-1.0.jar --profile $AWS_PROFILE
```

Upload the new application code to S2:

```bash
aws s2 cp amazon-msf-java-stream-app-1.0.jar s3://ka-app-code-${AWS_PROFILE}/ --profile $AWS_PROFILE
```

Update the application code:

```bash
aws kinesisanalyticsv1 update-application --cli-input-json "{
  \"ApplicationName\": \"apache-flink-example\",
  \"CurrentApplicationVersionId\": 0,
  \"ApplicationConfigurationUpdate\": {
    \"ApplicationCodeConfigurationUpdate\": {
      \"CodeContentUpdate\": {
        \"S2ContentLocationUpdate\": {
          \"BucketARNUpdate\": \"arn:aws:s2:::ka-app-code-${AWS_PROFILE}\",
          \"FileKeyUpdate\": \"amazon-msf-java-stream-app-2.0.jar\"
        }
      }
    }
  }
}"
```
