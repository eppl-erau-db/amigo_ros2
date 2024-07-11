# generated from rosidl_generator_py/resource/_idl.py.em
# with input from realsense2_camera_msgs:srv/DeviceInfo.idl
# generated code does not contain a copyright notice


# Import statements for member types

import rosidl_parser.definition  # noqa: E402, I100


class Metaclass_DeviceInfo_Request(type):
    """Metaclass of message 'DeviceInfo_Request'."""

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
            module = import_type_support('realsense2_camera_msgs')
        except ImportError:
            import logging
            import traceback
            logger = logging.getLogger(
                'realsense2_camera_msgs.srv.DeviceInfo_Request')
            logger.debug(
                'Failed to import needed modules for type support:\n' +
                traceback.format_exc())
        else:
            cls._CREATE_ROS_MESSAGE = module.create_ros_message_msg__srv__device_info__request
            cls._CONVERT_FROM_PY = module.convert_from_py_msg__srv__device_info__request
            cls._CONVERT_TO_PY = module.convert_to_py_msg__srv__device_info__request
            cls._TYPE_SUPPORT = module.type_support_msg__srv__device_info__request
            cls._DESTROY_ROS_MESSAGE = module.destroy_ros_message_msg__srv__device_info__request

    @classmethod
    def __prepare__(cls, name, bases, **kwargs):
        # list constant names here so that they appear in the help text of
        # the message class under "Data and other attributes defined here:"
        # as well as populate each message instance
        return {
        }


class DeviceInfo_Request(metaclass=Metaclass_DeviceInfo_Request):
    """Message class 'DeviceInfo_Request'."""

    __slots__ = [
    ]

    _fields_and_field_types = {
    }

    SLOT_TYPES = (
    )

    def __init__(self, **kwargs):
        assert all('_' + key in self.__slots__ for key in kwargs.keys()), \
            'Invalid arguments passed to constructor: %s' % \
            ', '.join(sorted(k for k in kwargs.keys() if '_' + k not in self.__slots__))

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
        return True

    @classmethod
    def get_fields_and_field_types(cls):
        from copy import copy
        return copy(cls._fields_and_field_types)


# Import statements for member types

import builtins  # noqa: E402, I100

# already imported above
# import rosidl_parser.definition


class Metaclass_DeviceInfo_Response(type):
    """Metaclass of message 'DeviceInfo_Response'."""

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
            module = import_type_support('realsense2_camera_msgs')
        except ImportError:
            import logging
            import traceback
            logger = logging.getLogger(
                'realsense2_camera_msgs.srv.DeviceInfo_Response')
            logger.debug(
                'Failed to import needed modules for type support:\n' +
                traceback.format_exc())
        else:
            cls._CREATE_ROS_MESSAGE = module.create_ros_message_msg__srv__device_info__response
            cls._CONVERT_FROM_PY = module.convert_from_py_msg__srv__device_info__response
            cls._CONVERT_TO_PY = module.convert_to_py_msg__srv__device_info__response
            cls._TYPE_SUPPORT = module.type_support_msg__srv__device_info__response
            cls._DESTROY_ROS_MESSAGE = module.destroy_ros_message_msg__srv__device_info__response

    @classmethod
    def __prepare__(cls, name, bases, **kwargs):
        # list constant names here so that they appear in the help text of
        # the message class under "Data and other attributes defined here:"
        # as well as populate each message instance
        return {
        }


class DeviceInfo_Response(metaclass=Metaclass_DeviceInfo_Response):
    """Message class 'DeviceInfo_Response'."""

    __slots__ = [
        '_device_name',
        '_serial_number',
        '_firmware_version',
        '_usb_type_descriptor',
        '_firmware_update_id',
        '_sensors',
    ]

    _fields_and_field_types = {
        'device_name': 'string',
        'serial_number': 'string',
        'firmware_version': 'string',
        'usb_type_descriptor': 'string',
        'firmware_update_id': 'string',
        'sensors': 'string',
    }

    SLOT_TYPES = (
        rosidl_parser.definition.UnboundedString(),  # noqa: E501
        rosidl_parser.definition.UnboundedString(),  # noqa: E501
        rosidl_parser.definition.UnboundedString(),  # noqa: E501
        rosidl_parser.definition.UnboundedString(),  # noqa: E501
        rosidl_parser.definition.UnboundedString(),  # noqa: E501
        rosidl_parser.definition.UnboundedString(),  # noqa: E501
    )

    def __init__(self, **kwargs):
        assert all('_' + key in self.__slots__ for key in kwargs.keys()), \
            'Invalid arguments passed to constructor: %s' % \
            ', '.join(sorted(k for k in kwargs.keys() if '_' + k not in self.__slots__))
        self.device_name = kwargs.get('device_name', str())
        self.serial_number = kwargs.get('serial_number', str())
        self.firmware_version = kwargs.get('firmware_version', str())
        self.usb_type_descriptor = kwargs.get('usb_type_descriptor', str())
        self.firmware_update_id = kwargs.get('firmware_update_id', str())
        self.sensors = kwargs.get('sensors', str())

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
        if self.device_name != other.device_name:
            return False
        if self.serial_number != other.serial_number:
            return False
        if self.firmware_version != other.firmware_version:
            return False
        if self.usb_type_descriptor != other.usb_type_descriptor:
            return False
        if self.firmware_update_id != other.firmware_update_id:
            return False
        if self.sensors != other.sensors:
            return False
        return True

    @classmethod
    def get_fields_and_field_types(cls):
        from copy import copy
        return copy(cls._fields_and_field_types)

    @builtins.property
    def device_name(self):
        """Message field 'device_name'."""
        return self._device_name

    @device_name.setter
    def device_name(self, value):
        if __debug__:
            assert \
                isinstance(value, str), \
                "The 'device_name' field must be of type 'str'"
        self._device_name = value

    @builtins.property
    def serial_number(self):
        """Message field 'serial_number'."""
        return self._serial_number

    @serial_number.setter
    def serial_number(self, value):
        if __debug__:
            assert \
                isinstance(value, str), \
                "The 'serial_number' field must be of type 'str'"
        self._serial_number = value

    @builtins.property
    def firmware_version(self):
        """Message field 'firmware_version'."""
        return self._firmware_version

    @firmware_version.setter
    def firmware_version(self, value):
        if __debug__:
            assert \
                isinstance(value, str), \
                "The 'firmware_version' field must be of type 'str'"
        self._firmware_version = value

    @builtins.property
    def usb_type_descriptor(self):
        """Message field 'usb_type_descriptor'."""
        return self._usb_type_descriptor

    @usb_type_descriptor.setter
    def usb_type_descriptor(self, value):
        if __debug__:
            assert \
                isinstance(value, str), \
                "The 'usb_type_descriptor' field must be of type 'str'"
        self._usb_type_descriptor = value

    @builtins.property
    def firmware_update_id(self):
        """Message field 'firmware_update_id'."""
        return self._firmware_update_id

    @firmware_update_id.setter
    def firmware_update_id(self, value):
        if __debug__:
            assert \
                isinstance(value, str), \
                "The 'firmware_update_id' field must be of type 'str'"
        self._firmware_update_id = value

    @builtins.property
    def sensors(self):
        """Message field 'sensors'."""
        return self._sensors

    @sensors.setter
    def sensors(self, value):
        if __debug__:
            assert \
                isinstance(value, str), \
                "The 'sensors' field must be of type 'str'"
        self._sensors = value


class Metaclass_DeviceInfo(type):
    """Metaclass of service 'DeviceInfo'."""

    _TYPE_SUPPORT = None

    @classmethod
    def __import_type_support__(cls):
        try:
            from rosidl_generator_py import import_type_support
            module = import_type_support('realsense2_camera_msgs')
        except ImportError:
            import logging
            import traceback
            logger = logging.getLogger(
                'realsense2_camera_msgs.srv.DeviceInfo')
            logger.debug(
                'Failed to import needed modules for type support:\n' +
                traceback.format_exc())
        else:
            cls._TYPE_SUPPORT = module.type_support_srv__srv__device_info

            from realsense2_camera_msgs.srv import _device_info
            if _device_info.Metaclass_DeviceInfo_Request._TYPE_SUPPORT is None:
                _device_info.Metaclass_DeviceInfo_Request.__import_type_support__()
            if _device_info.Metaclass_DeviceInfo_Response._TYPE_SUPPORT is None:
                _device_info.Metaclass_DeviceInfo_Response.__import_type_support__()


class DeviceInfo(metaclass=Metaclass_DeviceInfo):
    from realsense2_camera_msgs.srv._device_info import DeviceInfo_Request as Request
    from realsense2_camera_msgs.srv._device_info import DeviceInfo_Response as Response

    def __init__(self):
        raise NotImplementedError('Service classes can not be instantiated')
