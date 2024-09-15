/*****************************************************************************
* | File        :   DRV8825.c
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
#include "DRV8825.h"
#include "Debug.h"  //DEBUG()
#include <stdlib.h> //exit()
#include <stdio.h>  //printf()
#include <string.h> //strcmp()

MOTOR Motor;

char *microstepmode[6] =  {
    "fullstep",
    "halfstep",
    "1/4step",
    "1/8step",
    "1/16step",
    "1/32step",
};

/**
 * Select motor
 *
 * @param name: motor.
 *
 * Example:
 * DRV8825_SelectMotor(MOTOR1);
 * or: DRV8825_SelectMotor(MOTOR2);
 */
void DRV8825_SelectMotor(UBYTE name)
{
    Motor.Name = name;
    if(name == MOTOR1) {
        Motor.EnablePin = M1_ENABLE_PIN;
        Motor.DirPin = M1_DIR_PIN;
        Motor.StepPin = M1_STEP_PIN;
        Motor.M0Pin = M1_M0_PIN;
        Motor.M1Pin = M1_M1_PIN;
        Motor.M2Pin = M1_M2_PIN;
    } else if(name == MOTOR2) {
        Motor.EnablePin = M2_ENABLE_PIN;
        Motor.DirPin = M2_DIR_PIN;
        Motor.StepPin = M2_STEP_PIN;
        Motor.M0Pin = M2_M0_PIN;
        Motor.M1Pin = M2_M1_PIN;
        Motor.M2Pin = M2_M2_PIN;
    } else {
        DEBUG("please set motor: MOTOR1 or MOTOR2\r\n");
    }
}

/**
 * The motor stops rotating and the driver chip is disabled.
 *
 */
static void DRV8825_Enable(void)
{
    DEV_Digital_Write(Motor.EnablePin, 1);
}

void DRV8825_Stop(void)
{
    DEV_Digital_Write(Motor.EnablePin, 0);
}

/**
 * Set control method and micro Stepping format
 *
 * @param mode: control method:
 *      should be: HARDWARD or SOFTWARD
 *      if use HARDWARD,Stepformat will be invalid
 *      if use SOFTWARD,You have to solder the 6 resistors on the back  
 * @param stepformat: micro Stepping format:
 *      should be: "fullstep","halfstep","1/4step","1/8step","1/16step","1/32step"
 * Example:
 * DRV8825_SetMicroStep(HARDWARD, "fullstep");
 * DRV8825_SetMicroStep(SOFTWARD, "fullstep");
 */
void DRV8825_SetMicroStep(char mode, const char *stepformat)
{
    if(mode == HARDWARD) {
        DEBUG("use hardware control\r\n");
        return;
    } else {
        DEBUG("use software control\r\n");
    }
    DEBUG("step formoat = %s\r\n", stepformat);

    char i = 0;
    char **str = microstepmode;
    for(i = 0; i < 6; i++) {
        if(strcmp(stepformat, *str) == 0) {
            Motor.MicroStep = *str;
            break;
        }
        str++;
    }
    printf("MicroStep = %s\r\n", Motor.MicroStep);
    if(i == 6) {
        DEBUG("The stepformat must be : \"fullstep\",\"halfstep\",\"1/4step\",\"1/8step\",\"1/16step\",\"1/32step\"\r\n");
        exit(0);
    }

    DEV_Digital_Write(Motor.M0Pin, i & 0x01);
    DEV_Digital_Write(Motor.M1Pin, (i >> 1) & 0x01);
    DEV_Digital_Write(Motor.M2Pin, (i >> 2) & 0x01);
}

/**
 * turn.
 *
 * @param dir: direction.
 * @param steps: Step count.
 * @param stepdelay: step delay.
 *
 * Example:
 * UBYTE buf = DRV8825_ReadByte(0x00);
 */
void DRV8825_TurnStep(UBYTE dir, UWORD steps, UWORD stepdelay)
{
    Motor.Dir = dir;
    if(dir == FORWARD) {
        DEBUG("motor %d formward\r\n", Motor.Name);
        DRV8825_Enable();
        DEV_Digital_Write(Motor.DirPin, 0);
    } else if(dir == BACKWARD) {
        DEBUG("motor %d backmward\r\n", Motor.Name);
        DRV8825_Enable();
        DEV_Digital_Write(Motor.DirPin, 1);
    } else {
        DRV8825_Stop();
    }

    if(steps == 0)
        return;

    UWORD i = 0;
    DEBUG("turn %d steps\r\n", steps);
    for(i = 0; i < steps; i++) {
        DEV_Digital_Write(Motor.StepPin, 1);
        DEV_Delay_ms(stepdelay);
        DEV_Digital_Write(Motor.StepPin, 0);
        DEV_Delay_ms(stepdelay);
    }

}
