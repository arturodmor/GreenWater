import pandas as pd
import numpy as np
import os
import logging
import pickle as pkl
from datetime import datetime
from sklearn.linear_model import LinearRegression


logger=logging.getLogger(__name__)

class Utils():

    def __init__(self, df = None, csv_path = None, model_path = None):
        
        self.df = df

        base_dir = os.path.dirname(__file__)

        self.csv_path = csv_path
        self.csv_path = os.path.join(base_dir, '..', 'data', 'data.csv')

        self.model_path = model_path
        self.model_path = os.path.join(base_dir, '..', 'models')


    def data_processing(self):
        
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
    

    def train_model(self):

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