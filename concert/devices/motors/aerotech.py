'''
Created on Apr 10, 2013

@author: farago
'''
from concert.devices.motors.base import ContinuousMotor, LinearCalibration,\
    Motor
import quantities as q
from concert.connection import AerotechConnection
import time
from concert.asynchronous import async


class Aerorot(ContinuousMotor):
    HOST = ""
    PORT = 0
    AXIS = "X"
    
    # status constants (bits of the AXISSTATUS output (see HLe docs))
    AXISSTATUS_ENABLED = 0
    AXISSTATUS_HOMED = 1
    AXISSTATUS_IN_POSITION = 2
    AXISSTATUS_MOVE_ACTIVE = 3
    AXISSTATUS_ACCEL_PHASE = 4
    AXISSTATUS_DECEL_PHASE = 5
    AXISSTATUS_POSITION_CAPTURE = 6
    AXISSTATUS_HOMING = 14
    
    EPSILON = 1e-1
    SLEEP_TIME = 0.1
    
    def __init__(self):
        pos_calib = LinearCalibration(1*q.mm, 0*q.mm)
        velo_calib = LinearCalibration(1*q.mm, 0*q.mm)
        super(Aerorot, self).__init__(pos_calib, velo_calib)
        
        self._connection = AerotechConnection(Aerorot.HOST, Aerorot.PORT)

    def _query_state(self):
        return self._connection.execute("AXISSTATUS(%s)" % (Aerorot.AXIS))
        
    def _get_position(self):
        self._connection.execute("PFBK(%s)%s" % (Aerorot.AXIS))
        return float(self._connection.recv())
        
    def _set_position(self, steps):
        self._connection.execute("MOVEABS %s %f%s" % (Aerorot.AXIS, steps))
        lower = steps - Aerorot.EPSILON
        upper = steps + Aerorot.EPSILON
        while lower < self._get_position() < upper:
            time.sleep(Aerorot.SLEEP_TIME) 
    
    def _get_velocity(self):
        self._connection.execute("VFBK(%s)%s" % (Aerorot.AXIS))
        return float(self._connection.recv())
    
    def _set_velocity(self, steps):
        self._connection.execute("FREERUN %s %f%s" % (Aerorot.AXIS, steps))
        
        # Allow 0.1 % discrepancy.
        while self._get_velocity() < steps - steps/1000.:
            time.sleep(Aerorot.SLEEP_TIME)
            
    def _get_state(self):
        res = self._query_state()
        if res >> Aerorot.AXISSTATUS_MOVE_ACTIVE:
            self._state = Motor.MOVING
        else:
            self._state = Motor.STANDBY
            
    def _stop(self):
        if self.state == Motor.MOVING:
            self._connection.execute("ABORT %s" % (Aerorot.AXIS))
        
        while self.state == Motor.MOVING:
            time.sleep(Aerorot.SLEEP_TIME)
        
    def _home(self):
        self._connection.execute("HOME %s" % (Aerorot.AXIS))
        
        while self.state == Motor.MOVING:
            time.sleep(Aerorot.SLEEP_TIME)
            
    def get_digital_in(self, port, bit):
        """Get TTL level on *port* and *bit*."""
        res = self._connection.execute("DIN(%s,%d,%d)" %\
                                       (Aerorot.AXIS, port, bit))
        return res == "1"
    
    def set_digital_out(self, port, bit, value):
        """Set TTL level on *port* and *bit* to *value*"""
        self._connection.execute("DOUT %s, %d, %d:%d" % (Aerorot.AXIS, port,
                                    bit, value))
        
    @async
    def on(self):
        """
        on()
        
        Turn the motor on.
        """
        self._connection.execute("ENABLE %s" % (Aerorot.AXIS))
        
    @async
    def off(self):
        """
        off()
        
        Turn the motor off.
        """
        self._connection.execute("DISABLE %s" % (Aerorot.AXIS))