import os
import argparse
from experiment import Experiment

class ExperimentBinaryImages(Experiment):
	def prepareExperimentData(self):
		os.system('mkdir '+self.config_info["output_directory_info"]["project_dir"])
		os.system('mkdir '+self.config_info["output_directory_info"]["binary_images_dir"])
	def prepareExperimentState(self):
		os.system('cp '+self.args.config_file_name+' ' +self.config_info["output_directory_info"]["project_dir"]+'config_create_images.json')
	def executeExperiment(self):
		os.system('python '+self.config_info["code_info"]['script_create_binary_images']+' '+self.config_info['input_directory_info']['image_dir']+' '+self.config_info['output_directory_info']['binary_images_dir'] + ' '+str(self.config_info['algorithm_info']['width'])+ ' '+str(self.config_info['algorithm_info']['height']))

if __name__ == "__main__":
	ExperimentBinaryImages("Create binary images.").run()
