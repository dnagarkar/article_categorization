from os.path import dirname
from os.path import join
from os.path import exists
from os.path import expanduser
from os.path import isdir
from os import listdir
from os import makedirs
import numpy as np

from sklearn.datasets.base import Bunch
from sklearn.utils import check_random_state

def load_files_edited(container_path, categories=None, load_content=True, shuffle=True, encoding=None, random_state=0, ignore_files=None):
    target = []
    target_names = []
    filenames = []

    folders = [f for f in sorted(listdir(container_path))
               if isdir(join(container_path, f))]

    if categories is not None:
        folders = [f for f in folders if f in categories]

    for label, folder in enumerate(folders):
        target_names.append(folder)
        folder_path = join(container_path, folder)
        documents = [ join(folder_path, d)
                     for d in sorted(listdir(folder_path)) if ignore_files is not None and d not in ignore_files ]
        target.extend(len(documents) * [label])
        filenames.extend(documents)

    # convert to array for fancy indexing
    filenames = np.array(filenames)
    target = np.array(target)

    if shuffle:
        random_state = check_random_state(random_state)
        indices = np.arange(filenames.shape[0])
        random_state.shuffle(indices)
        filenames = filenames[indices]
        target = target[indices]

    if load_content:
        data = []
        for filename in filenames:
            with open(filename, 'rb') as f:
                data.append(f.read())
        if encoding is not None:
            #data = [d.decode(encoding, decode_error) for d in data]
            #tries 2 types of common encoding for a more robust load_files
            for d in range(0, len(data)):
                try:
                    data[d] = data[d].decode(encoding, "strict")
                except ValueError:
                    if(encoding== 'uft-8'):
                        data[d] = data[d].decode('ISO-8859-2', "strict")
                    else:
                        data[d] = data[d].decode('uft-8', "strict")

        return Bunch(data=data,
                     filenames=filenames,
                     target_names=target_names,
                     target=target)

    return Bunch(filenames=filenames,
                 target_names=target_names,
                 target=target)