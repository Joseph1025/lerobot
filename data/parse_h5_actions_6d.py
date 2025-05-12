import h5py
import sys

# def list_h5_structure(file_path):
#     try:
#         with h5py.File(file_path, 'r') as f:
#             def print_structure(name, obj):
#                 print(name)

#             print("HDF5 file structure:")
#             f.visititems(print_structure)

    # except Exception as e:
    #     print(f"An error occurred while listing the file structure: {e}")

def read_root_item(file_path, item_name):
    try:
        with h5py.File(file_path, 'r') as f:
            if item_name not in f:
                print(f"'{item_name}' not found in the root directory.")
                return None

            data = f[item_name][:]
            print(f"Data from root item '{item_name}':")
            print(data)

            # Check the length of each array in the dataset
            if isinstance(data, (list, tuple)) or hasattr(data, '__len__'):
                for idx, item in enumerate(data):
                    print(f"Length of array at index {idx}: {len(item)}")
            return data

    except Exception as e:
        print(f"An error occurred while reading the root item: {e}")
        return None
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python parse_h5_obs.py <file_path>")
        sys.exit(1)

    file_path = sys.argv[1]


    # # List the HDF5 file structure
    # print("\nListing the structure of the HDF5 file...")
    # list_h5_structure(file_path)

    read_root_item(file_path, "actions_6d")

