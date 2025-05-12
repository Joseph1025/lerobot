import h5py
import sys

def list_action_dict_items(file_path):
    try:
        with h5py.File(file_path, 'r') as f:
            if 'action_dict' not in f:
                print("The file does not contain an 'action_dict' group.")
                return []

            action_dict_group = f['action_dict']
            available_items = list(action_dict_group.keys())
            print("Available items in 'action_dict':")
            for item in available_items:
                print(f"  - {item}")
            return available_items

    except Exception as e:
        print(f"An error occurred while reading the file: {e}")
        return []

def read_action_dict_item(file_path, item_name):
    try:
        with h5py.File(file_path, 'r') as f:
            if 'action_dict' not in f:
                print("The file does not contain an 'action_dict' group.")
                return None

            obs_group = f['action_dict']
            if item_name not in obs_group:
                print(f"'{item_name}' not found in 'obs'.")
                return None

            data = obs_group[item_name][:]
            print(f"Data from '{item_name}':")
            print(data)
            return data

    except Exception as e:
        print(f"An error occurred while reading the file: {e}")
        return None

# def list_h5_structure(file_path):
#     try:
#         with h5py.File(file_path, 'r') as f:
#             def print_structure(name, obj):
#                 print(name)

#             print("HDF5 file structure:")
#             f.visititems(print_structure)

    # except Exception as e:
    #     print(f"An error occurred while listing the file structure: {e}")
        
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python parse_h5_obs.py <file_path>")
        sys.exit(1)

    file_path = sys.argv[1]

    print(f"Reading H5 file: {file_path}\n")
    available_items = list_action_dict_items(file_path)

    if available_items:
        print("\nYou can read data for any of the following items.")
        print("Enter the name of the item you want to read (or 'exit' to quit):")

        while True:
            item_name = input("Item name: ").strip()
            if item_name.lower() == 'exit':
                print("Exiting.")
                break
            if item_name in available_items:
                read_action_dict_item(file_path, item_name)
            else:
                print(f"Invalid item name. Available items: {available_items}")

    # # List the HDF5 file structure
    # print("\nListing the structure of the HDF5 file...")
    # list_h5_structure(file_path)
