#!/bin/bash
clear

if [ -z "$1" ]; then echo "Please select -d or --dev for dev ENV and -p or --prod for prod ENV"; exit 1; fi

key="$1"

case $key in
    -d|--dev)
    export AWS_PROFILE=dev
    ;;
    -p|--prod)
    export AWS_PROFILE=prod
    ;;
esac

## Checking whether the stack-name is passed as an arguement
if [ -z "$2" ]; then
	echo "Please enter the stack name";
	exit 1;
else
	echo "VPC stack getting created...."
fi

echo "Creating cloud stack with name: $2"

stackList=$(aws cloudformation list-stacks --query 'StackSummaries[?StackStatus != `DELETE_COMPLETE`].{StackName:StackName}')


if [  `echo $stackList | grep -w -c $2 ` -gt 0 ]
then
  echo "Stack with name: $2  exists"
  echo "Stack creation failed"
  echo "Exiting.."
  exit 1
fi

#Replacing the STACK_NAME passed by the user in the csye6225-cf-networking-parameters.json
sed -i "s/REPLACE_STACK_NAME/$2/g" csye6225-cf-networking-parameters.json

##Creating Stack
#echo "Creating Cloud Stack $1"
response=$(aws cloudformation create-stack --stack-name "$2" --template-body file://csye6225-cf-networking.json --parameters file://csye6225-cf-networking-parameters.json)
echo "Waiting for Stack $2 to be created"
echo "$response"

aws cloudformation wait stack-create-complete --stack-name $2
echo "stack $2 created successfully"
sed -i "s/$2/REPLACE_STACK_NAME/g" csye6225-cf-networking-parameters.json