/*****************************************************************************
* | File        :   DRV8825.h
* | Author      :   Waveshare team
* | Function    :   Drive DRV8825
* | Info        :
*                The DRV8825 provides an integrated motor driver solution for
*                printers, scanners, and other automated equipment applications.
*                The device has two H-bridge drivers and a microstepping indexer,
*                and is intended to drive a bipolar stepper motor.
*----------------
* |	This version:   V1.0
* | Date        :   2018-10-13
* | Info        :   Basic version
*
******************************************************************************/
#ifndef __PCA9685_H_
#define __PCA9685_H_

#include "DEV_Config.h"

#define MOTOR1  1
#define MOTOR2  2

//Motor Dir
#define FORWARD 0
#define BACKWARD 1

//Control Mode
#define HARDWARD 0
#define SOFTWARD 1

typedef struct {
    UBYTE Name;
    char *MicroStep;
    UBYTE Dir;
    UBYTE EnablePin;
    UBYTE DirPin;
    UBYTE StepPin;
    UBYTE M0Pin;
    UBYTE M1Pin;
    UBYTE M2Pin;
} MOTOR;

void DRV8825_SelectMotor(UBYTE name);
void DRV8825_Stop(void);
void DRV8825_SetMicroStep(char mode, const char *stepformat);
void DRV8825_TurnStep(UBYTE dir, UWORD steps, UWORD stepdelay);
#endif