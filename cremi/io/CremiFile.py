import h5py
import numpy as np
from .. import Annotations

class CremiFile(object):

    def __init__(self, filename, mode):

        self.h5file = h5py.File(filename, mode)

        if mode == "w" or mode == "a":
            self.h5file["/"].attrs["file_format"] = "0.2"

    def __create_group(self, group):

        path = "/"
        for d in group.split("/"):
            path += d + "/"
            try:
                self.h5file.create_group(path)
            except ValueError:
                pass

    def __write_volume(self, volume, ds_name, resolution, offset, dtype, comment):

        self.__create_group("/".join(ds_name.split("/")[:-1]))
        self.h5file.create_dataset(ds_name, data=volume, dtype=dtype)
        self.h5file[ds_name].attrs["resolution"] = resolution
        if comment is not None:
            self.h5file[ds_name].attrs["comment"] = str(comment)
        if offset != (0.0, 0.0, 0.0):
            self.h5file[ds_name].attrs["offset"] = offset

    def __read_volume(self, ds_name):

        volume = self.h5file[ds_name]
        resolution = self.h5file[ds_name].attrs["resolution"]
        offset = (0.0, 0.0, 0.0)
        if "offset" in self.h5file[ds_name].attrs:
            offset = self.h5file[ds_name].attrs["offset"]
        comment = None
        if "comment" in self.h5file[ds_name].attrs:
            comment = self.h5file[ds_name].attrs["comment"]

        return (volume, resolution, offset, comment)

    def write_raw(self, raw, resolution, comment = None):
        """Write a raw volume with the given resolution.
        The resolution is the size of a voxel (depth, height, width) in nm.
        Optionally, a comment string can be attached.
        """

        self.__write_volume(raw, "/volumes/raw", resolution, (0, 0, 0), np.uint8, comment)

    def write_neuron_ids(self, neuron_ids, resolution, offset = (0.0, 0.0, 0.0), comment = None):
        """Write a volume of segmented neurons with the given resolution.
        The resolution is the size of a voxel (depth, height, width) in nm.
        Optionally, an offset in nm (relative to (0,0,0) of the raw volume) and a comment string can be given.
        """

        self.__write_volume(neuron_ids, "/volumes/labels/neuron_ids", resolution, offset, np.uint64, comment)

    def write_clefts(self, clefts, resolution, offset = (0.0, 0.0, 0.0), comment = None):
        """Write a volume of segmented synaptic clefts with the given resolution.
        The resolution is the size of a voxel (depth, height, width) in nm.
        Optionally, an offset in nm (relative to (0,0,0) of the raw volume) and a comment string can be given.
        """

        self.__write_volume(clefts, "/volumes/labels/clefts", resolution, offset, np.uint64, comment)

    def write_annotations(self, annotations, offset = (0.0, 0.0, 0.0)):
        """Write pre- and post-synaptic site annotations.
        Optionally, an offset in nm (relative to (0,0,0) of the raw volume) can be given.
        """

        if len(annotations.ids()) == 0:
            return

        self.__create_group("/annotations")
        if offset != (0.0, 0.0, 0.0):
            self.h5file["/annotations"].attrs["offset"] = offset

        self.h5file.create_dataset("/annotations/ids", data=annotations.ids(), dtype=np.uint64)
        self.h5file.create_dataset("/annotations/types", data=annotations.types(), dtype=h5py.special_dtype(vlen=unicode), compression="gzip")
        self.h5file.create_dataset("/annotations/locations", data=annotations.locations(), dtype=np.double)

        if len(annotations.comments) > 0:
            self.__create_group("/annotations/comments")
            self.h5file.create_dataset("/annotations/comments/target_ids", data=annotations.comments.keys(), dtype=np.uint64)
            self.h5file.create_dataset("/annotations/comments/comments", data=annotations.comments.values(), dtype=h5py.special_dtype(vlen=unicode))

        if len(annotations.pre_post_partners) > 0:
            self.__create_group("/annotations/presynaptic_site")
            self.h5file.create_dataset("/annotations/presynaptic_site/partners", data=annotations.pre_post_partners, dtype=np.uint64)

    def read_raw(self):
        """Read the raw volume.
        Returns a tuple (volume, resolution, offset, comment).
        """

        return self.__read_volume("/volumes/raw")

    def read_neuron_ids(self):
        """Read the volume of segmented neurons.
        Returns a tuple (volume, resolution, offset, comment).
        """

        return self.__read_volume("/volumes/labels/neuron_ids")

    def read_clefts(self):
        """Read the volume of segmented synaptic clefts.
        Returns a tuple (volume, resolution, offset, comment).
        """

        return self.__read_volume("/volumes/labels/clefts")

    def read_annotations(self):
        """Read pre- and post-synaptic site annotations.
        """

        annotations = Annotations()
        offset = (0.0, 0.0, 0.0)

        if not "/annotations" in self.h5file:
            return (annotations, offset)

        if "offset" in self.h5file["/annotations"].attrs:
            offset = self.h5file["/annotations"].attrs["offset"]

        ids = self.h5file["/annotations/ids"]
        types = self.h5file["/annotations/types"]
        locations = self.h5file["/annotations/locations"]
        for i in range(len(ids)):
            annotations.add_annotation(ids[i], types[i], locations[i])

        if "comments" in self.h5file["/annotations"]:
            ids = self.h5file["/annotations/comments/target_ids"]
            comments = self.h5file["/annotations/comments/comments"]
            for (id, comment) in zip(ids, comments):
                annotations.add_comment(id, comment)

        if "presynaptic_site/partners" in self.h5file["/annotations"]:
            pre_post = self.h5file["/annotations/presynaptic_site/partners"]
            for (pre, post) in pre_post:
                annotations.set_pre_post_partners(pre, post)

        return (annotations, offset)

    def close(self):

        self.h5file.close()
