#%% Overview
import numpy as np
import pandas as pd
import random
try:
    from sklearnex import patch_sklearn
    patch_sklearn()
except:
    pass

#%% Read Inputs
from loader import load_kaggle_player_games

df = load_kaggle_player_games()

#%% Filter unwanted rows
MIN_SEASON = 20132014
MIN_TOI = 500 #seconds
# TODO filter out 4th line plugs that aren't fantasy relevant. Some kind of filtering on points

df = df[(df['season'] >= MIN_SEASON) \
        & (df['TOI'] >= MIN_TOI)]

##### FEATURE EXTRACTION:
#%% Compute rate stats
from stats import add_rate_stats

df['S%'] = (df['G'] / df['S']).fillna(0).replace(np.inf, 1)

df = add_rate_stats(df, ['G', 'A', 'S', 'HIT', 'BLK']) # computes /60 stats
df = add_rate_stats(df, ['PPG', 'PPA'], time='PP') # computes /60PP stats
df = add_rate_stats(df, ['SHG', 'SHA'], time='SH') # computes /60SH stats
#%% Compute windowed sums (general-purpose function that returns sums over last n games or seasons)

##### MODEL TRAINING
#%% Train-test split
# We preserve temporal order since there is a timeseries structure

#%% Model selection and training. Print evaluation metrics

#%% Commit to GitHub and update writeup