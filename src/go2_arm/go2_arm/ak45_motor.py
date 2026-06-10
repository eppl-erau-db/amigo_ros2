"""
CubeMars AK45-36 motor controller over servo CAN protocol via a gs_usb adapter.

Vendored from the robot's ``ak45_motor_gs_usb_fixed.py`` and adapted for use as a
ROS 2 package module:

* the ``gs_usb`` import is guarded so the module can be imported (and the replay
  node can run in ``dry_run`` mode) on machines without the gs_usb library or the
  physical CAN dongle attached;
* the per-frame RX debug print is gated behind a ``debug`` flag so it does not
  spam when driven by a ROS node.

Motor parameters (AK45-36):
  Kt          = 0.11  Nm/A  (motor-phase torque constant)
  pole_pairs  = 14
  gear_ratio  = 36:1
  torque_limit = 34.0 Nm output

CAN protocol (CubeMars servo / VESC-based):
  TX message ID = (packet_type << 8) | motor_can_id   (extended frame)
  RX message ID = motor_can_id                         (extended frame)

  Packet types used:
    1  SET_CURRENT      data: int32  = current [mA]
    3  SET_RPM          data: int32  = ERPM
    4  SET_POS          data: int32  = position [deg x 10000]
    6  SET_POS_SPD      data: int32 pos [deg x 10000] + uint16 vel [ERPM] + uint16 acc [ERPM/s]

  Feedback (8 bytes, extended frame, ID = (0x29 << 8) | motor_can_id):
    bytes 0-1  int16   position   x 0.1       -> degrees
    bytes 2-3  int16   speed      x 10        -> ERPM
    bytes 4-5  int16   current    x 0.01      -> Amps
    byte  6    uint8   temperature             -> C
    byte  7    uint8   error code
"""
from __future__ import annotations

import math
import struct
import threading
import time
from dataclasses import dataclass

# gs_usb (python-gs_usb) is only needed when actually talking to hardware.  Guard
# the import so dry-run / unit tests work without the library installed.
try:  # pragma: no cover - import guard
    from gs_usb.constants import CAN_EFF_FLAG
    from gs_usb.gs_usb import GsUsb
    from gs_usb.gs_usb_frame import GsUsbFrame

    GS_USB_AVAILABLE = True
    GS_USB_IMPORT_ERROR = None
except Exception as exc:  # pragma: no cover - import guard
    GS_USB_AVAILABLE = False
    GS_USB_IMPORT_ERROR = exc
    CAN_EFF_FLAG = 0x80000000

# Motor constants
KT = 0.11    # Nm/A
POLE_PAIRS = 14
GEAR_RATIO = 36
TRQ_LIMIT = 34.0    # Nm output
ERPM_CONV = POLE_PAIRS * GEAR_RATIO * 60.0 / (2.0 * math.pi)  # (rad/s -> ERPM)

# CAN packet type IDs
SET_CURRENT = 1
SET_RPM = 3
SET_POS = 4
SET_POS_SPD = 6

ERROR_CODES = {
    0: "OK",
    1: "Over-temperature",
    2: "Over-current",
    3: "Over-voltage",
    4: "Under-voltage",
    5: "Encoder fault",
    6: "MOSFET over-temperature",
    7: "Motor stall",
}


@dataclass
class MotorState:
    position: float = float("nan")     # rad  (encoder-zero corrected, output shaft)
    velocity: float = float("nan")     # rad/s (output shaft)
    current: float = float("nan")      # A
    torque: float = float("nan")       # Nm  (output shaft)
    temperature: float = float("nan")  # C
    error: int = 0


class AK45Motor:
    """Controls a single CubeMars AK45-36 motor via servo CAN.

    Args:
        can_id:  CAN node ID programmed into the motor (1-127).
        enc_off: Encoder zero offset in radians. Subtracted from raw position.
        bus:     A MotorBus instance (shared across motors on the same bus).
    """

    def __init__(self, can_id: int, enc_off: float = 0.0, bus=None):
        self.can_id = can_id
        self.enc_off = enc_off
        self.bus = bus
        self.state = MotorState()
        self._lock = threading.Lock()

    def _send(self, packet_type: int, data: bytes):
        msg_id = (packet_type << 8) | self.can_id
        self.bus.send(msg_id, data)

    def set_position(self, pos_rad: float, vel_limit: float = 1.0, acc_limit: float = 5.0):
        """Move to position using SET_POS_SPD (mode 6)."""
        pos_int = int(pos_rad * 180.0 / math.pi * 10000.0)
        vel_erpm = int(max(1, min(vel_limit * ERPM_CONV, 32767)))
        acc_erpm = int(max(1, min(acc_limit * ERPM_CONV, 32767)))
        data = struct.pack(">iHH", pos_int, vel_erpm, acc_erpm)
        self._send(SET_POS_SPD, data)

    def set_velocity(self, vel_rad_s: float):
        """Run at constant velocity (output shaft, signed)."""
        erpm = int(vel_rad_s * ERPM_CONV)
        erpm = max(-100000, min(erpm, 100000))
        self._send(SET_RPM, struct.pack(">i", erpm))

    def set_current(self, current_a: float):
        """Direct current (torque) control, max +/-60 A."""
        current_ma = int(current_a * 1000.0)
        current_ma = max(-60000, min(current_ma, 60000))
        self._send(SET_CURRENT, struct.pack(">i", current_ma))

    def set_torque(self, torque_nm: float):
        """Output torque control (converted to current internally)."""
        self.set_current(torque_nm / (KT * GEAR_RATIO))

    def stop(self):
        """Coast to stop by zeroing current."""
        self.set_current(0.0)

    def parse_feedback(self, data: bytes):
        """Update state from an 8-byte feedback CAN frame."""
        if len(data) < 8:
            return
        pos_raw = struct.unpack(">h", data[0:2])[0]
        spd_raw = struct.unpack(">h", data[2:4])[0]
        cur_raw = struct.unpack(">h", data[4:6])[0]
        temp = data[6]
        error = data[7]
        with self._lock:
            self.state.position = pos_raw * 0.1 * math.pi / 180.0 - self.enc_off
            self.state.velocity = spd_raw * 10.0 / ERPM_CONV
            self.state.current = cur_raw * 0.01
            self.state.torque = self.state.current * KT * GEAR_RATIO
            self.state.temperature = float(temp)
            self.state.error = error

    def get_state(self) -> MotorState:
        with self._lock:
            return MotorState(
                position=self.state.position,
                velocity=self.state.velocity,
                current=self.state.current,
                torque=self.state.torque,
                temperature=self.state.temperature,
                error=self.state.error,
            )


class MotorBus:
    """CAN bus manager using a gs_usb adapter.

    Raises a clear RuntimeError if the gs_usb library is unavailable so callers
    (e.g. the replay node) can fall back to dry-run instead of crashing on import.

    The ``channel`` keyword is accepted (and ignored) for drop-in compatibility
    with SocketCAN-style call sites that pass ``channel='can0'``.
    """

    def __init__(self, motors=None, bitrate: int = 1_000_000, channel=None, debug: bool = False):
        if not GS_USB_AVAILABLE:
            raise RuntimeError(
                f"gs_usb library unavailable ({GS_USB_IMPORT_ERROR}); cannot open the arm CAN bus."
            )
        del channel  # accepted for API compatibility; gs_usb auto-discovers the device
        self.debug = debug
        self.motors = {m.can_id: m for m in (motors or [])}

        devs = GsUsb.scan()
        if not devs:
            raise RuntimeError("No gs_usb device found")
        self.dev = devs[0]

        # Reset to bus-off before configuring (handles re-run without unplug)
        self.dev.stop()
        if not self.dev.set_bitrate(bitrate):
            raise RuntimeError(f"Failed to set bitrate: {bitrate}")
        self.dev.start()

        self._stop = threading.Event()
        self._thread = threading.Thread(target=self._recv_loop, daemon=True)
        self._thread.start()

    def _recv_loop(self):
        iframe = GsUsbFrame()
        while not self._stop.is_set():
            if self.dev.read(iframe, 10):  # timeout_ms = 10
                raw_id = iframe.can_id & 0x1FFFFFFF
                motor_id = raw_id & 0xFF
                if self.debug:
                    print(f"RX 0x{raw_id:X} motor_id={motor_id} data={[f'{b:02X}' for b in iframe.data]}")
                if motor_id in self.motors:
                    self.motors[motor_id].parse_feedback(bytes(iframe.data))

    def send(self, can_id: int, data: bytes):
        """Send an extended CAN frame."""
        frame = GsUsbFrame(can_id=can_id | CAN_EFF_FLAG, data=data)
        if not self.dev.send(frame):
            raise RuntimeError(f"Failed to send CAN frame to ID 0x{can_id:X}")

    def close(self):
        self._stop.set()
        self._thread.join(timeout=1.0)
        self.dev.stop()

    def __enter__(self):
        return self

    def __exit__(self, *_):
        self.close()
