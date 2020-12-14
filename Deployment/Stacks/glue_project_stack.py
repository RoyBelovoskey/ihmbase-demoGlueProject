# from aws_cdk import core


# class GlueProjectStack(core.Stack):

#     def __init__(self, scope: core.Construct, construct_id: str, **kwargs) -> None:
#         super().__init__(scope, construct_id, **kwargs)

#         # The code that defines your stack goes here
#
from aws_cdk import core
from aws_cdk import aws_glue as glue
from aws_cdk import aws_iam as iam

class ScheduledGlueJob (core.Stack):
    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        policy_statement = iam.PolicyStatement(actions=['logs:*','s3:*','iam:*','cloudwatch:*','dynamodb:*','glue:*'])
        policy_statement.add_all_resources()
        #define role
        glue_job_role = iam.Role(self,'Glue-Job-Role',assumed_by=iam.ServicePrincipal('glue.amazonaws.com'))
        glue_job_role.add_to_policy(policy_statement)
        #define job
        job = glue.CfnJob(self,'glue-test-job',role=glue_job_role.role_arn,allocated_capacity=10,command=glue.CfnJob.JobCommandProperty(name='glueetl',script_location='s3://base-nonprod/GlueETLScripts//hello.py'))

# create inline statement, policy then role
# statement = iam.PolicyStatement(actions=["s3:GetObject","s3:PutObject"],
#                                         resources=["arn:aws:s3:::mybucketname",
#                                                     "arn:aws:s3:::mybucketname/data_warehouse/units/*"])
#         write_to_s3_policy = iam.PolicyDocument(statements=[statement])
#         glue_role = iam.Role(
#             self, 'GlueCrawlerFormyDataScienceRole',
#             role_name = 'GlueCrawlerFormyDataScienceRole',
#             inline_policies=[write_to_s3_policy],
#             assumed_by=iam.ServicePrincipal('glue.amazonaws.com'),
#             managed_policies=[iam.ManagedPolicy.from_aws_managed_policy_name('service-role/AWSGlueServiceRole')]
#         )

#define crawler
        # glue_crawler = glue.CfnCrawler(
        #     self, 'glue-crawler-id',
        #     description="Glue Crawler for my-data-science-s3",
        #     name='any name',
        #     database_name='units',
        #     schedule={"scheduleExpression": "cron(5 * * * ? *)"},
        #     role=glue_role.role_arn,
        #     targets={"s3Targets": [{"path": "s3://mybucketname/data_warehouse/units"}]}
        # )
# from aws_cdk import core as cdk
# from aws_cdk import awsglue as glue
# from aws_cdk import aws
# #import * as glue from "@aws-cdk/aws-glue";
# import * as s3 from "@aws-cdk/aws-s3";
# import * as s3Deployment from "@aws-cdk/aws-s3-deployment";
# import * as iam from "@aws-cdk/aws-iam";
# import { replaceValues } from "./lib";
# import { config } from "dotenv";
# config();
#
# const PYTHON_VERSION = "3";
# const GLUE_VERSION = "1.0";
#
# //This value must be glueetl for Apache Spark
# const COMMAND_NAME = "glueetl";
#
# const { RTK, COLLECTIONS, BUCKET_NAME }= process.env;
#
# class GlueETLStack extends cdk.Stack {
#     constructor(scope: cdk.Construct, id: string, props?: cdk.StackProps) {
#         super(scope, id, props);
#
#         const s3Bucket = new s3.Bucket(this, "etl-bucket", {
#             bucketName: BUCKET_NAME,
#             removalPolicy: cdk.RemovalPolicy.DESTROY
#         });
#
#         const dependenciesDeployment = new s3Deployment.BucketDeployment(this, "dependencies-deployment", {
#             sources: [s3Deployment.Source.asset("../dependencies")],
#             destinationBucket: s3Bucket,
#             destinationKeyPrefix: "dependencies"
#         });
#
#         # // Replace hardcoded values in script
#         # replaceValues(
#         #     "scripts/script.py",
#         #     RTK as string,
#         #     MONGO_SERVER as string,
#         #     MONGO_USER as string,
#         #     MONGO_PASSWORD as string,
#         #     MONGO_PORT as string,
#         #     MONGO_SSL == "true" ? "True" : "False",
#         #     MONGO_DATABASE as string,
#         #     `s3://${BUCKET_NAME}/${MONGO_DATABASE as string}/`,
#         #     COLLECTIONS as string
#         # );
#
#         const scriptsDeployment = new s3Deployment.BucketDeployment(this, "scripts-deployment", {
#             sources: [s3Deployment.Source.asset("scripts")],
#             destinationBucket: s3Bucket,
#             destinationKeyPrefix: "scripts"
#         });
#
#         const glueRole = new iam.Role(this, "glue-role", {
#             roleName: "glue-etl-role",
#             assumedBy: new iam.ServicePrincipal("glue.amazonaws.com"),
#             managedPolicies: [
#                 iam.ManagedPolicy.fromAwsManagedPolicyName("AmazonS3FullAccess")
#             ],
#         });
#
#         const glueJob = new glue.CfnJob(this, "glue-job", {
#             name: "glue-job",
#             role: glueRole.roleArn,
#             command: {
#                 name: COMMAND_NAME,
#                 pythonVersion: PYTHON_VERSION,
#                 scriptLocation: `s3://${s3Bucket.bucketName}/scripts/script.py`
#             },
#             glueVersion: GLUE_VERSION,
#             defaultArguments: {
#                 "--extra-jars": `s3://${s3Bucket.bucketName}/${JDBC_PATH}`
#             }
#         });
#
#         const glueTrigger = new glue.CfnTrigger(this, "glue-trigger", {
#             name: "etl-trigger",
#             schedule: "cron(5 * * * ? *)",
#             type: "SCHEDULED",
#             actions: [
#                 {
#                     jobName: glueJob.name
#                 }
#             ],
#             startOnCreation: true
#         });
#         glueTrigger.addDependsOn(glueJob);
#     }
# }