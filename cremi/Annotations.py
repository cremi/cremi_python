class Annotations:

    def __init__(self, offset = (0.0, 0.0, 0.0)):

        self.__types = {}
        self.__locations = {}
        self.comments = {}
        self.pre_post_partners = []
        self.offset = offset

    def __check(self, id):
        if not id in self.__types.keys():
            raise "there is no annotation with id " + str(id)

    def add_annotation(self, id, type, location):
        """Add a new annotation.

        Parameters
        ----------

            id: int
                The ID of the new annotation.

            type: string
                A string denoting the type of the annotation. Use 
                "presynaptic_site" or "postsynaptic_site" for pre- and 
                post-synaptic annotations, respectively.

            location: tuple, float
                The location of the annotation, relative to the offset.
        """

        self.__types[id] = type.encode('utf8')
        self.__locations[id] = location

    def add_comment(self, id, comment):
        """Add a comment to an annotation.
        """

        self.__check(id)
        self.comments[id] = comment.encode('utf8')

    def set_pre_post_partners(self, pre_id, post_id):
        """Mark two annotations as pre- and post-synaptic partners.
        """

        self.__check(pre_id)
        self.__check(post_id)
        self.pre_post_partners.append((pre_id, post_id))

    def ids(self):
        """Get the ids of all annotations.
        """

        return self.__types.keys()

    def types(self):
        """Get the types of all annotations.
        """

        return self.__types.values()

    def locations(self):
        """Get the locations of all annotations. Locations are in world units, 
        relative to the offset.
        """

        return self.__locations.values()

    def get_annotation(self, id):
        """Get the type and location of an annotation by its id.
        """

        self.__check(id)
        return (self.__types[id], self.__locations[id])
