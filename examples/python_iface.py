from cltemwf.batch import run_pyiface

# Set the flags. Config_extra accepts the dictionary to merge into the default_config, which can be changed as well by
# either giving a path to a new config, or passing a dictionary via --config input keyword argument
run_pyiface(cif='Si.cif', config_extra={"slice thickness":{"val": 1.92}}, other_args_string='-d gpu -s 30,30,10 -z 1,1,0 -n 0,0,1')
