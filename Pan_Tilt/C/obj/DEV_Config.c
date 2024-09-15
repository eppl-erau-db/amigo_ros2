/*****************************************************************************
* | File        :   DEV_Config.c
* | Author      :   Waveshare team
* | Function    :   Hardware underlying interface
* | Info        :
*                Used to shield the underlying layers of each master
*                and enhance portability
*----------------
* |	This version:   V1.0
* | Date        :   2018-09-03
* | Info        :   Basic version
*
******************************************************************************/
#include "DEV_Config.h"
#include "Debug.h"  //DEBUG()



/**
 * Module Initialize, use BCM2835 library.
 *
 * Example:
 * if(DEV_ModuleInit())
 *   exit(0);
 */
UBYTE DEV_ModuleInit(void)
{
    SYSFS_GPIO_Export(M1_ENABLE_PIN);
    SYSFS_GPIO_Export(M1_DIR_PIN);
    SYSFS_GPIO_Export(M1_STEP_PIN);
    SYSFS_GPIO_Export(M1_M0_PIN);
    SYSFS_GPIO_Export(M1_M1_PIN);
    SYSFS_GPIO_Export(M1_M2_PIN);


    DEV_Digital_Write(M2_DIR_PIN, 1);
    DEV_Digital_Write(M1_DIR_PIN, 1);

    SYSFS_GPIO_Direction(M1_ENABLE_PIN, OUT);
    SYSFS_GPIO_Direction(M1_DIR_PIN, OUT);
    SYSFS_GPIO_Direction(M1_STEP_PIN, OUT);
    SYSFS_GPIO_Direction(M1_M0_PIN, OUT);   
    SYSFS_GPIO_Direction(M1_M1_PIN, OUT);   
    SYSFS_GPIO_Direction(M1_M2_PIN, OUT);   
    
    
    SYSFS_GPIO_Export(M2_ENABLE_PIN);
    SYSFS_GPIO_Export(M2_DIR_PIN);
    SYSFS_GPIO_Export(M2_STEP_PIN);
    SYSFS_GPIO_Export(M2_M0_PIN);
    SYSFS_GPIO_Export(M2_M1_PIN);
    SYSFS_GPIO_Export(M2_M2_PIN);

    SYSFS_GPIO_Direction(M2_ENABLE_PIN, OUT);
    SYSFS_GPIO_Direction(M2_DIR_PIN, OUT);
    SYSFS_GPIO_Direction(M2_STEP_PIN, OUT);
    SYSFS_GPIO_Direction(M2_M0_PIN, OUT);   
    SYSFS_GPIO_Direction(M2_M1_PIN, OUT);   
    SYSFS_GPIO_Direction(M2_M2_PIN, OUT);   


    return 0;
}

/**
 * Module Exit, close BCM2835 library.
 *
 * Example:
 * DEV_ModuleExit();
 */
void DEV_ModuleExit(void)
{

}

/**
 * Millisecond delay.
 *
 * @param xms: time.
 *
 * Example:
 * DEV_Delay_ms(500);//delay 500ms
 */
void DEV_Delay_ms(uint32_t xms)
{
    for(int j=xms; j > 0; j--)
        for(int i=50000; i > 0; i--);
}

/**
 * Microsecond delay.
 *
 * @param xus: time.
 *
 * Example:
 * DEV_Delay_us(500);//delay 500us
 */
void DEV_Delay_us(uint32_t xus)
{
    int j;
    for(j=xus; j > 0; j--);
}
