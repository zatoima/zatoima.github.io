---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "API Gateway+LambdaのSAMでCanaryデプロイを実施"
subtitle: ""
summary: " "
tags: ["AWS"]
categories: ["AWS"]
url: aws-lambda-sam-api-canary-deploy
date: 2022-05-31
featured: false
draft: false

# Featured image
# To use, add an image named `featured.jpg/png` to your pages folder.
# Focal points: Smart, Center, TopLeft, Top, TopRight, Left, Right, BottomLeft, Bottom, BottomRight.
image:
  caption: ""
  focal_point: ""
  preview_only: fals
---

### 前提条件

- SAM CLIがインストールされていること

### SAM INIT

```sh
[ec2-user@bastin test]$ sam init

You can preselect a particular runtime or package type when using the `sam init` experience.
Call `sam init --help` to learn more.

Which template source would you like to use?
	1 - AWS Quick Start Templates
	2 - Custom Template Location
Choice: 1

Choose an AWS Quick Start application template
	1 - Hello World Example
	2 - Multi-step workflow
	3 - Serverless API
	4 - Scheduled task
	5 - Standalone function
	6 - Data processing
	7 - Infrastructure event management
	8 - Machine Learning
Template: 1

Use the most popular runtime and package type? (Python and zip) [y/N]: y

Would you like to enable X-Ray tracing on the function(s) in your application?  [y/N]: y
X-Ray will incur an additional cost. View https://aws.amazon.com/xray/pricing/ for more details

Project name [sam-app]: 

Cloning from https://github.com/aws/aws-sam-cli-app-templates (process may take a moment)


    -----------------------
    Generating application:
    -----------------------
    Name: sam-app
    Runtime: python3.9
    Architectures: x86_64
    Dependency Manager: pip
    Application Template: hello-world
    Output Directory: .
    
    Next steps can be found in the README file at ./sam-app/README.md
        

    Commands you can use next
    =========================
    [*] Create pipeline: cd sam-app && sam pipeline init --bootstrap
    [*] Validate SAM template: sam validate
    [*] Test Function in the Cloud: sam sync --stack-name {stack-name} --watch
   
```

#### 作成されたtemplate.yaml

`Runtime: python3.8`だけ実環境に合わせて修正

```sh
[ec2-user@bastin sam-app]$ cat template.yaml 
AWSTemplateFormatVersion: '2010-09-09'
Transform: AWS::Serverless-2016-10-31
Description: >
  sam-app

  Sample SAM Template for sam-app

# More info about Globals: https://github.com/awslabs/serverless-application-model/blob/master/docs/globals.rst
Globals:
  Function:
    Timeout: 3
    Tracing: Active

Resources:
  HelloWorldFunction:
    Type: AWS::Serverless::Function # More info about Function Resource: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlessfunction
    Properties:
      CodeUri: hello_world/
      Handler: app.lambda_handler
      Runtime: python3.8
      Architectures:
        - x86_64
      Events:
        HelloWorld:
          Type: Api # More info about API Event Source: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#api
          Properties:
            Path: /hello
            Method: get

Outputs:
  # ServerlessRestApi is an implicit API created out of Events key under Serverless::Function
  # Find out more about other implicit resources you can reference within SAM
  # https://github.com/awslabs/serverless-application-model/blob/master/docs/internals/generated_resources.rst#api
  HelloWorldApi:
    Description: "API Gateway endpoint URL for Prod stage for Hello World function"
    Value: !Sub "https://${ServerlessRestApi}.execute-api.${AWS::Region}.amazonaws.com/Prod/hello/"
  HelloWorldFunction:
    Description: "Hello World Lambda Function ARN"
    Value: !GetAtt HelloWorldFunction.Arn
  HelloWorldFunctionIamRole:
    Description: "Implicit IAM Role created for Hello World function"
    Value: !GetAtt HelloWorldFunctionRole.Arn
```

### SAM BUILD

```sh
[ec2-user@bastin sam-app]$ sam build
Your template contains a resource with logical ID "ServerlessRestApi", which is a reserved logical ID in AWS SAM. It could result in unexpected behaviors and is not recommended.
Building codeuri: /home/ec2-user/tmp/test/sam-app/hello_world runtime: python3.8 metadata: {} architecture: x86_64 functions: ['HelloWorldFunction']
Running PythonPipBuilder:ResolveDependencies
Running PythonPipBuilder:CopySource

Build Succeeded

Built Artifacts  : .aws-sam/build
Built Template   : .aws-sam/build/template.yaml

Commands you can use next
=========================
[*] Validate SAM template: sam validate
[*] Invoke Function: sam local invoke
[*] Test Function in the Cloud: sam sync --stack-name {stack-name} --watch
[*] Deploy: sam deploy --guided
        
[ec2-user@bastin sam-app]$ 
```

### SAM DEPLOY

```sh
[ec2-user@bastin sam-app]$ sam deploy --guided

Configuring SAM deploy
======================

	Looking for config file [samconfig.toml] :  Not found

	Setting default arguments for 'sam deploy'
	=========================================
	Stack Name [sam-app]: 
	AWS Region [ap-northeast-1]: 
	#Shows you resources changes to be deployed and require a 'Y' to initiate deploy
	Confirm changes before deploy [y/N]: n
	#SAM needs permission to be able to create roles to connect to the resources in your template
	Allow SAM CLI IAM role creation [Y/n]: y
	#Preserves the state of previously provisioned resources when an operation fails
	Disable rollback [y/N]: n
	HelloWorldFunction may not have authorization defined, Is this okay? [y/N]: y
	Save arguments to configuration file [Y/n]: y
	SAM configuration file [samconfig.toml]:  
	SAM configuration environment [default]: 

	Looking for resources needed for deployment:
	Creating the required resources...
	Successfully created!
	 Managed S3 bucket: aws-sam-cli-managed-default-samclisourcebucket-g2l8ba259m80
	 A different default S3 bucket can be set in samconfig.toml

	Saved arguments to config file
	Running 'sam deploy' for future deployments will use the parameters saved above.
	The above parameters can be changed by modifying samconfig.toml
	Learn more about samconfig.toml syntax at 
	https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-sam-cli-config.html

Uploading to sam-app/abd834336b3b9a077d1ef4926a7e0945  458806 / 458806  (100.00%)

	Deploying with following values
	===============================
	Stack name                   : sam-app
	Region                       : ap-northeast-1
	Confirm changeset            : False
	Disable rollback             : False
	Deployment s3 bucket         : aws-sam-cli-managed-default-samclisourcebucket-g2l8ba259m80
	Capabilities                 : ["CAPABILITY_IAM"]
	Parameter overrides          : {}
	Signing Profiles             : {}

Initiating deployment
=====================
Uploading to sam-app/3c45e542dd42c86b02969d562b823531.template  1199 / 1199  (100.00%)

Waiting for changeset to be created..

～省略～

Successfully created/updated stack - sam-app in ap-northeast-1
```

試しに実行

```sh
[ec2-user@bastin sam-app]$ for i in {1..10}; do curl -w '\n' https://ody2prbd53.execute-api.ap-northeast-1.amazonaws.com/Prod/hello/; done
{"message": "hello world"}
{"message": "hello world"}
{"message": "hello world"}
{"message": "hello world"}
{"message": "hello world"}
{"message": "hello world"}
{"message": "hello world"}
{"message": "hello world"}
{"message": "hello world"}
{"message": "hello world"}
[ec2-user@bastin sam-app]$ 
```

Pythonコードを一部修正。`"message": "hello world v2",`に。

```sh
[ec2-user@bastin sam-app]$ cat hello_world/app.py 
import json

# import requests


def lambda_handler(event, context):
    """Sample pure Lambda function

    Parameters
    ----------
    event: dict, required
        API Gateway Lambda Proxy Input Format

        Event doc: https://docs.aws.amazon.com/apigateway/latest/developerguide/set-up-lambda-proxy-integrations.html#api-gateway-simple-proxy-for-lambda-input-format

    context: object, required
        Lambda Context runtime methods and attributes

        Context doc: https://docs.aws.amazon.com/lambda/latest/dg/python-context-object.html

    Returns
    ------
    API Gateway Lambda Proxy Output Format: dict

        Return doc: https://docs.aws.amazon.com/apigateway/latest/developerguide/set-up-lambda-proxy-integrations.html
    """

    # try:
    #     ip = requests.get("http://checkip.amazonaws.com/")
    # except requests.RequestException as e:
    #     # Send some context about this error to Lambda Logs
    #     print(e)

    #     raise e

    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": "hello world v2",
            # "location": ip.text.replace("\n", "")
        }),
    }

```

SAMテンプレートを修正

下記を追加

>       AutoPublishAlias: live
>       DeploymentPreference:
>         Type: Linear10PercentEvery10Minutes

```sh
[ec2-user@bastin sam-app]$ cat template.yaml 
AWSTemplateFormatVersion: '2010-09-09'
Transform: AWS::Serverless-2016-10-31
Description: >
  sam-app

  Sample SAM Template for sam-app

# More info about Globals: https://github.com/awslabs/serverless-application-model/blob/master/docs/globals.rst
Globals:
  Function:
    Timeout: 3
    Tracing: Active

Resources:
  HelloWorldFunction:
    Type: AWS::Serverless::Function # More info about Function Resource: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlessfunction
    Properties:
      CodeUri: hello_world/
      Handler: app.lambda_handler
      Runtime: python3.8
      Architectures:
        - x86_64
      AutoPublishAlias: live
      DeploymentPreference:
        Type: Linear10PercentEvery10Minutes
      Events:
        HelloWorld:
          Type: Api # More info about API Event Source: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#api
          Properties:
            Path: /hello
            Method: get
```

### sam build＆Deploy

```sh
[ec2-user@bastin sam-app]$ sam build
Your template contains a resource with logical ID "ServerlessRestApi", which is a reserved logical ID in AWS SAM. It could result in unexpected behaviors and is not recommended.
Building codeuri: /home/ec2-user/tmp/test/sam-app/hello_world runtime: python3.8 metadata: {} architecture: x86_64 functions: ['HelloWorldFunction']
Running PythonPipBuilder:ResolveDependencies
Running PythonPipBuilder:CopySource

Build Succeeded

Built Artifacts  : .aws-sam/build
Built Template   : .aws-sam/build/template.yaml

Commands you can use next
=========================
[*] Validate SAM template: sam validate
[*] Invoke Function: sam local invoke
[*] Test Function in the Cloud: sam sync --stack-name {stack-name} --watch
[*] Deploy: sam deploy --guided
[ec2-user@bastin sam-app]$ sam deploy
Uploading to sam-app/81d9b12cbf5541a6c9ff2fcf17671808  458809 / 458809  (100.00%)

	Deploying with following values
	===============================
	Stack name                   : sam-app
	Region                       : ap-northeast-1
	Confirm changeset            : False
	Disable rollback             : False
	Deployment s3 bucket         : aws-sam-cli-managed-default-samclisourcebucket-g2l8ba259m80
	Capabilities                 : ["CAPABILITY_IAM"]
	Parameter overrides          : {}
	Signing Profiles             : {}

Initiating deployment
=====================
Uploading to sam-app/5e5bb4c759ce5a0dac0216a727528b16.template  1300 / 1300  (100.00%)

Waiting for changeset to be created..

~省略~

Successfully created/updated stack - sam-app in ap-northeast-1

```

**<u>DeploymentPreference直後はエイリアス管理されていないので2回ほどコードを修正して動作を確認する。</u>**

```sh
[ec2-user@bastin ~]$ for i in {1..20}; do curl -w '\n' https://ody2prbd53.execute-api.ap-northeast-1.amazonaws.com/Prod/hello/; done
{"message": "hello world v2"}
{"message": "hello world v2"}
{"message": "hello world v2"}
{"message": "hello world v2"}
{"message": "hello world v2"}
{"message": "hello world v2"}
{"message": "hello world v2"}
{"message": "hello world v2"}
{"message": "hello world v2"}
{"message": "hello world v2"}
{"message": "hello world v3"}
{"message": "hello world v2"}
{"message": "hello world v2"}
{"message": "hello world v2"}
{"message": "hello world v2"}
{"message": "hello world v2"}
{"message": "hello world v2"}
{"message": "hello world v2"}
{"message": "hello world v2"}
{"message": "hello world v2"}
[ec2-user@bastin ~]$ 
```



