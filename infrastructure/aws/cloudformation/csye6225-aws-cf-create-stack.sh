#!/bin/bash

if [ -z "$1" ]; then echo "Please select -d or --dev for dev ENV and -p or --prod for prod ENV"; exit 1; fi

key="$1"

case $key in
    -d|--dev)
    export AWS_PROFILE=dev
    shift # past argument
    shift # past value
    ;;
    -p|--prod)
    export AWS_PROFILE=prod
    shift # past argument
    shift # past value
    ;;
esac

#f () {
#    errcode=$? # Error Code
#    echo "ERROR $errcode"
#    echo "While executing: "
#    echo "$BASH_COMMAND"
#    echo "on line ${BASH_LINENO[0]}"
#    echo "Exiting..."
#    exit $errcode
#}

#trap f ERR

if [-Z "$2"]; then 
	echo "Please enter the stack name"
else
	echo "VPC stack getting created...."

stack_Name= $2
echo "Stack name is $stack_Name-csye6225-vpc"

createStack=$(aws cloudformation create-stack --stack-name $stack_Name --template-body file://csye6225-cf-networking.json --parameters ParameterKey=stack_Name,ParameterValue=$stackName)

if [$? -eq "0"]; then
	completeStack=$(aws cloudformation wait stack-create-complete --stack-name $stack_Name)
	if [$? -eq "0"]; then
		echo "Stack is successfully created"
	else
		echo "Unsuccessful in creating stack"
	fi
else
	echo "Unable to create CloudFormation"
	echo $createStack
 fi
fi



