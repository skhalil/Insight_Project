from PIL import Image          
import numpy as np             
import os                      
from random import shuffle     
from tqdm import tqdm
import matplotlib.pyplot as plt
TRAIN_DIR = 'TRAIN'
TEST_DIR = 'TEST'

IMG_SIZE = 120
LR = 1e-3

MODEL_NAME = 'CNN--{}-{}.model'.format(LR, '6conv-basic')
