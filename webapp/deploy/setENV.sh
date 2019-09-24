#!/bin/bash

file=deploy/ENV.secret
if [ -e "$file" ]; then
    while IFS=" " read -r key value
    do
      echo export ${key}="${value}" >> ~/.bashrc
    done < "deploy/ENV.secret"
else
    while IFS=" " read -r key value
    do
      echo export ${key}="${value}" >> ~/.bashrc
    done < "ENV.secret"
fi
