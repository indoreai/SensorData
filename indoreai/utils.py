
def model_to_python(model_object):
    if model_object:
        model_object=model_object.__dict__
        model_object.pop('_sa_instance_state', None)
    return model_object


def model_list_to_python(model_list):
   retlist=[model_to_python(model_object) for model_object in model_list ]
   return retlist
