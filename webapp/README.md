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
sudo ./deploy/dbsetup.sh
```

## Run

Run the app by using 
```
./gunicornstart.sh
```