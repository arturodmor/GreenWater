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
<div align="center">
	<img src="https://github.com/user-attachments/assets/8d13f6dc-0db3-4772-9ecd-477d9c7cbb54">
</div>

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
![image-1](https://github.com/user-attachments/assets/d2be775b-0e63-4479-98e9-31ee6c03fe3d)

- ***/upload*** : Insert csv from data folder
![image-2](https://github.com/user-attachments/assets/4846d9fa-1caf-4b1a-8cd5-75d2462416ba)

- ***/train-model*** : Updating training. In the next images, you can see how the .pkl file was updated in the source code when the process was executed in API.
![image-3](https://github.com/user-attachments/assets/76f9ea9c-eaa8-4131-b51e-14fb6a993867)
![image-4](https://github.com/user-attachments/assets/f7a90dcb-56e3-4ed6-8944-dc9057c9eb48)

- ***/train-model*** : A box is available for entering new sensor B measurements with which to generate predictions. As a result, a json is generated corresponding to the new instance that is added to the database.
![image-5](https://github.com/user-attachments/assets/bc24ef77-8962-4649-8f02-5ae0f7e82cc6)
![image-6](https://github.com/user-attachments/assets/af99add0-b4f1-433b-8567-7648fdcb6b91)
![image-7](https://github.com/user-attachments/assets/2947856f-8379-4e2a-8708-343d97160889)