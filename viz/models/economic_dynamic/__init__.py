# -*- coding: utf-8 -*-
import pandas as pd

tips = None
def load_data(args):
    global tips
    tips = pd.read_csv('./viz/data/economic/results_summary_bycrop.csv')