# Welcome to your Private URL Shortener CDK Python project!

The CDK Python Script and Python Lambda function is available in the repository

The AWS Cloud Development Kit (AWS CDK) lets you define your cloud infrastructure as code in one of its supported programming languages. It is intended for moderately to highly experienced AWS users.

Installation of CDK
--------------------------------------------------------------------------------
python -m pip install aws-cdk-lib

To use the CDK library files installed use the below statement to import it to your script

import aws_cdk as cdk

Pre-requisites for AWS CDK in Python
--------------------------------------------------------------------------------
python -m ensurepip --upgrade
python -m pip install --upgrade pip
python -m pip install --upgrade virtualenv

Steps to use the URL Shortener CDK Script available in the repo
--------------------------------------------------------------------------------
>> mkdir url-shortener             # Enter your Directory Name
>> cd url-shortener                # Change to the created Directory

Import the Python and lambda scripts available in the repo

Create & Activate Virtual Environment
-------------------------------------
>> python -m venv .venv         # In-case of Linux / MAC
>> source venv/source/activate  # For Windows

CDK Init - To Initialze
-------------------------------------
>> cdk init app --language python  # To initialize the CDK

Refer the below output:

(.venv) D:Surl\short-url>cdk init
Available templates:
* app: Template for a CDK Application
   └─ cdk init app --language=[csharp|fsharp|go|java|javascript|python|typescript]
* lib: Template for a CDK Construct Library
   └─ cdk init lib --language=typescript
* sample-app: Example CDK Application with some constructs
   └─ cdk init sample-app --language=[csharp|fsharp|go|java|javascript|python|typescript]
****************************************************
*** Newer version of CDK is available [2.70.0]   ***
*** Upgrade recommended (npm install -g aws-cdk) ***
****************************************************

CDK Bootstrap - To establish connectivity between the env and aws account
-------------------------------------------------------------------------
>> cdk bootstrap aws://<ACCOUNT-ID>/us-east-1   # Enter the command as per account-id and region using for the deployment

CDK Diff - To view the resources in the stack need to be created
-------------------------------------------------------------------------
>> cdk diff

Refer the below output:

Stack ShortUrlStack
IAM Statement Changes


┌───┬──────────────────────────────────────────────────────┬────────┬──────────────────────────────────────────────────────┬───────────────────────────────────────────
│   │ Resource                                             │ Effect │ Action                                               │ Principal                                 
├───┼──────────────────────────────────────────────────────┼────────┼──────────────────────────────────────────────────────┼───────────────────────────────────────────
│ + │ ${Custom::S3AutoDeleteObjectsCustomResourceProvider/ │ Allow  │ sts:AssumeRole                                       │ Service:lambda.amazonaws.com               
│   │ Role.Arn}                                            │        │                                                      │                                           
├───┼──────────────────────────────────────────────────────┼────────┼──────────────────────────────────────────────────────┼───────────────────────────────────────────
│ + │ ${sURL-lmbda/ServiceRole.Arn}                        │ Allow  │ sts:AssumeRole                                       │ Service:lambda.amazonaws.com               
├───┼──────────────────────────────────────────────────────┼────────┼──────────────────────────────────────────────────────┼───────────────────────────────────────────
│ + │ ${sURL-pub-s3.Arn}                                   │ Allow  │ s3:DeleteObject*                                                               
│   │ ${sURL-pub-s3.Arn}/*                                 │        │ s3:GetBucket*                                        │ r/Role.Arn}                               
│   │                                                      │        │ s3:List*                                             │                                           
│ + │ ${sURL-pub-s3.Arn}                                   │ Allow  │ s3:GetBucketWebsite                                  │ AWS:${sURL-lmbda/ServiceRole}             
│   │ ${sURL-pub-s3.Arn}/*                                 │        │ s3:GetObject                                         │                                           
│   │                                                      │        │ s3:GetObjectAcl                                      │                                           
│   │                                                      │        │ s3:GetObjectAttributes                               │                                           
│   │                                                      │        │ s3:ListAllMyBuckets                                  │                                           
│   │                                                      │        │ s3:ListBucket                                        │                                           
│   │                                                      │        │ s3:PutObject                                         │                                           
│   │                                                      │        │ s3:PutObjectAcl                                      │                                           
├───┼──────────────────────────────────────────────────────┼────────┼──────────────────────────────────────────────────────┼───────────────────────────────────────────
│ + │ ${sURL-pub-s3.Arn}/*                                 │ Allow  │ s3:GetObject                                         │ AWS:*                                     
└───┴──────────────────────────────────────────────────────┴────────┴──────────────────────────────────────────────────────┴───────────────────────────────────────────

IAM Policy Changes
┌───┬───────────────────────────────────────────────────────────┬──────────────────────────────────────────────────────────────────────────────────────────────┐
│   │ Resource                                                  │ Managed Policy ARN                                                                           │
├───┼───────────────────────────────────────────────────────────┼──────────────────────────────────────────────────────────────────────────────────────────────┤
│ + │ ${Custom::S3AutoDeleteObjectsCustomResourceProvider/Role} │ {"Fn::Sub":"arn:${AWS::Partition}:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"} │
├───┼───────────────────────────────────────────────────────────┼──────────────────────────────────────────────────────────────────────────────────────────────┤
│ + │ ${sURL-lmbda/ServiceRole}                                 │ arn:${AWS::Partition}:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole               │
│ + │ ${sURL-lmbda/ServiceRole}                                 │ arn:${AWS::Partition}:iam::aws:policy/service-role/AWSLambdaVPCAccessExecutionRole           │
└───┴───────────────────────────────────────────────────────────┴──────────────────────────────────────────────────────────────────────────────────────────────┘
Security Group Changes
┌───┬─────────────────────────┬─────┬────────────┬─────────────────┐
│   │ Group                   │ Dir │ Protocol   │ Peer            │
├───┼─────────────────────────┼─────┼────────────┼─────────────────┤
│ + │ ${HttpsInbound.GroupId} │ In  │ TCP 443    │ CIDR            |
│ + │ ${HttpsInbound.GroupId} │ In  │ TCP 443    │ CIDR            |
│ + │ ${HttpsInbound.GroupId} │ Out │ Everything │ Everyone (IPv4) │
└───┴─────────────────────────┴─────┴────────────┴─────────────────┘
(NOTE: There may be security-related changes not in this list. See https://github.com/aws/aws-cdk/issues/1299)

Parameters
[+] Parameter BootstrapVersion BootstrapVersion: {"Type":"AWS::SSM::Parameter::Value<String>","Default":"/cdk-bootstrap/hnb659fds/version","Description":"Version of the CDK Bootstrap resources in this environment, automatically retrieved from SSM Parameter Store. [cdk:skip]"}

Conditions
[+] Condition CDKMetadata/Condition CDKMetadataAvailable: {"Fn::Or":[{"Fn::Or":[{"Fn::Equals":[{"Ref":"AWS::Region"},"af-south-1"]},{"Fn::Equals":[{"Ref":"AWS::Region"},"ap-east-1"]},{"Fn::Equals":[{"Ref":"AWS::Region"},"ap-northeast-1"]},{"Fn::Equals":[{"Ref":"AWS::Region"},"ap-northeast-2"]},{"Fn::Equals":[{"Ref":"AWS::Region"},"ap-south-1"]},{"Fn::Equals":[{"Ref":"AWS::Region"},"ap-southeast-1"]},{"Fn::Equals":[{"Ref":"AWS::Region"},"ap-southeast-2"]},{"Fn::Equals":[{"Ref":"AWS::Region"},"ca-central-1"]},{"Fn::Equals":[{"Ref":"AWS::Region"},"cn-north-1"]},{"Fn::Equals":[{"Ref":"AWS::Region"},"cn-northwest-1"]}]},{"Fn::Or":[{"Fn::Equals":[{"Ref":"AWS::Region"},"eu-central-1"]},{"Fn::Equals":[{"Ref":"AWS::Region"},"eu-north-1"]},{"Fn::Equals":[{"Ref":"AWS::Region"},"eu-south-1"]},{"Fn::Equals":[{"Ref":"AWS::Region"},"eu-west-1"]},{"Fn::Equals":[{"Ref":"AWS::Region"},"eu-west-2"]},{"Fn::Equals":[{"Ref":"AWS::Region"},"eu-west-3"]},{"Fn::Equals":[{"Ref":"AWS::Region"},"me-south-1"]},{"Fn::Equals":[{"Ref":"AWS::Region"},"sa-east-1"]},{"Fn::Equals":[{"Ref":"AWS::Region"},"us-east-1"]},{"Fn::Equals":[{"Ref":"AWS::Region"},"us-east-2"]}]},{"Fn::Or":[{"Fn::Equals":[{"Ref":"AWS::Region"},"us-west-1"]},{"Fn::Equals":[{"Ref":"AWS::Region"},"us-west-2"]}]}]}

Resources
[+] AWS::S3::Bucket sURL-pub-s3 <S3 Bucket ID>
[+] AWS::S3::BucketPolicy sURL-pub-s3/Policy <S3 POLICY ID>
[+] Custom::S3AutoDeleteObjects sURL-pub-s3/AutoDeleteObjectsCustomResource <S3 POLICY ID>
[+] AWS::IAM::Role Custom::S3AutoDeleteObjectsCustomResourceProvider/Role <ROLE ID>
[+] AWS::Lambda::Function Custom::S3AutoDeleteObjectsCustomResourceProvider/Handler <FUNCTION ID>
[+] AWS::CloudFront::Distribution sURL-cldfrnt <CLOUDFRONT-ID>
[+] AWS::EC2::SecurityGroup HttpsInbound <Security-Group-ID>
[+] AWS::IAM::Role sURL-lmbda/ServiceRole <ROLE-ID>
[+] AWS::Lambda::Function sURL-lmbda <FUNCTION-ID>
[+] AWS::IAM::Policy allow-sURL-BucketAccess <POLICY-ID>

Outputs
[+] Output S3Bucket S3Bucket: {"Value":{"Ref":"S3-bucket-id"}}
[+] Output Distribution Distribution: {"Value":{"Ref":"Cloudfront-distribution-id"}}
[+] Output Lambda Lambda: {"Value":{"Ref":"Lambda-Function-id"}}

Other Changes
[+] Unknown Rules: {"CheckBootstrapVersion":{"Assertions":[{"Assert":{"Fn::Not":[{"Fn::Contains":[["1","2","3","4","5"],{"Ref":"BootstrapVersion"}]}]},"AssertDescription":"CDK bootstrap stack version 6 required. Please run 'cdk bootstrap' with a recent version of the CDK CLI."}]}}


Configure the ACM in AWS Console
-------------------------------------------
Create a Private Domain of your own in the ACM and configure it to the respective Cloudfront Distribution created in the above deployment.

Configure Route 53
-------------------------------------------
Create a CNAME Record with the ACM certificate CNAME record and Value

Now test the lambda function with an URL as input and get the output as Shortened URL with private domain!
