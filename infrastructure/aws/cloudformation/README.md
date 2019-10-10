# Cloudformation Deployment

## Input Variables
### Environment:
**The first parameter should be the Environment**
* Development Environment: `-d` or `--dev`
* Production Environment: `-p` or `--prod`
### Stack Name
**The second parameter should be the Stack Name**
* String value only 

## Deploying Infrastructure Over AWS Cloudformation:

**Run the script using the following command**
```shell script
bash csye6225-aws-cf-create-stack.sh <ENV> <STACK_NAME>
```
If the stack is created successfully, infrastructure is deployed, else error messages are displayed.

## Teardown the Infrastructure Over AWS Cloudformation:

**Run the script using the following command**
```shell script
bash csye6225-aws-cf-create-terminate-stack.sh <ENV> <STACK_NAME>
```
If the stack is deleted successfully, infrastructure is torn down, else error messages are displayed.
