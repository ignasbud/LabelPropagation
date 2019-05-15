import os
import glob
import argparse
from shutil import copyfile
from experiment import Experiment
import numpy as np
import cv2
from utils import convertImageToBinaryFile

class ExperimentBinaryImages(Experiment):
	def prepareExperimentData(self):
		if not os.path.isdir(self.config_info["output_directory_info"]["project_dir"]):
			os.mkdir(self.config_info["output_directory_info"]["project_dir"])
		if not os.path.isdir(self.config_info["output_directory_info"]["binary_images_dir"]):
			os.mkdir(self.config_info["output_directory_info"]["binary_images_dir"])
	def prepareExperimentState(self):
		copyfile(self.args.config_file_name, self.config_info["output_directory_info"]["project_dir"]+'config_create_images.json')

	def executeExperiment(self):
		print('Creating binary images in folder: '+self.config_info['output_directory_info']['binary_images_dir'])
		[convertImageToBinaryFile(file_name,self.config_info['output_directory_info']['binary_images_dir']+os.path.splitext(os.path.basename(file_name))[0]+'.bin',self.config_info['algorithm_info']['width'],self.config_info['algorithm_info']['height']) for file_name in sorted(glob.glob(self.config_info['input_directory_info']['images_dir']+'*.png'))]
		#Parallel(n_jobs=multiprocessing.cpu_count())(delayed(saveCombinedLabelFiles)(file_name+'_LAB.png',[file_name+'_O.png',file_name+'_OR.png'],self.config_info['algorithm_info']['width'],self.config_info['algorithm_info']['height'],self.config_info['algorithm_info']['propagation_void_color'])

if __name__ == "__main__":
	ExperimentBinaryImages("Create binary images.").run()
