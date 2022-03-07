import json
<<<<<<< HEAD
from pathlib import Path
# import os.path as osp
=======
import os
import os.path as osp
from typing import Callable, List, Optional
>>>>>>> 4557254c849eda62ce1860a56370eb4a54aa76dd

import numpy as np
import scipy.sparse as sp
import torch

from torch_geometric.data import Data, InMemoryDataset, download_url


class AmazonProducts(InMemoryDataset):
    r"""The Amazon dataset from the `"GraphSAINT: Graph Sampling Based
    Inductive Learning Method" <https://arxiv.org/abs/1907.04931>`_ paper,
    containing products and its categories.

    Args:
        root (string): Root directory where the dataset should be saved.
        transform (callable, optional): A function/transform that takes in an
            :obj:`torch_geometric.data.Data` object and returns a transformed
            version. The data object will be transformed before every access.
            (default: :obj:`None`)
        pre_transform (callable, optional): A function/transform that takes in
            an :obj:`torch_geometric.data.Data` object and returns a
            transformed version. The data object will be transformed before
            being saved to disk. (default: :obj:`None`)

    Stats:
        .. list-table::
            :widths: 10 10 10 10
            :header-rows: 1

            * - #nodes
              - #edges
              - #features
              - #classes
            * - 1,569,960
              - 264,339,468
              - 200
              - 107
    """
    url = 'https://docs.google.com/uc?export=download&id={}&confirm=t'

    adj_full_id = '17qhNA8H1IpbkkR-T2BmPQm8QNW5do-aa'
    feats_id = '10SW8lCvAj-kb6ckkfTOC5y0l8XXdtMxj'
    class_map_id = '1LIl4kimLfftj4-7NmValuWyCQE8AaE7P'
    role_id = '1npK9xlmbnjNkV80hK2Q68wTEVOFjnt4K'

    def __init__(self, root: str, transform: Optional[Callable] = None,
                 pre_transform: Optional[Callable] = None):
        super().__init__(root, transform, pre_transform)
        self.data, self.slices = torch.load(self.processed_paths[0])

    @property
    def raw_file_names(self) -> List[str]:
        return ['adj_full.npz', 'feats.npy', 'class_map.json', 'role.json']

    @property
    def processed_file_names(self) -> str:
        return 'data.pt'

    def download(self):
<<<<<<< HEAD
        from google_drive_downloader import GoogleDriveDownloader as gdd

        # path = osp.join(self.raw_dir, 'adj_full.npz')
        path = Path.joinpath(Path(self.raw_dir), 'adj_full.npz')
        gdd.download_file_from_google_drive(self.adj_full_id, path)

        # path = osp.join(self.raw_dir, 'feats.npy')
        path = Path.joinpath(Path(self.raw_dir), 'feats.npy')
        gdd.download_file_from_google_drive(self.feats_id, path)

        # path = osp.join(self.raw_dir, 'class_map.json')
        path = Path.joinpath(Path(self.raw_dir), 'class_map.json')
        gdd.download_file_from_google_drive(self.class_map_id, path)

        # path = osp.join(self.raw_dir, 'role.json')
        path = Path.joinpath(Path(self.raw_dir), 'role.json')
        gdd.download_file_from_google_drive(self.role_id, path)
=======
        path = download_url(self.url.format(self.adj_full_id), self.raw_dir)
        os.rename(path, osp.join(self.raw_dir, 'adj_full.npz'))

        path = download_url(self.url.format(self.feats_id), self.raw_dir)
        os.rename(path, osp.join(self.raw_dir, 'feats.npy'))

        path = download_url(self.url.format(self.class_map_id), self.raw_dir)
        os.rename(path, osp.join(self.raw_dir, 'class_map.json'))

        path = download_url(self.url.format(self.role_id), self.raw_dir)
        os.rename(path, osp.join(self.raw_dir, 'role.json'))
>>>>>>> 4557254c849eda62ce1860a56370eb4a54aa76dd

    def process(self):
        f = np.load(Path.joinpath(Path(self.raw_dir), 'adj_full.npz'))
        adj = sp.csr_matrix((f['data'], f['indices'], f['indptr']), f['shape'])
        adj = adj.tocoo()
        row = torch.from_numpy(adj.row).to(torch.long)
        col = torch.from_numpy(adj.col).to(torch.long)
        edge_index = torch.stack([row, col], dim=0)

        x = np.load(Path.joinpath(Path(self.raw_dir), 'feats.npy'))
        x = torch.from_numpy(x).to(torch.float)

        ys = [-1] * x.size(0)
        with open(Path.joinpath(Path(self.raw_dir), 'class_map.json')) as f:
            class_map = json.load(f)
            for key, item in class_map.items():
                ys[int(key)] = item
        y = torch.tensor(ys)

        with open(Path.joinpath(Path(self.raw_dir), 'role.json')) as f:
            role = json.load(f)

        train_mask = torch.zeros(x.size(0), dtype=torch.bool)
        train_mask[torch.tensor(role['tr'])] = True

        val_mask = torch.zeros(x.size(0), dtype=torch.bool)
        val_mask[torch.tensor(role['va'])] = True

        test_mask = torch.zeros(x.size(0), dtype=torch.bool)
        test_mask[torch.tensor(role['te'])] = True

        data = Data(x=x, edge_index=edge_index, y=y, train_mask=train_mask,
                    val_mask=val_mask, test_mask=test_mask)

        data = data if self.pre_transform is None else self.pre_transform(data)

        torch.save(self.collate([data]), self.processed_paths[0])
