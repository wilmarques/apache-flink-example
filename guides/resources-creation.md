# Create resources for the Flink Application

## Create IAM policies

Create a policy that allows the Flink application to read from the input stream and write to the output stream:

```bash
aws iam create-policy --profile $AWS_PROFILE --policy-name AKReadSourceStreamWriteSinkStream --policy-document "{
  \"Version\": \"2012-10-17\",
  \"Statement\": [
    {
      \"Sid\": \"S3\",
      \"Effect\": \"Allow\",
      \"Action\": [
        \"s3:GetObject\",
        \"s3:GetObjectVersion\"
      ],
      \"Resource\": [
        \"arn:aws:s3:::ka-app-code-${AWS_PROFILE}\",
        \"arn:aws:s3:::ka-app-code-${AWS_PROFILE}/*\"
      ]
    },
    {
      \"Sid\": \"ReadInputStream\",
      \"Effect\": \"Allow\",
      \"Action\": \"kinesis:*\",
      \"Resource\": \"arn:aws:kinesis:${AWS_REGION}:${AWS_ACCOUNT_ID}:stream/ExampleInputStream\"
    },
    {
      \"Sid\": \"WriteOutputStream\",
      \"Effect\": \"Allow\",
      \"Action\": \"kinesis:*\",
      \"Resource\": \"arn:aws:kinesis:${AWS_REGION}:${AWS_ACCOUNT_ID}:stream/ExampleOutputStream\"
    }
  ]
}"
```

Create a role that will be assumed by the Flink application:

```bash
aws iam create-role --profile $AWS_PROFILE --role-name MF-stream-rw-role --assume-role-policy-document '{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Service": "kinesisanalytics.amazonaws.com"
      },
      "Action": "sts:AssumeRole"
    }
  ]
}'
```

Attach the policy to the role:

```bash
aws iam attach-role-policy --profile $AWS_PROFILE --role-name MF-stream-rw-role --policy-arn arn:aws:iam::${AWS_ACCOUNT_ID}:policy/AKReadSourceStreamWriteSinkStream
```

## Create the Managed Service for Apache Flink application

```bash
aws kinesisanalyticsv2 create-application --profile $AWS_PROFILE --cli-input-json "{
  \"ApplicationName\": \"apache-flink-example\",
  \"RuntimeEnvironment\": \"FLINK-1_18\",
  \"ServiceExecutionRole\": \"arn:aws:iam::${AWS_ACCOUNT_ID}:role/MF-stream-rw-role\",
  \"ApplicationConfiguration\": {
    \"ApplicationCodeConfiguration\": {
      \"CodeContent\": {
        \"S3ContentLocation\": {
          \"BucketARN\": \"arn:aws:s3:::ka-app-code-${AWS_PROFILE}\",
          \"FileKey\": \"amazon-msf-java-stream-app-1.0.jar\"
        }
      },
      \"CodeContentType\": \"ZIPFILE\"
    },
    \"EnvironmentProperties\": {
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
