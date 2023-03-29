from aws_cdk import (
    Duration,
    Stack,
    CfnParameter as param,
    RemovalPolicy as removalPolicy,
    aws_s3 as s3,
    aws_ec2 as ec2,
    aws_cloudfront as cldfrnt,
    aws_cloudfront_origins as origins,
    aws_apigateway as apg,
    aws_certificatemanager as acm,
    aws_lambda as lmbda,
    CfnOutput as output,
    aws_iam as iam,
    Fn as Fn,
)
from constructs import Construct


class ShortUrlStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        #Initialising the existing resource details as variables
        
        VPC_ID = '<VPC-ID>'                     #Enter your VPC ID
        VPC_CIDR = '<VPC-CIDR>'                 #Enter your VPC CIDR
        #APIGW_CIDR = '<API-GATEWAY-CIDR>'      #Enter your API GATEWAY CIDR
        SUBNET_IDS = ["<SUBNET-ID-2>", "<SUBNET-ID-2>"]               #Enter your Subnet ID's
        ROUTETABLE_IDS = ["<ROUTE-TABLE-ID-1>", "<ROUTE-TABLE-ID-2>"] #Enter your Route Table ID
        FQDN = '<FQDN>'                         #Enter your ACM FQDN
        ACM_CERT_ARN = '<ACM Certificate ARN>'  #Enter your ACM Certificate ARN

        #Creating S3 Bucket with with auto-delete policies
        bkt = s3.Bucket(self, "<S3 Bucket Name>",    #Enter Name for S3 Bucket    
                    auto_delete_objects=True,
                    public_read_access=True,
                    removal_policy= removalPolicy.DESTROY,
                    website_index_document="0000",
                    lifecycle_rules=[
                                {   "abortIncompleteMultipartUploadAfter": Duration.days(30),
                                    "expiration": Duration.days(30),
                                    "id": "DeleteAfter30days"
                                }
                                ])
        
        #Creating the ACM Certificate
        cert = acm.Certificate. from_certificate_arn(self,'sURL-cert', 
                    ACM_CERT_ARN)

        #Creating Cloudfront Distribution
        dist = cldfrnt.Distribution(self, "sURL-cldfrnt",
                    default_behavior= cldfrnt.BehaviorOptions(
                    origin=origins.HttpOrigin(domain_name=bkt.bucket_website_domain_name)),
                    domain_names=[FQDN],
                    certificate=cert,
                        )

        #Retrieve existing VPC Configurations
        vpcWSubnets = ec2.Vpc.from_vpc_attributes(self,"existing-VPC",
                            vpc_id=VPC_ID,
                            vpc_cidr_block=VPC_CIDR,
                            availability_zones= Fn.get_azs(),
                            private_subnet_ids=SUBNET_IDS,
                            private_subnet_route_table_ids=ROUTETABLE_IDS)
        

        # HTTPS Listener and HTTPS Security Group for Lambda Function
        https_sg = ec2.SecurityGroup(self, 
                        "HttpsInbound",
                        vpc=vpcWSubnets,
                        security_group_name= "HttpsInbound"
                        )
        https_sg.add_ingress_rule(ec2.Peer.ipv4(vpcWSubnets.vpc_cidr_block),
                        ec2.Port.tcp(443), 
                        description='allow HTTPS access from Local VPC')
        
        https_sg.add_ingress_rule(ec2.Peer.ipv4(APIGW_CIDR),
                        ec2.Port.tcp(443), 
                        description='allow HTTPS access from API Gateway VPC')
            
        #Lambda Function to control access
        func = lmbda.Function(self, "sURL-lmbda",
                    runtime=lmbda.Runtime.PYTHON_3_9,
                    code=lmbda.Code.from_asset('./lambda/'),
                    handler='lambda_function.lambda_handler',
                    vpc=vpcWSubnets,
                    security_groups=[https_sg],
                    environment={'BUCKET_NAME':bkt.bucket_name,
                                'FQDN_NAME':'https://url.domain.com/',  #Enter your domain with url
                                'LOG_LEVEL':'40'}
                    )

        #Policy that allows the Lambda function to access the S3 bucket hosting the website
        func.role.attach_inline_policy(iam.Policy(self,"allow-sURL-BucketAccess",
                    statements=[iam.PolicyStatement( # Restrict to listing and describing tables
                                    effect=iam.Effect.ALLOW,
                                    actions=["s3:GetObjectAcl",
                                    "s3:GetBucketWebsite",
                                    "s3:GetObjectAttributes",
                                    "s3:PutObject",
                                    "s3:GetObject",
                                    "s3:ListBucket",
                                    "s3:GetObjectAcl",
                                    "s3:PutObjectAcl",
                                    "s3:ListAllMyBuckets"],
                                    resources=[bkt.bucket_arn,
                                    bkt.bucket_arn + "/*",])]))
        
        # Optional Part create API Gateway if required

        # apiGwy = apg.RestApi(self, "s3URL",
        #             endpoint_types=[apg.EndpointType.REGIONAL,],
        #             policy=(iam.PolicyDocument(statements=[iam.PolicyStatement(effect=iam.Effect.ALLOW,
        #                                             actions=['execute-api:Invoke',],
        #                                             principals= [iam.AnyPrincipal(),],
        #                                             resources=['execute-api:/*/*/*',]),
        #                                         iam.PolicyStatement(effect=iam.Effect.ALLOW,
        #                                             actions=['lambda:InvokeFunction',],
        #                                             principals= [iam.AnyPrincipal(),],
        #                                             resources=['lambda.amazonaws.com',]),
        #                                         ]))
        #             #endpoint_configuration=apg.EndpointConfiguration(vpc_endpoints=),
        #             )
        
        # apiGwy.root.add_method('POST', 
        #             apg.LambdaIntegration(handler=func,
        #                     proxy=True, ))
        output(self, "S3Bucket", value=bkt.bucket_name)
        output(self, "Distribution", value=dist.distribution_id)
        output(self, "Lambda", value=func.function_name)
