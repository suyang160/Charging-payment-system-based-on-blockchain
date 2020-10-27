#include "led.h"
#include "delay.h"
#include "key.h"
#include "sys.h"
#include "usart.h"
#include "timer.h"
 
/************************************************
 ALIENTEKս��STM32������ʵ��4
 ����ʵ�� 
 ����֧�֣�www.openedv.com
 �Ա����̣�http://eboard.taobao.com 
 ��ע΢�Ź���ƽ̨΢�źţ�"����ԭ��"����ѻ�ȡSTM32���ϡ�
 ������������ӿƼ����޹�˾  
 ���ߣ�����ԭ�� @ALIENTEK
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
	delay_init();	    	 //��ʱ������ʼ��	  
	NVIC_PriorityGroupConfig(NVIC_PriorityGroup_2); //����NVIC�жϷ���2:2λ��ռ���ȼ���2λ��Ӧ���ȼ�
	uart_init(9600);	 //���ڳ�ʼ��Ϊ9600
	uart2_init(4800);	 //���ڳ�ʼ��Ϊ4800
 	control_charger_pin_Init();			     //LED�˿ڳ�ʼ��
	KEY_Init();          //��ʼ���밴�����ӵ�Ӳ���ӿ�
	TIM3_Int_Init(499,7199);//10Khz�ļ���Ƶ�ʣ�������500Ϊ50ms  
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
//			Start_charge=0;//�������
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
				if(detect_charge == 1)//�������
				{
					Start_charge = 0;    //�������
				}
			}
		}
		
		if(USART2_RX_STA&0x8000)
		{					   
			len=USART2_RX_STA&0x3fff;//�õ��˴ν��յ������ݳ���
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

