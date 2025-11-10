from ophyd import (
    Component,
    FormattedComponent,
    Device,
    EpicsSignal,
    EpicsSignalRO,
    Kind,
)


class _Step(Device):
    setpoint = FormattedComponent(
        EpicsSignal,
        read_pv="{prefix}getSetPoint_{index}",
        write_pv="{prefix}SetPoint_{index}",
    )
    ramp_rate = FormattedComponent(
        EpicsSignal,
        read_pv="{prefix}getRampRate_{index}",
        write_pv="{prefix}RampRate_{index}",
    )
    soak_time = FormattedComponent(
        EpicsSignal,
        read_pv="{prefix}getStepTime_{index}",
        write_pv="{prefix}StepTime_{index}",
    )

    def __init__(self, index: int, **kwargs):
        self.index = index

        super().__init__(**kwargs)


class E5CK(Device):
    state = Component(EpicsSignalRO, "State", kind=Kind.config)

    number_of_steps = Component(
        EpicsSignal, read_pv="getStepNumbers", write_pv="NumSteps"
    )
    control = Component(EpicsSignalRO, "termopar")
    target = Component(EpicsSignalRO, "target")
    power = Component(EpicsSignalRO, "power")

    run_stop = Component(EpicsSignal, "run_stop", kind=Kind.omitted)
    continue_pause = Component(EpicsSignal, "continue_pause", kind=Kind.omitted)

    pid_on_off = Component(
        EpicsSignal, read_pv="get_PID_OnOff", write_pv="PID_OnOff_SET"
    )
    p = Component(EpicsSignal, read_pv="getP", write_pv="setP")
    i = Component(EpicsSignal, read_pv="getI", write_pv="setI")
    d = Component(EpicsSignal, read_pv="getD", write_pv="setD")

    current_step = Component(
        EpicsSignal, read_pv="CurrentStep", write_pv="CurrentStep_SET"
    )
    advance_step = Component(EpicsSignal, "advance")
    first_step = Component(_Step, index=0)
    second_step = Component(_Step, index=1)
    third_step = Component(_Step, index=2)
    fourth_step = Component(_Step, index=3)
    fifth_step = Component(_Step, index=4)
    sixth_step = Component(_Step, index=5)
    seventh_step = Component(_Step, index=6)
    eighth_step = Component(_Step, index=7)

    operation_power_on = Component(
        EpicsSignal, read_pv="getOpPowerOn", write_pv="OpPowerOn_SET"
    )
    set_point_at_start = Component(
        EpicsSignal, read_pv="SetPointProgStart_RBV", write_pv="SetPointProgStart"
    )
    end_condition = Component(
        EpicsSignal, read_pv="getEndCondition", write_pv="EndCondition"
    )
    program_type = Component(
        EpicsSignal, read_pv="getProgramType", write_pv="ProgramType"
    )
    program_time_unit = Component(
        EpicsSignal, read_pv="getProgTimeUnit", write_pv="ProgramTimeUnit"
    )
    time_unit_ramp_rate = Component(
        EpicsSignal, read_pv="getTimeUnitRamp", write_pv="TimeUnitRamp"
    )

    heating_side_output = Component(EpicsSignalRO, "HeatingSideOutPut_status")
    cooling_side_output = Component(EpicsSignalRO, "CoolingSideOutPut_status")
    input_error = Component(EpicsSignalRO, "InputError_status")
    a_d_converter_error = Component(EpicsSignalRO, "ADConvertError_status")
    program_end_status = Component(EpicsSignalRO, "ProgramEnd_status")

    run_reset_status = Component(EpicsSignalRO, "RunReset_status")
    auto_manual_status = Component(EpicsSignalRO, "AutoManual_status")
    remote_local_status = Component(EpicsSignalRO, "RemoteLocal_status")
    auto_tuning_status = Component(EpicsSignalRO, "AutoTuning_status")
    ramp_soak_status = Component(EpicsSignalRO, "RampSoak_status")
