class Factory:
    @staticmethod
    def build_sequence():
        return []


    @staticmethod
    def build_number(string):
        return int(string.strip())


class Loader:
    @staticmethodd
    def parse_format(string, Factory):
        seq = Factory.build_sequence()
        for sub in string.split(","):
            item = Factory.build_number(sub)
            seq.append(item)
        return seq

res = Loader.parse_format("4, 5, -6", Factory)