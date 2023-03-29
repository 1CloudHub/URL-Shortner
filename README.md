# Welcome to your Private URL Shortener CDK Python project!

The AWS Cloud Development Kit (AWS CDK) lets you define your cloud infrastructure as code in one of its supported programming languages. It is intended for moderately to highly experienced AWS users.

The CDK Python Script and Python Lambda function is available in the repository

Installation of CDK
--------------------------------------------------------------------------------
```
python -m pip install aws-cdk-lib
```
To use the CDK library files installed use the below statement to import it to your script
```
import aws_cdk as cdk
```
Pre-requisites for AWS CDK in Python
--------------------------------------------------------------------------------
```
python -m ensurepip --upgrade
python -m pip install --upgrade pip
python -m pip install --upgrade virtualenv
```
Steps to use the URL Shortener CDK Script available in the repo
--------------------------------------------------------------------------------
```
mkdir url-shortener             # Enter your Directory Name
cd url-shortener                # Change to the created Directory
```
Import the Python and lambda scripts available in the repo

Create & Activate Virtual Environment
-------------------------------------
```
python -m venv .venv         # For Linux / MAC
source venv/source/activate  # For Windows
```
CDK Init - To Initialze
-------------------------------------
```
cdk init app --language python  # To initialize the CDK
```
Refer the below output:

![CDK_INIT](https://raw.githubusercontent.com/1CloudHub/URL-Shortner/main/Images/cdk_init.jpg)

CDK Bootstrap - To establish connectivity between the env and aws account
-------------------------------------------------------------------------
```
cdk bootstrap aws://<ACCOUNT-ID>/us-east-1   # Enter the command as per account-id and region using for the deployment
```

CDK Diff - To view the resources in the stack need to be created
-------------------------------------------------------------------------
```
cdk diff
```
Refer the below output:

![CDK_DIFF](https://raw.githubusercontent.com/1CloudHub/URL-Shortner/main/Images/cdk_diff.jpg)

Configure the ACM in AWS Console
-------------------------------------------
Create a Private Domain of your own in the ACM and configure it to the respective Cloudfront Distribution created in the above deployment.

Configure Route 53
-------------------------------------------
Create a CNAME Record with the ACM certificate CNAME record and Value

Now test the lambda function with an URL as input and get the output as Shortened URL with private domain:thumbsup:
