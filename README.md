# GreenWater

A Python package to deploy FastAPI capable to optimize the water purification dosing process of the chemical "xy". The structure contains a MariaDB database that collect measurements from sensors A and B with the information cleaned. Also, it has integrated regression model to train and predict de chemical dosing.


## Installation

1. If the user wants to isolate dependencies, he can install a virtual environment as follows:
    ```bash
    python -m venv GreenWater
    source GreenWater/bin/activate  # En Windows: GreenWater\Scripts\activate
    ```
2. Install dependencies with a conda environment:
    ```bash
    conda env create --name recoveredenv --file environment.yml
    ```
3. If the user prefers use requirements:
    ```bash
    pip install -r requirements.txt
    ```
4. To install the package GreenWater with setup file:
    ```bash
    pip install -e .
    ```


## Folders

### Data
Contains the file data.csv with the raw data.

### Database
Contains the sqlite predictions.db with RegressionModel results ordered by timestamp execution. in the following image you can see its structure using the Dbeaver desktop interface.
![image](https://github.com/user-attachments/assets/8d13f6dc-0db3-4772-9ecd-477d9c7cbb54)

### GreenWater
This is the project package with which the api executes its functionalities. It is governed by the Utils() class that stores the different project directories. The methods inside the class are:

- ***data_processing*** : To perform data processing
- ***train_model*** : To train and save model, updating it with .pkl file
- ***prediction_and_write_database*** : To determine prediction of the chemical and save the results in a sqlite3 database

### Models
Is the folder that contains the train results, updating it according to the date of the last training session.


## API demostration

To start the API service, execute the following command:
    ```bash
    uvicorn api:app --reload
    ```
The terminal will display the IP to which the service is pointing. If you using the extension /docs, we can see the main menu:
![alt text](image-1.png)

- ***/upload*** : Insert csv from data folder
![alt text](image-2.png)

- ***/train-model*** : Updating training. In the next images, you can see how the .pkl file was updated in the source code when the process was executed in API.
![alt text](image-3.png)
![alt text](image-4.png)

- ***/train-model*** : A box is available for entering new sensor B measurements with which to generate predictions. As a result, a json is generated corresponding to the new instance that is added to the database.
![alt text](image-5.png)
![alt text](image-6.png)
![alt text](image-7.png)