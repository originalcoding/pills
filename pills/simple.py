'''
Validators that do not require third-party modules except validol.
'''


__all__ = ('closest', 'length', 'dt', 'attrs', 'fails', )


import  datetime 

from utils import validol


def closest(scheme):
    '''Get number closest to obj from scheme.'''
    def _closest(obj):
        try:
            return min(scheme, key=lambda x: abs(x - obj))
        except:
            raise validol.ValidationError(
                'Failed closest validation: %s' % (obj, ))
    return _closest


def length(*schemes):
    '''Validate length. Scheme can be a number or callable.'''
    def _length(obj):
        length = None
        try:
            length = len(obj)
        except:
            raise validol.ValidationError(
                'Failed length validation: %s' % (obj, ))

        ok = False
        
        for scheme in schemes:
            if callable(scheme):
                ok = validol.validate(scheme, length)
            else:
                ok = scheme == length

        if not ok:
            raise validol.ValidationError(
                'Failed length validation: %s' % (obj, ))
        
        return obj
    return _length


def dt(scheme):
    '''Validate datetime.'''
    def _dt(string):
        try:
            return datetime.datetime.strptime(string, scheme)
        except:
            raise validol.ValidationError(
                'Failed dt validation: %s' % (string, ))
    return _dt


def attrs(*args, **kwargs):
    '''Validate attributes.'''
    def _attrs(obj):
        for attr in args:
            if not hasattr(obj, attr):
                raise validol.ValidationError(
                    'Failed attrs validation: %s' % (obj, ))

        for attr, value in kwargs.items():
            if getattr(obj, attr, None) != value:
                raise validol.ValidationError(
                    'Failed attrs validation: %s' % (obj, ))
        
        return obj
    return _attrs


def fails(scheme):
    '''Raise ValidationError if validated successfully.'''
    def _fails(obj):
        try:
            validol.validate(scheme, obj)
        except validol.ValidationError:
            return obj
        raise validol.ValidationError(
            'Failed fails validation: %s' % (obj, ))
    return _fails
