# generated from rosidl_generator_py/resource/_idl.py.em
# with input from isaac_ros_tensor_list_interfaces:msg/Tensor.idl
# generated code does not contain a copyright notice


# Import statements for member types

# Member 'strides'
# Member 'data'
import array  # noqa: E402, I100

import builtins  # noqa: E402, I100

import rosidl_parser.definition  # noqa: E402, I100


class Metaclass_Tensor(type):
    """Metaclass of message 'Tensor'."""

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
            module = import_type_support('isaac_ros_tensor_list_interfaces')
        except ImportError:
            import logging
            import traceback
            logger = logging.getLogger(
                'isaac_ros_tensor_list_interfaces.msg.Tensor')
            logger.debug(
                'Failed to import needed modules for type support:\n' +
                traceback.format_exc())
        else:
            cls._CREATE_ROS_MESSAGE = module.create_ros_message_msg__msg__tensor
            cls._CONVERT_FROM_PY = module.convert_from_py_msg__msg__tensor
            cls._CONVERT_TO_PY = module.convert_to_py_msg__msg__tensor
            cls._TYPE_SUPPORT = module.type_support_msg__msg__tensor
            cls._DESTROY_ROS_MESSAGE = module.destroy_ros_message_msg__msg__tensor

            from isaac_ros_tensor_list_interfaces.msg import TensorShape
            if TensorShape.__class__._TYPE_SUPPORT is None:
                TensorShape.__class__.__import_type_support__()

    @classmethod
    def __prepare__(cls, name, bases, **kwargs):
        # list constant names here so that they appear in the help text of
        # the message class under "Data and other attributes defined here:"
        # as well as populate each message instance
        return {
        }


class Tensor(metaclass=Metaclass_Tensor):
    """Message class 'Tensor'."""

    __slots__ = [
        '_name',
        '_shape',
        '_data_type',
        '_strides',
        '_data',
    ]

    _fields_and_field_types = {
        'name': 'string',
        'shape': 'isaac_ros_tensor_list_interfaces/TensorShape',
        'data_type': 'int32',
        'strides': 'sequence<uint64>',
        'data': 'sequence<uint8>',
    }

    SLOT_TYPES = (
        rosidl_parser.definition.UnboundedString(),  # noqa: E501
        rosidl_parser.definition.NamespacedType(['isaac_ros_tensor_list_interfaces', 'msg'], 'TensorShape'),  # noqa: E501
        rosidl_parser.definition.BasicType('int32'),  # noqa: E501
        rosidl_parser.definition.UnboundedSequence(rosidl_parser.definition.BasicType('uint64')),  # noqa: E501
        rosidl_parser.definition.UnboundedSequence(rosidl_parser.definition.BasicType('uint8')),  # noqa: E501
    )

    def __init__(self, **kwargs):
        assert all('_' + key in self.__slots__ for key in kwargs.keys()), \
            'Invalid arguments passed to constructor: %s' % \
            ', '.join(sorted(k for k in kwargs.keys() if '_' + k not in self.__slots__))
        self.name = kwargs.get('name', str())
        from isaac_ros_tensor_list_interfaces.msg import TensorShape
        self.shape = kwargs.get('shape', TensorShape())
        self.data_type = kwargs.get('data_type', int())
        self.strides = array.array('Q', kwargs.get('strides', []))
        self.data = array.array('B', kwargs.get('data', []))

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
        if self.name != other.name:
            return False
        if self.shape != other.shape:
            return False
        if self.data_type != other.data_type:
            return False
        if self.strides != other.strides:
            return False
        if self.data != other.data:
            return False
        return True

    @classmethod
    def get_fields_and_field_types(cls):
        from copy import copy
        return copy(cls._fields_and_field_types)

    @builtins.property
    def name(self):
        """Message field 'name'."""
        return self._name

    @name.setter
    def name(self, value):
        if __debug__:
            assert \
                isinstance(value, str), \
                "The 'name' field must be of type 'str'"
        self._name = value

    @builtins.property
    def shape(self):
        """Message field 'shape'."""
        return self._shape

    @shape.setter
    def shape(self, value):
        if __debug__:
            from isaac_ros_tensor_list_interfaces.msg import TensorShape
            assert \
                isinstance(value, TensorShape), \
                "The 'shape' field must be a sub message of type 'TensorShape'"
        self._shape = value

    @builtins.property
    def data_type(self):
        """Message field 'data_type'."""
        return self._data_type

    @data_type.setter
    def data_type(self, value):
        if __debug__:
            assert \
                isinstance(value, int), \
                "The 'data_type' field must be of type 'int'"
            assert value >= -2147483648 and value < 2147483648, \
                "The 'data_type' field must be an integer in [-2147483648, 2147483647]"
        self._data_type = value

    @builtins.property
    def strides(self):
        """Message field 'strides'."""
        return self._strides

    @strides.setter
    def strides(self, value):
        if isinstance(value, array.array):
            assert value.typecode == 'Q', \
                "The 'strides' array.array() must have the type code of 'Q'"
            self._strides = value
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
                 all(val >= 0 and val < 18446744073709551616 for val in value)), \
                "The 'strides' field must be a set or sequence and each value of type 'int' and each unsigned integer in [0, 18446744073709551615]"
        self._strides = array.array('Q', value)

    @builtins.property
    def data(self):
        """Message field 'data'."""
        return self._data

    @data.setter
    def data(self, value):
        if isinstance(value, array.array):
            assert value.typecode == 'B', \
                "The 'data' array.array() must have the type code of 'B'"
            self._data = value
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
                "The 'data' field must be a set or sequence and each value of type 'int' and each unsigned integer in [0, 255]"
        self._data = array.array('B', value)
