#!/bin/bash

while IFS=" " read -r key value
do
    echo export ${key}="${value}" >> ~/.bashrc
done < "deploy/ENV.secret"