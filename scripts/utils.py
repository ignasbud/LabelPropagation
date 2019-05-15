import cv2
import numpy as np
import os

def convertStringToIntegerList(data,N):
	items = data.replace('[','').replace(']','').replace(' ','').split(',')
	assert len(items) == N, 'Wrong number of items in a list: '+str(data)+ ' Expected: '+str(N)
	return [int(item) for item in items]
def listExistingFiles(file_list):
        result=[]
        for fname in file_list:
                if(os.path.isfile(fname)): 
                        result.append(fname)
        return result

def saveTextFile(file_name,text):
        text_file = open(file_name, "w")
        text_file.write(text)
        text_file.close()
def readTextFileLines(file_name):
	f=open(file_name,'r')
        lines=f.readlines()
        f.close()   
	return lines

def readFileListsFromTextFile(file_name):
        lines= readTextFileLines(file_name)
        result=[ ]
        for line in lines:
		line = line.replace('\n','')
                if(len(line)>0):
                        items = line.split(' ')
                        result.append(items)
        return result

def findCommonIDList(id_array_list):
        result_set = set([])
        for id_array in id_array_list:
                id_set=set(id_array.flatten().tolist())
                result_set=result_set | id_set
        return sorted(list(result_set))

def createIDImage(image):
	return np.uint32(image[:,:,0])*256*256+np.uint32(image[:,:,1])*256+np.uint32(image[:,:,2])
def convertColorToID(color):
	return np.uint32(color[0])*256*256+np.uint32(color[1])*256+np.uint32(color[2])
def createRGBImageFromIDImage(id_image):
        result=np.zeros((id_image.shape[0],id_image.shape[1],3)).astype(np.uint8)
        result[:,:,0]=(id_image[:,:]/(256*256))%256
        result[:,:,1]=(id_image[:,:]/(256))%256
        result[:,:,2]=id_image[:,:]%256
        return result

def getIDImageFromImageFile(file):
        assert os.path.isfile(file), 'File does not exist: '+file
        image=cv2.imread(file)
        return createIDImage(image)

def getExtendedImageWithDelta(data,L,delta): 
	temp_data=np.zeros((data.shape[0],data.shape[1],data.shape[2]+1),dtype=np.float32)
        temp_data[:,:,0:L]=np.array(data,copy=True)
        temp_data[:,:,L]=(1.0/L)+delta
        return temp_data

def getExtendedMaxDataWithDelta(data,L,delta):
	return np.argmax(getExtendedImageWithDelta(data,L,delta), axis=2).astype(np.uint32)

def makeCombinedLabelImage(input_file_names,width,height,void_color):
	assert len(input_file_names)==2, 'Combined file should be made from 2 files!'
	for fname in input_file_names:
		assert os.path.isfile(fname), 'Label file does not exist! '+fname
	labels = [cv2.imread(fname) for fname in input_file_names]
	ids=[createIDImage(labels[i]) for i in range(len(labels))]
	difference_mask = (ids[0][:,:]!=ids[1][:,:])
	labels[0][difference_mask,:]=void_color
        return np.uint8(labels[0])

def saveCombinedLabelFiles(output_file_name,input_file_list,width,height,void_label):
	cv2.imwrite(output_file_name, makeCombinedLabelImage(input_file_list,width,height,void_label))

def saveBinaryImage(file_name,data):
	data.flatten().tofile(file_name)

def convertImageToBinaryFile(image_fname,output_fname,width,height,interpolation=cv2.INTER_CUBIC):
	#assert header_length % 4 == 0, 'Header length in bytes should be a multiple of 4'
        #header=np.zeros(header_length/4).astype(np.int32)
        image=cv2.imread(image_fname)
        if (not( width == image.shape[1] )) or (not(height == image.shape[0])):
		image=cv2.resize(image,(width,height),interpolation=interpolation)
	saveBinaryImage(output_fname,image)
	#data_file=open(output_fname,'w')
        #data_file.write(header.tobytes()+image.flatten().tobytes())
        #data_file.close()

def loadBinaryImage(file_name,width,height,L):
	return  np.reshape(np.fromfile(file_name, dtype=np.float32),(height,width,L))
