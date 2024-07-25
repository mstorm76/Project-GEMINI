import os
import nibabel as nib
import numpy as np

# Define the directories
organisedDir = './E.organised/'
normalisedDir = './F.normalised/'

# Function to normalise an image
def normaliseImage(image):
    minValue = np.min(image)
    absMinValue = abs(minValue)
    normalisedImage = image / absMinValue
    return normalisedImage

# Function to process and normalise files
def processFiles(srcDir, dstDir):
    if not os.path.exists(dstDir):
        os.makedirs(dstDir)

    for root, dirs, files in os.walk(srcDir):
        for file in files:
            if file.endswith('.nii.gz'):
                srcFilePath = os.path.join(root, file)
                relativePath = os.path.relpath(srcFilePath, srcDir)
                dstFilePath = os.path.join(dstDir, relativePath)
                dstFileDir = os.path.dirname(dstFilePath)

                if not os.path.exists(dstFileDir):
                    os.makedirs(dstFileDir)
                
                # Load the NIfTI file
                img = nib.load(srcFilePath)
                imgData = img.get_fdata()
                
                # Normalise the image
                normalisedData = normaliseImage(imgData)
                
                # Create a new Nifti1Image
                normalisedImg = nib.Nifti1Image(normalisedData, img.affine)
                
                # Save the normalised image
                nib.save(normalisedImg, dstFilePath)

# Process files in the organised directory
processFiles(organisedDir, normalisedDir)

print("Normalisation Complete.")
