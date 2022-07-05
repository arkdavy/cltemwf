from PIL import Image
import matplotlib.pyplot as plt
import numpy as np
import sys

def showtif():
   print("showtif() usage: cltemwf_showtif source.tif")
   fname = sys.argv[1]
   im = Image.open(fname)
   ar = np.asarray(im)

   # the commented code use the system tools to display the image, which makes an interpoation. 
   # The matplotlib way below does not do it, so that one is chosen for a moment

   # transform to 0..255
   #amin, amax = np.amin(ar), np.amax(ar)
   #ar = 255*(ar-amin)/(amax-amin)
   #ar = ar.astype(np.uint8)
   # show image
   #im = Image.fromarray(ar)
   #im.show()

   plt.imshow(ar, cmap='gray')
   plt.show()

if __name__ == "__main__":
    showtif()
