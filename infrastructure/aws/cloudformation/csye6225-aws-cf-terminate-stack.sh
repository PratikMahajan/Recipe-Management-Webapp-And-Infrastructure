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


f () {
    errcode=$? # save the exit code as the first thing done in the trap function
    echo "error $errcode"
    echo "the command executing at the time of the error was"
    echo "$BASH_COMMAND"
    echo "on line ${BASH_LINENO[0]}"
    echo "Exiting the script"
    exit $errcode
}

trap f ERR

if [ -z "$2" ]; then
	echo "Please enter the stack name";
	exit 1;
else
	echo "VPC stack getting deleted...."
fi

echo " "
echo "Deleting cloud stack with name: $2"
echo " "

stackList=$(aws cloudformation list-stacks --query 'StackSummaries[?StackStatus != `DELETE_COMPLETE`].{StackName:StackName}')

if [ ! `echo $stackList | grep -w -c $2 ` -gt 0 ]
then
  echo "Stack with name: $2 does not exists"
  echo "Stack deletion failed"
  echo "Exiting..."
  exit 2
fi


aws cloudformation delete-stack --stack-name $2
echo "Stack deletion in progress"
echo ""
echo "Waiting for the stack $2 to be deleted"

echo ""
aws cloudformation wait stack-delete-complete --stack-name $2
echo "Stack $2 deleted successfully"