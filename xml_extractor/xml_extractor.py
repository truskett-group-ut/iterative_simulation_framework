import xml.etree.ElementTree as ET

class XMLExtractor:
    #inital stuff
    def __init__(self):
        return None
    
    #recursively builds a nested dictionary
    def Parse(self, filename):
        self.tree = ET.parse(filename)
        return None

    #converts the xml to a nested dictionary
    def GetText(self, *args):
        root = self.tree.getroot()
        for key in args:
            children = root.findall(key)
            if len(children) == 1:
                root = children[0]
            elif len(children) == 0:
                raise AttributeError(('Key "%s" not found' % key))
            else:
                raise AttributeError(('More that one "%s" key found' % key))
        return root.text