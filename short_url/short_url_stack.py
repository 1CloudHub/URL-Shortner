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

        VPC_ID = 'vpc-03a7bf0fff077e4db'
        VPC_CIDR = '10.30.0.0/16'
        APIGW_CIDR = '10.3.0.0/16'
        SUBNET_IDS = ["subnet-0bdb2fd58eb851205", "subnet-010254035fdaf8b9c"]   #subnet-0f0056a9488994519, subnet-08fdb84f20d43f7dd
        ROUTETABLE_IDS = ["rtb-047756c651cb77d5f", "rtb-047756c651cb77d5f"]
        FQDN = 'surl1.1cloudhub.com'
        ACM_CERT_ARN = 'arn:aws:acm:us-east-1:272858488437:certificate/efdefd8e-2301-4c34-8fdf-f3a53146fe62'

        bkt = s3.Bucket(self, "sURL-pub-s3",
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
        
        cert = acm.Certificate. from_certificate_arn(self,'sURL-cert', 
                    ACM_CERT_ARN)

        dist = cldfrnt.Distribution(self, "sURL-cldfrnt",
                    default_behavior= cldfrnt.BehaviorOptions(
                    origin=origins.HttpOrigin(domain_name=bkt.bucket_website_domain_name)),
                    domain_names=[FQDN],
                    certificate=cert,
                        )
                
        vpcWSubnets = ec2.Vpc.from_vpc_attributes(self,"existing-VPC",
                            vpc_id=VPC_ID,
                            vpc_cidr_block=VPC_CIDR,
                            availability_zones= Fn.get_azs(),
                            private_subnet_ids=SUBNET_IDS,
                            private_subnet_route_table_ids=ROUTETABLE_IDS)
        # vpcWSubnets = ec2.Vpc.from_lookup(self,"Existing-VPC",
        #                     vpc_id=VPC_ID, 
        #                     #subnet_group_name_tag="1CH-PrivateSubnet-1a",
        #                     )

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
            
        
        func = lmbda.Function(self, "sURL-lmbda",
                    runtime=lmbda.Runtime.PYTHON_3_9,
                    code=lmbda.Code.from_asset('./lambda/'),
                    handler='lambda_function.lambda_handler',
                    vpc=vpcWSubnets,
                    # vpc_subnets=ec2.SubnetSelection(subnet_filters=[ec2.SubnetFilter.by_ids(SUBNET_IDS)]),
                    security_groups=[https_sg],
                    environment={'BUCKET_NAME':bkt.bucket_name,
                                #'FQDN_NAME':'https://' + dist.distribution_domain_name + '/',
                                'FQDN_NAME':'https://url.1cloudhub.com/',
                                'LOG_LEVEL':'40'}
                    )

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