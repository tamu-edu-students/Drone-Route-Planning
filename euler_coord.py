class euler_coord(object):
    def __init__(self, la, lo, node_id):
        self.latitude = la
        self.longitude = lo
        self.node_id = node_id

    def __str__(self):
        return "( %s, %s ) @ %s " % (
        self.latitude, self.longitude, self.node_id)

    def get_lat(self):
        return self.latitude

    def get_long(self):
        return self.longitude

    def get_node_id(self):
        return self.node_id

