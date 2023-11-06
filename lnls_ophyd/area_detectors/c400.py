from ophyd import Component, EpicsSignalRO, EpicsSignalWithRBV, Kind, SingleTrigger
from ophyd.areadetector.cam import CamBase
from ophyd.areadetector.detectors import DetectorBase
from ophyd.areadetector.plugins import ImagePlugin


class C400Cam(CamBase):
    burst_size = Component(
        EpicsSignalWithRBV, "BURST_SIZE", lazy=True, kind=Kind.config
    )
    dead_time = Component(EpicsSignalWithRBV, "DEAD_TIME", lazy=True, kind=Kind.config)
    encoder = Component(EpicsSignalRO, "ENCODER_RBV", lazy=True, kind=Kind.config)
    system_ipmode = Component(
        EpicsSignalWithRBV, "SYSTEM_IPMODE", lazy=True, kind=Kind.config
    )

    trigger_polarity = Component(
        EpicsSignalWithRBV, "TRIGGER_POLARITY", lazy=True, kind=Kind.config
    )
    trigger_start = Component(
        EpicsSignalWithRBV, "TRIGGER_START", lazy=True, kind=Kind.config
    )
    trigger_stop = Component(
        EpicsSignalWithRBV, "TRIGGER_STOP", lazy=True, kind=Kind.config
    )
    trigger_pause = Component(
        EpicsSignalWithRBV, "TRIGGER_PAUSE", lazy=True, kind=Kind.config
    )

    pulser_period = Component(
        EpicsSignalWithRBV, "PULSER_PERIOD", lazy=True, kind=Kind.config
    )
    pulser_width = Component(
        EpicsSignalWithRBV, "PULSER_WIDTH", lazy=True, kind=Kind.config
    )

    dac_ch1 = Component(EpicsSignalWithRBV, "DAC_ch1", lazy=True, kind=Kind.config)
    dac_ch2 = Component(EpicsSignalWithRBV, "DAC_ch2", lazy=True, kind=Kind.config)
    dac_ch3 = Component(EpicsSignalWithRBV, "DAC_ch3", lazy=True, kind=Kind.config)
    dac_ch4 = Component(EpicsSignalWithRBV, "DAC_ch4", lazy=True, kind=Kind.config)

    dhi_ch1 = Component(EpicsSignalWithRBV, "DHI_ch1", lazy=True, kind=Kind.config)
    dhi_ch2 = Component(EpicsSignalWithRBV, "DHI_ch2", lazy=True, kind=Kind.config)
    dhi_ch3 = Component(EpicsSignalWithRBV, "DHI_ch3", lazy=True, kind=Kind.config)
    dhi_ch4 = Component(EpicsSignalWithRBV, "DHI_ch4", lazy=True, kind=Kind.config)

    dlo_ch1 = Component(EpicsSignalWithRBV, "DLO_ch1", lazy=True, kind=Kind.config)
    dlo_ch2 = Component(EpicsSignalWithRBV, "DLO_ch2", lazy=True, kind=Kind.config)
    dlo_ch3 = Component(EpicsSignalWithRBV, "DLO_ch3", lazy=True, kind=Kind.config)
    dlo_ch4 = Component(EpicsSignalWithRBV, "DLO_ch4", lazy=True, kind=Kind.config)

    hivo_volts_ch1 = Component(
        EpicsSignalWithRBV, "HIVO_VOLTS_ch1", lazy=True, kind=Kind.config
    )
    hivo_volts_ch2 = Component(
        EpicsSignalWithRBV, "HIVO_VOLTS_ch2", lazy=True, kind=Kind.config
    )
    hivo_volts_ch3 = Component(
        EpicsSignalWithRBV, "HIVO_VOLTS_ch3", lazy=True, kind=Kind.config
    )
    hivo_volts_ch4 = Component(
        EpicsSignalWithRBV, "HIVO_VOLTS_ch4", lazy=True, kind=Kind.config
    )

    hivo_enable_ch1 = Component(
        EpicsSignalWithRBV, "HIVO_ENABLE_ch1", lazy=True, kind=Kind.config
    )
    hivo_enable_ch2 = Component(
        EpicsSignalWithRBV, "HIVO_ENABLE_ch2", lazy=True, kind=Kind.config
    )
    hivo_enable_ch3 = Component(
        EpicsSignalWithRBV, "HIVO_ENABLE_ch3", lazy=True, kind=Kind.config
    )
    hivo_enable_ch4 = Component(
        EpicsSignalWithRBV, "HIVO_ENABLE_ch4", lazy=True, kind=Kind.config
    )

    polarity_ch1 = Component(
        EpicsSignalWithRBV, "POLARITY_ch1", lazy=True, kind=Kind.config
    )
    polarity_ch2 = Component(
        EpicsSignalWithRBV, "POLARITY_ch2", lazy=True, kind=Kind.config
    )
    polarity_ch3 = Component(
        EpicsSignalWithRBV, "POLARITY_ch3", lazy=True, kind=Kind.config
    )
    polarity_ch4 = Component(
        EpicsSignalWithRBV, "POLARITY_ch4", lazy=True, kind=Kind.config
    )


class C400Detector(DetectorBase):
    cam = Component(C400Cam, "cam1:")


class C400(SingleTrigger, C400Detector):
    """This is a C400 (Four-channel Pulse Counting Detector Controller) device using an AreaDetector-based IOC."""

    image = Component(ImagePlugin, "image1:")
