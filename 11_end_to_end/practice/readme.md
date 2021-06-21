# **Behavioural Cloning Test Environment**

This repo provides a simplified test environment for Behavioural Cloning. 
It currently supports the CarRacing-v0 simulator of the OpenAI Gym environment (https://gym.openai.com)

`A`: Acceleration, `S`: Braking, `LEFT`: Left, `RIGHT`: Right

## **Getting Started**
### Requirements
- python 3.8 

- the following dependencies (see below for an instruction to install them)
    - torch
    - torchvision
    - matplotlib
    - numpy
    - pandas
    - gym
    - seaborn
    - pygame
	- Box2D
    - ffmpeg
    - PyOpenGL
	
### First steps

Activate the virtual environment and install all dependencies

`python -m pip install -r requirements.txt`

To execute the data collection run

`python collect.py`

To train the network run

`python train.py`

To test the overall result of the trained imitator run

`python test.py`



## **Data Collection**
With the `collect.py` script the expert data set can be sampled. With the hyperparameter `N_TRAJECTORY`the number of sampled trajectories can be set. `N_TIME` is the number of time steps that are recorded.
Use the above mentioned keyboard commands to play the game. The created trajectories are saved in the `expert` folder. 
In the `summary.csv` file all trajectories are stored that are used for a training.

## **Network Training**

In the folder `nets` there is the script `imitator.py`. In this script the network to be tested is defined. 
The training pipeline can be launched with the `train.py` script. To avoid overfitting of the network, early stopping can be set. 
The parameters and learning curves of the trained network will be saved in the  `result` folder. 

## **Testing the Imitator**

With the `test.py` script the testing of the previous trained network can be launched. `N_TRAJECTORIES` set the number of trials. 
At the end a statistics about the gained reward is printed. The `METHOD` parameter set the network you want to test.
