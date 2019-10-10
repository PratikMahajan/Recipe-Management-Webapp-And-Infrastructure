# Awscli Deployment

## Input Variables
### Environment:
**The first parameter should be the Environment**
* Development Environment: `-d` or `--dev`
* Production Environment: `-p` or `--prod`

## Deploying Infrastructure Over AWScli:

**Run the script using the following command**
```shell script
sh csye6225-aws-networking-setup.sh <ENV> 
```
**Please enter information as instructed in the script**
If the vpc is created successfully, infrastructure is deployed, else error messages are displayed.

## Teardown the Infrastructure Over AWS Cloudformation:

**Run the script using the following command**
```shell script
sh csye6225-aws-networking-teardown.sh <ENV>
```
**Please enter information as instructed in the script**

If the vpc is deleted successfully, infrastructure is torn down, else error messages are displayed.
