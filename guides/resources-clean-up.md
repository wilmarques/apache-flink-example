# Clean up resources for the Flink Application

## Delete the Apache Flink application

Get the creation timestamp of the application:

```bash
flink_app_creation_timestamp=$(aws kinesisanalyticsv2 describe-application --profile $AWS_PROFILE --application-name apache-flink-example | jq -r '.ApplicationDetail.CreateTimestamp')
```

Delete the application:

```bash
aws kinesisanalyticsv2 delete-application --profile $AWS_PROFILE --application-name apache-flink-example --create-timestamp $flink_app_creation_timestamp
```

## Delete the IAM resources

Detach the policy from the role:

```bash
aws iam detach-role-policy --profile $AWS_PROFILE --role-name MF-stream-rw-role --policy-arn arn:aws:iam::${AWS_ACCOUNT_ID}:policy/AKReadSourceStreamWriteSinkStream
```

Delete the role:

```bash
aws iam delete-role --profile $AWS_PROFILE --role-name MF-stream-rw-role
```

Delete the policy:

```bash
aws iam delete-policy --profile $AWS_PROFILE --policy-arn arn:aws:iam::${AWS_ACCOUNT_ID}:policy/AKReadSourceStreamWriteSinkStream
```

## Delete your Kinesis data streams

Delete your Kinesis data streams:

```bash
aws kinesis delete-stream --profile $AWS_PROFILE --stream-name ExampleInputStream
aws kinesis delete-stream --profile $AWS_PROFILE --stream-name ExampleOutputStream
```

## Delete your Amazon S3 object and bucket

Delete the objects in the bucket:

```bash
aws s3 rm --profile $AWS_PROFILE s3://ka-app-code-${AWS_PROFILE}/ --recursive
```

## Delete your CloudWatch resources

Delete the log group:

```bash
aws logs delete-log-group --profile $AWS_PROFILE --log-group-name /aws/kinesis-analytics/apache-flink-example
```
