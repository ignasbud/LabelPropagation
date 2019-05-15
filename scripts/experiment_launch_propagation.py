import argparse
import json
import os
import glob
import cv2

from experiment import Experiment
from utils import saveCombinedLabelFiles,saveTextFile
from joblib import Parallel, delayed
import multiprocessing 

class ExperimentLaunchPropagation(Experiment):
        def appendArguments(self):
                super(ExperimentLaunchPropagation,self).appendArguments()
                self.parser.add_argument('gpu_id', metavar='gpu_id', type=int, help='gpu id')
		self.parser.add_argument('seed_file_name',metavar='seed_file_name',type=str,help='full path to the file from which a propagation should be launched')
	def copyClassifierFiles(self):
		for fname in sorted(glob.glob(self.config_info['input_directory_info']['classifier_dir']+'*.png')):
	        	new_fname=self.config_info['output_directory_info']['classifier_dir']+os.path.basename(fname)
        		cv2.imwrite(new_fname,cv2.resize(cv2.imread(fname),(self.config_info['algorithm_info']['width'],self.config_info['algorithm_info']['height']),interpolation=cv2.INTER_NEAREST))
        def prepareExperimentData(self):
		if not os.path.isdir(self.config_info["output_directory_info"]["classifier_dir"]):
			os.system('mkdir '+self.config_info["output_directory_info"]["classifier_dir"])
		assert os.path.isdir(self.config_info['output_directory_info']['classifier_dir']), 'Classifier directory does not exist! '+self.config_info['output_directory_info']['classifier_dir']
		self.copyClassifierFiles()
		if not os.path.isdir(self.config_info['output_directory_info']['propagation_output_dir']):
			os.system('mkdir '+self.config_info['output_directory_info']['propagation_output_dir'])
        def prepareExperimentState(self):
                os.system('cp '+self.args.config_file_name+' ' +self.config_info["output_directory_info"]["project_dir"]+'config_calculate_mappings.json')

	def createLine(self,map_type,canonical_mapping_file_name,canonical_file_name):
        	return  self.config_info["output_directory_info"]["mappings_dir"]+canonical_mapping_file_name+'_'+map_type+'.bin'+ " " + self.config_info["output_directory_info"]["classifier_dir"]+canonical_file_name+".bin"+" " + self.config_info["output_directory_info"]["propagation_output_dir"]+canonical_file_name+"_"+map_type+".bin"+"\n"

	def createPropagationInformationFile(self,file_id,map_type,file_list):
	        result=''
	        file_lists = []
                for count in range(0,self.config_info['algorithm_info']['propagation_half_distance']*2+1):
	                        new_fid=file_id-(self.config_info['algorithm_info']['propagation_half_distance']-count-1)+ self.config_info['algorithm_info']['propagation_half_distance']-1
	                        if (not (new_fid>=0))or (not(new_fid<len(file_list))):
					continue
				if(map_type=='O'):
	                                result= result + self.createLine('O',os.path.splitext(file_list[new_fid])[0],os.path.splitext(file_list[new_fid])[0])
				elif(map_type=='OR'):
					result = self.createLine('OR',os.path.splitext(file_list[new_fid])[0],os.path.splitext(file_list[new_fid])[0])+result
				else:
					assert False, "Invalid map_type: "+str(map_type)
				file_lists.append(self.config_info["output_directory_info"]["propagation_output_dir"]+os.path.splitext(file_list[new_fid])[0])

	        list_file_name=self.config_info['output_directory_info']["propagation_output_dir"]+'propagation_info_'+str(self.config_info['algorithm_info']['propagation_half_distance'])+'_'+file_list[file_id].split('.')[0]+'_'+map_type+'.txt'
	        saveTextFile(list_file_name,result)
        	return list_file_name, file_lists
	def performPropagation(self,file_id,map_type,file_list):
	        list_file_name, file_lists = self.createPropagationInformationFile(file_id,map_type,file_list)
	        assert os.path.isfile(list_file_name), 'File does not exist. '+list_file_name
	        os.system("python "+self.config_info['code_info']['script_propagate_one_side']+ " " +
				    self.config_info['code_info']['exec_propagation']+ " " +
				    list_file_name+ " "+ str(self.args.gpu_id)+" "+
				    str(self.config_info['algorithm_info']['propagation_void_color']).replace(' ','')+" "+
				    str(self.config_info['algorithm_info']['max_classes']) +" " +
				    str(self.config_info['algorithm_info']['width'])+" " +
				    str(self.config_info['algorithm_info']['height']))
	        return file_lists

        def executeExperiment(self):
		print('Starting propagation experiment')
		image_file_list=sorted([os.path.basename(fname) for fname in glob.glob(self.config_info['output_directory_info']['binary_images_dir']+'*.bin')],reverse=False)
		fid = image_file_list.index(os.path.basename(self.args.seed_file_name))
		assert (fid>=0), "Binary image not found. "+ os.path.basename(self.args.seed_file_name)
                propagation_result_info=[self.performPropagation(fid,map_type,image_file_list) for map_type in ['O','OR']]
                Parallel(n_jobs=multiprocessing.cpu_count())(delayed(saveCombinedLabelFiles)(file_name+'_LAB.png',[file_name+'_O.png',file_name+'_OR.png'],self.config_info['algorithm_info']['width'],self.config_info['algorithm_info']['height'],self.config_info['algorithm_info']['propagation_void_color']) for file_name in propagation_result_info[0])

if __name__ == "__main__":
        ExperimentLaunchPropagation("Launch propagation.").run()
