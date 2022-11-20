# LIBRERIAS requeridas
#!/bin/env python3

import argparse
import base64
import os
import re
import subprocess
import sys
from tempfile import mkstemp

import requests
from tqdm import tqdm

#    master_json_url = "https://91vod-adaptive.akamaized.net" \
#    "/exp=1668939686" \
#    "~acl=%2F842360cb-7711-4e48-9bd5-144e4686a2e2%2F%2A" \
#    "~hmac=a982f9ed2cc1e2fc7c61201f9997e0262917b13a89494c4169e4b3848d148f59/842360cb-7711-4e48-9bd5-144e4686a2e2" \
#    "/sep" \
#    "/video/e524c67d,336fea7d,5e87cb6d,306933cc,d42a911f" \
#    "/audio/ebb79ef9,7c03de6a,cad3266d" \
#    "/master.json?query_string_ranges=1&base64_init=1" \

master_json_url = 'https://117vod-adaptive.akamaized.net/exp=1668959455~acl=%2Fa78da094-44ed-4dc3-980a-19095f3b9acc%2F%2A~hmac=abf8ebfffc8c80493c37fd6cef039d13fd7371e53e72db5ba133abe20ba619f2/a78da094-44ed-4dc3-980a-19095f3b9acc/sep/video/6b418e99,7f63dda2,525c4a3c,2db888c3/audio/d874131e,0878800d,5b4700ca/master.json?query_string_ranges=1&base64_init=1'
output_file = "./result.mp4"

#if len(sys.argv) > 1:
#     master_json_url = sys.argv[1]
#     output_file = sys.argv[2]
#else:
#    print('master.json must be passed as argument', file=sys.stderr)
#    exit(1)

# eliminanos de /SEP/ en adelante y agregamos /PARCEL/
base_url = master_json_url[:master_json_url.rfind('/sep/')]
#base_url = "https://117vod-adaptive.akamaized.net/exp=1668959455~acl=%2Fa78da094-44ed-4dc3-980a-19095f3b9acc%2F%2A~hmac=abf8ebfffc8c80493c37fd6cef039d13fd7371e53e72db5ba133abe20ba619f2/a78da094-44ed-4dc3-980a-19095f3b9acc/"
base_url = base_url + "/parcel/"

# Descarga el Master.JSON    simil al MPD
resp = requests.get(master_json_url)
content = resp.json()

# obtenemos la calidad mas alta de video
# Selecciona la mas alta calidad disponible en el Master.JSON
heights = [(i, d['height']) for (i, d) in enumerate(content['video'])]
idx, _ = max(heights, key=lambda h: h[1])
video = content['video'][idx]
video_base_url = base_url + video['base_url']
print('base url:', video_base_url)

# Descarga de Video de la mas alta calidad disponible segmento por segmento
filenameVideo = mkstemp(prefix='.mp4')[1]
print ('saving to {}'.format(filenameVideo))
video_file = open(filenameVideo, 'wb')

init_segment = base64.b64decode(video['init_segment'])
video_file.write(init_segment)

for segment in tqdm(video['segments']):
    segment_url = video_base_url + segment['url']
    resp = requests.get(segment_url, stream=True)
    if resp.status_code != 200:
        print('not 200!')
        print(resp)
        print(segment_url)
        break
    for chunk in resp:
        video_file.write(chunk)

video_file.flush()
video_file.close()

# Audio con la mas alta calidad
bitrate = [(i, d['bitrate']) for (i, d) in enumerate(content['audio'])]

print('Bitrate', bitrate)

idx, _ = max(bitrate, key=lambda x: x[1])
audio = content['audio'][idx]
audio_base_url = base_url + audio['base_url']
print('Base url:', audio_base_url)

# Descarga el Audio segmento por segmento
filenameAudio = mkstemp(prefix='.mp4')[1]
print('Saving AUDIO to %s' % filenameAudio)

audio_file = open(filenameAudio, 'wb')

init_segment = base64.b64decode(audio['init_segment'])
audio_file.write(init_segment)

for segment in tqdm(audio['segments']):
    segment_url = audio_base_url + segment['url']
    segment_url = re.sub(r'/[a-zA-Z0-9_-]*/\.\./',r'/',segment_url.rstrip())
    resp = requests.get(segment_url, stream=True)
    if resp.status_code != 200:
        print('not 200!')
        print(resp)
        print(segment_url)
        break
    for chunk in resp:
        audio_file.write(chunk)

audio_file.flush()
audio_file.close()

#Combinar Audio y Video en un solo archivo
print('Combining video and audio...')
cmd = 'ffmpeg -y -i '
cmd += filenameAudio
cmd += ' -i '
cmd += filenameVideo
cmd += ' ' + output_file
subprocess.call(cmd, shell=True)
print('Mixing Done!')

# Delete the remaining single audio and video files
os.remove(filenameAudio)
os.remove(filenameVideo)
print("Temporary files removed!")

print("Done!")
