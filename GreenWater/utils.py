import pandas as pd
import numpy as np
import os
import glob
import logging
import pickle as pkl
from datetime import datetime
from sklearn.linear_model import LinearRegression
import sqlite3

logger=logging.getLogger(__name__)

class Utils():

    """ This class contains all functions to complete all GreenWater requirements"""

    def __init__(self, df = None, csv_path = None, model_path = None, database_path = None):
        
        # Dataframe for data science
        self.df = df

        # Base dir to work with relative paths
        base_dir = os.path.dirname(__file__)

        # Path to open data
        self.csv_path = csv_path
        self.csv_path = os.path.join(base_dir, '..', 'data', 'data.csv')

        # Path for save and load model
        self.model_path = model_path
        self.model_path = os.path.join(base_dir, '..', 'models')

        # Path to connect to database
        self.database_path = database_path
        self.database_path = os.path.join(base_dir, '..', 'database','predictions.db')


    def data_processing(self,df):
        
        """To prepare data ready for database writing

        Returns:
            df: Dataframe without null's and thresholds applied
        """

        self.df = pd.read_csv(self.csv_path)

        for i in self.df.columns[1:]:
            self.df[i] = pd.to_numeric(self.df[i], errors='coerce') # To become 'null' str in NaN
            self.df[i] = self.df[i].fillna(self.df[i].expanding().mean()) # To replace NaN for acumulative mean

            if i=='sensor_a':
                self.df[i] = self.df[i].clip(4,7.5) # sensor_a threshold
            else:
                self.df[i] = self.df[i].clip(5000,7500) # sensor_b threshold
        
        return self.df
    

    def train_model(self,df):

        """To train LinearRegression model, and save results

        Returns:
            model.pkl: The model results are storing in .pkl inside of /models 
        """

        # Reshape data
        X = self.df['sensor_b'].to_numpy().reshape(-1,1)
        y = self.df['sensor_a'].to_numpy().reshape(-1,1)

        # Train data
        model = LinearRegression()
        model.fit(X,y)

        #Last model trained. Previous models will be deleted
        for file in os.listdir(self.model_path):
            file_path = os.path.join(self.model_path, file)
            os.remove(file_path)

        # Write model.pkl with last timestamp
        train_dt = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(os.path.join(self.model_path,'linear_model_{}.pkl'.format(train_dt)), 'wb') as f:
            pkl.dump(model, f)
        
        logger.info(f"New model trained in {train_dt}")

        return model
    

    def prediction_and_write_database(self,sensor_b):

        """To do predictions and write results in database

        Args:
            sensor_b(float): Input measurements

        Returns:
            predictions(float)
            predict_dt(Timestamp): The time when the prediction was done
        """

        # Open model
        file = os.listdir(self.model_path)

        with open(os.path.join(self.model_path,file[0]),'rb') as f:
            model = pkl.load(f)

        # Condition to avoid to store prediction with measurements outside the threshold
        try:
            if 5000 <= sensor_b <= 7500:
                # To do the prediction was necessary pass data in 2D array, but in database only store the float number
                prediction = model.predict([[sensor_b]])[0][0]
                predict_dt = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            else:
                raise ValueError("sensor_b is outside of range [5000,7500]")
    
        except ValueError as e:
            logger.error(e)


        # DATABASE
        # Create and establish database connection
        conn = sqlite3.connect(self.database_path)

        # Interact with database
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS predictions (predict_dt TIMESTAMP PRIMARY KEY, sensor_b FLOAT, predict_value FLOAT)''')
        cursor.execute(f'''INSERT INTO predictions (predict_dt, sensor_b, predict_value) VALUES ('{predict_dt}', '{sensor_b}', '{prediction}');''')
    
        # Apply changes and close connection
        conn.commit()
        conn.close()

        return {"predict_dt": predict_dt, "sensor_b": sensor_b, "value": prediction}