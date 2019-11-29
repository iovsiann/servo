#!/usr/bin/env python

import rospy, time, pigpio
from std_msgs.msg import Float32

G = int(rospy.get_param('~pin_num', '18'))
f = int(rospy.get_param('~frequency', '100'))
mx = int(rospy.get_param('~max_pulse_width_us', '2400'))
mn = int(rospy.get_param('~min_pulse_width_us', '600'))

pi = pigpio.pi()
pi.set_PWM_frequency(G, f)
pi.set_PWM_range(G, 1000000/f)

def callback(data):
    if not pi.connected:
        rospy.logerror('pigpio not connected')
    else:
        d = max([data.data, 0])
        d = min([data.data, 1.0])
        d = (mx - mn) * d + mn
        rospy.loginfo(rospy.get_caller_id() + 'Setting %s', data.data)
        pi.set_PWM_dutycycle(G, d)

def on_shutdown():
    rospy.loginfo('Stopping servo')
    pi.stop()

def listener():
    rospy.init_node('servo_node', anonymous=True)
    rospy.Subscriber('servo_angle', Float32, callback)
    rospy.on_shutdown(on_shutdown)
    rospy.spin()

if __name__ == '__main__':
    listener()
