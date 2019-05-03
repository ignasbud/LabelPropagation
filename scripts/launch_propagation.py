import sys
import os
from label_file_visualisation import LabelFileVisualisation
import numpy as np
from joblib import Parallel, delayed
import multiprocessing
import glob
def createLine(dir_info,map_type,canonical_mapping_file_name,canonical_file_name):
	#print ('canonical '+str(canonical_file_name))	
	#result_line=dir_info['mapping']+canonical_mapping_file_name+'_'+map_type+'.bix'+ " " +dir_info['label_marking']+canonical_file_name+".bin"+" " +dir_info['output']+canonical_file_name+"_"+map_type+"_LAB.bix"
	result_line=dir_info['mapping']+canonical_mapping_file_name+'_'+map_type+'.bin'+ " " +dir_info['label_marking']+canonical_file_name+".bin"+" " +dir_info['output']+canonical_file_name+"_"+map_type+".bin"
	#print result_line
	return result_line

def save_text(file_name,text):
        text_file = open(file_name, "w")
        text_file.write(text)
        text_file.close()
def combine_files(file_name,width,height):
	#file_name_OR=file_name.split('_O_LAB.bix')[0].split('_OR_LAB.bix')[0]+"_OR_LAB.bix"
        file_name_OR=file_name.split('_O.')[0].split('_OR.')[0]+"_OR.bin"
        #file_name_output=file_name.split('_O_LAB.bix')[0].split('_OR_LAB.bix')[0]+"_LAB.bix"
	file_name_output=file_name.split('_O.')[0].split('_OR.')[0]+"_LAB.bin"

        #print("checking combination " +file_name + " and " +file_name_OR+"\n\n\n\n")
        if (os.path.isfile(os.path.splitext(file_name)[0]+'.png'))and(os.path.isfile(os.path.splitext(file_name_OR)[0]+'.png')):
		LabelFileVisualisation.produce_combined_visual_file([os.path.splitext(file_name)[0]+'.png',os.path.splitext(file_name_OR)[0]+'.png'],os.path.splitext(file_name_output)[0]+'.png',width,height,(255,255,255))
	else:
		print('COUND NOT FIND '+file_name)
		#print('loooking '+os.path.splitext(file_name)[0]+'.png') + ' and '+ os.path.splitext(file_name_OR)[0]+'.png'
		#pass
 		#LabelFileVisualisation.produce_combined_file([file_name,file_name_OR],file_name_output,width,height,L,LabelFileVisualisation.COLOR_CAMVID_ORIGINAL)
		#os.system("rm "+file_name)
		#os.system("rm "+file_name_OR)
		#os.system("rm "+file_name_output)

exec_propagation=sys.argv[1]
gpu_id=sys.argv[2]
target=sys.argv[3]
width=(int)(sys.argv[4])
height=(int)(sys.argv[5])
maxL= (int)(sys.argv[6])
distance=(int)(sys.argv[7])
#print('distance = '+str(distance))
#exit(1)
offset=distance-1

#print ("L = "+str(L))
full_label_file_name=sys.argv[8]
#print('Full label file name '+str(full_label_file_name))
#exit(1)
dir_info={'label_marking':sys.argv[9],'mapping':sys.argv[10],'output':sys.argv[11],'images':sys.argv[12]}
for key in dir_info.keys():
	assert os.path.isdir(dir_info[key]), 'Directory does not exist: '+str(dir_info[key])
#print('full label file name '+full_label_file_name)
base_image_file_name=os.path.basename(full_label_file_name)
#print('base image file name '+base_image_file_name)
file_list=sorted([os.path.basename(fname) for fname in glob.glob(dir_info['images']+'*.bin')],reverse=False)
#file_list=[base_image_file_name]
#print('file list: '+str(file_list))
#exit(1)
#print("File list length = "+str(len(file_list)))
#print("-------------------------")
print("Looking for "+base_image_file_name)
for fid, full_file_name in enumerate(file_list):
	file_name =os.path.basename(full_file_name)
	print("FILE = "+file_name)
	#break
	#print('fid = '+str(fid))
	#exit(1)
	if(file_name==base_image_file_name):
		#print("Found "+file_name)
		#exit(1)
		file_lists={'O':[],'OR':[]}
	        for map_type in ['O','OR']:
	                result=''
	                if(map_type=='OR'):
	                        for count in range(0,distance*2+1):
					new_fid=fid-(distance-count-1)+offset
					new_tk_fid=new_fid+0
					#print("new fid = "+str(new_fid))
					if(new_fid>=0)and(new_fid<len(file_list))and(new_tk_fid>=0)and(new_tk_fid<len(file_list)):
						line =createLine(dir_info,'O',file_list[new_tk_fid].split(".")[0],file_list[new_fid].split(".")[0])
		                                result=result+line+'\n'
						file_lists[map_type].append(line.split(" ")[2].split('\n')[0])
	                else:
	                        for count in range(0,distance*2+1):
					new_fid=fid-(distance-count-1)+offset
					new_tk_fid=new_fid+0
					if(new_fid>=0)and(new_fid<len(file_list))and(new_tk_fid>=0)and(new_tk_fid<len(file_list)):
						line=createLine(dir_info,'OR',file_list[new_tk_fid].split(".")[0],file_list[new_fid].split(".")[0])
		                                result=line+'\n'+result
						file_lists[map_type].append(line.split(" ")[2].split('\n')[0])

			list_file_name=dir_info['output']+'/propagation_info_'+str(distance)+'_'+file_name.split('.')[0]+'_'+map_type+'.txt'
			#print list_file_name
        	        save_text(list_file_name,result)
			assert os.path.isfile(list_file_name), 'File does not exist. '+list_file_name
			#exit(1)
			os.system("python "+target+ " " +exec_propagation+ " " +list_file_name+ " "+ str(gpu_id)+" "+"1"+" "+str(maxL) +" " + str(width)+" " +str(height))
		
			#exit(1)
			#break
		#Parallel(n_jobs=multiprocessing.cpu_count())(delayed(combine_files)(file_name,width,height,L) for file_name in file_lists['OR'])
		for file_name in file_lists['OR']:
			print('combining '+file_name)
			combine_files(file_name,width,height)
        	break
print("Finished")
