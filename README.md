# cltemwf

A wrapper for creating templated workflows for [clTEM](https://jjppeters.github.io/clTEM) code.
One can run the workflow from within a bash script and a python script as well. 
Follow the example file `examples/run_batch.sh` with a description of these two cases.

Run `pip install .` to install the package (or `pip install . --user` for the `home/` installation)

The main code is embedded in the `cltemwf_batch` script. Run `cltemwf_batch --help` for further instructions.

There are additional commands for postprocess the data:

`cltemwf_showtif` for viewing the tiff data using matplotlib. This is useful for linux where tiff may not be opened properly.
`cltemwf_converttif` converts the data in the tiff file to the format of choice. 

Run these scripts in the command line to view the further instructions after a successful installation
