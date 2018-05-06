import os
import subprocess
import datetime
from sets import Set

base_dir = '/home/xian/treefinder'
data_dir = os.path.join(base_dir, 'Data')
videos_dir = os.path.join(data_dir, 'Videos')
fotos_dir = os.path.join(data_dir, 'Fotos')
resumo_dir = os.path.join(base_dir, 'Resumos')

lista_vistas = ['FollasMoitas', 'Outro', 'FollasCerca', 'Tronco', 'VistaCompleta', 'Copa']
lista_arbores_videos = os.listdir(videos_dir)
lista_arbores_fotos= os.listdir(fotos_dir)
lista_arbores = Set(lista_arbores_videos) | Set(lista_arbores_fotos)

lista_nvideos_arbores = []
lista_nframes_arbores = []

lista_nfotos = []
total_fotos = 0

total_videos = 0
total_frames = 0
nerrors = 0


# Videos:
for arbore in lista_arbores:
	print('')
	print('Arbore: ' + arbore)
	arbore_dir = os.path.join(videos_dir, arbore)
	lista_nvideos_vista = []
	lista_nframes_vista = []
	if os.path.exists(arbore_dir):
		lista_vistas_check = os.listdir(arbore_dir)
		for vista in lista_vistas_check:
			if not vista in lista_vistas:
				raise Exception('Nome de vista incorrecto: ' + vista)
		for vista in lista_vistas:
			caso_dir = os.path.join(arbore_dir, vista)
			if os.path.exists(caso_dir):
				lista_videos = os.listdir(caso_dir)
				nvideoscaso = len(lista_videos)
				nframes_accum = 0
				for video in lista_videos:
					total_videos += 1
					videoPath = os.path.join(caso_dir, video)
					args_list = ['ffprobe', '-v', 'error', '-count_frames', '-select_streams', 'v:0', '-show_entries', 'stream=nb_frames', '-of', 'default=nokey=1:noprint_wrappers=1', videoPath]
					try:
						nframes_str = subprocess.check_output(args_list)
						idx = nframes_str.find('\n')
						nframes = int(nframes_str[0:idx])
						nframes_accum += nframes
						total_frames += nframes
					except:
						nerrors += 1
				print('  - ' + vista + ': ' + str(nvideoscaso) + ' videos, ' + str(nframes_accum) + ' frames')
				lista_nvideos_vista.append(nvideoscaso)
				lista_nframes_vista.append(nframes_accum)
			else:
				lista_nvideos_vista.append(0)
				lista_nframes_vista.append(0)
	else:
		for vista in lista_vistas:
			lista_nvideos_vista.append(0)
			lista_nframes_vista.append(0)
	lista_nvideos_arbores.append(lista_nvideos_vista)
	lista_nframes_arbores.append(lista_nframes_vista)

print('')
print('Total number of videos: ' + str(total_videos))
print('Total number of frames: ' + str(total_frames))
print('Number of errors counting frames: ' + str(nerrors))


# Fotos:
for arbore in lista_arbores:
	print('')
	print('Arbore: ' + arbore)
	arbore_dir = os.path.join(fotos_dir, arbore)
	if os.path.exists(arbore_dir):
		lista_fotos = os.listdir(arbore_dir)
		nfotos = len(lista_fotos)
		total_fotos += nfotos
	else:
		nfotos = 0
	lista_nfotos.append(nfotos)
	print(str(nfotos))

print('')
print('Total number of photos: ' + str(total_fotos))



# Escribir resumo a ficheiro:
print('')
print('Writing results to file...')
now = datetime.datetime.now()
date = now.strftime('%Y-%m-%d')
fileName = 'resumo-' + date + '.csv'
ncolumns = len(lista_arbores) + 2
with open(os.path.join(resumo_dir, fileName), 'w') as fid:
	# Primeira linha:
	fid.write('Date: ' + date)
	for j in range(ncolumns - 1):
		fid.write(';')
	fid.write('\n')
	# Encabezado videos:
	fid.write('VIDEOS')
	for arbore in lista_arbores:
		fid.write(';' + arbore)
	fid.write(';\n')
	# Unha linha por cada arbore, para o numero de videos:
	for i in range(len(lista_vistas)):
		fid.write(lista_vistas[i])
		suma = 0
		for j in range(len(lista_arbores)):
			nvideos = lista_nvideos_arbores[j][i]
			suma += nvideos
			fid.write(';' + str(nvideos))
		fid.write(';' + str(suma))
		fid.write('\n')
	# Linha de suma:
	suma_total = 0
	for j in range(len(lista_arbores)):
		suma = 0
		for i in range(len(lista_vistas)):
			nvideos = lista_nvideos_arbores[j][i]
			suma += nvideos
		suma_total += suma
		fid.write(';' + str(suma))
	fid.write(';' + str(suma_total))
	fid.write('\n')
	# Encabezado frames:
	fid.write('FRAMES')
	for arbore in lista_arbores:
		fid.write(';' + arbore)
	fid.write(';\n')
	# Unha linha por cada arbore, para o numero de frames:
	for i in range(len(lista_vistas)):
		fid.write(lista_vistas[i])
		suma = 0
		for j in range(len(lista_arbores)):
			nframes = lista_nframes_arbores[j][i]
			suma += nframes
			fid.write(';' + str(nframes))
		fid.write(';' + str(suma))
		fid.write('\n')
	# Linha de suma:
	suma_total = 0
	for j in range(len(lista_arbores)):
		suma = 0
		for i in range(len(lista_vistas)):
			nframes = lista_nframes_arbores[j][i]
			suma += nframes
		suma_total += suma
		fid.write(';' + str(suma))
	fid.write(';' + str(suma_total))
	fid.write('\n')
	# Fotos:
	fid.write('FOTOS')
	for arbore in lista_arbores:
		fid.write(';' + arbore)
	fid.write(';\n')
	# Linha co numero de fotos:
	for j in range(len(lista_arbores)):
		fid.write(';' + str(lista_nfotos[j]))
print('Done.')










