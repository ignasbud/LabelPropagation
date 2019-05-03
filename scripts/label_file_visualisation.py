#!/usr/bin/env python2
import cv2
from scipy import misc
import numpy as np
import os
#import matplotlib.pyplot as plt

from PIL import Image

import pdb
import sys


#mport matplotlib.pyplot as plt

#     this.colors = new byte[]{
#                128, 128,128,
#                128, 0, 0,
#                192, 192, 128,
#                128, 64, 128,
#                0, 0, 192,
#                128, 128, 0,
#                192,128,128,
#                64, 64 , 128,
#                64, 0, 128,
#                64, 64, 0,
#                0, 128, 192};


class LabelFileVisualisation:

	#COLOR_CITYSCAPES = {0:(128,64,128),1:(244,35,232),2:(70,70,70),3:(102,102,156),4:(190,153,153),5:(153,153,153),6:(250,170,30),7:(220,220,0),8:(107,142,35),9:(152,251,152),10:(70,130,180),11:(220,20,60),12:(255,0,0),13:(0,0,142),14:(0,0,70),15:(0,60,100),16:(0,80,100),17:(0,0,230),18:(119,11,32),19:(0,0,0)}
        #COLOR_CAMVIDTOY={0:(128,64,128),1:(244,35,232),2:(70,70,70),3:(102,102,156),4:(190,153,153),5:(153,153,153),6:(250,170,30),7:(220,220,0),8:(107,142,35),9:(152,251,152),10:(70,130,180),11:(220,20,60),12:(255,0,0),13:(0,0,0)} 
	#COLOR_CAMVID_ORIGINAL={0:(128, 128,128),1:(128, 0, 0),2:(192, 192, 128),3:(128, 64, 128),4:(0, 0, 192),5:(128, 128, 0),6:(192,128,128),7:(64, 64 , 128),8:(64, 0, 128),9:(64, 64, 0),10:( 0, 128, 192),11:(0,0,0)}
        #COLOR_2CLASS={0:(255,0,0),1:(0,0,255),2:(0,0,0)}
	COLOR_2CLASS={0:(0,0,0),1:(255,255,255),2:(127,127,127)}
	def __init__(self,color,L):
		self.color=color
		self.lut=self.make_lut()
		self.L=L	
	def make_lut(self):
	    lut = np.random.randint(0, 255, size=(256,3))
	    for i, c in enumerate(self.color):
        	lut[i,:] = self.color[i]
	    return lut.flatten("C").tolist()
        @staticmethod
	def get_extended_image(data,L):
		temp_data=np.zeros((data.shape[0],data.shape[1],data.shape[2]+1),dtype=np.float32)
                temp_data[:,:,0:L]=np.array(data,copy=True)
                temp_data[:,:,L]=(1.0/L)+0.0001
		return temp_data
	@staticmethod
        def get_extended_image_with_delta(data,L,delta): 
                temp_data=np.zeros((data.shape[0],data.shape[1],data.shape[2]+1),dtype=np.float32)
                temp_data[:,:,0:L]=np.array(data,copy=True)
                temp_data[:,:,L]=(1.0/L)+delta
                return temp_data

	@staticmethod
	def getExtendedMaxData(data,L):
		temp_data=LabelFileVisualisation.get_extended_image(data,L)
		amax = np.argmax(temp_data, axis=2).astype(np.uint8)
		return amax
        @staticmethod
        def getExtendedMaxDataWithDelta(data,L,delta):
                temp_data=LabelFileVisualisation.get_extended_image_with_delta(data,L,delta)
                amax = np.argmax(temp_data, axis=2).astype(np.uint8)
                return amax
	@staticmethod
	def produce_combined_file(in_fn_list,o_fn,width,height,L,color):
		max_data=[]
		label_data=[]
		for in_fn in in_fn_list:
			data=LabelFileVisualisation.read_label_image(in_fn,width,height,L)
			label_data.append(data)
			max_data.append(LabelFileVisualisation.getExtendedMaxData(data,L))
		max_data[0][max_data[0]!=max_data[1]]=L
		
		result_data=np.zeros((height,width,L),dtype=np.float32)
		result_data.fill(1.0/L)
		print("max data shape = " +str(max_data[0].shape)+ " result data shape = "+str(result_data.shape))
		result_data[max_data[0]<L,:]=label_data[0][max_data[0]<L,:]
		LabelFileVisualisation.save_label_image(o_fn,result_data)
		#assert(L==2), "Currently only L=2 is supported"
		lfv = LabelFileVisualisation(color,L)
		img=lfv.convert_image(result_data)
		print("FILE NAME = " + o_fn.split('.bix')[0]+'.png')
		img.save(o_fn.split('.bix')[0]+'.png')
	@staticmethod
        def produce_combined_visual_file(in_fn_list,o_fn,width,height,color):
                max_data=[]
                label_data=[]
                for in_fn in in_fn_list:
                        data=cv2.imread(in_fn)
                        label_data.append(data)
  
		ids_0= label_data[0][:,:,0].astype(np.int32)*256*256+label_data[0][:,:,1].astype(np.int32)*256+label_data[0][:,:,2].astype(np.int32)
		ids_1= label_data[1][:,:,0].astype(np.int32)*256*256+label_data[1][:,:,1].astype(np.int32)*256+label_data[1][:,:,2].astype(np.int32)
		mask = (ids_0[:,:]!=ids_1[:,:])
		print('mask shape = '+str(mask.shape))
     
           	label_data[0][mask,:]=color

                cv2.imwrite(o_fn,label_data[0])

	@staticmethod
        def save_label_image(file_name,data):
                print("File name = "+file_name)
                data=np.reshape(data.flatten(),(data.shape[0],data.shape[1],data.shape[2])).flatten()
                f=open(file_name,'wb')
		f.write(data.tobytes())
		f.close()

	@staticmethod
	def read_label_image(file_name,width,height,L):
		print("File name = "+file_name)
		data=np.fromfile(file_name, dtype=np.float32)
		data=np.reshape(data,(height,width,L))
		return data
	def convert_image(self,data):
		
		print("DATA size = "+str(data.shape))
		amax=LabelFileVisualisation.getExtendedMaxData(data,self.L)
		img = Image.fromarray(amax, "P")
    		img.putpalette(self.lut)
  	        #img.save(file_name)
		return img
