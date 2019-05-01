import cv2
import sys
import os
import numpy as np
import glob

def convertImageToBinaryFile(image_fname,output_fname):
	header=np.zeros(4).astype(np.int32)
	image_info=cv2.imread(input_directory_name+file_name)
        data_file=open(output_directory_name+output_file_name,'w')
        data_file.write(header.tobytes()+image_info.flatten().tobytes())
        data_file.close()

def performConversion(input_directory_name,output_directory_name):
	if not (os.path.isdir(output_directory_name)):
		os.system("mkdir "+output_directory_name)
	for file_name in sorted(os.listdir(input_directory_name)):
		convertImageToBinaryFile(file_name,file_name.split('.')[0]+'.bix')

assert sys.argv == 3, 'Input and output files should be privided as arguments.'
input_dir= sys.argv[1]
putput_dir=sys.argv[2]
performConversion(input_dir,output_dir')

