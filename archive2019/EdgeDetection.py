
import Image
import ImageFilter

def countEdgePixels(file):
    
        # define threshold for edges
        threshold = 150 
        
        # open image and filter
        im = Image.open(file)
	im2 = im.filter(ImageFilter.FIND_EDGES)
	im2.save("Filtered.jpg")
	im2 = im2.convert("L")
	
	# load pixels and count edge pixels
        pix = im2.load()
        pixels = 0
        for x in range(0,im.size[0]):
            for y in range(0, im.size[1]):
                if pix[x,y] > threshold:
                    pixels += 1

	return float(pixels) / (im.size[0]*im.size[1])
