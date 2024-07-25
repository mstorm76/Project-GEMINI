import os
import nibabel as nib
import numpy as np
from scipy.ndimage import zoom

# Define the target directories
dataDir = './C.split/'
noisyDir = './D.noisy/'
noiseStds = [5, 10, 15, 20, 25, 30]  # Define the array of different normalised noiseStd values

# Create the main noisy directory
os.makedirs(noisyDir, exist_ok=True)

# Function to apply noise and then nearest neighbour downsampling
def processImage(image, downsampleFactor=0.65, interpolationOrder=0, noiseMean=0, noiseStd=0):
    originalShape = image.shape
    
    # Add tissue mask so it only affects the tissue
    tissueMask = image > -1024
    
    # Generate Gaussian noise for the entire volume
    noise = np.random.normal(noiseMean, noiseStd, originalShape)
    
    # Apply noise while respecting the tissue mask
    noisyImage = image + (tissueMask * noise)
    
    # Calculate the downsampled shape
    downsampledShape = tuple(int(dim * downsampleFactor) for dim in originalShape)
    
    # Downsample the noisy image
    downsampledImage = zoom(noisyImage, zoom=(downsampledShape[0] / originalShape[0], downsampledShape[1] / originalShape[1], downsampledShape[2] / originalShape[2]), order=interpolationOrder)
    
    # Upsample back to original size
    upsampledImage = zoom(downsampledImage, zoom=(originalShape[0] / downsampledShape[0], originalShape[1] / downsampledShape[1], originalShape[2] / downsampledShape[2]), order=interpolationOrder)
    
    return upsampledImage

# Function to process files in a directory
def processFiles(srcDir, dstDir, noiseStd):
    for file in os.listdir(srcDir):
        if file.endswith('.nii.gz'):
            srcFilePath = os.path.join(srcDir, file)
            dstFilePath = os.path.join(dstDir, f'input_noisy_Std{noiseStd}_' + file)
            
            # Load the NIfTI file
            img = nib.load(srcFilePath)
            imgData = img.get_fdata()
            
            # Process the image
            processedData = processImage(imgData, noiseStd=noiseStd)
            
            # Create a new Nifti1Image
            processedImg = nib.Nifti1Image(processedData, img.affine)
            
            # Save the processed image
            nib.save(processedImg, dstFilePath)

# Loop over each noiseStd value and process files
for noiseStd in noiseStds:
    for dataset in ['train', 'test', 'validation']:
        srcDir = os.path.join(dataDir, dataset)
        dstDir = os.path.join(noisyDir, f'noisy{noiseStd}', f'noisy{dataset.capitalize()}')
        
        # Create the destination directories
        os.makedirs(dstDir, exist_ok=True)
        
        # Process the files in the source directory and save them to the destination directory
        processFiles(srcDir, dstDir, noiseStd)

print("Processing Complete.")
