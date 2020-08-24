#We keep all of our import statements in one place, so updates can be done in one place. Please update the values below.


#Libraries
import numpy as np
import os
import pynwb #NWB API
import pandas as pd
import h5py #Provides methods to supplement NWB
import datajoint as dj #
import csv 
import import_ipynb #This lets us pass values from Jupyter to this script

from datetime import datetime
from dateutil import tz
from pynwb import NWBHDF5IO
from nwbwidgets import nwb2widget #Displays file contents in Jupyter
from matplotlib import pylab as plt



# 1) PROVIDE YOUR DATAJOINT CREDENTIALS

def connect_to_dj():
    dj.config['database.host'] = 'tutorial-db.datajoint.io' #Tutorial server
    dj.config['database.user'] = 'marikelreimer'
    dj.config['database.password'] = 'AreRA3c5yc'

    dj.conn()

    #Create a schema to organize the pipeline. Defining it here means you only need to change the code in one place.
    current_schema = dj.schema('marikelreimer_tutorial', locals())
    return current_schema

schema = connect_to_dj()
schema

# 2) Specify the source data type.  Chapter 4 demonstrates how to swich to NWB

file_type = 'NoseLocationLog.csv'

# 3) Chapter 4 uses a function so that you can tell it which file type you want to read.

def file_reader(file_type):
    #def type_handler(self, file_type):
    if file_type == 'nwb':
        #See Chapter 2 for details about this method of accessing timeseries names
        timeseries_name = str(list(nwbfile.processing['behavior'].data_interfaces))        
        #Clean the sting before we use it
        timeseries_name = timeseries_name[:]
        #Use timeseries name to retrieve data in timeseries group
        data = nwbfile.processing['behavior'][timeseries_name].data[:]
        
        #Extract data from the data variable in the timeseries group
        print(data)
        return data

    elif file_type == 'NoseLocationLog.csv':
        data = np.genfromtxt('NoseLocationLog.csv', delimiter=',', skip_header=1)
        return data

    else:
        print('file not recognized')

# 4) Table definitions from Chapter 1

@schema
class Mouse(dj.Manual):
    definition = """
    subject_id: varchar(128)                  # Primary keys above the '---'
    ---
    #non-primary columns below the '---' in alphabetical order
    date_of_birth: timestamp 
    genotype: enum('B6', 'BalbC')    
    sex: enum('M', 'F', 'U')
    species: varchar(128)
    subject_description: varchar(128)
    weight: varchar(128)
    """


@schema
class Session(dj.Manual):
        definition = """
        ->Mouse                                  #Dependency on Mouse table established
        name: varchar(128)                  #Primary key for the session table
        ---
        comments: varchar(128)
        description: varchar(128) #Timeseries description
        experiment_description: varchar(128)
        experimenter: enum('Experimenter 1', 'Experimenter 2')
        identifier: varchar(128)                
        institution: varchar(128)
        lab: varchar(128)
        rate: float
        raw_data_link: varchar(128)
        reference_frame: varchar(128)
        session_description: varchar(128)
        session_start_time: timestamp
        starting_time: float
        """



@schema
class Position(dj.Imported):
    definition = """
    -> Session
    ---
    coordinates:  longblob    # X,Y coordinates of mouse
    """
    
    def _make_tuples(self, key):
        #Pass the file_type variable to the file_reader function and store the results in 'data'
        data = file_reader(file_type)
        #Associate 'data' with the coordinates key
        key['coordinates'] = data
        #Insert into Position table
        self.insert1(key)
        print('Populated a position for {subject_id}'.format(**key))


@schema
class PositionStatistics(dj.Computed):
    definition = """
    -> Position
    ---
    left_side: float    # coordinates in left half
    right_side: float    #coordinates in the right half
    preference_index: float #left_side - right_side/ left_side + right_side 
    """
    
    def _make_tuples(self, key):
        print('Populating for: ', key)
        

        coordinates = (Position() & key).fetch1('coordinates')    # fetch activity as NumPy array
        coordinates = coordinates[:,0] #We use only the X values, since we are comparing time spent in the left versus right half of the arena
        
        arena_length = max(coordinates)

        #Check out the DataJoint tutorial for saving electrophysiology as an array  
        left_side = (coordinates < (arena_length/2)).astype(np.int)
        right_side = (coordinates > (arena_length/2)).astype(np.int)

        preference_index = (left_side.sum() - right_side.sum())/(left_side.sum() + right_side.sum())

        # save results and insert
        key['left_side'] = left_side.sum()
        key['right_side'] = right_side.sum()
        key['preference_index'] = preference_index
        self.insert1(key)

