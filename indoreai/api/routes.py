"""
Created on Feb 06th, 2020

@author: rajesh
"""
import csv
import os
from datetime import datetime
from flask import (render_template, url_for, flash,
                   redirect, request, Response, jsonify, abort, Blueprint, current_app)
from indoreai.services.sampleservice import sample_mata_get_data_service, common_get_data_service
from indoreai.services.pcaservice import get_pca_feature_data_local
import numpy as np


api = Blueprint('api', __name__)


@api.route("/api/get_meta_sample_data/", methods=['GET', 'POST'])
def get_meta_sample_data():
    """ Api call get simple set id  call service
     sample_mata_get_data_service
    """
    user_id = request.get_json().get('user_id')
    device_name = request.get_json().get("device_name")
    # db for sample_meta database
    sample_data = sample_mata_get_data_service(user_id=user_id, device_name=device_name)
    return jsonify({"success": True, "data": sample_data})


@api.route("/api/get_sample_data/", methods=['GET', 'POST'])
def get_sample_data():
    """ Api call get graph  data from call services
         common_get_data_service
        """
    # print("request", request.args)
    user_id = request.get_json().get('user_id')
    device_name = request.get_json().get("device_name")
    sensor = request.get_json().get("sensor")
    sample_set_id = request.get_json().get("sample_set_id")
    # db for sample databse
    sensor1 = 'Sample'
    sensor_list = [sensor, sensor1]
    sample_data = common_get_data_service(sensor_list, user_id=user_id, device_name=device_name,
                                          sample_set_id=sample_set_id)
    return jsonify({"success": True, "data": sample_data})


@api.route("/api/get_sample_data_pca_graph/", methods=['GET', 'POST'])
def get_sample_data_pca():
    """ Api call get graph  data from call services
         common_get_data_service
        """
    filename = 'train_'+datetime.now().strftime("%Y%m%d%H%M%S")+'.csv'
    # print("request", request.args)
    user_id = request.get_json().get('user_id')
    device_name = request.get_json().get("device_name")
    sensor = request.get_json().get("sensor")
    sample_set_id = request.get_json().get("sample_set_id")
    sensor_list = [sensor]
    for sample_set in sample_set_id:
        sample_data = common_get_data_service(sensor_list, user_id=user_id, device_name=device_name,
                                              sample_set_id=sample_set)
        sample_data = [s_data[0] for s_data in sample_data[:1200]]
        np_list = np.array(sample_data)
        sample_data = np.reshape(np_list, (10, 120))
        # print(sample_data)
        print("shape ", sample_data.size)
        with open(filename, 'a+') as csvfile:
            # creating a csv writer object
            csvwriter = csv.writer(csvfile)
            # writing the data rows
            for s_data in sample_data.tolist():
                # print("s_data", s_data)
                csvwriter.writerow([sample_set] + s_data)
    # if int(current_app.config.get('USE_SAGEMAKER')) == 1:
    #     ret_data_list, legend_list, variance_list = get_pca_feature_data(filename)
    # else:
    ret_data_list , legend_list , variance_list = get_pca_feature_data_local(filename)
    print('ret_data_list ', ret_data_list, type(ret_data_list))
    print("legend_list", legend_list)
    try:
        os.remove(filename)
    except:
        pass
    return jsonify({"success": True, "data": ret_data_list, "legend_list": legend_list ,'variance_list' : variance_list})
