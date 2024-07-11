# generated from rosidl_generator_py/resource/_idl.py.em
# with input from isaac_ros_nova_interfaces:msg/CorrelatedTimestamp.idl
# generated code does not contain a copyright notice


# Import statements for member types

import builtins  # noqa: E402, I100

import rosidl_parser.definition  # noqa: E402, I100


class Metaclass_CorrelatedTimestamp(type):
    """Metaclass of message 'CorrelatedTimestamp'."""

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
            module = import_type_support('isaac_ros_nova_interfaces')
        except ImportError:
            import logging
            import traceback
            logger = logging.getLogger(
                'isaac_ros_nova_interfaces.msg.CorrelatedTimestamp')
            logger.debug(
                'Failed to import needed modules for type support:\n' +
                traceback.format_exc())
        else:
            cls._CREATE_ROS_MESSAGE = module.create_ros_message_msg__msg__correlated_timestamp
            cls._CONVERT_FROM_PY = module.convert_from_py_msg__msg__correlated_timestamp
            cls._CONVERT_TO_PY = module.convert_to_py_msg__msg__correlated_timestamp
            cls._TYPE_SUPPORT = module.type_support_msg__msg__correlated_timestamp
            cls._DESTROY_ROS_MESSAGE = module.destroy_ros_message_msg__msg__correlated_timestamp

            from std_msgs.msg import Header
            if Header.__class__._TYPE_SUPPORT is None:
                Header.__class__.__import_type_support__()

    @classmethod
    def __prepare__(cls, name, bases, **kwargs):
        # list constant names here so that they appear in the help text of
        # the message class under "Data and other attributes defined here:"
        # as well as populate each message instance
        return {
        }


class CorrelatedTimestamp(metaclass=Metaclass_CorrelatedTimestamp):
    """Message class 'CorrelatedTimestamp'."""

    __slots__ = [
        '_header',
        '_phc_val',
        '_tsc_val',
        '_phc2_val',
        '_sys_val',
        '_phc_latency',
    ]

    _fields_and_field_types = {
        'header': 'std_msgs/Header',
        'phc_val': 'uint64',
        'tsc_val': 'uint64',
        'phc2_val': 'uint64',
        'sys_val': 'uint64',
        'phc_latency': 'uint64',
    }

    SLOT_TYPES = (
        rosidl_parser.definition.NamespacedType(['std_msgs', 'msg'], 'Header'),  # noqa: E501
        rosidl_parser.definition.BasicType('uint64'),  # noqa: E501
        rosidl_parser.definition.BasicType('uint64'),  # noqa: E501
        rosidl_parser.definition.BasicType('uint64'),  # noqa: E501
        rosidl_parser.definition.BasicType('uint64'),  # noqa: E501
        rosidl_parser.definition.BasicType('uint64'),  # noqa: E501
    )

    def __init__(self, **kwargs):
        assert all('_' + key in self.__slots__ for key in kwargs.keys()), \
            'Invalid arguments passed to constructor: %s' % \
            ', '.join(sorted(k for k in kwargs.keys() if '_' + k not in self.__slots__))
        from std_msgs.msg import Header
        self.header = kwargs.get('header', Header())
        self.phc_val = kwargs.get('phc_val', int())
        self.tsc_val = kwargs.get('tsc_val', int())
        self.phc2_val = kwargs.get('phc2_val', int())
        self.sys_val = kwargs.get('sys_val', int())
        self.phc_latency = kwargs.get('phc_latency', int())

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
        if self.phc_val != other.phc_val:
            return False
        if self.tsc_val != other.tsc_val:
            return False
        if self.phc2_val != other.phc2_val:
            return False
        if self.sys_val != other.sys_val:
            return False
        if self.phc_latency != other.phc_latency:
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
            from std_msgs.msg import Header
            assert \
                isinstance(value, Header), \
                "The 'header' field must be a sub message of type 'Header'"
        self._header = value

    @builtins.property
    def phc_val(self):
        """Message field 'phc_val'."""
        return self._phc_val

    @phc_val.setter
    def phc_val(self, value):
        if __debug__:
            assert \
                isinstance(value, int), \
                "The 'phc_val' field must be of type 'int'"
            assert value >= 0 and value < 18446744073709551616, \
                "The 'phc_val' field must be an unsigned integer in [0, 18446744073709551615]"
        self._phc_val = value

    @builtins.property
    def tsc_val(self):
        """Message field 'tsc_val'."""
        return self._tsc_val

    @tsc_val.setter
    def tsc_val(self, value):
        if __debug__:
            assert \
                isinstance(value, int), \
                "The 'tsc_val' field must be of type 'int'"
            assert value >= 0 and value < 18446744073709551616, \
                "The 'tsc_val' field must be an unsigned integer in [0, 18446744073709551615]"
        self._tsc_val = value

    @builtins.property
    def phc2_val(self):
        """Message field 'phc2_val'."""
        return self._phc2_val

    @phc2_val.setter
    def phc2_val(self, value):
        if __debug__:
            assert \
                isinstance(value, int), \
                "The 'phc2_val' field must be of type 'int'"
            assert value >= 0 and value < 18446744073709551616, \
                "The 'phc2_val' field must be an unsigned integer in [0, 18446744073709551615]"
        self._phc2_val = value

    @builtins.property
    def sys_val(self):
        """Message field 'sys_val'."""
        return self._sys_val

    @sys_val.setter
    def sys_val(self, value):
        if __debug__:
            assert \
                isinstance(value, int), \
                "The 'sys_val' field must be of type 'int'"
            assert value >= 0 and value < 18446744073709551616, \
                "The 'sys_val' field must be an unsigned integer in [0, 18446744073709551615]"
        self._sys_val = value

    @builtins.property
    def phc_latency(self):
        """Message field 'phc_latency'."""
        return self._phc_latency

    @phc_latency.setter
    def phc_latency(self, value):
        if __debug__:
            assert \
                isinstance(value, int), \
                "The 'phc_latency' field must be of type 'int'"
            assert value >= 0 and value < 18446744073709551616, \
                "The 'phc_latency' field must be an unsigned integer in [0, 18446744073709551615]"
        self._phc_latency = value
