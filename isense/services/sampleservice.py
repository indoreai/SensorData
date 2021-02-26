"""
Created on Feb 06th, 2020

@author: rajesh
"""
from isense import db
from isense.pca.models import Samples, Samples_meta, Samples_userdevices
from isense.utils import model_to_python, model_list_to_python
from sqlalchemy import and_


def sample_get_data_service(**kwargs):
    """  call select all data in samples table
        **kwargs is multiple filtering column
        """
    sample_data = Samples.query.filter_by(**kwargs).all()
    # remove  unused  object call model_list_to_python functions after return
    return model_list_to_python(sample_data)


def sample_get_data_sensor_service(sensor, sample_start_id, sample_end_id):
    """  call select all data in samples table using limit start and end
            sensor list of multiple filtering column
        """
    search_columns = [getattr(Samples, i) for i in sensor]
    return db.session.query(Samples).with_entities(*search_columns).filter(
        and_(Samples.id >= sample_start_id, Samples.id <= sample_end_id)).all()


def sample_get_data_first_service(**kwargs):
    """  call select matched  data in samples table
        **kwargs is multiple filtering column single matched data
        """
    sample_data = Samples.query.filter_by(**kwargs).first()
    # remove single object call model_list_to_python functions after return
    return model_to_python(sample_data)


def sample_mata_get_data_service(**kwargs):
    """  call select all data in samples meta table
        **kwargs is multiple filtering column
        """
    sample_meta_data = Samples_meta.query.filter_by(**kwargs).all()
    # remove  unused  object call model_list_to_python functions after return
    return model_list_to_python(sample_meta_data)


def sample_mata_get_data_first_service(**kwargs):
    """  call select matched  data in samples meta  table
        **kwargs is multiple filtering column return single matched data
        """
    sample_meta_data = Samples_meta.query.filter_by(**kwargs).first()
    # remove  unused  object call model_list_to_python functions after return
    return model_to_python(sample_meta_data)


def samples_userdevices_get_data_service(**kwargs):
    """  call select all data in samples userservice table
        **kwargs is multiple filtering column
        """
    samples_user_devices = Samples_userdevices.query.filter_by(**kwargs).all()
    # remove  unused  object call model_list_to_python functions after return
    return model_list_to_python(samples_user_devices)


def Samples_userdevices_get_data_first_service(**kwargs):
    """  call select matched  data in samples userservice  table
        **kwargs is multiple filtering column return single matched data
        """
    samples_user_devices = Samples_userdevices.query.filter_by(**kwargs).first()
    # remove  unused  object call model_list_to_python functions after return
    return model_to_python(samples_user_devices)


def common_get_data_service(sensor_list, user_id, device_name, sample_set_id):
    """  common service call internally sample meta data table and samples table
            sensor_list is list of sensor,user id(int), device_name(str), sample_set_id(str)
        """
    sample_meta_data = sample_mata_get_data_first_service(user_id=user_id, device_name=device_name,
                                                          sample_set_id=sample_set_id)
    sample_start_id = sample_meta_data.get('start_sample_id')
    sample_end_id = sample_meta_data.get('end_sample_id')
    return sample_get_data_sensor_service(sensor_list, sample_start_id, sample_end_id)
