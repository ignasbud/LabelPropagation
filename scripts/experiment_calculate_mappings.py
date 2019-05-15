import argparse
from shutil import copyfile
import os
import glob
import datetime
from experiment import Experiment

class ExperimentCalculateMappings(Experiment):

	def appendArguments(self):

		super(ExperimentCalculateMappings,self).appendArguments()

		self.parser.add_argument('gpu_id', metavar='gpu_id', type=int, help='gpu id')
		self.parser.add_argument('--modulus', type=int, default=1, help='modulus of file to process')
		self.parser.add_argument('--remainder', type=int, default=0, help='remainder of file to process')

        def prepareExperimentData(self):

		if not os.path.isdir(self.config_info["output_directory_info"]["project_dir"]):
	                os.mkdir(self.config_info["output_directory_info"]["project_dir"])

		if not os.path.isdir(self.config_info["output_directory_info"]["mappings_dir"]):
	                os.mkdir(self.config_info["output_directory_info"]["mappings_dir"])

        def prepareExperimentState(self):

		copyfile(self.args.config_file_name,self.config_info["output_directory_info"]["project_dir"]+'config_calculate_mappings.json')

	def construct_line(self,mapping_fname,source_fname,destination_fname):

	        assert os.path.isfile(source_fname)
	        assert os.path.isfile(destination_fname)
	        assert os.stat(source_fname).st_size ==os.stat(destination_fname).st_size
		assert os.stat(source_fname).st_size == self.config_info['algorithm_info']['width']*self.config_info['algorithm_info']['height']*3, 'Wrong file sizes! '+str(os.stat(source_fname))+ ' '+str(os.stat(destination_fname))+' ' +str(self.config_info['algorithm_info']['width'])+ ' '+str(self.config_info['algorithm_info']['height'])

	        return self.config_info['code_info']['exec_mappings']+" "+str(self.args.gpu_id)+" "+str(self.config_info['algorithm_info']['width'])+" "+str(self.config_info['algorithm_info']['height'])+ " " + str(self.config_info['algorithm_info']['half_patch_size']) + " " +source_fname+" "+destination_fname+" NONE "+mapping_fname

	def mappingsPerFile(self,file_id,file_list,file_id_neighbour,mapping_type):

		if not( file_id%self.args.modulus ==self.args.remainder):
                	return
		if(file_id_neighbour<0)and(file_id_neighbour>=len(file_list)):
			return

               	mapping_file_name=self.config_info['output_directory_info']['mappings_dir']+os.path.splitext(file_list[file_id])[0]+'_'+mapping_type+'.bin'
                print('Calculating mappings: '+mapping_file_name+', '+str(datetime.datetime.now()))

                if not os.path.isfile(mapping_file_name):
                        os.system(self.construct_line(mapping_file_name,self.config_info['output_directory_info']['binary_images_dir']+file_list[file_id],self.config_info['output_directory_info']['binary_images_dir']+file_list[file_id_neighbour]))
 		else:
                	print('Mappings already calculated: ' + mapping_file_name)

	def performMappings(self):

		file_list=[os.path.basename(fname) for fname in sorted(glob.glob(self.config_info['output_directory_info']['binary_images_dir']+'*.bin'))]
		[(self.mappingsPerFile(file_id,file_list,file_id+1,'O'),self.mappingsPerFile(file_id,file_list,file_id-1,'OR')) for file_id,file_name in enumerate(file_list)]

        def executeExperiment(self):

		self.performMappings()


if __name__ == "__main__":

        ExperimentCalculateMappings("Calculate mappings.").run()
