/*****************************************************************************
* | File        :   Debug.h
* | Author      :   Waveshare team
* | Function    :   debug with printf
* | Info        :
*----------------
* | This version:   V1.0
* | Date        :   2018-01-11
* | Info        :   Basic version
*
******************************************************************************/
#ifndef __DEBUG_H_
#define __DEBUG_H_

#include <stdio.h>

#define USE_DEBUG 0
#if USE_DEBUG
#define DEBUG(__info,...) printf("Debug : " __info,##__VA_ARGS__)
#else
#define DEBUG(__info,...)
#endif

#endif

