import os
import subprocess

base_dir = '/home/xian/treefinder'
data_dir = os.path.join(base_dir, 'Data')
videos_dir = os.path.join(data_dir, 'Videos')
frames_dir = os.path.join(data_dir, 'Frames')

lista_vistas = ['FollasMoitas', 'Outro', 'FollasCerca', 'Tronco', 'VistaCompleta', 'Copa']
lista_arbores = os.listdir(videos_dir)

for arbore in lista_arbores:
	arbore_dir_frames = os.path.join(frames_dir, arbore)
	if not os.path.exists(arbore_dir_frames):
		os.makedirs(arbore_dir_frames)
	arbore_dir = os.path.join(videos_dir, arbore)
	lista_vistas_check = os.listdir(arbore_dir)
	for vista in lista_vistas_check:
		if not vista in lista_vistas:
			raise Exception('Nome de vista incorrecto: ' + vista)
	for vista in lista_vistas:
		caso_dir_frames = os.path.join(arbore_dir_frames, vista)
		if not os.path.exists(caso_dir_frames):
			os.makedirs(caso_dir_frames)
		caso_dir = os.path.join(arbore_dir, vista)
		if os.path.exists(caso_dir):
			lista_videos = os.listdir(caso_dir)
			for video in lista_videos:
				videoPath = os.path.join(caso_dir, video)
				idx = video.find('.')
				rawName = video[0:idx]
				videoDir = os.path.join(caso_dir_frames, rawName)
				if not os.path.exists(videoDir):
					print('Extracting frames of ' + videoPath)
					os.makedirs(videoDir)
					framesPath = os.path.join(videoDir, 'f%04d.jpg')
					args_list = ['ffmpeg', '-i', videoPath, framesPath]
					subprocess.check_output(args_list)
				else:
					print('Frames of video ' + videoPath + ' already exist.')
				



