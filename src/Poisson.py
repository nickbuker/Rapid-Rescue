import pandas as pd
import numpy as np
import cPickle as pickle
from statsmodels.discrete.discrete_model import Poisson
from sklearn.preprocessing import StandardScaler


class PoissonModel(object):

    def __init__(self, data):
        # data is path for csv file
        self.data = data
        self.df = pd.read_csv(self.data, low_memory=False)
        # Drop extra column
        self.df.drop(['Unnamed: 0'], axis=1, inplace=True)
        # Create X and y
        self.y = self.df.pop('freq')
        self.X = self.df

    def fit(self):
        # Create scaler and scale X
        scaler = StandardScaler(with_mean=False)
        self.X = scaler.fit_transform(self.X)
        # Fit Poisson model to data
        self.poisson_model = Poisson(self.y, self.X).fit()

    def predict(self, query):
        # Feed query DataFrame to model
        self.query = query
        self.preds = self.poisson_model.predict(query)
        self.zones = ['zone1', 'zone2', 'zone3', 'zone4',
                      'zone5', 'zone6', 'zone7']
        self.results = zip(self.zones, self.preds)
        # Return a list of tuples
        return self.results


if __name__ == '__main__':
    model = PoissonModel('../data/model_data_counted_no_out.csv')
    model.fit()
    # Save fitted model as pickle
    with open('PoissonModel.pkl', 'w') as f:
        pickle.dump(model, f)
