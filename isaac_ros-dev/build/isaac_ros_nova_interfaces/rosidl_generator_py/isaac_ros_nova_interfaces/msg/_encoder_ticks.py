# generated from rosidl_generator_py/resource/_idl.py.em
# with input from isaac_ros_nova_interfaces:msg/EncoderTicks.idl
# generated code does not contain a copyright notice


# Import statements for member types

import builtins  # noqa: E402, I100

import rosidl_parser.definition  # noqa: E402, I100


class Metaclass_EncoderTicks(type):
    """Metaclass of message 'EncoderTicks'."""

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
                'isaac_ros_nova_interfaces.msg.EncoderTicks')
            logger.debug(
                'Failed to import needed modules for type support:\n' +
                traceback.format_exc())
        else:
            cls._CREATE_ROS_MESSAGE = module.create_ros_message_msg__msg__encoder_ticks
            cls._CONVERT_FROM_PY = module.convert_from_py_msg__msg__encoder_ticks
            cls._CONVERT_TO_PY = module.convert_to_py_msg__msg__encoder_ticks
            cls._TYPE_SUPPORT = module.type_support_msg__msg__encoder_ticks
            cls._DESTROY_ROS_MESSAGE = module.destroy_ros_message_msg__msg__encoder_ticks

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


class EncoderTicks(metaclass=Metaclass_EncoderTicks):
    """Message class 'EncoderTicks'."""

    __slots__ = [
        '_header',
        '_left_ticks',
        '_right_ticks',
        '_encoder_timestamp',
    ]

    _fields_and_field_types = {
        'header': 'std_msgs/Header',
        'left_ticks': 'uint32',
        'right_ticks': 'uint32',
        'encoder_timestamp': 'uint64',
    }

    SLOT_TYPES = (
        rosidl_parser.definition.NamespacedType(['std_msgs', 'msg'], 'Header'),  # noqa: E501
        rosidl_parser.definition.BasicType('uint32'),  # noqa: E501
        rosidl_parser.definition.BasicType('uint32'),  # noqa: E501
        rosidl_parser.definition.BasicType('uint64'),  # noqa: E501
    )

    def __init__(self, **kwargs):
        assert all('_' + key in self.__slots__ for key in kwargs.keys()), \
            'Invalid arguments passed to constructor: %s' % \
            ', '.join(sorted(k for k in kwargs.keys() if '_' + k not in self.__slots__))
        from std_msgs.msg import Header
        self.header = kwargs.get('header', Header())
        self.left_ticks = kwargs.get('left_ticks', int())
        self.right_ticks = kwargs.get('right_ticks', int())
        self.encoder_timestamp = kwargs.get('encoder_timestamp', int())

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
        if self.left_ticks != other.left_ticks:
            return False
        if self.right_ticks != other.right_ticks:
            return False
        if self.encoder_timestamp != other.encoder_timestamp:
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
    def left_ticks(self):
        """Message field 'left_ticks'."""
        return self._left_ticks

    @left_ticks.setter
    def left_ticks(self, value):
        if __debug__:
            assert \
                isinstance(value, int), \
                "The 'left_ticks' field must be of type 'int'"
            assert value >= 0 and value < 4294967296, \
                "The 'left_ticks' field must be an unsigned integer in [0, 4294967295]"
        self._left_ticks = value

    @builtins.property
    def right_ticks(self):
        """Message field 'right_ticks'."""
        return self._right_ticks

    @right_ticks.setter
    def right_ticks(self, value):
        if __debug__:
            assert \
                isinstance(value, int), \
                "The 'right_ticks' field must be of type 'int'"
            assert value >= 0 and value < 4294967296, \
                "The 'right_ticks' field must be an unsigned integer in [0, 4294967295]"
        self._right_ticks = value

    @builtins.property
    def encoder_timestamp(self):
        """Message field 'encoder_timestamp'."""
        return self._encoder_timestamp

    @encoder_timestamp.setter
    def encoder_timestamp(self, value):
        if __debug__:
            assert \
                isinstance(value, int), \
                "The 'encoder_timestamp' field must be of type 'int'"
            assert value >= 0 and value < 18446744073709551616, \
                "The 'encoder_timestamp' field must be an unsigned integer in [0, 18446744073709551615]"
        self._encoder_timestamp = value
