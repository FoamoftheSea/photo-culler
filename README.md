# Photo-Culler

![photo_culler](photo_culler.jpg)

Tool for culling bad photos from large collections to save photographers time.

The tool uses the LLaVA multimodal model to evaluate images on a set of criteria, providing an overall score from 1-10
which is then used to determine if an image is a "keeper" based on a user-specified threshold.

The `cull_photos.py` script does not delete the rejected images from the original folder, but rather copies the keepers 
into a new folder to keep things non-destructive. This script will print out scores and notes into the terminal, as 
well as saving them into a file called `photo_reviews.json` in the destination folder for later review.

## Setup and Instructions
1. Make sure you have miniconda/anaconda and ollama installed on your system.
2. If you have not already done so, open a terminal and run `ollama pull llava`
3. In your terminal, navigate to this repo, and run `conda env create -f environment.yml`
4. Run `python create_custom_ollama.py` to create a special-tagged LLaVA model for this application.
5. Run `python cull_photos.py -i <path to your images> -o <desired output location>`
