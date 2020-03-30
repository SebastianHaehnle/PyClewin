#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Oct  2 09:05:40 2019

@author: kevink
"""

from PyClewin import *

import numpy as np



class Paired_inductor(object):
    '''
    Paired inductor where both lines meander together, optional to seperate arms in last meander for coupling
    Input:
        line        :: line width
        gap         :: gap width
        linelayer   :: metal layer for line
        mesh
        corner      :: corner type, square or round
    '''
    def __init__(self, line, gap, linelayer):
        self.type = 'paired_inductor'
        self.line = line
        self.gap = gap
        self.linelayer = linelayer
        self.tm_type = 'strip'
        self.direction = 1
    
    def process_direction(self, direction):
        if direction == None or direction == 0:
            direction = self.direction
        else:
            self.direction = direction
        return direction
    
    def wire(self, direction, L):
        direction = self.process_direction(direction)
        layername(self.linelayer)
        
        wire(direction, float(L), self.line, (0,(self.line+self.gap)/2.))
        wire(direction, float(L), self.line, (0,-(self.line+self.gap)/2.))
        return direction
    
    def wirego(self, direction, L, *args, **kwargs):
        direction = self.process_direction(direction)
        self.wire(direction, L, *args, **kwargs)
        rot(direction)
        go(float(L), 0)
        rotback()
        #self.used_wires.append([direction, L, self.direction])
        return direction
    
    def square_turn(self, direction_in, direction_out, *args, **kwargs):
        if base.cornerDirection(direction_in, direction_out) > 0:
            wire(direction_in, (2*self.line + self.gap), self.line, (0,-(self.line+self.gap)/2.))
            wire(direction_in, (self.line), self.line, (0,(self.line+self.gap)/2.))
            wire(direction_out, (self.line + self.gap), self.line, (-self.gap/2,-(1.5*self.line + self.gap)))
        else:
            wire(direction_in, (2*self.line + self.gap), self.line, (0,(self.line+self.gap)/2.))
            wire(direction_in, (self.line), self.line, (0,-(self.line+self.gap)/2.))
            wire(direction_out, (self.line + self.gap), self.line, (-self.gap/2,(1.5*self.line + self.gap)))
            
    def square_turn_go(self, direction_in, direction_out, *args, **kwargs):
        if base.cornerDirection(direction_in, direction_out) > 0:
            wire(direction_in, (2*self.line + self.gap), self.line, (0,-(self.line+self.gap)/2.))
            wire(direction_in, (self.line), self.line, (0,(self.line+self.gap)/2.))
            wire(direction_out, (self.line + self.gap), self.line, (-self.gap/2,-(1.5*self.line + self.gap)))
        else:
            wire(direction_in, (2*self.line + self.gap), self.line, (0,(self.line+self.gap)/2.))
            wire(direction_in, (self.line), self.line, (0,-(self.line+self.gap)/2.))
            wire(direction_out, (self.line + self.gap), self.line, (-self.gap/2,(1.5*self.line + self.gap)))
        movedirection(direction_in,self.gap/2+self.line)
        movedirection(direction_out,(self.gap/2 + self.line))
        return direction_out
    
    def square_turn_go_widen(self, direction_in, direction_out, width, *args, **kwargs):
        if base.cornerDirection(direction_in, direction_out) > 0:
            wire(direction_in, (2*self.line + width), self.line, (0,-(self.line+self.gap)/2.))
            wire(direction_in, (self.line), self.line, (0,(self.line+self.gap)/2.))
            wire(direction_out, (self.line + self.gap), self.line, (-self.gap/2,-(width + 1.5*self.line)))
        else:
            wire(direction_in, (2*self.line + width), self.line, (0,(self.line+self.gap)/2.))
            wire(direction_in, (self.line), self.line, (0,-(self.line+self.gap)/2.))
            wire(direction_out, (self.line + self.gap), self.line, (-self.gap/2,(width + 1.5*self.line)))
        movedirection(direction_in,width/2+self.line)
        movedirection(direction_out,(self.gap/2 + self.line))
        return direction_out
        
    def rounded_turn_go_widen(self, direction_in, direction_out, width, R_base):
        movedirection(direction_out,self.gap/2+self.line/2)
        if direction_in == 1j:
            turnup(direction_in, R_base+self.line/2,self.line,36, shift = (0,0))
            movedirection(-direction_out,self.gap+self.line)
            wirego(direction_in,width+R_base,self.line)
            turnupgo(direction_in, R_base+self.line/2,self.line,36, shift = (0,0))
            wirego(direction_out, R_base + self.line/2, self.line)
            movedirection(-direction_in,width/2 + self.line/2)
        elif direction_in == -1j:
            turndown(direction_in, R_base+self.line/2,self.line,36, shift = (0,0))
            movedirection(-direction_out,self.gap+self.line)
            wirego(direction_in,width+R_base,self.line)
            turndowngo(direction_in, R_base+self.line/2,self.line,36, shift = (0,0))
            wirego(direction_out, R_base + self.line/2, self.line)
            movedirection(-direction_in,width/2 + self.line/2)
    
    def square_180(self, direction, orientation):
            self.square_turn_go(direction, abs(orientation))
            self.wirego(abs(orientation),self.gap) 
            self.square_turn_go(abs(orientation), -direction)
    
    def round_180(self,direction,R_base):
        if direction == 1j:
            turn180(direction, R_base+self.line/2, self.line, 36, shift = (0, -2*(R_base+self.line/2) - (self.line+self.gap)/2))
            turn180(direction, R_base+(1.5*self.line+self.gap), self.line, 36, shift = (0, -2*(R_base+(1.5*self.line+self.gap)) + (self.line+self.gap)/2))
        elif direction == -1j:
            turn180(direction, R_base+self.line/2, self.line, 36, shift = (0,self.gap/2+self.line/2))
            turn180(direction, R_base+(1.5*self.line+self.gap), self.line, 36, shift = (0,-self.gap/2-self.line/2))
        movedirection(1,2*R_base+2*self.line+self.gap)
    
    def end_circle(self,direction,R_large,R_small):
        movedirection(-1,self.line/2 + self.gap/2)
        wirego(direction,R_large+R_small+self.line,self.line)
        #turn180go(direction, R_large+self.line/2, self.line, 36, shift=(0,-2*R_large-self.line))
        if direction == 1j:
            direction = turndowngo(direction, R_large+self.line/2, self.line, 36, shift = (0,0))
            direction = turndowngo(direction, R_large+self.line/2, self.line, 36, shift = (0,0))
            direction = turndowngo(direction, R_large+self.line/2, self.line, 36, shift = (0,0))
            direction = turnupgo(direction, R_small+self.line/2, self.line, 36, shift = (0,0))
        elif direction == -1j:
            direction = turnupgo(direction, R_large+self.line/2, self.line, 36, shift = (0,0))
            direction = turnupgo(direction, R_large+self.line/2, self.line, 36, shift = (0,0))
            direction = turnupgo(direction, R_large+self.line/2, self.line, 36, shift = (0,0))
            direction = turndowngo(direction, R_small+self.line/2, self.line, 36, shift = (0,0))
            
    def end_bar(self, direction):
        base.bar(direction, self.line, (self.line*2+self.gap), (self.line/2,0))
        

class ID_capacitor(object):
    '''
    NOTE!!!! I SWAPPED THE CONNECTOR LINE AND CONNECTOR GAP DEFINITIONS SINCE I'M DRAWING THIS SECTION AS TWO LINES WITH A GAP
    
    Interdigitated capacitor wich connects to a meander inductor
    Input:
        line        :: line width
        gap         :: gap width
        connector_line :: line width of the connector
        connector_gap :: gap at the connector
        linelayer   :: metal layer for line
        mesh
        corner      :: corner type, square or round
    '''
    def __init__(self, line, connector_line, connector_gap, arm_a, arm_b, finger_line, finger_gap, linelayer):
        self.type = 'id_capacitor'
        self.line = line
        self.gap = arm_a + arm_b + connector_gap + 2.*connector_line
        self.connector_line = connector_line
        self.connector_gap = connector_gap
        self.arm_a = arm_a
        self.arm_b = arm_b
        self.finger_line = finger_line
        self.finger_gap = finger_gap
        self.linelayer = linelayer
        self.tm_type = 'strip'
        self.direction = 1
    
    
    def process_direction(self, direction):
        if direction == None or direction == 0:
            direction = self.direction
        else:
            self.direction = direction
        return direction
    
    def wire(self, direction, L):
        direction = self.process_direction(direction)
        layername(self.linelayer)
        
        wire(direction, float(L), self.line, (0,(self.line+self.gap)/2.))
        wire(direction, float(L), self.line, (0,-(self.line+self.gap)/2.))
        return direction
    
    def wirego(self, direction, L, *args, **kwargs):
        direction = self.process_direction(direction)
        self.wire(direction, L, *args, **kwargs)
        rot(direction)
        go(float(L), 0)
        rotback()
        #self.used_wires.append([direction, L, self.direction])
        return direction
    
    def wire_connector(self, direction, L):
        direction = self.process_direction(direction)
        layername(self.linelayer)
        
        wire(direction, float(L), self.connector_line, (0,(self.connector_line+self.connector_gap)/2.))
        wire(direction, float(L), self.connector_line, (0,-(self.connector_line+self.connector_gap)/2.))
        return direction
    
    def widen(self, direction):
        movedirection(abs(direction),self.line/2)
        wire(direction*-1j, self.arm_a+self.connector_line+self.line ,self.line, (self.connector_gap/2,0))
        wire(direction*1j, self.arm_b+self.connector_line+self.line ,self.line, (self.connector_gap/2,0))

        
    def fingers_single(self,direction,N,length_finger,fshift,finger_cut,max_finger_cut):
        req_cut = fshift*finger_cut;
        num_full_cut_fingers = np.floor(req_cut/max_finger_cut)
        last_cut = np.remainder(req_cut,max_finger_cut)
        
        full_cut_list = (N-1) - (np.arange(num_full_cut_fingers)+1)*2
        if len(full_cut_list) == 0:
            partial_cut = N-3    
        else:
            partial_cut = min(full_cut_list) - 2
        
        for n in range(1,N+1):
            if n == 1:
                movedirection(-abs(direction),self.finger_gap+self.finger_line/2)
                wire(direction*-1j, length_finger, self.finger_line)
            elif n in full_cut_list:
                if np.mod(n,2) == 0:
                    movedirection(-abs(direction),self.finger_gap+self.finger_line)
                    wire(direction*-1j, length_finger-max_finger_cut, self.finger_line,(self.finger_gap+max_finger_cut,0))
                else:
                    movedirection(-abs(direction),self.finger_gap+self.finger_line)
                    wire(direction*-1j, length_finger-max_finger_cut, self.finger_line,(0,0))
            elif n == partial_cut:
                if np.mod(n,2) == 0:
                    movedirection(-abs(direction),self.finger_gap+self.finger_line)
                    wire(direction*-1j, length_finger-last_cut, self.finger_line,(self.finger_gap+last_cut,0))
                else:
                    movedirection(-abs(direction),self.finger_gap+self.finger_line)
                    wire(direction*-1j, length_finger-last_cut, self.finger_line,(0,0))
            else:
                if np.mod(n,2) == 0:
                    movedirection(-abs(direction),self.finger_gap+self.finger_line)
                    wire(direction*-1j, length_finger, self.finger_line,(self.finger_gap,0))
                else:
                    movedirection(-abs(direction),self.finger_gap+self.finger_line)
                    wire(direction*-1j, length_finger, self.finger_line,(0,0))
    
    def fingers_all(self,direction,N,length_finger,fshift,finger_cut,safe_fingers):
        req_cut = fshift*finger_cut;
        

        for n in range(1,N+1):
            
            if n == 1:
                movedirection(-abs(direction),self.finger_gap+self.finger_line/2)
                wire(direction*-1j, length_finger, self.finger_line)
            
            elif np.mod(n,2) == 1 : # uneven finger, this is the finger we cut
                if n not in safe_fingers:
                    movedirection(-abs(direction),self.finger_gap+self.finger_line)
                    wire(direction*-1j, length_finger-req_cut, self.finger_line,(0,0))
                else:
                    movedirection(-abs(direction),self.finger_gap+self.finger_line)
                    wire(direction*-1j, length_finger, self.finger_line,(0,0))             
            else: # even finger, this is the finger we never cut
                movedirection(-abs(direction),self.finger_gap+self.finger_line)
                wire(direction*-1j, length_finger, self.finger_line,(self.finger_gap,0))    

            
    
    def coupling_bar(self,direction,length,width,d,width_bar,overlap,extension):
        wire(direction*-1j,length,width)
        movedirection(-abs(direction),d+width/2+width_bar/2)
        #movedirection(direction*1j,self.line)
        wire(direction*-1j,overlap,width_bar)
        wire(direction*1j,extension,width_bar)
    

        
        
        