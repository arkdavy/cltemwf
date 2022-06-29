#!/bin/bash

# prerequisites: 
# (1) clTEM_cmd installed on the system
# (2) cltemwf code installed (e.g., with 'pip install .' from the project's root)
# (3) (cif)text files imported form Windows has to be converted with "tr -d '\r' < Si_win.cif > Si_lin.cif" command to fix the Windows-specific line endings

# Add clTEM_cmd into the environent if installed with the module system
module purge
module load GCC/10.2.0 CUDA/11.1.1 OpenMPI/4.0.5
module load Python/3.8.6
module load clTEM/0.3.4

# the whole config can be provided as a string of dictionary, as here, or via a path to a new config.
config='{"ctem": {"cropped padding": true}, "default padding": {"xy": {"units": "\u00c5", "val": 8.0}, "z": {"units": "\u00c5", "val": 3.0}}, "double precision": false, "filename": "None.cif", "full 3d": {"state": false}, "intermediate output": {"enabled": false, "slice interval": 0}, "maintain areas": false, "microscope": {"aberrations": {"C10": {"units": "nm", "val": 0.0}, "C12": {"ang": 0.0, "mag": 0.0, "units": "nm, \u00b0"}, "C21": {"ang": 0.0, "mag": 0.0, "units": "nm, \u00b0"}, "C23": {"ang": 0.0, "mag": 0.0, "units": "nm, \u00b0"}, "C30": {"units": "\u03bcm", "val": 1.0}, "C32": {"ang": 0.0, "mag": 0.0, "units": "\u03bcm, \u00b0"}, "C34": {"ang": 0.0, "mag": 0.0, "units": "\u03bcm, \u00b0"}, "C41": {"ang": 0.0, "mag": 0.0, "units": "\u03bcm, \u00b0"}, "C43": {"ang": 0.0, "mag": 0.0, "units": "\u03bcm, \u00b0"}, "C45": {"ang": 0.0, "mag": 0.0, "units": "\u03bcm, \u00b0"}, "C50": {"units": "\u03bcm", "val": 0.0}, "C52": {"ang": 0.0, "mag": 0.0, "units": "\u03bcm, \u00b0"}, "C54": {"ang": 0.0, "mag": 0.0, "units": "\u03bcm, \u00b0"}, "C56": {"ang": 0.0, "mag": 0.0, "units": "\u03bcm, \u00b0"}}, "aperture": {"units": "mrad", "val": 20.0}, "aperture smooth radius": {"units": "mrad", "val": 0.0}, "beam tilt": {"azimuth": {"units": "\u00b0", "val": 0.0}, "inclination": {"units": "mrad", "val": 0.0}}, "voltage": {"units": "kV", "val": 200.0}}, "mode": {"id": 2, "name": "STEM"}, "potentials": "kirkland", "resolution": 1024, "simulation area": {"x": {"finish": 10.0, "padding": 5.0, "start": 0.0, "units": "\u00c5"}, "y": {"finish": 10.0, "padding": 5.0, "start": 1.0, "units": "\u00c5"}, "z": {"finish": 10.0, "padding": 5.0, "start": 1.0, "units": "\u00c5"}}, "slice count": 10, "slice offset": {"units": "\u00c5", "val": 0.96}, "slice thickness": {"val": 1.92}, "stem": {"area": {"padding": {"units": "\u00c5", "val": 0.0}, "x": {"finish": 18.2799, "start": 10.6, "units": "\u00c5"}, "y": {"finish": 15.5305, "start": 10.1, "units": "\u00c5"}}, "concurrent pixels": 1, "detectors": {"ADF": {"centre": {"units": "mrad", "x": 0.0, "y": 0.0}, "radius": {"inner": 50.0, "outer": 180.0, "units": "mrad"}}}, "scan": {"x": {"pixels": 77}, "y": {"pixels": 54}}}}'
me/adavydov/work/UWA/godzilla/codes/clTEM/example/clTEM_Si/Screenshot-5.jpg' 

# its elements can be updated via extra config string, which must not change the default config structure, 
# i.e., it should keep the depth, the number and names of fields unchanged
config_extra='{"slice thickness":{"val": 1.92}}'

# remove spaces between entries, and place '_' instead of the key's spaces. This is required for arguments parsed safely
config=`echo $config | sed 's/: /:/g' | sed 's/, /,/g' | sed 's/ /_/g'`
config_extra=`echo $config_extra | sed 's/: /:/g'| sed 's/, /,/g' | sed 's/ /_/g'`

# as mentioned, the default config can be replaced with a file instead of dictionary above
config_path=./new_config.json

# in this example, the following is used to call cltemwf from this script. Alternative value will launched a python interface
bashiface=true

if $bashiface; then
 
  # the example below shows the usage of the code within the batch script
  echo "Running bash interface"
  
  # the helper from clTEM itself
  clTEM_cmd --help

  # cltemwf_batch has also a helper function, which describes flags recognised by cltemwf
  cltemwf_batch --help

  # call to cltemwf. The extra configuration flag takes a dictionary here, which will be merged onto the default configuration.
  cltemwf_batch --cif Si.cif --config_extra ${config_extra} --files-to-copy '*.tif,*.json' --outdir 'outdir' -d gpu -s 1,1,1 -z 0,0,1

  # default config is provided by a file on the $config_path
  #cltemwf_batch --cif Si.cif --config=$config_path --config_extra ${config_extra} --files-to-copy '*.tif' -d gpu -s 1,1,1 -z 0,0,1

  # or we can set config directly from the dictionary, which makes config_extra practically unnecessary
  #cltemwf_batch --cif Si.cif --config ${config} -d gpu -s 2,2,2 -z 0,0,1

else

  echo "Running python interface"

  # it is also possible to set the same input flags within a python script
  python python_iface.py

fi
