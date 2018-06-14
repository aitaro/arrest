# common
import pandas as pd
import numpy as np
from pandas import DataFrame
import re
import datetime
import random
from common import logger

train_data= pd.read_csv('../csv/train.csv', low_memory=False)
test_data = pd.read_csv('../csv/test.csv')
gps_data = pd.read_csv('../csv/country_location.csv')

def fix(data,type):

    fixed_train_data = pd.DataFrame()
    fixed_train_data['driver_age'] = data.driver_age
    fixed_train_data['county_fips'] = data.county_fips
    if type == 'train':
        fixed_train_data = pd.merge(data, gps_data, on='county_fips').loc[:,['stop_time',
                                                                                   'stop_date',
                                                                                   'lat',
                                                                                   'lng',
                                                                                   'driver_gender',
                                                                                   'driver_age',
                                                                                   'driver_race',
                                                                                   'violation',
                                                                                   'search_conducted',
                                                                                   'search_type',
                                                                                   'contraband_found',
                                                                                   'stop_duration',
                                                                                   'is_arrested'
                                                                                  ]]
    else:
        fixed_train_data = pd.merge(data, gps_data, on='county_fips').loc[:,['stop_time',
                                                                                   'stop_date',
                                                                                   'lat',
                                                                                   'lng',
                                                                                   'driver_gender',
                                                                                   'driver_age',
                                                                                   'driver_race',
                                                                                   'violation',
                                                                                   'search_conducted',
                                                                                   'search_type',
                                                                                   'contraband_found',
                                                                                   'stop_duration'
                                                                                  ]]

    fixed_train_data.loc[fixed_train_data['driver_gender'] == 'M', 'driver_gender'] = 1
    fixed_train_data.loc[fixed_train_data['driver_gender'] == 'F', 'driver_gender'] = 0

    fixed_train_data.loc[fixed_train_data['driver_race'] == 'White', 'white'] = 1
    fixed_train_data.loc[fixed_train_data['driver_race'] == 'Black', 'black'] = 1
    fixed_train_data.loc[fixed_train_data['driver_race'] == 'Hispanic', 'hispanic'] = 1
    fixed_train_data.loc[fixed_train_data['driver_race'] == 'Asian', 'asian'] = 1

    fixed_train_data.loc[fixed_train_data['violation'] == 'Speeding', 'speeding'] = 1
    fixed_train_data.loc[fixed_train_data['violation'] == 'Registration/plates  ', 'plate'] = 1
    fixed_train_data.loc[fixed_train_data['violation'] == 'Moving violation', 'moving_violation'] = 1
    fixed_train_data.loc[fixed_train_data['violation'] == 'Cell phone', 'cell_phone'] = 1
    fixed_train_data.loc[fixed_train_data['violation'] == 'Seat belt', 'seat_belt'] = 1
    fixed_train_data.loc[fixed_train_data['violation'] == 'Lights', 'lights'] = 1

    fixed_train_data.loc[fixed_train_data['search_conducted'] == True, 'search_conducted'] = 1
    fixed_train_data.loc[fixed_train_data['search_conducted'] == False, 'search_conducted'] = 0

    fixed_train_data.loc[fixed_train_data['search_type'] == 'Consent', 'consent'] = 1
    fixed_train_data.loc[fixed_train_data['search_type'] == 'Inventory', 'inventory'] = 1

    fixed_train_data.loc[fixed_train_data['contraband_found'] == True, 'contraband_found'] = 1
    fixed_train_data.loc[fixed_train_data['contraband_found'] == False, 'contraband_found'] = 0

    fixed_train_data.loc[fixed_train_data['stop_duration'] == '1-15 min', 'stop_duration'] = 1
    fixed_train_data.loc[fixed_train_data['stop_duration'] == '16-30 min', 'stop_duration'] = 2
    fixed_train_data.loc[fixed_train_data['stop_duration'] == '30+ min', 'stop_duration'] = 3

    # fixed_train_data = fixed_train_data.fillna({'stop_time': '%02d' % random.randrange(24) + ':' + '%02d' % random.randrange(60)})
    fixed_train_data = fixed_train_data.fillna({'stop_time': '12:00'})

    fixed_train_data.stop_time = fixed_train_data.apply(lambda x: int(x.stop_time[0:2]) * 60 + int(x.stop_time[3:5]), axis=1)

    fixed_train_data = fixed_train_data.fillna(0)

    fixed_train_data = fixed_train_data.drop("stop_date", axis=1)
    fixed_train_data = fixed_train_data.drop("driver_race", axis=1)
    fixed_train_data = fixed_train_data.drop("violation", axis=1)
    fixed_train_data = fixed_train_data.drop("search_type", axis=1)

    return fixed_train_data

fixed_train_data = fix(train_data, 'train')
fixed_train_data.to_csv("../csv/fixed_train.csv")
logger.info('finish fixing train data')
fix(test_data, 'test').to_csv("../csv/fixed_test.csv")
logger.info('finish fixing test data')
