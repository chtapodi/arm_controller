import time
import pigpio

import argparse
import sys
import readchar


class arm_controller :

    #pin list is a list of the pins in order from base to tip
    #rotation list defines if the segment is arc or rotation.0s for arcs, 1s for rotation
    #starting angle is an optional list which preconfigures starting angles.
    def __init__(self, pin_list, rotation_list, start_angle,=120) :
        #generates a list that contains all the current angles of the arm
        self.angle_list=[start_angle for seg in pin_list]
        self.pin_list=pin_list
        self.rotation_list=rotation_list

        #initializes pin interface
        self.pi = pigpio.pi()
        for pin in self.pin_list : #iteritavely configures pin outsputs.
            self.pi.set_mode(pin, pigpio.OUTPUT)

        #controller settings/constants
        self.servo_min=0
        self.servo_max=175
        self.min_duty=500
        self.max_duty=2500


    def keyboard_control(self) :

        delta=3
        print("use keys to control servos")
        while True:
            key=readchar.readkey()
            #try :
            segmemt=0
            if key=='q' :
                self.angle_list[segmemt]+=delta
            elif key=='a':
                self.angle_list[segmemt]-=delta

            segmemt=1
            if key=='w' :
                self.angle_list[segmemt]+=delta
            elif key=='s':
                self.angle_list[segmemt]-=delta

            segmemt=2
            if key=='e' :
                self.angle_list[segmemt]+=delta
            elif key=='d':
                self.angle_list[segmemt]-=delta

            segmemt=3
            if key=='r' :
                self.angle_list[segmemt]+=delta
            elif key=='f':
                self.angle_list[segmemt]-=delta

            elif readchar.key.ESC :
                break

            else :
                pass

            for angle in self.angle_list :
                if(angle<self.servo_min) : angle=self.servo_min
                if(angle>self.servo_max) : angle=self.servo_max

            print(self.angle_list)
            self.update_arm()


            # time.sleep(.1)
            #except KeyboardInterrupt:
                #break

    #updates the arm to match the angle list
    def update_arm(self) :
        for pin, angle in zip(self.pin_list,self.angle_list) :
            self.pi.set_servo_pulsewidth(pin, self.angle_to_sigal(angle))


    #updates segmemt postion to inputed angle
    def segment_to_angle(self, segment, angle) :
        self.pi.set_servo_pulsewidth(segment, self.angle_to_sigal(angle))

    #converts angle to duty cycle
    def angle_to_sigal(self, angle) :

        return (((angle - self.servo_min) * (self.max_duty - self.min_duty)) / (self.servo_max - self.servo_min)) + self.min_duty

def main() :
    controller=arm_controller(17,27,22,17)
    controller.keyboard_control()


if __name__ == "__main__":
    # execute only if run as a script
    main()
