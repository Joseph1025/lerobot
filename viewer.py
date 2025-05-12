import torch
import json
from lerobot.common.policies.pi0.modeling_pi0 import PI0Policy
from lerobot.common.datasets.lerobot_dataset import LeRobotDataset
import h5py

def view_lerobot_dataset():
    """
    
    """
    # Load dataset
    dataset_repo_id = "danaaubakirova/koch_test"
    dataset = LeRobotDataset(dataset_repo_id, episodes=[0])

    # DataLoader
    dataloader = torch.utils.data.DataLoader(
        dataset,
        num_workers=0,
        batch_size=1,
    )

    # Get batch
    batch = next(iter(dataloader))
    print(batch.keys())
    print(batch)

    # Extract dimensions of the batch
    batch_dimensions = {k: v.shape if isinstance(v, torch.Tensor) else None for k, v in batch.items()}

    # Write the batch dimensions to a new JSON file
    with open('batch_dimensions.json', 'w') as f:
        json.dump(batch_dimensions, f, indent=4)

    print("Batch dimensions written to batch_dimensions.json")


def view_h5_file(file_path):
    with h5py.File(file_path, 'r') as f:
        # Dictionary to store dimensions
        dimensions = {}

        def get_dimensions(name, obj):
            if isinstance(obj, h5py.Dataset):
                dimensions[name] = obj.shape
                print(f"Dimensions for dataset {name}: {obj.shape}")

        # Visit all items in the file
        f.visititems(get_dimensions)

        # Write dimensions to a JSON file
        with open('data_dimensions.json', 'w') as json_file:
            json.dump(dimensions, json_file, indent=4)

        print("Data dimensions written to data_dimensions.json")


view_h5_file('data/data.hdf5')
    
