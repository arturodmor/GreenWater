import pandas as pd
import numpy as np
import os
import logging

logger=logging.getLogger(__name__)

class Utils():

    def __init__(self, csv_path = None):

        base_dir = os.path.dirname(__file__)
        self.csv_path = csv_path
        self.csv_path = os.path.join(base_dir, '..', 'data', 'data.csv')

        self.data_processing()


    def data_processing(self):
        
        """To prepare data ready for database writing

        Returns:
            df: Dataframe without null's and thresholds applied
        """

        df = pd.read_csv(self.csv_path)
        for i in df.columns[1:]:
            df[i] = pd.to_numeric(df[i], errors='coerce') # To become 'null' str in NaN
            df[i] = df[i].fillna(df[i].expanding().mean()) # To replace NaN for acumulative mean

            if i=='sensor_a':
                df[i]=df[i].clip(4,7.5) # sensor_a threshold
            else:
                df[i]=df[i].clip(5000,7500) # sensor_b threshold
        
        return df