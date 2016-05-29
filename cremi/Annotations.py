class Annotations:

    def __init__(self):

        self.__types = {}
        self.__locations = {}
        self.comments = {}
        self.pre_post_partners = []

    def __check(self, id):
        if not id in self.__types.keys():
            raise "there is no annotation with id " + str(id)

    def add_annotation(self, id, type, location):

        self.__types[id] = type.encode('utf8')
        self.__locations[id] = location

    def add_comment(self, id, comment):

        self.__check(id)
        self.comments[id] = comment.encode('utf8')

    def set_pre_post_partners(self, pre_id, post_id):

        self.__check(pre_id)
        self.__check(post_id)
        self.pre_post_partners.append((pre_id, post_id))

    def ids(self):

        return self.__types.keys()

    def types(self):

        return self.__types.values()

    def locations(self):

        return self.__locations.values()

    def get_annotation(self, id):

        self.__check(id)
        return (self.__types[id], self.__locations[id])
