from PyQt5.QtCore import pyqtSignal
from pymodaq.daq_utils.daq_utils import ThreadCommand, get_plugins, set_logger, get_module_name

logger = set_logger(get_module_name(__file__))

DAQ_Move_Stage_type = get_plugins('daq_move')
DAQ_0DViewer_Det_types = get_plugins('daq_0Dviewer')
DAQ_1DViewer_Det_types = get_plugins('daq_1Dviewer')
DAQ_2DViewer_Det_types = get_plugins('daq_2Dviewer')
DAQ_NDViewer_Det_types = get_plugins('daq_NDviewer')


class OutputToActuator:
    def __init__(self, mode='rel', values=[]):
        super().__init__()
        if mode not in ['abs', 'rel']:
            raise ValueError(f'Incorrect mode for the OutputToActuator object: {mode}')

        self.mode = mode
        self.values = values

class PIDModelGeneric:
    limits = dict(max=dict(state=False, value=1),
                  min=dict(state=False, value=0),)
    konstants = dict(kp=1, ki=0.1, kd=0.001)
    params = []

    Nsetpoint = 1
    setpoint_ini = [0. for ind in range(Nsetpoint)]

    actuators_name = []
    detectors_name = []

    def __init__(self, pid_controller):
        self.pid_controller = pid_controller  # instance of the pid_controller using this model
        self.get_mod_from_name = pid_controller.module_manager.get_mod_from_name

        self.settings = self.pid_controller.settings.child('models', 'model_params')  # set of parameters
        self.data_names = None
        self.curr_output = None
        self.curr_input = None

        self.check_modules(pid_controller.module_manager)



    def setpoint(self, values):
        self.pid_controller.setpoint = values

    def apply_constants(self):
        for kxx in self.konstants:
            self.pid_controller.settings.child('main_settings', 'pid_controls', 'pid_constants',
                                               kxx).setValue(self.konstants[kxx])

    def apply_limits(self):
        for limit in self.limits:
            self.pid_controller.settings.child('main_settings', 'pid_controls', 'output_limits',
                                               f'output_limit_{limit}').setValue(self.limits[limit]['value'])
            self.pid_controller.settings.child('main_settings', 'pid_controls', 'output_limits',
                                               f'output_limit_{limit}_enabled').setValue(self.limits[limit]['state'])

    def check_modules(self, module_manager):
        for act in self.actuators_name:
            if act not in module_manager.actuators_name:
                logger.warning(f'The actuator {act} defined in the PID model is not present in the Dashboard')
                return False
        for det in self.detectors_name:
            if det not in module_manager.detectors_name:
                logger.warning(f'The detector {det} defined in the PID model is not present in the Dashboard')

    def update_detector_names(self):
        names = self.pid_controller.settings.child('main_settings', 'detector_modules').value()['selected']
        self.data_names = []
        for name in names:
            name = name.split('//')
            self.data_names.append(name)


    def update_settings(self, param):
        """
        Get a parameter instance whose value has been modified by a user on the UI
        To be overwritten in child class
        """
        if param.name() == '':
            pass

    def ini_model(self):
        self.apply_limits()
        self.setpoint(self.setpoint_ini)
        self.apply_constants()

    def convert_input(self, measurements):
        """
        Convert the measurements in the units to be fed to the PID (same dimensionality as the setpoint)
        Parameters
        ----------
        measurements: (Ordereddict) Ordereded dict of object from which the model extract a value of the same units as the setpoint

        Returns
        -------
        float: the converted input

        """
        return 0

    def convert_output(self, output, dt):
        """
        Convert the output of the PID in units to be fed into the actuator
        Parameters
        ----------
        output: (float) output value from the PID from which the model extract a value of the same units as the actuator
        dt: (float) ellapsed time in seconds since last call
        Returns
        -------
        list: the converted output as a list (in case there are a few actuators)

        """
        #print('output converted')
        out_put_to_actuator = OutputToActuator('rel', values=[output])

        return out_put_to_actuator

