from scipy import misc
import sys
import os
import numpy as np
import glob

def performConversion(input_directory_name,output_directory_name):
	header=np.zeros(4).astype(np.int32)
	if not (os.path.isdir(output_directory_name)):
		os.system("mkdir "+output_directory_name)
	for file_name in sorted(os.listdir(input_directory_name)):
		output_file_name=file_name.split('.')[0]+'.bix'
		print("File name = "+file_name)
		image_info=misc.imread(input_directory_name+file_name)
		data_file=open(output_directory_name+output_file_name,'w')
		data_file.write(header.tobytes()+image_info.flatten().tobytes())
		data_file.close()

input_dir='../'
performConversion(input_dir+'images/',input_dir+'/images_raw/')
		
print("Finished")

