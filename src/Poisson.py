import pandas as pd
import numpy as np
import cPickle as pickle
from statsmodels.discrete.discrete_model import Poisson
from sklearn.preprocessing import StandardScaler
from datetime import date
from math import cos, pi


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
        # Busy travel times (2010-2020)
        self.trav_hol = ['2010-11-23', '2010-11-25', '2010-11-26', '2010-12-24',
                         '2010-12-25', '2010-12-26',
                         '2011-11-23', '2011-11-24', '2011-11-25', '2011-12-24',
                         '2011-12-25', '2011-12-26',
                         '2012-11-21', '2012-11-22', '2012-11-23', '2012-12-24',
                         '2012-12-25', '2012-12-26',
                         '2013-11-27', '2013-11-28', '2013-11-29', '2013-12-24',
                         '2013-12-25', '2013-12-26',
                         '2014-11-26', '2014-11-27', '2014-11-28', '2014-12-24',
                         '2014-12-25', '2014-12-26',
                         '2015-11-25', '2015-11-26', '2015-11-27', '2015-12-24',
                         '2015-12-25', '2015-12-26',
                         '2016-11-23', '2016-11-24', '2016-11-25', '2016-12-24',
                         '2016-12-25', '2016-12-26',
                         '2017-11-22', '2017-11-23', '2017-11-24', '2017-12-24',
                         '2017-12-25', '2017-12-26',
                         '2018-11-21', '2018-11-22', '2018-11-23', '2018-12-24',
                         '2018-12-25', '2018-12-26',
                         '2019-11-27', '2019-11-28', '2019-11-29', '2019-12-24',
                         '2019-12-25', '2019-12-26',
                         '2020-11-25', '2020-11-26', '2020-11-27', '2020-12-24',
                         '2020-12-25', '2020-12-26' ]

        # Dangerous holidays are New Years day and July 4th (2010-2020)
        self.dang_hol = ['2010-01-01', '2010-07-04', '2011-01-01', '2011-07-04',
                         '2012-01-01', '2012-07-04', '2013-01-01', '2013-07-04',
                         '2014-01-01', '2014-07-04', '2015-01-01', '2015-07-04',
                         '2016-01-01', '2016-07-04', '2017-01-01', '2017-07-04',
                         '2018-01-01', '2018-07-04', '2019-01-01', '2019-07-04',
                         '2020-01-01', '2020-07-04']

        # Create empyt DataFrame
        zeros = np.zeros((7,21))
        self.columns = [u'mariners_home', u'seahawks_home', u'sounders_home', u'trav_holiday',
                   u'dang_holiday', u'night', u'Monday', u'Saturday', u'Sunday',
                   u'Thursday', u'Tuesday', u'Wednesday', u'day_num', u'zone1', u'zone2',
                   u'zone3', u'zone4', u'zone5', u'zone6', u'zone7', u'seasonality',]
        self.X_test = pd.DataFrame(zeros, columns=self.columns)

    def fit(self):
        # Create scaler and scale X
        self.scaler = StandardScaler(with_mean=False)
        self.X = self.scaler.fit_transform(self.X)
        # Fit Poisson model to data
        self.poisson_model = Poisson(self.y, self.X).fit()

    def query_to_X(self, query):
        # Set zones
        self.X_test.ix[0, 'zone1'] = 1
        self.X_test.ix[1, 'zone2'] = 1
        self.X_test.ix[2, 'zone3'] = 1
        self.X_test.ix[3, 'zone4'] = 1
        self.X_test.ix[4, 'zone5'] = 1
        self.X_test.ix[5, 'zone6'] = 1
        self.X_test.ix[6, 'zone7'] = 1

        #Set home games:
        if self.query['home_game'] == 'mariners':
            self.X_test['mariners_home'] = 1
        if self.query['home_game'] == 'seahawks':
            self.X_test['seahawks_homes'] = 1
        if self.query['home_game'] == 'sounders':
            self.X_test['sounders_home'] = 1

        # Set holidays
        self.X_test['trav_holiday'] = int(self.query['date_input'] in self.trav_hol)
        self.X_test['dang_holiday'] = int(self.query['date_input'] in self.dang_hol)

        # Set night:
        self.X_test['night'] = self.query['time_range']

        # Set weekday
        date_input = pd.to_datetime(self.query['date_input'])
        weekday = date_input.weekday_name
        if weekday in self.columns:
            self.X_test[weekday] = 1

        # Set day_num using timedelta with earliest date in dataset
        day0 = date(2010,6,29)
        self.X_test['day_num'] = (date_input.date() - day0).days

        # Set seasonality
        f = lambda x: 1 + cos(((2 * pi) / 365.25) * (x - 35))
        self.X_test['seasonality'] = self.X_test.day_num.apply(f)

        return self.X_test

    def predict(self, query):
        # Scale data and feed query DataFrame to model
        self.query = query
        self.X_test = self.query_to_X(self.query)
        self.X_test = self.scaler.transform(self.X_test)
        self.preds = self.poisson_model.predict(self.X_test)
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
