import os
from pathlib import Path
from deepdiff import DeepDiff
import json
import argparse
import tempfile
import shutil


#print(json.__version__)
#print(argparse.__version__)
def print_dict(dictionary):
   print(json.dumps(dictionary, indent = 4, sort_keys=True, ensure_ascii=False))

def argument_parser():
   parser = argparse.ArgumentParser()
   parser.add_argument('--cif', help='cif file path')
   parser.add_argument('-c', '--config', help='path containing the (default)config file or the corresponding dictionary')
   parser.add_argument('-c_extra', '--config_extra', help='accepts dictionary with fields to substitute in the default config')
   parser.add_argument('-o', '--outdir', help='the output directory path')
   parser.add_argument('-fc', '--files-to-copy', help='comma-separated pattern list of files to be copied from the temporary directory')
   args, unknown_args = parser.parse_known_args()
   return args, unknown_args


class Config:

   def clean_config_keys(self, old_dict):
      """
         Replace underscores in key names with spaces
      """
      new_dict = {}
      for key in old_dict.keys():
          new_key = key.replace('_', ' ')
          if isinstance(old_dict[key], dict):
              new_dict[new_key] = self.clean_config_keys(old_dict[key])
          else:
              new_dict[new_key] = old_dict[key]

      return  new_dict

   def __init__(self, config=None):

      if config is None:
           config = Path( __file__ ).parent.absolute()
           with open(config / 'default_config.json') as f: self.config = json.load(f)
      elif (isinstance(config, dict)):
           self.config = config
      elif (isinstance(config, str) and config[0]=="{" and config[-1]=="}"):
           self.config = json.loads(config)
      else:
           with open(config) as f: self.config = json.load(f)

      self.config = self.clean_config_keys(self.config.copy())

   def update_config(self, config_extra):
      """
         recursive update dictionary entries in the config
      """

      config_check = self.config.copy()
      self.config.update(config_extra)

      ddiff = DeepDiff(config_check, self.config, ignore_order=True)
      if 'dictionary_item_added' in ddiff:
         print(ddiff)
         raise ValueError("""the input config_extra resulted in the data structure change in the config dictionary, which is unsafe.
Please, provide a new default config file via --config flag""")

      self.config = self.clean_config_keys(self.config.copy())
    

def run_cltem(cif, setup, outdir, files_to_copy, other_args_string):
  
   # create temporary directory
   tmp = tempfile.mkdtemp()

   # dump the config into a temporary json file
   tmpconf = tmp + "/config.json"
   with open(tmpconf, 'w') as cfg: json.dump(setup.config, cfg, indent = 4, sort_keys=True, ensure_ascii=True)

   # create the output directories
   tmpout = '{}/{}'.format(tmp, 'outdir'); os.mkdir(tmpout); os.makedirs(outdir, exist_ok=True)

   command = 'clTEM_cmd {} -c {} -o {} {}'.format(cif, tmpconf, tmpout, other_args_string)
   print('command passed to clTEM:\n "{}"'.format(command))

   postproc_command = ' && '.join(['cp {}/{} {} 2>/dev/null'.format(tmpout, fil, outdir) for fil in files_to_copy.split(',')])
   print('postprocessing command:\n "{}"'.format(postproc_command))

   print("\n... Launching clTEM ...\n")
   os.system(command)

   # postprocessing 
   os.system(postproc_command)
   
   # delete tmp directory
   shutil.rmtree(tmp)


def run_pyiface(cif=None, config=None, config_extra=None, outdir='outdir', files_to_copy='*.tif,*.png', other_args_string='-d gpu -s 2,2,2 -z 0,0,1'):
   
   print("\n... Entered run_pyiface() ...\n")

   # init the Config class object
   setup = Config(config=config)

   # update the configuration if extra dictionary is given
   if (config_extra): setup.update_config(config_extra)

   # run clTEM code and copy the resulting data
   run_cltem(cif, setup, outdir, files_to_copy, other_args_string)

   return

def run_batch(cif=None, config=None, config_extra=None, outdir='outdir', files_to_copy='*.tif,*.png', other_args_string='-d gpu -s 2,2,2 -z 0,0,1'):
   
   print("\n... Entered run_batch() ...\n")

   # init the Config class object
   setup = Config()

   # parse the command-line arguments
   args, unknown_args = argument_parser()
  
   print("The following arguments have been provided:")
   for arg in vars(args):

       # value of a command-line argument
       val = getattr(args, arg)

       # print out the command line arguments and values
       if (val): print('  {:>20}: {}'.format(arg, val))

       # re-init the config class with a new default configuration
       if (arg=='config' and val): setup = Config(config=val)
 
       # update the configuration if the extra flag is given
       if (arg=='config_extra'and val): 
         cleaned_extra_config = setup.clean_config_keys(json.loads(val))
         setup.update_config(cleaned_extra_config)

       # change the output directory
       if (arg=='outdir' and val): outdir = val

       # change the output directory
       if (arg=='files_to_copy' and val): files_to_copy = val
   
   cif = args.cif
   other_args_string = ' '.join(unknown_args)

   # run clTEM code and copy the resulting data
   run_cltem(cif, setup, outdir, files_to_copy, other_args_string)

   return

if __name__ == "__main__":
    run_batch()
