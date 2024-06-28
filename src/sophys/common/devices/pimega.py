#!/usr/bin/env python3

from ophyd import (
    ADComponent,
    EpicsSignal,
    EpicsSignalRO,
    EpicsSignalWithRBV,
    SingleTrigger,
    Device
)
from ophyd.areadetector.cam import CamBase
from ophyd.areadetector.detectors import DetectorBase


class Digital2AnalogConverter(Device):

    cas = ADComponent(EpicsSignalWithRBV, "CAS")
    delay = ADComponent(EpicsSignalWithRBV, "Delay")
    disc = ADComponent(EpicsSignalWithRBV, "Disc")
    disch = ADComponent(EpicsSignalWithRBV, "DiscH")
    discl = ADComponent(EpicsSignalWithRBV, "DiscL")
    discls = ADComponent(EpicsSignalWithRBV, "DiscLS")
    fbk = ADComponent(EpicsSignalWithRBV, "FBK")
    gnd = ADComponent(EpicsSignalWithRBV, "GND")
    ikrum = ADComponent(EpicsSignalWithRBV, "IKrum")
    preamp = ADComponent(EpicsSignalWithRBV, "Preamp")
    RPZ = ADComponent(EpicsSignalWithRBV, "RPZ")
    shaper = ADComponent(EpicsSignalWithRBV, "Shaper")
    threshold0 = ADComponent(EpicsSignalWithRBV, "ThresholdEnergy0")
    threshold1 = ADComponent(EpicsSignalWithRBV, "ThresholdEnergy1")
    tp_buffer_in = ADComponent(EpicsSignalWithRBV, "TPBufferIn")
    tp_buffer_out = ADComponent(EpicsSignalWithRBV, "TPBufferOut")
    tpref = ADComponent(EpicsSignalWithRBV, "TPRef")
    tpref_a = ADComponent(EpicsSignalWithRBV, "TPRefA")
    tpref_b = ADComponent(EpicsSignalWithRBV, "TPRefB")


class PimegaCam(CamBase):

    magic_start = ADComponent(EpicsSignal, "MagicStart")
    acquire_capture = ADComponent(EpicsSignal, "AcquireCapture")
    num_capture = ADComponent(EpicsSignalWithRBV, "NumCapture")

    medipix_mode = ADComponent(EpicsSignalWithRBV, "MedipixMode")

    detector_state = ADComponent(EpicsSignalRO, "DetectorState_RBV")
    processed_acquisition_counter = ADComponent(EpicsSignalRO, "ProcessedAcquisitionCounter_RBV")
    num_captured = ADComponent(EpicsSignalRO, "NumCaptured_RBV")
    
    dac = ADComponent(Digital2AnalogConverter, "DAC_")


    file_name = ADComponent(EpicsSignalWithRBV, "FileName")
    file_path = ADComponent(EpicsSignalWithRBV, "FilePath")
    file_number = ADComponent(EpicsSignalWithRBV, "FileNumber")
    file_template = ADComponent(EpicsSignalWithRBV, "FileTemplate")
    auto_increment = ADComponent(EpicsSignalWithRBV, "AutoIncrement")
    auto_save = ADComponent(EpicsSignalWithRBV, "AutoSave")

    def __init__(self, prefix, name, **kwargs):
        super(PimegaCam, self).__init__(prefix, name=name, **kwargs)


class PimegaDetector(DetectorBase):
    cam = ADComponent(PimegaCam, "cam1:", kind="config")


class Pimega(SingleTrigger, PimegaDetector):
    def __init__(self, name, prefix, **kwargs):
        super(Pimega, self).__init__(prefix, name=name, **kwargs)
