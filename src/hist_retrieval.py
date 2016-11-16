import pandas as pd
import numpy as np
from datetime import date


def hist_retriever(df, mariners, seahawks, sounders, date_, night, zone):
    """
    Input:
    df = Pandas DataFrame of hist_date_no_out.csv
    mariners, seahawks, sounders = 0 if no home game and 1 if homegame
    date = date of interest
    night = 0 if 6am to 6pm (day) and 1 if 6pm to 6am (night)
    zone = string such as 'zone1' indicating zone of interest
    Ouput: History DataFrame
    """

    # Busy travel times (2010-2020)
    trav_hol = ['2010-11-23', '2010-11-25', '2010-11-26', '2010-12-24',
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
    dang_hol = ['2010-01-01', '2010-07-04', '2011-01-01', '2011-07-04',
                '2012-01-01', '2012-07-04', '2013-01-01', '2013-07-04',
                '2014-01-01', '2014-07-04', '2015-01-01', '2015-07-04',
                '2016-01-01', '2016-07-04', '2017-01-01', '2017-07-04',
                '2018-01-01', '2018-07-04', '2019-01-01', '2019-07-04',
                '2020-01-01', '2020-07-04']

    # If major travel holiday, look up historical data on travel holidays
    if date_ in trav_hol:
        history = df[df.trav_holiday == 1]

    # If 4th of July or New Years day, look up historical data on those days
    elif date_ in dang_hol:
        history = df[df.dang_holiday == 1]

    # Grab historical data based on home games, weekday, and area of Seattle
    else:
        date_ = pd.to_datetime(date_)
        weekday = date_.weekday_name
        history = df[(df.mariners_home == mariners) &
                     (df.seahawks_home == seahawks) &
                     (df.sounders_home == sounders) &
                     (df.weekday == weekday) &
                     (df[zone] == 1)]

    return history
