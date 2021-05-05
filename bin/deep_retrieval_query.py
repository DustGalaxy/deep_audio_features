import argparse
import torch
from torch.utils.data import DataLoader
from dataloading.dataloading import FeatureExtractorDataset
from lib.training import test
from utils.model_editing import drop_layers
import config
import os
import glob
import numpy as np
import pickle
import scipy.spatial.distance
import deep_retrieval_build_db


def search_deep_database(database_path, query_wav):
    with open(database_path, 'rb') as f:
        all_features = pickle.load(f)
        all_features_temporal = pickle.load(f)
        f_names = pickle.load(f)
        audio_files = pickle.load(f)
        models_folder = pickle.load(f)

    models = deep_retrieval_build_db.load_models(models_folder)
    f, f_temp, f_names = deep_retrieval_build_db.get_meta_features(query_wav, models)
    print(all_features_temporal[0])
    d = scipy.spatial.distance.cdist(f.reshape(-1, 1).T, all_features)[0]
    file_sorted = ([x for _, x in sorted(zip(d, audio_files))])
    distances_sorted = sorted(d)

    for d, f in zip(file_sorted, distances_sorted):
        print(f'{d} {f}')


if __name__ == '__main__':
    # Read arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--db', required=True,
                        type=str, help='Dir of models')
    parser.add_argument('-i', '--input', required=True,
                        type=str, help='Input file for testing')
    args = parser.parse_args()

    search_deep_database(args.db, args.input)