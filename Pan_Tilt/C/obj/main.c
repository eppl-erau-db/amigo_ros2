#include <stdio.h>      //printf()
#include <stdlib.h>     //exit()
#include <signal.h>
#include "DEV_Config.h"
#include "DRV8825.h"

void  Handler(int signo)
{
    //System Exit
    printf("\r\nHandler:Motor Stop\r\n");
    DRV8825_SelectMotor(MOTOR1);
    DRV8825_Stop();
    DRV8825_SelectMotor(MOTOR2);
    DRV8825_Stop();
    DEV_ModuleExit();

    exit(0);
}

int main(void)
{
    //1.System Initialization
    if(DEV_ModuleInit())
        exit(0);
    
    // Exception handling:ctrl + c
    signal(SIGINT, Handler);
    while(1){
        /*
        # 1.8 degree: nema23, nema14
        # softward Control :
        # 'fullstep': A cycle = 200 steps
        # 'halfstep': A cycle = 200 * 2 steps
        # '1/4step': A cycle = 200 * 4 steps
        # '1/8step': A cycle = 200 * 8 steps
        # '1/16step': A cycle = 200 * 16 steps
        # '1/32step': A cycle = 200 * 32 steps
        */
    
        DRV8825_SelectMotor(MOTOR1);
        DRV8825_SetMicroStep(HARDWARD, "fullstep");
        DRV8825_TurnStep(BACKWARD, 2000, 1);
        DRV8825_Stop();

        /*
        # 28BJY-48:
        # softward Control :
        # 'fullstep': A cycle = 2048 steps
        # 'halfstep': A cycle = 2048 * 2 steps
        # '1/4step': A cycle = 2048 * 4 steps
        # '1/8step': A cycle = 2048 * 8 steps
        # '1/16step': A cycle = 2048 * 16 steps
        # '1/32step': A cycle = 2048 * 32 steps
        */
        DRV8825_SelectMotor(MOTOR2);
        DRV8825_SetMicroStep(HARDWARD, "fullstep");
        DRV8825_TurnStep(BACKWARD, 2000, 1);
        DRV8825_Stop();
    }
    
    //3.System Exit
    DEV_ModuleExit();
    return 0;
}

