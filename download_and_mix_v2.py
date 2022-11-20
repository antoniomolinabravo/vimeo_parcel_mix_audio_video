import subprocess
import requests

#AQUI >> EL URL de master.json
master_json_url = "https://91vod-adaptive.akamaized.net/exp=1668939686~acl=%2F842360cb-7711-4e48-9bd5-144e4686a2e2%2F%2A~hmac=a982f9ed2cc1e2fc7c61201f9997e0262917b13a89494c4169e4b3848d148f59/842360cb-7711-4e48-9bd5-144e4686a2e2/sep/video/e524c67d,336fea7d,5e87cb6d,306933cc,d42a911f/audio/ebb79ef9,7c03de6a,cad3266d/master.json?query_string_ranges=1&base64_init=1"
output_file = "./result.mp4"

# eliminanos de /SEP/ en adelante y agregamos /PARCEL/
base_url = master_json_url[:master_json_url.rfind('/sep/')]
base_url = base_url + "/parcel/"

# obtenemos el MASTER.JSON
resp = requests.get(master_json_url)
content = resp.json()

# obtenemos la calidad mas alta de video
heights = [(i, d['height']) for (i, d) in enumerate(content['video'])]
idx, _ = max(heights, key=lambda h: h[1])
video = content['video'][idx]
video_base_url = base_url + video['base_url']
video_file =  video['id'] + '.mp4'
video_url = video_base_url + video_file
print('VIDEO URL:', video_url)

# Audio download here
bitrate = [(i, d['bitrate']) for (i, d) in enumerate(content['audio'])]
print('Bitrate', bitrate)
idx, _ = max(bitrate, key=lambda x: x[1])
audio = content['audio'][idx]
audio_base_url = base_url + audio['base_url']
audio_file = audio['id'] + '.mp4'
audio_url = video_base_url + audio_file
print('AUDIO URL:', audio_url)

print("Downloading Files ...")

# archivos temporales como Arg para procesos OS
with open("files.txt","w") as file:
    file.write(video_file+"\n")
    file.write(audio_file+"\n")

with open("urls.txt","w") as file:
    file.write(video_url+"\n")
    file.write(audio_url+"\n")

# Descarga de archivos audio y video
%time !wget -i urls.txt
print("Download Files!!!")

print( audio_file )
print( video_file )

# combinamos el audio y video en result.mp4
print('Combining video and audio...')
cmd = 'ffmpeg -y -i '
cmd += audio_file
cmd += ' -i '
cmd += video_file
cmd += ' ' + output_file
%time subprocess.call(cmd, shell=True)
print('Mixing Done!')

# Borrar los archivos 
!rm -f `cat files.txt`
print("Temporary files removed!")

print("Done!")
