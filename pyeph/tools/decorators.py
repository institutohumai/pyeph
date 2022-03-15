def translate_params(params={}):
    def function_in_question(fn):
        def wrapper(*args, **kwargs):
            for param in params.keys():
                if param in kwargs.keys():
                    kwargs[params[param]] = kwargs.pop(param)
            return fn(*args, **kwargs)
        return wrapper
    return function_in_question

def validate_group_by(fn):
    def wrapper(*args, **kwargs):
        if "group_by" in kwargs.keys():
            if not isinstance(kwargs['group_by'], (list, str)):
                raise TypeError("group_by debe ser una lista o un string")
        return fn(*args, **kwargs)
    return wrapper

def validate_div_by(fn):
    def wrapper(*args, **kwargs):
        options = {'PT': '"PT" (Población Total)', 'PET': '"PET" (Población en Edad de Trabajar)'}
        if "div_by" in kwargs.keys():
            if not (
                isinstance(kwargs['div_by'], str) and
                kwargs['div_by'] in options.keys()
            ):
                raise TypeError("div_by debe ser un string: {}".format(" o ".join(options.values())))
        return fn(*args, **kwargs)
    return wrapper

