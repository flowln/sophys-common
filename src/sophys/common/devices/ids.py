from enum import IntEnum
from typing import Annotated as A

from bluesky.protocols import Movable, Stoppable

from ophyd import (
    Device,
    Component,
    EpicsSignal,
    EpicsSignalRO,
    PVPositionerIsClose,
    Kind,
)

from ophyd_async.core import (
    SignalR,
    SignalRW,
    SignalX,
    StandardReadable,
    WatchableAsyncStatus,
    DEFAULT_TIMEOUT,
)
from ophyd_async.core import StandardReadableFormat as Format
from ophyd_async.epics.core import EpicsDevice, PvSuffix as Pv
from ophyd_async.epics.core import epics_signal_r, epics_signal_w, epics_signal_rw

from .async_positioner import BasePositioner
from ..utils.signals import EpicsSignalMon


class EpicsSignalIDs(PVPositionerIsClose):
    setpoint = Component(EpicsSignal, "-SP")
    readback = Component(EpicsSignalMon, "")


# Reference:
# https://cnpemcamp.sharepoint.com/:x:/s/Comissionamento/Eabdu5JQhm1Oh8xjo25QNkEBeA8lLoRFrrTI0nVYT6t9aw?e=JnWNx9
class UndulatorKymaAPU(Device):
    """Ophyd device for the Kyma APU Undulator."""

    # Control registers and flags
    class Command(IntEnum):
        No = 0
        Stop = 1
        Reset = 2
        Start = 3
        CalibTilt = 4
        Standby = 5
        Home = 10

    class StateHW(IntEnum):
        Off = 0x00
        HWInit = 0x01
        ConfigError = 0x02
        Init = 0x03
        Alarm = 0x04
        Warning = 0x08
        BusyPositiveAlarm = 0x14
        BusyPositiveWarning = 0x18
        BusyPositive = 0x1C
        BusyNegativeAlarm = 0x28
        BusyNegativeWarning = 0x24
        BusyNegative = 0x2C
        ReadyAlarm = 0x34
        ReadyWarning = 0x38
        Ready = 0x3C
        OpAlarm = 0x44
        OpWarning = 0x48
        Op = 0x4C

    class State(IntEnum):
        Na = 0
        Op = 1
        Start = 2
        Jog = 3
        Standby = 4
        CalibTilt = 5
        Backup = 6
        Restore = 7
        BackupEncoders = 8
        RestoreEncoders = 9
        ForceNewPosition = 10
        Home = 11
        Error = 12
        Reset = 13
        Stop = 14
        ErrorStop = 15
        PowerOff = 16
        Init = 17
        ConfigError = 18

    command = Component(
        EpicsSignal,
        "DevCtrl-Cmd",
        lazy=True,
        kind=Kind.omitted,
    )
    state_hw = Component(EpicsSignalMon, "StateHw", lazy=True, kind=Kind.omitted)
    state = Component(EpicsSignalMon, "State", lazy=True, kind=Kind.omitted)

    is_operational = Component(
        EpicsSignalMon, "IsOperational", lazy=True, kind=Kind.omitted
    )
    is_motors_on = Component(
        EpicsSignalMon, "MotorsEnbld", lazy=True, kind=Kind.omitted
    )
    is_alarm_set = Component(EpicsSignalMon, "Alarm", lazy=True, kind=Kind.omitted)
    is_moving_set = Component(EpicsSignalMon, "Moving", lazy=True, kind=Kind.omitted)

    is_remote = Component(EpicsSignalMon, "IsRemote", lazy=True, kind=Kind.omitted)
    interface = Component(EpicsSignalMon, "Interface", lazy=True, kind=Kind.omitted)

    home_axis = Component(EpicsSignal, "HomeAxis-Sel", lazy=True, kind=Kind.omitted)

    phase = Component(
        EpicsSignalIDs,
        "Phase",
        lazy=True,
        kind=Kind.hinted,
    )

    phase_speed = Component(
        EpicsSignalIDs,
        "PhaseSpeed",
        lazy=True,
        kind=Kind.config,
    )
    phase_max_speed = Component(
        EpicsSignalRO,
        "MaxPhaseSpeed-RB",
        lazy=True,
        kind=Kind.config,
    )

    # Status
    class PhaseAlarm(IntEnum):
        DriveError = 0
        PowerOff = 1
        Lag = 2
        Overload = 3
        InputInvalid = 4
        EncodeError = 5
        Disabled = 6
        NotHomed = 7
        KillSwitchLow = 8

    class PhaseAlarmState(IntEnum):
        Off = 0x00
        HWInit = 0x01
        ConfigError = 0x02
        Init = 0x03
        Alarm = 0x04
        Warning = 0x08
        BusyPositiveAlarm = 0x14
        BusyPositiveWarning = 0x18
        BusyPositive = 0x1C
        BusyNegativeAlarm = 0x28
        BusyNegativeWarning = 0x24
        BusyNegative = 0x2C
        ReadyAlarm = 0x34
        ReadyWarning = 0x38
        Ready = 0x3C
        OpAlarm = 0x44
        OpWarning = 0x48
        Op = 0x4C

    phase_alarm = Component(EpicsSignalMon, "AlrmPhase", lazy=True, kind=Kind.omitted)
    # Reference:
    # https://infosys.beckhoff.com/english.php?content=../content/1033/tcncerrcode2/index.html
    phase_alarm_errid = Component(
        EpicsSignalMon, "AlrmPhaseErrID", lazy=True, kind=Kind.omitted
    )
    phase_alarm_sdw = Component(
        EpicsSignalMon, "AlrmPhaseSttDW", lazy=True, kind=Kind.omitted
    )
    phase_alarm_state = Component(
        EpicsSignalMon, "AlrmPhaseStt", lazy=True, kind=Kind.omitted
    )
    rack_alarm_estop = Component(
        EpicsSignalMon, "AlrmRackEStop", lazy=True, kind=Kind.omitted
    )
    rack_alarm_kill = Component(
        EpicsSignalMon, "AlrmRackKill", lazy=True, kind=Kind.omitted
    )
    rack_alarm_kill_disabled = Component(
        EpicsSignalMon, "AlrmRackKillDsbld", lazy=True, kind=Kind.omitted
    )
    rack_alarm_power_disabled = Component(
        EpicsSignalMon, "AlrmRackPwrDsbld", lazy=True, kind=Kind.omitted
    )

    # Interlock
    interlock_in_stop = Component(
        EpicsSignalMon, "IntlkInStop", lazy=True, kind=Kind.omitted
    )
    interlock_in_open_gap = Component(
        EpicsSignalMon, "IntlkInEOpnGap", lazy=True, kind=Kind.omitted
    )
    interlock_out_gap_opened = Component(
        EpicsSignalMon, "IntlkOutGapStt", lazy=True, kind=Kind.omitted
    )
    interlock_out_status_ok = Component(
        EpicsSignalMon, "IntlkOutStsOk", lazy=True, kind=Kind.omitted
    )
    interlock_out_ccps_enabled = Component(
        EpicsSignalMon, "IntlkOutCCPSEnbld", lazy=True, kind=Kind.omitted
    )
    interlock_out_power_enabled = Component(
        EpicsSignalMon, "IntlkOutPwrEnbld", lazy=True, kind=Kind.omitted
    )

    # Beamline control
    beamline_control_status = Component(
        EpicsSignalRO, "BeamLineCtrlEnbl-Sts", lazy=True, kind=Kind.omitted
    )


class _IVUPositioner(BasePositioner, EpicsDevice):
    setpoint: A[SignalRW[float], Pv("-RB"), Pv("-SP")]
    readback: A[SignalR[float], Pv("-Mon"), Format.HINTED_SIGNAL]

    actuate_value = 1
    done_value = 0

    def __init__(self, prefix: str, parent_prefix: str, name: str = ""):
        with self.add_children_as_readables():
            self.actuate = epics_signal_w(str, f"{parent_prefix}KParamChange-Cmd")
            self.done = epics_signal_r(bool, f"{parent_prefix}Moving-Mon")

        super().__init__(prefix=prefix, name=name)


class IVU(EpicsDevice, StandardReadable, Movable, Stoppable):
    control_enabled: A[SignalR[bool], Pv("BeamLineCtrl-Mon")]
    is_moving: A[SignalR[bool], Pv("Moving-Mon")]

    abort: A[SignalX, Pv("Abort-Cmd")]
    reset: A[SignalX, Pv("Reset-Cmd")]

    def __init__(self, prefix: str, name: str = "", supports_step_scan: bool = False):
        self.gap = _IVUPositioner(prefix + "KParam", prefix)
        self.velocity = _IVUPositioner(prefix + "KParamVelo", prefix)

        self.add_readables([self.gap.readback], Format.HINTED_SIGNAL)

        if supports_step_scan:
            with self.add_children_as_readables():
                self.step_mode = epics_signal_rw(bool, prefix + "Step_Mode")
                self.read_csv = epics_signal_rw(
                    bool, prefix + "Read_State", prefix + "Read_StepCsv"
                )
                self.scan_done = epics_signal_r(bool, prefix + "Scan_Done")

        super().__init__(prefix=prefix, name=name)

    @WatchableAsyncStatus.wrap
    async def set(self, new_gap: float, timeout=DEFAULT_TIMEOUT):
        control_enabled = await self.control_enabled.get_value()
        if not control_enabled:
            raise PermissionError(
                f"Tried to move the IVU while control is not enabled ({self.control_enabled.source})."
            )

        await self.gap.set(new_gap, timeout=timeout)

    async def stop(self, success=True):
        await self.abort.trigger()
