# generated from rosidl_generator_py/resource/_idl.py.em
# with input from nvblox_msgs:msg/MeshBlock.idl
# generated code does not contain a copyright notice


# Import statements for member types

# Member 'triangles'
import array  # noqa: E402, I100

import builtins  # noqa: E402, I100

import rosidl_parser.definition  # noqa: E402, I100


class Metaclass_MeshBlock(type):
    """Metaclass of message 'MeshBlock'."""

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
                'nvblox_msgs.msg.MeshBlock')
            logger.debug(
                'Failed to import needed modules for type support:\n' +
                traceback.format_exc())
        else:
            cls._CREATE_ROS_MESSAGE = module.create_ros_message_msg__msg__mesh_block
            cls._CONVERT_FROM_PY = module.convert_from_py_msg__msg__mesh_block
            cls._CONVERT_TO_PY = module.convert_to_py_msg__msg__mesh_block
            cls._TYPE_SUPPORT = module.type_support_msg__msg__mesh_block
            cls._DESTROY_ROS_MESSAGE = module.destroy_ros_message_msg__msg__mesh_block

            from geometry_msgs.msg import Point32
            if Point32.__class__._TYPE_SUPPORT is None:
                Point32.__class__.__import_type_support__()

            from std_msgs.msg import ColorRGBA
            if ColorRGBA.__class__._TYPE_SUPPORT is None:
                ColorRGBA.__class__.__import_type_support__()

    @classmethod
    def __prepare__(cls, name, bases, **kwargs):
        # list constant names here so that they appear in the help text of
        # the message class under "Data and other attributes defined here:"
        # as well as populate each message instance
        return {
        }


class MeshBlock(metaclass=Metaclass_MeshBlock):
    """Message class 'MeshBlock'."""

    __slots__ = [
        '_vertices',
        '_normals',
        '_colors',
        '_triangles',
    ]

    _fields_and_field_types = {
        'vertices': 'sequence<geometry_msgs/Point32>',
        'normals': 'sequence<geometry_msgs/Point32>',
        'colors': 'sequence<std_msgs/ColorRGBA>',
        'triangles': 'sequence<int32>',
    }

    SLOT_TYPES = (
        rosidl_parser.definition.UnboundedSequence(rosidl_parser.definition.NamespacedType(['geometry_msgs', 'msg'], 'Point32')),  # noqa: E501
        rosidl_parser.definition.UnboundedSequence(rosidl_parser.definition.NamespacedType(['geometry_msgs', 'msg'], 'Point32')),  # noqa: E501
        rosidl_parser.definition.UnboundedSequence(rosidl_parser.definition.NamespacedType(['std_msgs', 'msg'], 'ColorRGBA')),  # noqa: E501
        rosidl_parser.definition.UnboundedSequence(rosidl_parser.definition.BasicType('int32')),  # noqa: E501
    )

    def __init__(self, **kwargs):
        assert all('_' + key in self.__slots__ for key in kwargs.keys()), \
            'Invalid arguments passed to constructor: %s' % \
            ', '.join(sorted(k for k in kwargs.keys() if '_' + k not in self.__slots__))
        self.vertices = kwargs.get('vertices', [])
        self.normals = kwargs.get('normals', [])
        self.colors = kwargs.get('colors', [])
        self.triangles = array.array('i', kwargs.get('triangles', []))

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
        if self.vertices != other.vertices:
            return False
        if self.normals != other.normals:
            return False
        if self.colors != other.colors:
            return False
        if self.triangles != other.triangles:
            return False
        return True

    @classmethod
    def get_fields_and_field_types(cls):
        from copy import copy
        return copy(cls._fields_and_field_types)

    @builtins.property
    def vertices(self):
        """Message field 'vertices'."""
        return self._vertices

    @vertices.setter
    def vertices(self, value):
        if __debug__:
            from geometry_msgs.msg import Point32
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
                 all(isinstance(v, Point32) for v in value) and
                 True), \
                "The 'vertices' field must be a set or sequence and each value of type 'Point32'"
        self._vertices = value

    @builtins.property
    def normals(self):
        """Message field 'normals'."""
        return self._normals

    @normals.setter
    def normals(self, value):
        if __debug__:
            from geometry_msgs.msg import Point32
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
                 all(isinstance(v, Point32) for v in value) and
                 True), \
                "The 'normals' field must be a set or sequence and each value of type 'Point32'"
        self._normals = value

    @builtins.property
    def colors(self):
        """Message field 'colors'."""
        return self._colors

    @colors.setter
    def colors(self, value):
        if __debug__:
            from std_msgs.msg import ColorRGBA
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
                 all(isinstance(v, ColorRGBA) for v in value) and
                 True), \
                "The 'colors' field must be a set or sequence and each value of type 'ColorRGBA'"
        self._colors = value

    @builtins.property
    def triangles(self):
        """Message field 'triangles'."""
        return self._triangles

    @triangles.setter
    def triangles(self, value):
        if isinstance(value, array.array):
            assert value.typecode == 'i', \
                "The 'triangles' array.array() must have the type code of 'i'"
            self._triangles = value
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
                 all(val >= -2147483648 and val < 2147483648 for val in value)), \
                "The 'triangles' field must be a set or sequence and each value of type 'int' and each integer in [-2147483648, 2147483647]"
        self._triangles = array.array('i', value)
