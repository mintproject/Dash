# -*- coding: utf-8 -*-
import pandas as pd

df = None
def load_data(args):
    global df
    if "filename" in args and args["filename"] is not None:
        filename = args["filename"][0]
        df = pd.read_csv('./viz/data/economic/{}'.format(filename))         
    else:
        df = pd.read_csv('./viz/data/economic/results_summary_bycrop_aggregate.csv') 