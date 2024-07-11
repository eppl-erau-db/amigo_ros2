# generated from rosidl_generator_py/resource/_idl.py.em
# with input from nvblox_msgs:srv/EsdfAndGradients.idl
# generated code does not contain a copyright notice


# Import statements for member types

import builtins  # noqa: E402, I100

import rosidl_parser.definition  # noqa: E402, I100


class Metaclass_EsdfAndGradients_Request(type):
    """Metaclass of message 'EsdfAndGradients_Request'."""

    _CREATE_ROS_MESSAGE = None
    _CONVERT_FROM_PY = None
    _CONVERT_TO_PY = None
    _DESTROY_ROS_MESSAGE = None
    _TYPE_SUPPORT = None

    __constants = {
    }

    @classmethod
    def __import_type_support__(cls):
        try:
            from rosidl_generator_py import import_type_support
            module = import_type_support('nvblox_msgs')
        except ImportError:
            import logging
            import traceback
            logger = logging.getLogger(
                'nvblox_msgs.srv.EsdfAndGradients_Request')
            logger.debug(
                'Failed to import needed modules for type support:\n' +
                traceback.format_exc())
        else:
            cls._CREATE_ROS_MESSAGE = module.create_ros_message_msg__srv__esdf_and_gradients__request
            cls._CONVERT_FROM_PY = module.convert_from_py_msg__srv__esdf_and_gradients__request
            cls._CONVERT_TO_PY = module.convert_to_py_msg__srv__esdf_and_gradients__request
            cls._TYPE_SUPPORT = module.type_support_msg__srv__esdf_and_gradients__request
            cls._DESTROY_ROS_MESSAGE = module.destroy_ros_message_msg__srv__esdf_and_gradients__request

            from geometry_msgs.msg import Point
            if Point.__class__._TYPE_SUPPORT is None:
                Point.__class__.__import_type_support__()

            from geometry_msgs.msg import Vector3
            if Vector3.__class__._TYPE_SUPPORT is None:
                Vector3.__class__.__import_type_support__()

    @classmethod
    def __prepare__(cls, name, bases, **kwargs):
        # list constant names here so that they appear in the help text of
        # the message class under "Data and other attributes defined here:"
        # as well as populate each message instance
        return {
        }


class EsdfAndGradients_Request(metaclass=Metaclass_EsdfAndGradients_Request):
    """Message class 'EsdfAndGradients_Request'."""

    __slots__ = [
        '_aabb_min_m',
        '_aabb_size_m',
    ]

    _fields_and_field_types = {
        'aabb_min_m': 'geometry_msgs/Point',
        'aabb_size_m': 'geometry_msgs/Vector3',
    }

    SLOT_TYPES = (
        rosidl_parser.definition.NamespacedType(['geometry_msgs', 'msg'], 'Point'),  # noqa: E501
        rosidl_parser.definition.NamespacedType(['geometry_msgs', 'msg'], 'Vector3'),  # noqa: E501
    )

    def __init__(self, **kwargs):
        assert all('_' + key in self.__slots__ for key in kwargs.keys()), \
            'Invalid arguments passed to constructor: %s' % \
            ', '.join(sorted(k for k in kwargs.keys() if '_' + k not in self.__slots__))
        from geometry_msgs.msg import Point
        self.aabb_min_m = kwargs.get('aabb_min_m', Point())
        from geometry_msgs.msg import Vector3
        self.aabb_size_m = kwargs.get('aabb_size_m', Vector3())

    def __repr__(self):
        typename = self.__class__.__module__.split('.')
        typename.pop()
        typename.append(self.__class__.__name__)
        args = []
        for s, t in zip(self.__slots__, self.SLOT_TYPES):
            field = getattr(self, s)
            fieldstr = repr(field)
            # We use Python array type for fields that can be directly stored
            # in them, and "normal" sequences for everything else.  If it is
            # a type that we store in an array, strip off the 'array' portion.
            if (
                isinstance(t, rosidl_parser.definition.AbstractSequence) and
                isinstance(t.value_type, rosidl_parser.definition.BasicType) and
                t.value_type.typename in ['float', 'double', 'int8', 'uint8', 'int16', 'uint16', 'int32', 'uint32', 'int64', 'uint64']
            ):
                if len(field) == 0:
                    fieldstr = '[]'
                else:
                    assert fieldstr.startswith('array(')
                    prefix = "array('X', "
                    suffix = ')'
                    fieldstr = fieldstr[len(prefix):-len(suffix)]
            args.append(s[1:] + '=' + fieldstr)
        return '%s(%s)' % ('.'.join(typename), ', '.join(args))

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        if self.aabb_min_m != other.aabb_min_m:
            return False
        if self.aabb_size_m != other.aabb_size_m:
            return False
        return True

    @classmethod
    def get_fields_and_field_types(cls):
        from copy import copy
        return copy(cls._fields_and_field_types)

    @builtins.property
    def aabb_min_m(self):
        """Message field 'aabb_min_m'."""
        return self._aabb_min_m

    @aabb_min_m.setter
    def aabb_min_m(self, value):
        if __debug__:
            from geometry_msgs.msg import Point
            assert \
                isinstance(value, Point), \
                "The 'aabb_min_m' field must be a sub message of type 'Point'"
        self._aabb_min_m = value

    @builtins.property
    def aabb_size_m(self):
        """Message field 'aabb_size_m'."""
        return self._aabb_size_m

    @aabb_size_m.setter
    def aabb_size_m(self, value):
        if __debug__:
            from geometry_msgs.msg import Vector3
            assert \
                isinstance(value, Vector3), \
                "The 'aabb_size_m' field must be a sub message of type 'Vector3'"
        self._aabb_size_m = value


# Import statements for member types

# already imported above
# import builtins

# already imported above
# import rosidl_parser.definition


class Metaclass_EsdfAndGradients_Response(type):
    """Metaclass of message 'EsdfAndGradients_Response'."""

    _CREATE_ROS_MESSAGE = None
    _CONVERT_FROM_PY = None
    _CONVERT_TO_PY = None
    _DESTROY_ROS_MESSAGE = None
    _TYPE_SUPPORT = None

    __constants = {
    }

    @classmethod
    def __import_type_support__(cls):
        try:
            from rosidl_generator_py import import_type_support
            module = import_type_support('nvblox_msgs')
        except ImportError:
            import logging
            import traceback
            logger = logging.getLogger(
                'nvblox_msgs.srv.EsdfAndGradients_Response')
            logger.debug(
                'Failed to import needed modules for type support:\n' +
                traceback.format_exc())
        else:
            cls._CREATE_ROS_MESSAGE = module.create_ros_message_msg__srv__esdf_and_gradients__response
            cls._CONVERT_FROM_PY = module.convert_from_py_msg__srv__esdf_and_gradients__response
            cls._CONVERT_TO_PY = module.convert_to_py_msg__srv__esdf_and_gradients__response
            cls._TYPE_SUPPORT = module.type_support_msg__srv__esdf_and_gradients__response
            cls._DESTROY_ROS_MESSAGE = module.destroy_ros_message_msg__srv__esdf_and_gradients__response

            from std_msgs.msg import Float32
            if Float32.__class__._TYPE_SUPPORT is None:
                Float32.__class__.__import_type_support__()

            from std_msgs.msg import Float32MultiArray
            if Float32MultiArray.__class__._TYPE_SUPPORT is None:
                Float32MultiArray.__class__.__import_type_support__()

    @classmethod
    def __prepare__(cls, name, bases, **kwargs):
        # list constant names here so that they appear in the help text of
        # the message class under "Data and other attributes defined here:"
        # as well as populate each message instance
        return {
        }


class EsdfAndGradients_Response(metaclass=Metaclass_EsdfAndGradients_Response):
    """Message class 'EsdfAndGradients_Response'."""

    __slots__ = [
        '_voxel_size',
        '_esdf_and_gradients',
    ]

    _fields_and_field_types = {
        'voxel_size': 'std_msgs/Float32',
        'esdf_and_gradients': 'std_msgs/Float32MultiArray',
    }

    SLOT_TYPES = (
        rosidl_parser.definition.NamespacedType(['std_msgs', 'msg'], 'Float32'),  # noqa: E501
        rosidl_parser.definition.NamespacedType(['std_msgs', 'msg'], 'Float32MultiArray'),  # noqa: E501
    )

    def __init__(self, **kwargs):
        assert all('_' + key in self.__slots__ for key in kwargs.keys()), \
            'Invalid arguments passed to constructor: %s' % \
            ', '.join(sorted(k for k in kwargs.keys() if '_' + k not in self.__slots__))
        from std_msgs.msg import Float32
        self.voxel_size = kwargs.get('voxel_size', Float32())
        from std_msgs.msg import Float32MultiArray
        self.esdf_and_gradients = kwargs.get('esdf_and_gradients', Float32MultiArray())

    def __repr__(self):
        typename = self.__class__.__module__.split('.')
        typename.pop()
        typename.append(self.__class__.__name__)
        args = []
        for s, t in zip(self.__slots__, self.SLOT_TYPES):
            field = getattr(self, s)
            fieldstr = repr(field)
            # We use Python array type for fields that can be directly stored
            # in them, and "normal" sequences for everything else.  If it is
            # a type that we store in an array, strip off the 'array' portion.
            if (
                isinstance(t, rosidl_parser.definition.AbstractSequence) and
                isinstance(t.value_type, rosidl_parser.definition.BasicType) and
                t.value_type.typename in ['float', 'double', 'int8', 'uint8', 'int16', 'uint16', 'int32', 'uint32', 'int64', 'uint64']
            ):
                if len(field) == 0:
                    fieldstr = '[]'
                else:
                    assert fieldstr.startswith('array(')
                    prefix = "array('X', "
                    suffix = ')'
                    fieldstr = fieldstr[len(prefix):-len(suffix)]
            args.append(s[1:] + '=' + fieldstr)
        return '%s(%s)' % ('.'.join(typename), ', '.join(args))

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        if self.voxel_size != other.voxel_size:
            return False
        if self.esdf_and_gradients != other.esdf_and_gradients:
            return False
        return True

    @classmethod
    def get_fields_and_field_types(cls):
        from copy import copy
        return copy(cls._fields_and_field_types)

    @builtins.property
    def voxel_size(self):
        """Message field 'voxel_size'."""
        return self._voxel_size

    @voxel_size.setter
    def voxel_size(self, value):
        if __debug__:
            from std_msgs.msg import Float32
            assert \
                isinstance(value, Float32), \
                "The 'voxel_size' field must be a sub message of type 'Float32'"
        self._voxel_size = value

    @builtins.property
    def esdf_and_gradients(self):
        """Message field 'esdf_and_gradients'."""
        return self._esdf_and_gradients

    @esdf_and_gradients.setter
    def esdf_and_gradients(self, value):
        if __debug__:
            from std_msgs.msg import Float32MultiArray
            assert \
                isinstance(value, Float32MultiArray), \
                "The 'esdf_and_gradients' field must be a sub message of type 'Float32MultiArray'"
        self._esdf_and_gradients = value


class Metaclass_EsdfAndGradients(type):
    """Metaclass of service 'EsdfAndGradients'."""

    _TYPE_SUPPORT = None

    @classmethod
    def __import_type_support__(cls):
        try:
            from rosidl_generator_py import import_type_support
            module = import_type_support('nvblox_msgs')
        except ImportError:
            import logging
            import traceback
            logger = logging.getLogger(
                'nvblox_msgs.srv.EsdfAndGradients')
            logger.debug(
                'Failed to import needed modules for type support:\n' +
                traceback.format_exc())
        else:
            cls._TYPE_SUPPORT = module.type_support_srv__srv__esdf_and_gradients

            from nvblox_msgs.srv import _esdf_and_gradients
            if _esdf_and_gradients.Metaclass_EsdfAndGradients_Request._TYPE_SUPPORT is None:
                _esdf_and_gradients.Metaclass_EsdfAndGradients_Request.__import_type_support__()
            if _esdf_and_gradients.Metaclass_EsdfAndGradients_Response._TYPE_SUPPORT is None:
                _esdf_and_gradients.Metaclass_EsdfAndGradients_Response.__import_type_support__()


class EsdfAndGradients(metaclass=Metaclass_EsdfAndGradients):
    from nvblox_msgs.srv._esdf_and_gradients import EsdfAndGradients_Request as Request
    from nvblox_msgs.srv._esdf_and_gradients import EsdfAndGradients_Response as Response

    def __init__(self):
        raise NotImplementedError('Service classes can not be instantiated')
