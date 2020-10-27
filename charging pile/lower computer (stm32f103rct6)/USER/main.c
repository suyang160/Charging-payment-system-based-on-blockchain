#include "led.h"
#include "delay.h"
#include "key.h"
#include "sys.h"
#include "usart.h"
#include "timer.h"
 
/************************************************
 ALIENTEK战舰STM32开发板实验4
 串口实验 
 技术支持：www.openedv.com
 淘宝店铺：http://eboard.taobao.com 
 关注微信公众平台微信号："正点原子"，免费获取STM32资料。
 广州市星翼电子科技有限公司  
 作者：正点原子 @ALIENTEK
************************************************/


 int main(void)
 {		
 	u16 t;  
	u16 len;	
	u16 times=0;
	u8 chongdian_flag=0;
	u8 chongdianzhong=0;
	u8 chaqiang_flag=0;
	double energy=0;
	double voltage=0;
	delay_init();	    	 //延时函数初始化	  
	NVIC_PriorityGroupConfig(NVIC_PriorityGroup_2); //设置NVIC中断分组2:2位抢占优先级，2位响应优先级
	uart_init(9600);	 //串口初始化为9600
	uart2_init(4800);	 //串口初始化为4800
 	control_charger_pin_Init();			     //LED端口初始化
	KEY_Init();          //初始化与按键连接的硬件接口
	TIM3_Int_Init(499,7199);//10Khz的计数频率，计数到500为50ms  
 	while(1)
	{
//		if(dianyuan_led==0)
//		{
//			printf("LED1 on\r\n");
//		}
//		else
//		{
//			printf("LED1 off\r\n");
//		}
//		if(zhunbei_led==0)
//		{
//			printf("LED2 on\r\n");
//		}
//		else
//		{
//			printf("LED2 off\r\n");
//			
//		}
//	  if(chongdianzhong==0)
//		{
//			if(chongdian_led==0)
//			{
//          chaqiang_flag=0;	
//			}
//			else
//			{
//				if(chongdian_flag==1)
//				{
//					printf("LED3 off\r\n");
//					GPIO_SetBits(GPIOC,GPIO_Pin_6);
//					chongdian_flag=0;				
//				}	
//			}
//		}
//		
//		if(detect_charge==1)
//		{
//			Start_charge=0;//启动充电
//		}
//		else
//		{
//			Start_charge=1;
//		}
//		if(error_led==0)
//		{
//			printf("LED4 on\r\n");
//		}
//		else
//		{
//			printf("LED4 off\r\n");
//		}
       
//			if(dianyuan_led==0&&chongdian_led==1)
//			{
//				printf("Waiting for the plug\r\n");
//			}
//		  if(dianyuan_led==0&&chongdian_led==1)
//			{
//				printf("Has pluged in\r\n");
//			}
    if(dianyuan_led==0)
		{
			if(plug_state==1)
			{
				printf("has not plugged in\r\n");
				Plug_out = 0;
				Plug_in = 1;
				Start_charge = 1;
			}
			if(plug_state==2)
			{
				printf("has plugged in\r\n");
				Plug_in = 0;
				Plug_out = 1;
				if(detect_charge == 1)//开启充电
				{
					Start_charge = 0;    //开启充电
				}
			}
		}
		
		if(USART2_RX_STA&0x8000)
		{					   
			len=USART2_RX_STA&0x3fff;//得到此次接收到的数据长度
			if(USART2_RX_BUF[0]==0x01&&USART2_RX_BUF[1]==0x03&&USART2_RX_BUF[2]==0x24)
			{
				energy = 0;
				for(t=3;t<=6;t++)
				{
					energy = USART2_RX_BUF[t]*256+energy;
				}
				energy = energy*0.01;
				printf("energy is %f\r\n",energy);
				voltage = USART2_RX_BUF[25]*256 + USART2_RX_BUF[26];
				voltage = voltage * 0.1;
				printf("voltage is %f\r\n",voltage);
			}
			USART2_RX_STA=0;
		}
		
		
	}	 
 }

