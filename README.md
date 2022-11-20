# vimeo_parcel_mix_audio_video

1. Para el proceso solo se requiere contar con el link del master.json que debe ser pegado en el codigo *master_json_url*
1. El proceso tomara el video y el audio de mas alta resolucion y calidad
1. Posteriormente los unira en un solo archivo ==> result.mp4
1. Borrando los otros dos archivos temporales para liberar espacio

##  Obtener el Link del master.json

### Opcion #1
* seleccionar el Video hacer [PLAY] poner [PAUSA] y seleccionar en menu contextual [INSPECCIONAR]
* buscar el primer <script>..</script>
* buscar master.json
* copiar la ruta completa
* se vera como el siguiente ej: 
```
https://91vod-adaptive.akamaized.net/exp=1668939686~acl=%2F842360cb-7711-4e48-9bd5-144e4686a2e2%2F%2A~hmac=a982f9ed2cc1e2fc7c61201f9997e0262917b13a89494c4169e4b3848d148f59/842360cb-7711-4e48-9bd5-144e4686a2e2/sep/video/e524c67d,336fea7d,5e87cb6d,306933cc,d42a911f/audio/ebb79ef9,7c03de6a,cad3266d/master.json?query_string_ranges=1&base64_init=1
```

### Opcion #2
* Seleccionar el Video hacer [PLAY] poner [PAUSA] y seleccionar en menu contextual [INSPECCIONAR]
* ir al panel [NETWORK] donde iran apareciendo la lista de solicitudes y respuestas
* tomar una y copiar el link
* reemplazar el archivo por master.json?query_string_ranges=1&base64_init=1

# Tiempo
* Descargar Audio (300Mb) y Video (500Mb) via Colab tomara aprox 30 minutos para un video como el del ejemplo de 3:30h en 1080p
* Pero el proceso de Unir Audio y Video (365Mb) tomara aprox 1 hora
* La estimacion dependera del Tiempo y Calidad del Video y Audio (tamaño en Mb)
* Esto No considera el tiempo que le tomara descargar el resultado a su PC o si lo dejara en su cuenta Drive

# Tiempo v2
* La version2 es mucho mas rapida, ya que descarga los archivos audio y video directamente sin bloques
* este proceso de descarga en el ejemplo tarda solo 2 minutos para un video de 1Gb y audio de 230Mb
* el proceso de conversion no ha sufrido cambios si que tardara dependiendo de la calidad y tiempo del video

---
==========================================================================================

## BASE PARA ENTENDER COMO SE HACE MANUALMENTE


### PASOS A PASO

##  Paso 1
* Extrar el JAVASCRIPT del VIDEO 
* Seleccionar el Video hacer [PLAY] y seleccionar en menu contextual [INSPECCIONAR]
* buscar el primer <script>..</script>

##  Paso 2
* Buscar el URL del link base
* como adelanto este link tiene las distintas variantes para descargar separados por coma
* referencia de busqueda => "akfire_interconnect_quic":{"url":

##  Paso 3
* Buscar configuracion de formatos
* seleccionar el formato 720 idealmente y extrar el primer bloque del ID
* referencia de busqueda => window.playerConfig = 

##  Paso 3.5
* Para saber cual es el mejor formato de audio debe descargar el master, ahi estan las caracteristicas
* Alternativamente puede descargar el primero de la lista

##  Paso 3.6
* Pude descargar el formato MPD como alternativa
* este es un formato XML que se puede abrir en excel
* solo se debe reemplazar .json por .mpd

##  Paso 4
* Reemplazar segmento de la URL base para descargar video y audio por separado
* desde "/sep/video" en adelante por "/parcel/video/bloqueIDvideo.mp4" y "/parcel/audio/bloqueIDaudio.mp4"
* cada uno de los que esta separado por coma es un formato disponible
* ej.   /sep/video/e524c67d,336fea7d,5e87cb6d,306933cc,d42a911f/audio/ebb79ef9,7c03de6a,cad3266d/master.json?query_string_ranges=1&base64_init=1

##  Paso 4.5
* Es posible descargar el video y audio por bloques o todo de una sola vez
* los rangos de los bloques estan en el Master, pero el rango se pueden establecer manualmente inicio-termino
* si no quiere bloques, puede omitir el rango en el link y solo llegar hasta .mp4

##  Paso 5
* Para descargar el Thumb de pantallas, buscar el link
* "thumb_preview":{"url":



---
==============================================================================

##  QUE SE OBTIENE ?

1. LOS VIDEOS ADAPTATIVE estan conformados por multiples formatos de videos y audios, los cuales estan por separados y puden ser accedidos por bloques de un determinado inicio y fin

1. Esto permite adelantar el video e ir a buscar ese bloque y no tener que esperar descargar todo, ademas si baja la velocidad de internet este baja la calidad del video y audio cambiando la fuente segun indica el archivo en alguno de sus formatos => master.json / master.mpd / master.m3u8
Tambien es posible descargar solo video o solo audio, como tambien es posible descargar una imagen con el Thumb de secuencias

1. Video.mp4 / Audio.mp4 / Thumb.jpg / master.m3u8 / master.json / master.mpd

##  LOS LINKS 
Vienen en dos formatos ADAPTATIVE y SKYFIRE, ambos dan el mismo resultado

##  EXPIRAN
Los links expiran, no son para siempre

##  COMPOSICION ADAPTATIVE
```
exp: tiempo para expirar link
acl: id unica del la ruta del video en formato escape (%)
hmac: id unica del video que incluye el acl en formato no escape
rutas: /sep/video   /sep/audio   /parcel/video   /parcel/audio
r:codigo parte del id del bloque
range: desde-hasta  porcion del bloque
```

En la ruta "/sep" del master encontrara separadas por coma todas las alternativas para descargar audio y video pero no sabra a que calidad corresponden
```
/sep
/video/e524c67d,336fea7d,5e87cb6d,306933cc,d42a911f
/audio/ebb79ef9,7c03de6a,cad3266d
```

##  EN SKYFIRE
hmac: es otro formato o codigo todo lo demas es igual pero es mas compacto el formato

##  EJEMPLOS DE RESULTADOS:

Video por bloque
```
https://91vod-adaptive.akamaized.net/exp=1668939686
~acl=%2F842360cb-7711-4e48-9bd5-144e4686a2e2%2F%2A
~hmac=a982f9ed2cc1e2fc7c61201f9997e0262917b13a89494c4169e4b3848d148f59
/842360cb-7711-4e48-9bd5-144e4686a2e2
/parcel/video/d42a911f.mp4
?r=dXMtd2VzdDE%3D
&range=0-1691476
```

Video sin bloques, todo de un solo llamado
```
https://91vod-adaptive.akamaized.net/exp=1668939686
~acl=%2F842360cb-7711-4e48-9bd5-144e4686a2e2%2F%2A
~hmac=a982f9ed2cc1e2fc7c61201f9997e0262917b13a89494c4169e4b3848d148f59
/842360cb-7711-4e48-9bd5-144e4686a2e2
/parcel/video/d42a911f.mp4
```

Audio
```
https://91vod-adaptive.akamaized.net/exp=1668939686
~acl=%2F842360cb-7711-4e48-9bd5-144e4686a2e2%2F%2A
~hmac=a982f9ed2cc1e2fc7c61201f9997e0262917b13a89494c4169e4b3848d148f59
/842360cb-7711-4e48-9bd5-144e4686a2e2
/parcel/audio/7c03de6a.mp4
?r=dXM%3D
&range=0-514562
```

Fotos
```
https://videoapi-sprites.vimeocdn.com/video-sprites/image/d76e740e-ed49-4dac-983f-85dab6a9fda1.0.jpeg
?ClientID=player-backend-prod
&Expires=1668901094
&Signature=ab9be9a1530250865e230eb95d02bb63953c57db
```

JSON
```
https://91vod-adaptive.akamaized.net/exp=1668939686
~acl=%2F842360cb-7711-4e48-9bd5-144e4686a2e2%2F%2A
~hmac=a982f9ed2cc1e2fc7c61201f9997e0262917b13a89494c4169e4b3848d148f59
/842360cb-7711-4e48-9bd5-144e4686a2e2
/sep
/video/e524c67d,336fea7d,5e87cb6d,306933cc,d42a911f
/audio/ebb79ef9,7c03de6a,cad3266d
/master.json
?query_string_ranges=1
&base64_init=1
```

MPD  Cambiar json por mpd
```
https://skyfire.vimeocdn.com/1668939686
-0x1d93ecc4e187484b09417aa99a49258a78c2ff55
/842360cb-7711-4e48-9bd5-144e4686a2e2
/sep
/video/e524c67d,336fea7d,5e87cb6d,306933cc,d42a911f
/audio/ebb79ef9,7c03de6a,cad3266d
/master.mpd
?query_string_ranges=1
&base64_init=1
```

M3U8  Cambiar json por m3u8
```
https://91vod-adaptive.akamaized.net/exp=1668939686
~acl=%2F842360cb-7711-4e48-9bd5-144e4686a2e2%2F%2A
~hmac=a982f9ed2cc1e2fc7c61201f9997e0262917b13a89494c4169e4b3848d148f59
/842360cb-7711-4e48-9bd5-144e4686a2e2
/sep
/video/e524c67d,336fea7d,5e87cb6d,306933cc,d42a911f
/audio/ebb79ef9,7c03de6a,cad3266d
/master.m3u8
?query_string_ranges=1
```

====================================================================

ARCHIVO M3u8
Se pueden apreciar las opciones de calidad solo de audio disponibles para descargar y sus links

```
#EXTM3U
#EXT-X-INDEPENDENT-SEGMENTS
#EXT-X-MEDIA:TYPE=AUDIO,GROUP-ID="audio-high",NAME="audio",AUTOSELECT=YES,DEFAULT=YES,CHANNELS="1",URI="../../../../audio/ebb79ef9/playlist.m3u8?query_string_ranges=1"
#EXT-X-STREAM-INF:CLOSED-CAPTIONS=NONE,BANDWIDTH=1434400,AVERAGE-BANDWIDTH=535000,RESOLUTION=960x540,FRAME-RATE=25.000,CODECS="avc1.64001F,mp4a.40.2",AUDIO="audio-high"../../../e524c67d/playlist.m3u8?query_string_ranges=1
#EXT-X-STREAM-INF:CLOSED-CAPTIONS=NONE,BANDWIDTH=3810817,AVERAGE-BANDWIDTH=986000,RESOLUTION=1920x1080,FRAME-RATE=25.000,CODECS="avc1.64002A,mp4a.40.2",AUDIO="audio-high"../../../306933cc/playlist.m3u8?query_string_ranges=1
#EXT-X-STREAM-INF:CLOSED-CAPTIONS=NONE,BANDWIDTH=507977,AVERAGE-BANDWIDTH=289000,RESOLUTION=426x240,FRAME-RATE=25.000,CODECS="avc1.640015,mp4a.40.2",AUDIO="audio-high"../../../336fea7d/playlist.m3u8?query_string_ranges=1
#EXT-X-STREAM-INF:CLOSED-CAPTIONS=NONE,BANDWIDTH=882738,AVERAGE-BANDWIDTH=377000,RESOLUTION=640x360,FRAME-RATE=25.000,CODECS="avc1.64001E,mp4a.40.2",AUDIO="audio-high"../../../5e87cb6d/playlist.m3u8?query_string_ranges=1
#EXT-X-STREAM-INF:CLOSED-CAPTIONS=NONE,BANDWIDTH=2444809,AVERAGE-BANDWIDTH=680000,RESOLUTION=1280x720,FRAME-RATE=25.000,CODECS="avc1.640020,mp4a.40.2",AUDIO="audio-high"../../../d42a911f/playlist.m3u8?query_string_ranges=1
```

====================================================================

EN EL SCRIPT puede encontrar las opciones de Video disponibles, pero solo es util el primer bloque del ID

```
window.playerConfig = 
{"cdn_url":"https://f.vimeocdn.com","vimeo_api_url":"api.vimeo.com","request":{"files":{"dash":{"separate_av":true,"streams":
[{"profile":"f9e4a5d7-8043-4af3-b231-641ca735a130","quality":"540p","id":"e524c67d-f4e6-48a3-b75a-460cb395cce2","fps":25}
,{"profile":"d0b41bac-2bf2-4310-8113-df764d486192","quality":"240p","id":"336fea7d-0250-45bf-b20b-de01bb4b53ca","fps":25}
,{"profile":"c3347cdf-6c91-4ab3-8d56-737128e7a65f","quality":"360p","id":"5e87cb6d-099f-494c-acb5-00243ffc44ed","fps":25}
,{"profile":"5ff7441f-4973-4241-8c2e-976ef4a572b0","quality":"1080p","id":"306933cc-6bcb-4333-a643-8a43f0b1d189","fps":25}
,{"profile":"f3f6f5f0-2e6b-4e90-994e-842d1feeabc0","quality":"720p","id":"d42a911f-6702-44b3-8420-85caa5112835","fps":25}]
```

Tambien lo encontrara en otro segmento del SCRIPT como:

```
"streams_avc":
[{"profile":"f9e4a5d7-8043-4af3-b231-641ca735a130","quality":"540p","id":"e524c67d-f4e6-48a3-b75a-460cb395cce2","fps":25}
,{"profile":"d0b41bac-2bf2-4310-8113-df764d486192","quality":"240p","id":"336fea7d-0250-45bf-b20b-de01bb4b53ca","fps":25}
,{"profile":"c3347cdf-6c91-4ab3-8d56-737128e7a65f","quality":"360p","id":"5e87cb6d-099f-494c-acb5-00243ffc44ed","fps":25}
,{"profile":"5ff7441f-4973-4241-8c2e-976ef4a572b0","quality":"1080p","id":"306933cc-6bcb-4333-a643-8a43f0b1d189","fps":25}
,{"profile":"f3f6f5f0-2e6b-4e90-994e-842d1feeabc0","quality":"720p","id":"d42a911f-6702-44b3-8420-85caa5112835","fps":25}]
```


---

* MASTER JSON 

1.  Contiene informacion de los formatos disponibles de audio y video
1.  Las listas pre calculadas de bloques por cada formato
1.  Archivo muy extenso

2.  inicia con el clip_id que es el acl
1.  le sigue la base_url, que es el retroceso hasta antes del /sep/ y lo reemplaza por /parcel/

3.  luego describe la lista de formatos y sus caracteristicas, en este ejemplo se ve solo el primero
1.  le sigue el init_segment, no util para nosotros
1.  el index_segment es el inicio del video o audio
1.  luego los segments donde detalla cada bloque y su rango
1.  cada segmento indica su inicio y fin en tiempo y el tamaño que acumulan hasta ese punto

Ej. un fragmento

```
{"clip_id":"842360cb-7711-4e48-9bd5-144e4686a2e2","base_url":"../../../../../parcel/"
,"video":
[{"id":"e524c67d","base_url":"video/","format":"dash"
,"mime_type":"video/mp4","codecs":"avc1.64001F"
,"bitrate":1115000,"avg_bitrate":344000,"duration":10473
,"framerate":25,"width":960,"height":540,"max_segment_duration":8
,"init_segment":"AAAAIGZ0eXBkYXNoAAAAAGRhc2htcDQybXA0MWlzbzYAAAMibW9vdgAAAGxtdmhkAAAAAN+Zv6rfmb+qAAAAGQAAAAAAAQAAAQAAAAAAAAAAAAAAAAEAAAAAAAAAAAAAAAAAAAABAAAAAAAAAAAAAAAAAABAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAgAAACFpb2RzAAAAABCAgIAQAE////9//w6AgIAEAAAAAQAAAlF0cmFrAAAAXHRraGQAAAAH35m/qt+Zv6oAAAABAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAEAAAAAAAAAAAAAAAAAAAABAAAAAAAAAAAAAAAAAABAAAAAA8AAAAIcAAAAAAAkZWR0cwAAABxlbHN0AAAAAAAAAAEAAAAAAAAAAwABAAAAAAHJbWRpYQAAACBtZGhkAAAAAN+Zv6rfmb+qAAAAGQAAAABVxAAAAAAANmhkbHIAAAAAAAAAAHZpZGUAAAAAAAAAAAAAAABMLVNNQVNIIFZpZGVvIEhhbmRsZXIAAAABa21pbmYAAAAUdm1oZAAAAAEAAAAAAAAAAAAAACRkaW5mAAAAHGRyZWYAAAAAAAAAAQAAAAx1cmwgAAAAAQAAAStzdGJsAAAAs3N0c2QAAAAAAAAAAQAAAKNhdmMxAAAAAAAAAAEAAAAAAAAAAAAAAAAAAAAAA8ACHABIAAAASAAAAAAAAAABCkFWQyBDb2RpbmcAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAP//AAAAOmF2Y0MBZAAf/+EAHWdkAB+sViQPARfuagwMDIAAAAMAgAAAGQeMGMTAAQAGaOiOyyLA/fj4AAAAABNjb2xybmNseAAGAAYABgAAAAAQc3R0cwAAAAAAAAAAAAAAEHN0c2MAAAAAAAAAAAAAABRzdHN6AAAAAAAAAAAAAAAAAAAAEHN0Y28AAAAAAAAAAAAAABhzZ3BkAQAAAHJvbGwAAAACAAAAAAAAABRzYmdwAAAAAHJvbGwAAAAAAAAAPG12ZXgAAAAUbWVoZAEAAAAAAAAAAAP+wQAAACB0cmV4AAAAAAAAAAEAAAABAAAAAQAAAAAAAQAA"
,"index_segment":"e524c67d.mp4?r=dXMtZWFzdDE%3D\u0026range=834-21805"
,"segments":
[{"start":0,"end":6.08,"url":"e524c67d.mp4?r=dXMtZWFzdDE%3D\u0026range=21806-35425","size":13619}
,{"start":6.08,"end":12.16,"url":"e524c67d.mp4?r=dXMtZWFzdDE%3D\u0026range=35426-126616","size":91190}
,{"start":12.16,"end":18.24,"url":"e524c67d.mp4?r=dXMtZWFzdDE%3D\u0026range=126617-362623","size":236006}
,{"start":18.24,"end":24.32,"url":"e524c67d.mp4?r=dXMtZWFzdDE%3D\u0026range=362624-447116","size":84492}
,{"start":24.32,"end":30.4,"url":"e524c67d.mp4?r=dXMtZWFzdDE%3D\u0026range=447117-546643","size":99526}
,{"start":30.4,"end":36.48,"url":"e524c67d.mp4?r=dXMtZWFzdDE%3D\u0026range=546644-652721","size":106077}
,{"start":36.48,"end":42.56,"url":"e524c67d.mp4?r=dXMtZWFzdDE%3D\u0026range=652722-749681","size":96959}
,{"start":42.56,"end":48.64,"url":"e524c67d.mp4?r=dXMtZWFzdDE%3D\u0026range=749682-907585","size":157903}
,{"start":48.64,"end":54.72,"url":"e524c67d.mp4?r=dXMtZWFzdDE%3D\u0026range=907586-1030805","size":123219}
,{"start":54.72,"end":60,"url":"e524c67d.mp4?r=dXMtZWFzdDE%3D\u0026range=1030806-1137670","size":106864}
,{"start":60,"end":66.08,"url":"e524c67d.mp4?r=dXMtZWFzdDE%3D\u0026range=1137671-1255762","size":118091}
,{"start":66.08,"end":72.16,"url":"e524c67d.mp4?r=dXMtZWFzdDE%3D\u0026range=1255763-1356863","size":101100}
,{"start":72.16,"end":78.24,"url":"e524c67d.mp4?r=dXMtZWFzdDE%3D\u0026range=1356864-1480061","size":123197}
,{"start":78.24,"end":84.32,"url":"e524c67d.mp4?r=dXMtZWFzdDE%3D\u0026range=1480062-1663879","size":183817}
,{"start":84.32,"end":90.4,"url":"e524c67d.mp4?r=dXMtZWFzdDE%3D\u0026range=1663880-1850423","size":186543}
,{"start":90.4,"end":96.48,"url":"e524c67d.mp4?r=dXMtZWFzdDE%3D\u0026range=1850424-2076200","size":225776}
,{"start":96.48,"end":102.56,"url":"e524c67d.mp4?r=dXMtZWFzdDE%3D\u0026range=2076201-2297828","size":221627}
,{"start":102.56,"end":108.64,"url":"e524c67d.mp4?r=dXMtZWFzdDE%3D\u0026range=2297829-2535139","size":237310}
,{"start":108.64,"end":114.72,"url":"e524c67d.mp4?r=dXMtZWFzdDE%3D\u0026range=2535140-2785899","size":250759}
,{"start":114.72,"end":120,"url":"e524c67d.mp4?r=dXMtZWFzdDE%3D\u0026range=2785900-2997033","size":211133}
,{"start":120,"end":126.08,"url":"e524c67d.mp4?r=dXMtZWFzdDE%3D\u0026range=2997034-3196278","size":199244}
,{"start":126.08,"end":132.16,"url":"e524c67d.mp4?r=dXMtZWFzdDE%3D\u0026range=3196279-3411175","size":214896}
,{"start":132.16,"end":138.24,"url":"e524c67d.mp4?r=dXMtZWFzdDE%3D\u0026range=3411176-3652675","size":241499}
,{"start":138.24,"end":144.32,"url":"e524c67d.mp4?r=dXMtZWFzdDE%3D\u0026range=3652676-3992495","size":339819}
,{"start":144.32,"end":150.4,"url":"e524c67d.mp4?r=dXMtZWFzdDE%3D\u0026range=3992496-4210143","size":217647}
```
