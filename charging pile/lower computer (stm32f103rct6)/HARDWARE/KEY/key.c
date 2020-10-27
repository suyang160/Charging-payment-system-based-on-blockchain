#include "stm32f10x.h"
#include "key.h"
#include "sys.h" 
#include "delay.h"
//////////////////////////////////////////////////////////////////////////////////	 
//本程序只供学习使用，未经作者许可，不得用于其它任何用途
//ALIENTEK战舰STM32开发板
//按键驱动代码	   
//正点原子@ALIENTEK
//技术论坛:www.openedv.com
//修改日期:2012/9/3
//版本：V1.0
//版权所有，盗版必究。
//Copyright(C) 广州市星翼电子科技有限公司 2009-2019
//All rights reserved									  
//////////////////////////////////////////////////////////////////////////////////  
								    
//按键初始化函数
void KEY_Init(void) //IO初始化
{ 
 	GPIO_InitTypeDef GPIO_InitStructure;
 
 	RCC_APB2PeriphClockCmd(RCC_APB2Periph_GPIOB,ENABLE);//使能PORTA,PORTE时钟

	GPIO_InitStructure.GPIO_Pin  = GPIO_Pin_7|GPIO_Pin_4|GPIO_Pin_5|GPIO_Pin_6;//KEY0-KEY2
	GPIO_InitStructure.GPIO_Mode = GPIO_Mode_IN_FLOATING; //设置成上拉输入
 	GPIO_Init(GPIOB, &GPIO_InitStructure);
	
  GPIO_InitStructure.GPIO_Pin =  GPIO_Pin_8; //连接模拟灯引脚
	GPIO_InitStructure.GPIO_Mode = GPIO_Mode_IPD;
	GPIO_Init(GPIOB, &GPIO_InitStructure);
	
}
