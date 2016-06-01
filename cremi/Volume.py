
class Volume:

    def __init__(self, data, resolution = (1.0, 1.0, 1.0), offset = (0.0, 0.0, 0.0), comment = ""):
        self.data = data
        self.resolution = resolution
        self.offset = offset
        self.comment = comment

    def __getitem__(self, location):
        """Get the closest value of this volume to the given location. The 
        location is in world units, relative to the volumes offset.

        This method takes into account the resolution of the volume. An 
        IndexError exception is raised if the location is not contained in this 
        volume.

        To access the raw pixel values, use the `data` attribute.
        """

        i = tuple([ round(location[d]/self.resolution[d]) for d in range(len(location)) ])

        if min(i) >= 0:
            try:
                return self.data[i]
            except IndexError as e:
                raise IndexError("location " + str(location) + " does not lie inside volume: " + str(e))

        raise IndexError("location " + str(location) + " does not lie inside volume")

    def __setitem__(self, location, value):
        """Set the closest value of this volume to the given location. The 
        location is in world units, relative to the volumes offset.

        This method takes into account the resolution of the volume. An 
        IndexError exception is raised if the location is not contained in this 
        volume.

        To access the raw pixel values, use the `data` attribute.
        """

        i = tuple([ round(location[d]/self.resolution[d]) for d in range(len(location)) ])

        if min(i) >= 0:
            try:
                self.data[i] = value
                return
            except IndexError as e:
                raise IndexError("location " + str(location) + " does not lie inside volume: " + str(e))

        raise IndexError("location " + str(location) + " does not lie inside volume")
