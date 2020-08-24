# Big-Data-with-DataJoint-and-NWB
Programming examples from the publication, "Core Principles for the Implementation of the Neurodata Without Borders Data Standard ."

Four Jupyter notebooks walk through the process of using the Neurodata Without Borders standard and database operations with DataJoint. Data for this workflow is in the 'Experimenter 1' folder and is divided for each mouse and each session. To demonstrate programming principles and collaboration, the Jupyter notebooks pass data to a a DataJoint pipeline which is written to the folder called "Shared Directory".

## Setup
Install the following libraries:
* pynwb
* nwbwidgets
* datajoint
* h5py
* numpy
* os
* csv
* datetime
* dateutil
* matplotlib - this should be installed with conda rather than pip to avoid an installation bug

## Obtain credentials for the Datajoint tutorial server:
https://tutorials.datajoint.io/setting-up/introduction.html

## Install Jupyter

## Using the Jupyter notebooks:
You will need to modify the path variable as indicated and enter your credentials for the DataJoint test server.

## ImportsAndTableDefinitions.py
We demonstrate the best practice of keeping definitions and credentials in a single file that is used by multiple scripts.   Update the path and DataJoint credentials in this file.  (If you don't have a python environement, this can be done with Notepad or equivalent plain text editor.)
