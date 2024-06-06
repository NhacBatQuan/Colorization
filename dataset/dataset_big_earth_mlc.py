import argparse
import glob
import time
from typing import Tuple

import numpy as np
import torch
from torch.utils.data import SubsetRandomSampler
import torch.nn as nn

from Colorization.dataset.dataset_big_earth import BigEarthDataset


class BigEarthDatasetMLC(BigEarthDataset):
    def __init__(self, csv_path: str, quantiles: str, random_seed: int, bands: list, bands_indices: list,
                 create_torch_dataset=0, n_samples=100000):
        BigEarthDataset.__init__(self, csv_path, quantiles, random_seed = random_seed, bands=bands, bands_indices=bands_indices,augmentation=1,
                                 create_torch_dataset=0, n_samples=n_samples)

    def __getitem__(self, index: int) -> Tuple[torch.tensor, torch.tensor, torch.tensor]:
        # obtain the right folder
        imgs_file = self.folder_path[index] # [2:-2] # to remove [\ \]
        imgs_file = 'Colorization/dataset/' + imgs_file
        imgs_bands = []
        # load image
        for b in self.bands:
            for filename in glob.iglob(imgs_file+"/*" + b + ".tif"):
                band = self.custom_loader(filename, b, self.quantiles)
                imgs_bands.append(band)
        spectral_img = np.concatenate(imgs_bands, axis=2)
        #them code ben _torch vao
        spectral_img = self.to_tensor(spectral_img)
        spectral_img = torch.squeeze(
            nn.functional.interpolate(input=torch.unsqueeze(spectral_img, dim=0), size=128))
        spectral_img = spectral_img[self.bands_indices]
        # if RGB: invert the indices as it is saved as BGR
        if sum(self.bands_indices) == 3:
            spectral_img = torch.flip(spectral_img, [0])
        # create multi-hot labels vector
        labels_index = list(map(int, self.labels_class[index][1:-1].split(',')))
        labels_class = np.zeros(19)
        labels_class[labels_index] = 1
        return spectral_img, torch.tensor(labels_class)


if __name__ == "__main__":
    argparser = argparse.ArgumentParser(description='BigEarthNetMLC dataset tiff version')
    argparser.add_argument('--csv_filename', type=str,
                           default='BigEarthNet_all_refactored_no_clouds_and_snow_server.csv',
                           required=True, help='csv containing dataset paths')
    argparser.add_argument('--n_samples', type=int, default=3000, help='Number of samples to create the csv file')

    args = argparser.parse_args()
    # Dataset definition
    big_earth = BigEarthDatasetMLC(csv_path=args.csv_filename, quantiles='../../Colorization/dataset/quantiles_590326.json',
                                   random_seed=19,
                                   bands=["B01", "B02", "B03", "B04", "B05", "B06", "B07", "B08", "B8A", "B09", "B11"
                                          "B12"], bands_indices=[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                                   n_samples=args.n_samples)
    # dataset split
    train_idx, val_idx, test_idx = big_earth.split_dataset(0.2, 0.4)
    # dataset sampler
    train_sampler = SubsetRandomSampler(train_idx)
    val_sampler = SubsetRandomSampler(val_idx)
    test_sampler = SubsetRandomSampler(test_idx)
    # dataset loader
    train_loader = torch.utils.data.DataLoader(big_earth, batch_size=16,
                                               sampler=train_sampler, num_workers=4)
    test_loader = torch.utils.data.DataLoader(big_earth, batch_size=1,
                                              sampler=test_sampler, num_workers=0)
    start_time = time.time()

    for idx, (spectral_img, labels) in enumerate(train_loader):
        print(idx)

    print("time: ", time.time() - start_time)
