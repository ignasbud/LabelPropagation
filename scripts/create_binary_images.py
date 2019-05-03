import cv2
import sys
import os
import numpy as np
import glob
import argparse

def convertImageToBinaryFile(image_fname,output_fname,W,H):
	header=np.zeros(4).astype(np.int32)
	image=cv2.imread(image_fname)
	if (not( W == image.shape[1] )) or (not(H == image.shape[0])):
		image=cv2.resize(image,(W,H),interpolation=cv2.INTER_CUBIC)

        data_file=open(output_fname,'w')
        data_file.write(header.tobytes()+image.flatten().tobytes())
        data_file.close()

def performConversion(input_dir,output_dir,W,H):
	assert os.path.isdir(input_dir), 'Input directory does not exist. '+input_dir
	assert os.path.isdir(output_dir), 'Output directory does not exist. '+output_dir

	for file_name in sorted(glob.glob(input_dir+'*.png')):
		convertImageToBinaryFile(file_name,output_dir+os.path.splitext(os.path.basename(file_name))[0]+'.bin',W,H)

def obtainArguments():
	parser = argparse.ArgumentParser(description='Create binary images.')
	parser.add_argument('input_directory', metavar='input_directory', type=str, help='path to input directory')
	parser.add_argument('output_directory', metavar='output_directory', type=str, help='path to output directory')
	parser.add_argument('W', metavar='W', type=int, help='desired width')
	parser.add_argument('H', metavar='H', type=int, help='desired height')
	args = parser.parse_args()
	return args

args = obtainArguments()
performConversion(args.input_directory,args.output_directory,args.W,args.H)
