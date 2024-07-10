# generated from rosidl_generator_py/resource/_idl.py.em
# with input from unitree_api:msg/Request.idl
# generated code does not contain a copyright notice


# Import statements for member types

# Member 'binary'
import array  # noqa: E402, I100

import builtins  # noqa: E402, I100

import rosidl_parser.definition  # noqa: E402, I100


class Metaclass_Request(type):
    """Metaclass of message 'Request'."""

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
            module = import_type_support('unitree_api')
        except ImportError:
            import logging
            import traceback
            logger = logging.getLogger(
                'unitree_api.msg.Request')
            logger.debug(
                'Failed to import needed modules for type support:\n' +
                traceback.format_exc())
        else:
            cls._CREATE_ROS_MESSAGE = module.create_ros_message_msg__msg__request
            cls._CONVERT_FROM_PY = module.convert_from_py_msg__msg__request
            cls._CONVERT_TO_PY = module.convert_to_py_msg__msg__request
            cls._TYPE_SUPPORT = module.type_support_msg__msg__request
            cls._DESTROY_ROS_MESSAGE = module.destroy_ros_message_msg__msg__request

            from unitree_api.msg import RequestHeader
            if RequestHeader.__class__._TYPE_SUPPORT is None:
                RequestHeader.__class__.__import_type_support__()

    @classmethod
    def __prepare__(cls, name, bases, **kwargs):
        # list constant names here so that they appear in the help text of
        # the message class under "Data and other attributes defined here:"
        # as well as populate each message instance
        return {
        }


class Request(metaclass=Metaclass_Request):
    """Message class 'Request'."""

    __slots__ = [
        '_header',
        '_parameter',
        '_binary',
    ]

    _fields_and_field_types = {
        'header': 'unitree_api/RequestHeader',
        'parameter': 'string',
        'binary': 'sequence<uint8>',
    }

    SLOT_TYPES = (
        rosidl_parser.definition.NamespacedType(['unitree_api', 'msg'], 'RequestHeader'),  # noqa: E501
        rosidl_parser.definition.UnboundedString(),  # noqa: E501
        rosidl_parser.definition.UnboundedSequence(rosidl_parser.definition.BasicType('uint8')),  # noqa: E501
    )

    def __init__(self, **kwargs):
        assert all('_' + key in self.__slots__ for key in kwargs.keys()), \
            'Invalid arguments passed to constructor: %s' % \
            ', '.join(sorted(k for k in kwargs.keys() if '_' + k not in self.__slots__))
        from unitree_api.msg import RequestHeader
        self.header = kwargs.get('header', RequestHeader())
        self.parameter = kwargs.get('parameter', str())
        self.binary = array.array('B', kwargs.get('binary', []))

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
        if self.header != other.header:
            return False
        if self.parameter != other.parameter:
            return False
        if self.binary != other.binary:
            return False
        return True

    @classmethod
    def get_fields_and_field_types(cls):
        from copy import copy
        return copy(cls._fields_and_field_types)

    @builtins.property
    def header(self):
        """Message field 'header'."""
        return self._header

    @header.setter
    def header(self, value):
        if __debug__:
            from unitree_api.msg import RequestHeader
            assert \
                isinstance(value, RequestHeader), \
                "The 'header' field must be a sub message of type 'RequestHeader'"
        self._header = value

    @builtins.property
    def parameter(self):
        """Message field 'parameter'."""
        return self._parameter

    @parameter.setter
    def parameter(self, value):
        if __debug__:
            assert \
                isinstance(value, str), \
                "The 'parameter' field must be of type 'str'"
        self._parameter = value

    @builtins.property
    def binary(self):
        """Message field 'binary'."""
        return self._binary

    @binary.setter
    def binary(self, value):
        if isinstance(value, array.array):
            assert value.typecode == 'B', \
                "The 'binary' array.array() must have the type code of 'B'"
            self._binary = value
            return
        if __debug__:
            from collections.abc import Sequence
            from collections.abc import Set
            from collections import UserList
            from collections import UserString
            assert \
                ((isinstance(value, Sequence) or
                  isinstance(value, Set) or
                  isinstance(value, UserList)) and
                 not isinstance(value, str) and
                 not isinstance(value, UserString) and
                 all(isinstance(v, int) for v in value) and
                 all(val >= 0 and val < 256 for val in value)), \
                "The 'binary' field must be a set or sequence and each value of type 'int' and each unsigned integer in [0, 255]"
        self._binary = array.array('B', value)
