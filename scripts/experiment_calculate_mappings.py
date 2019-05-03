import argparse
import os
from experiment import Experiment

class ExperimentCalculateMappings(Experiment):
	def appendArguments(self):
		super(ExperimentCalculateMappings,self).appendArguments()
		self.parser.add_argument('gpu_id', metavar='gpu_id', type=int, help='gpu id')
		self.parser.add_argument('--modulus', type=int, default=1, help='modulus of file to process')
		self.parser.add_argument('--remainder', type=int, default=0, help='remainder of file to process')
        def prepareExperimentData(self):
                os.system('mkdir '+self.config_info["output_directory_info"]["project_dir"])
                os.system('mkdir '+self.config_info["output_directory_info"]["mappings_dir"])
        def prepareExperimentState(self):
		os.system('cp '+self.args.config_file_name+' ' +self.config_info["output_directory_info"]["project_dir"]+'config_calculate_mappings.json')
        def executeExperiment(self):
		os.system('python '+self.config_info['code_info']['script_create_mappings']+' '+
                        str(self.args.gpu_id)+ ' '+
                        self.config_info['code_info']['exec_mapping']+' '+
                        self.config_info['output_directory_info']['binary_images_dir']+  ' ' +
                        self.config_info['output_directory_info']['mappings_dir']+ ' '+
                        str(self.config_info['algorithm_info']['patch_size'])+ ' '+
                        str(self.config_info['algorithm_info']['width'])+ ' '+
                        str(self.config_info['algorithm_info']['height'])+' '+
                        str(self.args.modulus)+ ' '+
                        str(self.args.remainder))

if __name__ == "__main__":
        ExperimentCalculateMappings("Calculate mappings.").run()
