#ifndef __KEY_H
#define __KEY_H	 
#include "sys.h"
//////////////////////////////////////////////////////////////////////////////////	 
//������ֻ��ѧϰʹ�ã�δ��������ɣ��������������κ���;
//ALIENTEKս��STM32������
//������������	   
//����ԭ��@ALIENTEK
//������̳:www.openedv.com
//�޸�����:2012/9/3
//�汾��V1.0
//��Ȩ���У�����ؾ���
//Copyright(C) ������������ӿƼ����޹�˾ 2009-2019
//All rights reserved									  
//////////////////////////////////////////////////////////////////////////////////   	 


//#define KEY0 PEin(4)   	//PE4
//#define KEY1 PEin(3)	//PE3 
//#define KEY2 PEin(2)	//PE2
//#define WK_UP PAin(0)	//PA0  WK_UP

#define dianyuan_led  GPIO_ReadInputDataBit(GPIOB,GPIO_Pin_4)
#define zhunbei_led  GPIO_ReadInputDataBit(GPIOB,GPIO_Pin_5)
#define chongdian_led GPIO_ReadInputDataBit(GPIOB,GPIO_Pin_6)
#define error_led   GPIO_ReadInputDataBit(GPIOB,GPIO_Pin_7)
#define detect_charge GPIO_ReadInputDataBit(GPIOB,GPIO_Pin_8) //��Ϊ�ߵ�ƽ���������


void KEY_Init(void);//IO��ʼ��
u8 KEY_Scan(u8);  	//����ɨ�躯��					    
#endif
