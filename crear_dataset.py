import numpy as np
from shutil import copyfile
import os
from random import shuffle
from sets import Set

basedir = '/home/xian/treefinder'
data_dir = os.path.join(base_dir, 'Data')
framesdir = os.path.join(data_dir, 'Frames')
fotosdir = os.path.join(data_dir, 'Fotos')
dirout = '/home/xian/datasets/dataset_arbores_3'

percent_frames = 10
train_percent = 80

lista_arbores_videos = os.listdir(framesdir)
lista_arbores_fotos= os.listdir(fotosdir)
lista_arbores = list(Set(lista_arbores_videos) | Set(lista_arbores_fotos))

path_trainlabels = os.path.join(dirout, 'train_labels.txt')
path_vallabels = os.path.join(dirout, 'val_labels.txt')

vistas_a_incluir = ['FollasCerca']

if not os.path.exists(dirout):
	os.makedirs(dirout)

lista_train = []
lista_val = []

# Loop over all the data:
for arbore_idx in range(len(lista_arbores)):
	arbore = lista_arbores[arbore_idx]
	print(arbore + ' - ' + str(arbore_idx))
	# Videos
	arboredir = os.path.join(framesdir, arbore)
	if os.path.exists(arboredir):
		subfolders = os.listdir(arboredir)
		for vista in subfolders:
			if vista in vistas_a_incluir:
				vistadir = os.path.join(arboredir, vista)
				videos = os.listdir(vistadir)
				for vid in videos:
					if np.random.rand() < train_percent / 100.0:
						is_train = True
						splitname = 'train'
					else:
						is_train = False
						splitname = 'val'
					videodir = os.path.join(vistadir, vid)
					frames = os.listdir(videodir)
					nframes = len(frames)
					nframes_sel = max(np.int16(percent_frames / 100.0 * nframes), 1)
					idxs_sel = np.int16(np.linspace(0, nframes - 1, nframes_sel))
					for i in idxs_sel:
						path_in = os.path.join(videodir, frames[i])
						folder_frame_out = os.path.join(dirout, splitname, arbore)
						if not os.path.exists(folder_frame_out):
							os.makedirs(folder_frame_out)
						path_out_rel = os.path.join(splitname, arbore, vista + '-' + vid + '-' + frames[i])
						path_out_abs = os.path.join(dirout, path_out_rel)
						copyfile(path_in, path_out_abs)
						if is_train:
							lista_train.append(path_out_rel + ',' + str(arbore_idx))
						else:
							lista_val.append(path_out_rel + ',' + str(arbore_idx))
	# Fotos
	arboredir = os.path.join(fotosdir, arbore)
	if os.path.exists(arboredir):
		fotos = os.listdir(arboredir)
		for fotoname in fotos:
			if np.random.rand() < train_percent / 100.0:
				is_train = True
				splitname = 'train'
			else:
				is_train = False
				splitname = 'val'
			path_in = os.path.join(arboredir, fotoname)
			folder_frame_out = os.path.join(dirout, splitname, arbore)
			if not os.path.exists(folder_frame_out):
				os.makedirs(folder_frame_out)
			path_out_rel = os.path.join(splitname, arbore, fotoname)
			path_out_abs = os.path.join(dirout, path_out_rel)
			copyfile(path_in, path_out_abs)
			if is_train:
				lista_train.append(path_out_rel + ',' + str(arbore_idx))
			else:
				lista_val.append(path_out_rel + ',' + str(arbore_idx))

# Shuffle files lists:
shuffle(lista_train)
shuffle(lista_val)

# Write lists:
with open(path_trainlabels, 'w') as trainlabels:
	for ann in lista_train:
		trainlabels.write(ann + '\n') 
with open(path_vallabels, 'w') as vallabels:
	for ann in lista_val:
		vallabels.write(ann + '\n') 

# Info file:
with open(os.path.join(dirout, 'dataset_info.xml'), 'w') as fid:
	fid.write('<root>\n')
	fid.write('    <format>jpg</format>\n')
	fid.write('    <classes>\n')
	for arbore_idx in range(len(lista_arbores)):
		fid.write('        <class>\n')
		fid.write('            <id>' + str(arbore_idx) + '</id>\n')
		fid.write('            <name>' + lista_arbores[arbore_idx] + '</name>\n')
		fid.write('        </class>\n')
	fid.write('    </classes>\n')
	fid.write('</root>\n')


















