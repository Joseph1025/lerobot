import h5py
import shutil

# Open the original HDF5 file in read mode
with h5py.File('usb.hdf5', 'r') as original_file:
    # Access the 'data' group
    data_group = original_file['data']
    
    # Iterate over each item in the 'data' group
    for demo_name, demo_group in data_group.items():
        # Define the new file name for each demo
        new_file_name = f'{demo_name}.h5'
        
        # Create a new HDF5 file for the current demo
        with h5py.File(new_file_name, 'w') as new_file:
            # Copy the 'obs' dataset from the original to the new file
            # original_file.copy(demo_group['obs'], new_file, 'obs')
            
            # If there are other datasets or attributes to copy, handle them here
            # For example, to copy all datasets within the demo group:
            for item_name, item in demo_group.items():
                original_file.copy(item, new_file, item_name)
            
            # To copy attributes from the demo group to the new file
            for attr_name, attr_value in demo_group.attrs.items():
                new_file.attrs[attr_name] = attr_value