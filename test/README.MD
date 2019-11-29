# Template Generator Test

This directory contains an example structure used to generate CloudFormation templates that generate S3 buckets in
two different environments.

## Development Environment Build

```bash
python3 ./template.py dev ./templates ./config ./output/dev.yml
```

### Example Template Output

```yaml
AWSTemplateFormatVersion: "2010-09-09"
Description: "Example Infrastructure Deployment (Development Environment)"
Resources:
   ExampleDevBucket1:
    Type: AWS::S3::Bucket
    Properties:
      BucketName: bucket-1.dev.example.eonx-poc.com
   ExampleDevBucket2:
    Type: AWS::S3::Bucket
    Properties:
      BucketName: bucket-2.dev.example.eonx-poc.com
Outputs:
   ExampleDevBucket1:
    Value: !Ref ExampleDevBucket1
    Export:
      Description: This is the development bucket 1
      Name: bucket-1.dev.example.eonx-poc.com
   ExampleDevBucket2:
    Value: !Ref ExampleDevBucket2
    Export:
      Description: This is the development bucket 2
      Name: bucket-2.dev.example.eonx-poc.com
```


## Production Environment Build

```bash
python3 ./template.py prod ./templates ./config ./output/prod.yml
```

### Example Template Output

```yaml
AWSTemplateFormatVersion: "2010-09-09"
Description: "Example Infrastructure Deployment (Development Environment)"
Resources:
   ExampleDevBucket1:
    Type: AWS::S3::Bucket
    Properties:
      BucketName: bucket-1.dev.example.eonx-poc.com
   ExampleDevBucket2:
    Type: AWS::S3::Bucket
    Properties:
      BucketName: bucket-2.dev.example.eonx-poc.com
Outputs:
   ExampleDevBucket1:
    Value: !Ref ExampleDevBucket1
    Export:
      Description: This is the development bucket 1
      Name: bucket-1.dev.example.eonx-poc.com
   ExampleDevBucket2:
    Value: !Ref ExampleDevBucket2
    Export:
      Description: This is the development bucket 2
      Name: bucket-2.dev.example.eonx-poc.com
```