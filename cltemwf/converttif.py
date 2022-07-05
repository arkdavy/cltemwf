from PIL import Image
import numpy as np
import sys
import json

def converttif():

   print("converttif() usage: cltemwf_converttif source.tif output.ext")
   print("where 'ext' defines the extension and the data format at the same time")

   in_fname = sys.argv[1]
   ou_fname = sys.argv[2]
   ext = ou_fname.split('.')[-1]

   if (in_fname == ou_fname): raise ValueError("input and output file names should not be the same")
  
   im = Image.open(in_fname)
   ar = np.asarray(im)

   if (ext == 'json'):
      with open(ou_fname, 'w') as f: json.dump(ar.tolist(), f, indent = 4, sort_keys=True, ensure_ascii=True)
   else:
      # transform to 0..255
      amin, amax = np.amin(ar), np.amax(ar)
      ar = 255*(ar-amin)/(amax-amin)
      ar = ar.astype(np.uint8)
      # save image
      im = Image.fromarray(ar)
      im.save(ou_fname)

   return 

if __name__ == "__main__":
    converttif()
