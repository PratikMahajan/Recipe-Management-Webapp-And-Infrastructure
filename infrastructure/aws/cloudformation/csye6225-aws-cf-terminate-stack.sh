#!/bin/bash
clear

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
	echo "Please enter stack name"
else
	stackName="$2"
	
	stackTerminate=$(aws cloudformation delete-stack --stack-name $stackName)
	if [$? -ep 0]; then
		echo "Stack Deletion in progress"
	
	aws cloudformation wait stack-delete-complete --stack-name $stackName
	echo $stackTerminate
	echo "Stack is successfully deleted"
        else
		echo "Error in deleting stack"
		echo $stackTerminate
	fi
fi

