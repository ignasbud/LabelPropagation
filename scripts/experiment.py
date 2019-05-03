import os
import json
import argparse

class Experiment(object):
	def __init__(self,experiment_name):
		self.experiment_name = experiment_name
		self.parser=argparse.ArgumentParser(description='Parser: '+self.experiment_name)
		self.appendArguments()
		self.obtainArguments()
		self.loadConfig()
	def appendArguments(self):
		self.parser.add_argument('config_file_name', metavar='config_file_name', type=str, help='path to config file')
	def obtainArguments(self):
                self.args = self.parser.parse_args()
	def loadConfig(self):
		assert os.path.isfile(self.args.config_file_name), 'Config file does not exist! '+self.args.config_file_name
	        with open(self.args.config_file_name, 'r') as f:
	                self.config_info = json.load(f)
	def prepareExperimentData(self):
		pass
	def prepareExperimentState(self):
		pass
	def executeExperiment(self):
		pass
	def run(self):
		self.prepareExperimentData()
		self.prepareExperimentState()
		self.executeExperiment()
