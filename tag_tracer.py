from potrace import Bitmap, POTRACE_CORNER, Path
import requests
import io
from PIL import Image
import pathlib
import os

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

#################################
#################################
#################################

# github raw-content URLs
lookup_tag_url_format_string = {
    'tag12h5' : 'https://raw.githubusercontent.com/AprilRobotics/apriltag-imgs/master/tag16h5/tag16_05_{:05d}.png',
    'tag25h9' : 'https://raw.githubusercontent.com/AprilRobotics/apriltag-imgs/master/tag25h9/tag25_09_{:05d}.png',
    'tag36h11': 'https://raw.githubusercontent.com/AprilRobotics/apriltag-imgs/master/tag36h11/tag36_11_{:05d}.png',
    'tagCircle21h7' : 'https://raw.githubusercontent.com/AprilRobotics/apriltag-imgs/master/tagCircle21h7/tag21_07_{:05d}.png',
    'tagCircle49h12' : 'https://raw.githubusercontent.com/AprilRobotics/apriltag-imgs/master/tagCircle49h12/tag49_12_{:05d}.png',
    'tagStandard41h12' : 'https://raw.githubusercontent.com/AprilRobotics/apriltag-imgs/master/tagStandard41h12/tag41_12_{:05d}.png',
    'tagStandard52h13' : 'https://raw.githubusercontent.com/AprilRobotics/apriltag-imgs/master/tagStandard52h13/tag52_13_{:05d}.png',
}

# Build Output Paths and ensure output dir exists
output_dir = os.path.join(pathlib.Path().resolve(),'tags', tag_library)
pathlib.Path(output_dir).mkdir(parents=True, exist_ok=True)

# Build Tag Indicies Range
tag_indicies = range(start_index, total_tags)

for tag_index in tag_indicies:
    # Build the download url
    url = lookup_tag_url_format_string[tag_library].format(tag_index)

    r = requests.get(url, timeout=4.0)
    if r.status_code != requests.codes.ok:
        assert False, 'Status code error: {}.'.format(r.status_code)

    # use Pillow to convert png image data to useable image
    pil_image = Image.open(io.BytesIO(r.content))

    # We want a zero-order upscaled image for tracing so use Image.Nearest to avoid resampling
    pil_image = pil_image.resize((pil_image.width * scale_factor, pil_image.height * scale_factor), resample = Image.NEAREST)

    # Build output file name
    output_file = os.path.join(output_dir, '{}_{:05d}.svg'.format(tag_library, tag_index))

    # Trace
    path = Bitmap(pil_image).trace()

    # Write out traced paths as svg file
    # modified from backend_svg function from https://github.com/tatarize/potrace-cli/blob/main/cli/backend_svg.py
    with open(output_file, "w") as fp:
        # open svg tag
        fp.write(
            '<svg version="1.1"' +
            ' xmlns="http://www.w3.org/2000/svg"' +
            ' xmlns:xlink="http://www.w3.org/1999/xlink"' +
            ' width="%d" height="%d"' % (pil_image.width, pil_image.height) +
            ' viewBox="0 0 %d %d">' % (pil_image.width, pil_image.height)
        )
        # combine path into svg:path data
        parts = []
        for curve in path:
            fs = curve.start_point
            parts.append("M%f,%f" % (fs.x, fs.y))
            for segment in curve.segments:
                if segment.is_corner:
                    a = segment.c
                    parts.append("L%f,%f" % (a.x, a.y))
                    b = segment.end_point
                    parts.append("L%f,%f" % (b.x, b.y))
                else:
                    a = segment.c1
                    b = segment.c2
                    c = segment.end_point
                    parts.append("C%f,%f %f,%f %f,%f" % (a.x, a.y, b.x, b.y, c.x, c.y))
            parts.append("z")
        # write path data
        fp.write(
            '<path stroke="none" fill="black" fill-rule="evenodd" d="%s"/>'
            % ("".join(parts))
        )
        # close svg tag
        fp.write("</svg>")

    print("Generated File:", output_file)
