import cv2
import numpy as np
import os
import sys
from utils import saveBinaryImage, loadBinaryImage,getExtendedMaxDataWithDelta,createRGBImageFromIDImage,getIDImageFromImageFile,readFileListsFromTextFile,listExistingFiles,findCommonIDList,convertStringToIntegerList,convertColorToID
from matplotlib import pyplot as plt
import argparse

def createPartialIDDistribution(id_file,id_range,void_color_id,L):
	result=np.full(id_file.shape,void_color_id,dtype=np.int32)
	dist_result=np.zeros((result.shape[0],result.shape[1],L),dtype=np.float32)
	dist_result[:,:,L-1]=1.0
	assert(len(id_range)==L-1),"wrong id_range length"
	for index in range(len(id_range)):
		id=id_range[index]
		mask=(id_file[:,:]==id)
		result[mask]=id
		dist_result[mask,L-1]=0.0
		dist_result[mask,index]=1.0
	return result,dist_result

def createBinaryClassifierFile(id_range,classifier_image_file_name,classifier_binary_file_name,classifier_files,classifier_id_list,L,void_color_id):
	if not (classifier_image_file_name in classifier_files):
		return
       	classifier_file_index = classifier_files.index(classifier_image_file_name)
	assert( not(void_color_id) in id_range),"Can not have void color as a part of original labels " +str(void_color_id)
        classifier_filtered,distribution=createPartialIDDistribution(classifier_id_list[classifier_file_index],id_range,void_color_id,L)
        saveBinaryImage(classifier_binary_file_name,distribution)

def accumulatePropagationResult(id_range,classifier_files,file_info,final_result_ids,width,height,L,void_color_id):
        if(os.path.splitext(file_info[1])[0]+'.png' in classifier_files):
        	os.system('rm '+file_info[1])
	result_file=file_info[2]
	assert os.path.isfile(result_file), 'Result file does not exist! '+result_file
        result_distribution=loadBinaryImage(result_file,width,height,L)
        max_ids=getExtendedMaxDataWithDelta(result_distribution,L,0.0001)
	for index in range(len(id_range)):
        	mask_predicted = (max_ids[:,:]==index)
                mask_unlabelled = (final_result_ids[:,:]==-1)
                mask_labelled = (final_result_ids[:,:]!=-1)
                final_result_ids[mask_predicted & mask_unlabelled] = id_range[index]
                final_result_ids[mask_predicted & mask_labelled] = void_color_id
        os.system('rm '+result_file)

def savePropagationResult(result_file,final_result_ids,void_color_id):
        final_result_ids[final_result_ids[:,:]==-1] = void_color_id
        final_result = createRGBImageFromIDImage(final_result_ids)
        cv2.imwrite(os.path.dirname(result_file)+'/'+os.path.basename(result_file).split('.')[0]+'.png',final_result)

def performPartialPropagation(args,id_range,file_list_info,classifier_files,classifier_id_list,final_result_ids_list,void_color_id):
	L_partial = len(id_range)+1
        [createBinaryClassifierFile(id_range,os.path.splitext(finfo[1])[0]+'.png',finfo[1],classifier_files,classifier_id_list,L_partial,void_color_id) for finfo in file_list_info]
	print('Launching propagation in GPU for file: '+args.information_file)
        os.system(args.propagation_executable+ " " +args.information_file+ " "+ str(args.gpu_id)+" "+"1"+" "+str(L_partial) +" " + str(args.width)+" " +str(args.height))
	print('Finished propagation in GPU')
        [accumulatePropagationResult(id_range,classifier_files,file_list_info[index],final_result_ids_list[index],args.width,args.height,L_partial,void_color_id) for index in range(len(file_list_info))]

def performPropagation(args):
	void_color_id = convertColorToID( convertStringToIntegerList(args.void_color,3))
	file_list_info=readFileListsFromTextFile(args.information_file)

	classifier_files=listExistingFiles([os.path.splitext(item[1])[0]+'.png' for item in file_list_info])
	classifier_id_list=[getIDImageFromImageFile(file) for file in classifier_files]
	id_list=findCommonIDList(classifier_id_list)
	final_result_ids_list=[np.full((args.height,args.width),-1,dtype=np.int32) for i in range(len(file_list_info))]

	label_id=0
	while(label_id<len(id_list)):
		performPartialPropagation(args,id_list[label_id:(label_id+args.L_max)],file_list_info,classifier_files,classifier_id_list,final_result_ids_list,void_color_id)
	        label_id=label_id+args.L_max
	print('Storing propagation results')
	[savePropagationResult(file_list_info[file_index][2], final_result_ids_list[file_index], void_color_id) for file_index in range(len(file_list_info))]
def loadArguments():
	parser=argparse.ArgumentParser(description='Propagation parser')
	parser.add_argument('propagation_executable', metavar='propagation_executable', type=str, help='propagation executable')
	parser.add_argument('information_file', metavar='information_file', type=str, help='information file')
	parser.add_argument('gpu_id', metavar='gpu_id', type=int, help='gpu id')
	parser.add_argument('void_color', metavar='void_color', type=str, help='void color')
	parser.add_argument('L_max', metavar='L_max', type=int, help='maximum number of classes for a single partial propagation')
	parser.add_argument('width', metavar='width', type=int, help='image width')
	parser.add_argument('height', metavar='height', type=int, help='image height')
	args = parser.parse_args()

	assert os.path.isfile(args.propagation_executable), 'Propagation executable does not exist. ' + args.propagation_executable

	return args


performPropagation(loadArguments())
