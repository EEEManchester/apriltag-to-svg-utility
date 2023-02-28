# AprilTag Image to SVG Utility

This is a rough and ready python script that can download AprilTag images from the AprilRobotic's Tag Image repo and trace them to create svg paths. These can be imported into CAD programs or edited in inkscape if required.

## Setup
Install the following dependencies:

https://pypi.org/project/requests/

https://pypi.org/project/potracer/ (a pure-python implementation of potrace which is slow but easy to install)

https://pypi.org/project/Pillow/ (you might need to uninstall old PIL package first)

```bash
python3 -m pip install --upgrade pip
python3 -m pip install --upgrade Pillow requests potracer 
```
(note on windows `python3` might just be `python`)

## `tag-tracer.py`

This script will download tags from github and trace them to output `.svg` files.

### Configuration
Configuration is achieved by editing the script parameters near the top of the file
 
 ```python

 #################################
##   Configuration Variables   ##
#################################

# family from the lookup_tag_url_format_string dict
tag_library = 'tagStandard41h12'
# total number of tags to download
total_tags = 5 
# start index (00000 is the first tag in the family)
start_index = 0
# scale factor to resize the tag by - 128 generates a tag approx 1000 x 1000 pixels
scale_factor = 128 

```

### Operation
Run the script with `Python3`. Tags will be downloaded to the `tag/<tag-family>` directory next to the `tag_tracer.py` file

### Licence
This is licenced with GPL2 in line with the dependencies used.

### Notes
I am not a python programmer so this is probably very poorly written code - hopefully it is useful nonetheless. Good luck!
