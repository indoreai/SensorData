import argparse
import os
import warnings


import pandas as pd 
import numpy as np
from sklearn.decomposition import PCA


if __name__=='__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--csv-file-name', default='train.csv')
    args, _ = parser.parse_known_args()
    
    print('Received arguments {}'.format(args))
    
    csv_file_name = args.csv_file_name
    input_data_path = os.path.join('/opt/ml/processing/input', csv_file_name)
    df = pd.read_csv(input_data_path,header=None)
    train_set=df.iloc [:, 1:]
    train_label=df.iloc [:, [0]]
    
    pca = PCA(n_components=2)
    train_features = pca.fit_transform(train_set)
    print(pca.explained_variance_ratio_, type(pca.explained_variance_ratio_))
    component1_ratio=str(pca.explained_variance_ratio_[0])
    component2_ratio = str(pca.explained_variance_ratio_[1])
    principal_df= pd.DataFrame(data = train_features, columns = ['component1_'+component1_ratio, 'component2_'+component2_ratio])
    train_label=train_label.rename(columns={0:'device'})

    final_df = pd.concat([principal_df, train_label], axis = 1)
    
    print('Train data shape after preprocessing: {}'.format(final_df.shape))
    train_features_output_path = os.path.join('/opt/ml/processing/train', 'train_features.csv')
    
    print('Saving training features to {}'.format(train_features_output_path))
    final_df.to_csv(train_features_output_path, index=False)


    
    