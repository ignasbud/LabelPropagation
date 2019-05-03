from scipy import misc
import sys
import os
import glob
def construct_line(cuda_id,target,map_fname,s_fname,d_fname,D,width,height):
	HEADER_SIZE=16
	assert os.path.isfile(s_fname)
	assert os.path.isfile(d_fname)
	assert os.stat(s_fname).st_size ==os.stat(d_fname).st_size and os.stat(s_fname).st_size == int(width)*int(height)*3+HEADER_SIZE, 'Wrong file sizes! '+str(os.stat(s_fname))+ ' '+str(os.stat(d_fname))+' ' +str(width)+ ' '+str(height)
	result=target+" "+cuda_id+" "+width+" "+height+ " " + D + " " +s_fname+" "+d_fname+" NONE "+map_fname
	return result

cuda_device_id=sys.argv[1]
mapping_file_location=sys.argv[2]
input_directory_name=sys.argv[3]
output_directory_name=sys.argv[4]
D = sys.argv[5]
width=sys.argv[6]
height=sys.argv[7]
modulus_N=int(sys.argv[8])
modulus_rem = int(sys.argv[9])
fname_split='.bin'
file_list=[fname.split('/')[-1] for fname in sorted(glob.glob(input_directory_name+'*.bin'))]
print('FILE LIST: '+str(file_list))
print('modulus_N = '+str(modulus_N))
print('modulus_rem = '+str(modulus_rem))
assert os.path.isdir(output_directory_name), "Output directory does not exist! "+output_directory_name
assert os.path.isdir(input_directory_name), "Input directory does not exist! " +input_directory_name
for list_id,file_name in enumerate(file_list):
	if not( list_id%modulus_N ==modulus_rem):
		continue
        #mapping_file_name_O=file_name.split('.')[0]+'_O.bix'
	#mapping_file_name_OR=file_name.split('.')[0]+'_OR.bix'
	if(list_id<len(file_list)-1):
		mapping_file_name_O=file_name.split(fname_split)[0]+'_O.bin' #_'+file_list[list_id+1].split(fname_split)[0]+'.bix'
		if not os.path.isfile(output_directory_name+mapping_file_name_O):
			elineO=construct_line(cuda_device_id,mapping_file_location,output_directory_name+mapping_file_name_O,input_directory_name+file_name,input_directory_name+file_list[list_id+1],D,width,height)
			os.system(elineO)
		else:
			print('Have it1: ' + output_directory_name+mapping_file_name_O)
	if(list_id>0):
		mapping_file_name_OR=file_name.split(fname_split)[0]+'_OR.bin' #'+file_list[list_id-1].split(fname_split)[0]+'.bix' 
		if (not(os.path.isfile(output_directory_name+mapping_file_name_OR))):
			elineOR=construct_line(cuda_device_id,mapping_file_location,output_directory_name+mapping_file_name_OR,input_directory_name+file_name,input_directory_name+file_list[list_id-1],D,width,height)
		        os.system(elineOR)
		else:
			print('Have it2: '+output_directory_name+mapping_file_name_OR)




