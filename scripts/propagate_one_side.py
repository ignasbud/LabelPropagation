import cv2
import numpy as np
import os
import sys
from label_file_visualisation import LabelFileVisualisation
from matplotlib import pyplot as plt
def get_file_lists(file_name):
	f=open(file_name,'r')
	data=f.read()
	f.close()
	lines=data.split('\n')
	result=[]
	for line in lines:
		if(len(line)>0):
			file_names = line.split(' ')
			assert(len(file_names)==3), str(file_names)
			result.append(file_names)
	return result

def get_classifier_file_name(file_info):
	assert (file_info[1].endswith('.bin'))
	return file_info[1].split('.bin')[0]+'.png'
	
def existing_classifier_files(file_list):
	result=[]
	for local in file_list:
		#print('local 1 = '+str(local[1]))
		classifier_image= get_classifier_file_name(local)
		#print('classifier image '+str(classifier_image))
		if(os.path.isfile(classifier_image)):
			result.append(classifier_image)
	#print('result = '+str(result))
	return result

def get_classifier_ids(classifier_files):
	result=[]
	for file in classifier_files:    
		#print('file '+str(file))
		#exit(1)
                file_id_array=get_file_id_array(file)
		result.append(file_id_array)
	return result


def get_file_id_array(file):
	#print('image file '+str(file))
	assert os.path.isfile(file), 'File does not exist: '+file
	image=cv2.imread(file)
	#plt.imshow(image)
	#plt.show()
	assert not(image is None)
	assert(image.shape[0]==height),"Wrong height: expected - "+str(height)+ ' received ' +str(image.shape[0])
	assert(image.shape[1]==width),"Wrong width: expected - " +str(width)+ ' received '+str(image.shape[1])
	result=np.zeros((height,width),dtype=np.int32)
	result=image[:,:,0].astype(np.int32)*256*256+image[:,:,1].astype(np.int32)*256+image[:,:,2].astype(np.int32)
	#print(str(image))
	#print('result type  ' +str(result.dtype))
	return result

def get_file_id_set(id_array):
	return set(id_array.flatten())

def find_common_ids_list(classifier_id_array):
	#assert(len(classifier_id_array)==2),"Wrong length of classifier file list"
	result_id_set = set([])
	for id_array in classifier_id_array:
		file_id_set=get_file_id_set(id_array)
		print('Unique ids for file ' +str(len(file_id_set)))
		result_id_set=result_id_set | file_id_set
	#print('Unique ids total :'+str(len(result_id_set)))
	return sorted(list(result_id_set))
def filter_ids(id_file,id_range,fill_value,new_L):
	result=np.full((height,width),fill_value,dtype=np.int32)
	dist_result=np.zeros((height,width,new_L),dtype=np.float32)
	dist_result[:,:,new_L-1]=1.0
	assert(len(id_range)==new_L-1),"wrong id_range length"
	for index in range(len(id_range)):
		id=id_range[index]
		mask=(id_file[:,:]==id)
		result[mask]=id
		dist_result[mask,new_L-1]=0.0
		dist_result[mask,index]=1.0
	return result,dist_result
	#return id_file,dist_result
def from_array_ids_to_rgb(ids_array):
	#print('ids array type ' +str(ids_array.dtype))
	#print('ids_array shape '+str(ids_array.shape))
	result=np.zeros((ids_array.shape[0],ids_array.shape[1],3)).astype(np.uint8)
	#print('result array shape '+str(result.shape))
	result[:,:,0]=(ids_array[:,:]/(256*256))%256
        result[:,:,1]=(ids_array[:,:]/(256))%256
        result[:,:,2]=ids_array[:,:]%256
	return result
#os.system(target+ " " +list_file_name+ " "+ str(gpu_id)+" "+"1"+" "+str(L) +" " + str(width)+" " +str(height))

#maxL=21
#maxL=3
#print('maxL = '+str(maxL))
#target = '../bin/propagation/TitanX/TitanX_propagation_gpu_v8_max31'
list_file_name =sys.argv[2]
target=sys.argv[1]
gpu_id=sys.argv[3]
increment=sys.argv[4]
maxL=int(sys.argv[5])
width=int(sys.argv[6])
height=int(sys.argv[7])

print('label_file_name: '+list_file_name)
print('target '+str(target))
print('gpu id '+str(gpu_id))
print('increment ' +str(increment))
print('maxL ' +str(maxL))
print ('width ' +str(width))
print('height ' +str(height))
#exit(1)
assert os.path.isfile(target), 'Propagation executable does not exist. '+target

file_list=get_file_lists(list_file_name)
classifier_files=existing_classifier_files(file_list)
#print('classifier files '+str(classifier_files))
#exit(1)
classifier_id_list=get_classifier_ids(classifier_files)
#print('classifier id list '+str(classifier_id_list))
#print('classifier id set '+str(set(classifier_id_list[0].flatten().tolist())))
#exit(1)
id_list=find_common_ids_list(classifier_id_list)
total_labels=len(id_list)
#print('Common id_set' +str(id_list))
#print('Total labels = '+str(total_labels))
label_id=0
fill_color=255*256*256+255*256+255

final_result_ids_list=[]
final_result_list=[]
for i in range(len(file_list)):
	final_result_ids_list.append(np.full((height,width),-1,dtype=np.int32))

#print('file list: '+str(file_list))
#exit(1)
while(label_id<total_labels):
	#if(label_id>0):
	#	label_id+=maxL	
	#	continue
	id_range=id_list[label_id:(label_id+maxL)]
	new_L=len(id_range)+1
	#print('new L '+str(new_L))
	#print('id range = '+str(id_range))
	#print('labels = '+str(len(id_range)))
	
	for file_info in file_list:
		classifier_file_name = get_classifier_file_name(file_info)
		#print('classifier file name '+str(classifier_file_name))
		if(classifier_file_name in classifier_files):
			classifier_file_index = classifier_files.index(classifier_file_name)

			assert( not(fill_color) in id_range),"Can not have color " +str(fill_color)
			classifier_filtered,distribution=filter_ids(classifier_id_list[classifier_file_index],id_range,fill_color,new_L)
			#print('Filtered ids = '+ str(get_file_id_set(classifier_filtered)))
			LabelFileVisualisation.save_label_image(file_info[1],distribution)
			
			label_rgb = from_array_ids_to_rgb(classifier_filtered)
			#label_rgb = from_array_ids_to_rgb(classifier_id_list[classifier_file_index])

			#print('label rgb shape '+str(label_rgb.shape))
			image=cv2.imread(classifier_file_name)
			#print('image shape '+str(image.shape))
			diff =abs( image-label_rgb)
			#diff =abs( image-image)
	
			#print('diff shape '+str(diff.shape))
			sum_diff=sum(sum(sum(diff)))
			#print('sum diff '+str(sum_diff))
			#assert(sum_diff == 0), "unequal"
			#cv2.imwrite(classifier_file_name.split('.')[0]+'_id_'+str(label_id).zfill(3)+'.png',label_rgb.astype(np.uint8))
			#exit()
			

	os.system(target+ " " +list_file_name+ " "+ str(gpu_id)+" "+"1"+" "+str(new_L) +" " + str(width)+" " +str(height))
	#exit(1)
	#print('---------------Should be prop here, id = '+str(label_id)+ " of "+str(total_labels))
	#id=id+maxL
	#exit()
	#continue
	for file_index in range(len(file_list)):
		file_info = file_list[file_index]
		#continue
                classifier_file_name = get_classifier_file_name(file_info)
		#exit(1)
                if(classifier_file_name in classifier_files):
                        os.system('rm '+file_info[1])
			#pass
		result_file=file_info[2]
		result_distribution=LabelFileVisualisation.read_label_image(result_file,width,height,new_L)
		max_ids=LabelFileVisualisation.getExtendedMaxDataWithDelta(result_distribution,new_L,0.0001)	
		#print('max values ' +str(set(list(max_ids.flatten()))))	
		final_result_ids=final_result_ids_list[file_index]

		#print("final_result_ids shape " +str(final_result_ids.shape))
		#print(max_ids)
		for index in range(len(id_range)): #note that void is handled implicitly
			mask = (max_ids[:,:]==index) 
			#print('index = '+str(index)+' '+str(sum(sum(mask))))
			mask2= (final_result_ids[:,:]==-1)
			mask3 = (final_result_ids[:,:]!=-1)
#			print('mask shape ' +str(mask.shape))
#			print('mask2 shape ' +str(mask2.shape))
#			print('mask3 shape ' +str(mask3.shape))
			final_result_ids[mask & mask2]=id_range[index]
			final_result_ids[mask & mask3]=fill_color  #maybe smth different?
			#final_result_ids[mask]=id_range[index]
		#print('final result set '+str(get_file_id_set(final_result_ids)))
		
		os.system('rm '+result_file)
	#exit()
	label_id=label_id+maxL
#print('FINAL RESULT')
#print('File list '+str(file_list))
#exit(1)
for file_index in range(len(file_list)):
	file_info = file_list[file_index]
        result_file=file_info[2]
	#print('result file '+str(result_file))
	final_result_ids=final_result_ids_list[file_index]
	final_result_ids[final_result_ids[:,:]==-1]= fill_color

        final_result = from_array_ids_to_rgb(final_result_ids)
	result_file_png= os.path.dirname(result_file)+'/'+os.path.basename(result_file).split('.')[0]+'.png'
	#print('result file png ' +str(result_file_png))
        cv2.imwrite(result_file_png,final_result)
	
#print('finished')



