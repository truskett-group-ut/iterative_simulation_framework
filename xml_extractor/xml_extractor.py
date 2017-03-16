import xml.etree.ElementTree as ET

class XMLExtractor:
    #inital stuff
    def __init__(self):
        return None
    
    #load in the file
    def Parse(self, filename):
        self.tree = ET.parse(filename)
        return None

    #crawls the parse tree according to key directions
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