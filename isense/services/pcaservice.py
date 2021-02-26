"""
    Get PCA Data from csv

    Created on Feb 07, 2020

    @author: Deepak Kanthi
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA

import boto3
import re
import os
import sagemaker
from sagemaker.sklearn.processing import SKLearnProcessor
from sagemaker.processing import ProcessingInput, ProcessingOutput

# role = ''
# bucket = ''
# prefix = ''
# region = boto3.session.Session().region_name

# sklearn_processor = SKLearnProcessor(framework_version='0.20.0',
#                                      role=role,
#                                      instance_type='ml.m5.xlarge',
#                                      instance_count=1)


# def get_pca_feature_data(csv_file):
#     """
#     Porcess on Sagemaker & perform PCA and return feature set
#     :param csv_file: absolute path of csv file
#     :return: List of 2 features
#     """
#     key = 'train.csv'
#     with open(csv_file, "rb") as f:
#         boto3.resource('s3').Bucket(bucket).Object(os.path.join(prefix, 'input', key)).upload_fileobj(f)

#     s3_train_data = 's3://{}/{}/input/{}'.format(bucket, prefix, key)
#     print('uploaded training data location: {}'.format(s3_train_data))

#     input_data = 's3://{}/{}/input/{}'.format(bucket, prefix, key)
#     print('uploaded preprocessing data location: {}'.format(input_data))

#     out_key = 'train_features.csv'
#     out_data = 's3://{}/{}/output/{}'.format(bucket, prefix, out_key)
#     print('Output preprocessing data location: {}'.format(out_data))

#     sklearn_processor.run(code='pcaprocessing.py',
#                           inputs=[ProcessingInput(
#                               source=input_data,
#                               destination='/opt/ml/processing/input')],
#                           outputs=[ProcessingOutput(output_name='train_data',
#                                                     source='/opt/ml/processing/train',
#                                                     destination=out_data)
#                                    ],
#                           arguments=['--csv-file-name', 'train.csv']
#                           )

#     preprocessing_job_description = sklearn_processor.jobs[-1].describe()
#     preprocessed_training_data = None
#     output_config = preprocessing_job_description['ProcessingOutputConfig']
#     for output in output_config['Outputs']:
#         if output['OutputName'] == 'train_data':
#             preprocessed_training_data = output['S3Output']['S3Uri']

#     if preprocessed_training_data:
#         print('preprocessed_training_data ', preprocessed_training_data)
#         training_features = pd.read_csv(preprocessed_training_data + '/train_features.csv')
#         header_list=list(training_features.columns.values)
#         print('header_list' , header_list)
#         variance_list=[float(header.split('_')[1])*100 for header in header_list[:2]]
#         print("variance_list ", variance_list)

#         #start
#         targets = training_features['device'].unique().tolist()
#         colors_all = ["#CC0000", "#007E33", "#ffbb33", "#0d47a1", "#9c27b0", "#3e2723", " #d84315", "#76ff03",
#                       "#eeff41",
#                       "#f50057"] * 5
#         colors = colors_all[0:len(targets)]
#         color_dict = {target: color for target, color in zip(targets, colors)}
#         count_dict = {target: 1 for target in targets}
#         legend_list = [{"text": target, "color": color} for target, color in zip(targets, colors)]

#         ret_list = [list(item) + [item[2]+"\n" +str(round(item[0],2))+ " , " +str(round(item[1],2))] for item in training_features.to_numpy()]
#         for item in ret_list:
#             item[3] = str(count_dict[item[2]]) + "\n" + str(round(item[0], 2)) + " , " + str(round(item[1], 2))
#             count_dict[item[2]] = count_dict[item[2]] + 1
#             item[2] = str({"fill-color": color_dict.get(item[2])}).replace('"', '').replace("'", '')

#         ret_list = [tuple(item) for item in ret_list]
#         ret_list = [('', '', {'role': 'style'}, {'role': 'tooltip'})] + ret_list

#         #end

#         print('Training features shape: {}'.format(training_features.shape))
#         # ret_list = [tuple(item) for item in training_features.to_numpy()]
#         return ret_list, legend_list, variance_list

#     return None, None, None


def get_pca_feature_data_local(csv_file):
    """
    Process on Local machine & perform PCA and return feature set
    :param csv_file: absolute path of csv file
    :return: List of 2 features
    """

    df = pd.read_csv(csv_file, header=None)
    train_set = df.iloc[:, 1:]
    train_label = df.iloc[:, [0]]

    pca = PCA(n_components=2)
    train_features = pca.fit_transform(train_set)
    print(pca.explained_variance_ratio_, type(pca.explained_variance_ratio_))
    component1_ratio = str(pca.explained_variance_ratio_[0])
    component2_ratio = str(pca.explained_variance_ratio_[1])

    principal_df = pd.DataFrame(data=train_features,
                                columns=['component1_' + component1_ratio, 'component2_' + component2_ratio])
    train_label = train_label.rename(columns={0: 'device'})

    final_df = pd.concat([principal_df, train_label], axis=1)

    print('Train data shape after preprocessing: {}'.format(final_df.shape))
    train_features_output_path = 'train_features.csv'

    print('Saving training features to {}'.format(train_features_output_path))
    final_df.to_csv(train_features_output_path, index=False)

    header_list=list(final_df.columns.values)
    print('header_list' , header_list)
    variance_list=[float(header.split('_')[1])*100 for header in header_list[:2]]
    print('variance_list' , variance_list)
    targets = final_df['device'].unique().tolist()
    colors_all = ["#CC0000", "#007E33", "#ffbb33", "#0d47a1", "#9c27b0", "#3e2723", " #d84315", "#76ff03", "#eeff41",
                  "#f50057"]*5
    colors = colors_all[0:len(targets)]
    print(final_df)
    color_dict = {target: color for target, color in zip(targets, colors)}
    count_dict = {target: 1 for target in targets}
    legend_list = [{"text": target, "color": color} for target, color in zip(targets, colors)]
    # for target, color in zip(targets, colors):
    #     final_df.loc[(final_df.device == target), 'device'] = str({'fill-color': color})

    ret_list = [list(item) + [item[2]+"\n"+str(round(item[0], 2))+ " , "+str(round(item[1], 2))] for item in final_df.to_numpy()]
    for item in ret_list:
        item[3]=str(count_dict[item[2]])+"\n"+str(round(item[0], 2))+" , " + str(round(item[1], 2))
        count_dict[item[2]] = count_dict[item[2]] + 1
        item[2] = str({"fill-color": color_dict.get(item[2])}).replace('"', '').replace("'", '')

    ret_list = [tuple(item) for item in ret_list]
    ret_list = [('', '', {'role': 'style'}, {'role': 'tooltip'})] + ret_list
    return ret_list, legend_list , variance_list
