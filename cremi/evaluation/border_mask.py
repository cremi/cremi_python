import h5py
import numpy as np
import scipy

def create_border_mask(input_data, target, max_dist, background_label,axis=0):
    """
    Overlay a border mask with background_label onto input data.
    A pixel is part of a border if one of its 4-neighbors has different label.
    
    Parameters
    ----------
    input_data : h5py.Dataset or numpy.ndarray - Input data containing neuron ids
    target : h5py.Datset or numpy.ndarray - Target which input data overlayed with border mask is written into.
    max_dist : int or float - Maximum distance from border for pixels to be included into the mask.
    background_label : int - Border mask will be overlayed using this label.
    axis : int - Axis of iteration (perpendicular to 2d images for which mask will be generated)
    """
    sl = [slice(None) for d in xrange(len(target.shape))]

    for z in xrange(target.shape[axis]):
        sl[ axis ] = z
        border = create_border_mask_2d(input_data[tuple(sl)], max_dist)
        target_slice = input_data[tuple(sl)] if isinstance(input_data,h5py.Dataset) else np.copy(input_data[tuple(sl)]) 
        target_slice[border] = background_label
        target[tuple(sl)] = target_slice

def create_and_write_masked_neuron_ids(in_file, out_file, max_dist, background_label, overwrite=False):
    """
    Overlay a border mask with background_label onto input data loaded from in_file and write into out_file.
    A pixel is part of a border if one of its 4-neighbors has different label.
    
    Parameters
    ----------
    in_file : CremiFile - Input file containing neuron ids
    out_file : CremiFile - Output file which input data overlayed with border mask is written into.
    max_dist : int or float - Maximum distance from border for pixels to be included into the mask.
    background_label : int - Border mask will be overlayed using this label.
    overwrite : bool - Overwrite existing data in out_file (True) or do nothing if data is present in out_file (False).
    """
    if ( not in_file.has_neuron_ids() ) or ( (not overwrite) and out_file.has_neuron_ids() ):
        return

    neuron_ids, resolution, offset, comment = in_file.read_neuron_ids()
    comment = ('' if comment is None else comment + ' ') + 'Border masked with max_dist=%f' % max_dist

    path = "/volumes/labels/neuron_ids"
    group_path = "/".join( path.split("/")[:-1] )
    ds_name = path.split("/")[-1]
    if ( out_file.has_neuron_ids() ):
        del out_file.h5file[path]
    if (group_path not in out_file.h5file):
        out_file.h5file.create_group(group_path)
        
    group = out_file.h5file[group_path]
    target = group.create_dataset(ds_name, shape=neuron_ids.shape, dtype=neuron_ids.dtype)
    target.attrs["resolution"] = resolution
    target.attrs["comment"] = comment
    if offset != (0.0, 0.0, 0.0):
        target.attrs["offset"] = offset
	
    create_border_mask(neuron_ids, target, max_dist, background_label)

def create_border_mask_2d(image, max_dist):
    """
    Create binary border mask for image.
    A pixel is part of a border if one of its 4-neighbors has different label.
    
    Parameters
    ----------
    image : numpy.ndarray - Image containing integer labels.
    max_dist : int or float - Maximum distance from border for pixels to be included into the mask.

    Returns
    -------
    mask : numpy.ndarray - Binary mask of border pixels. Same shape as image.
    """
    max_dist = max(max_dist, 0)
    
    padded = np.pad(image, 1, mode='edge')
    
    border_pixels = np.logical_and(
        np.logical_and( image == padded[:-2, 1:-1], image == padded[2:, 1:-1] ),
        np.logical_and( image == padded[1:-1, :-2], image == padded[1:-1, 2:] )
        )

    distances = scipy.ndimage.distance_transform_edt(
        border_pixels,
        return_distances=True,
        return_indices=False
        )

    return distances <= max_dist
    
