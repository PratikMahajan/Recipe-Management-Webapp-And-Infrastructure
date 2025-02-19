# Recipe Management Application 

## Setup

### Python Environment
Create a virtual environment using either of the following methods:
- `venv` built into the IDE
- `pipenv`
    - Install pipenv using `pip3 install virtualenv`
    - Create a Virtual Environment using `python3 -m virtualenv venv`

Activate the virtual environment using 
```
source venv/bin/activate
```

Setup working environment by running 
```
pip3 install -r requirements.txt
```

### Database
Run the following command to setup the Database

```shell script
make db-setup
```

## Preparing

### Initializing Environment Variables 
Add environment variables in ENV.secret file with the format <br/>
A ENV file is in folder, rename it to ENV.secret and add environment variables
```shell script
<KEY> <VALUE>
# For Example
KEY1 value_here
```

Run `setENV.sh` after setting environment variables to save it in `.bashrc` file

### Initializing Database
After setting up environment variables, Run 
```shell script
./dbinitsh # from deploy folder 
# OR
./deploy/dbinit.sh # from webapp folder
```

## Testing
To run tests, run
```shell script
nosetests test/app_test.py
```


## Run

Run the Web-app by using 
```shell script
make run
```

Enter the Database shell using 
```shell script
make db-shell
```