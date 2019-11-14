'''This is an example system created from quality control of blister packed medical pills.'''

from SimpleCV import *
import execnet


def call_python_version(Version, Module, Function, ArgumentList):
    gw = execnet.makegateway("popen//python=python%s" % Version)
    channel = gw.remote_exec("""
        from %s import %s as the_function
        channel.send(the_function(*channel.receive()))
    """ % (Module, Function))
    channel.send(ArgumentList)
    return channel.receive()


class Blister:
    def __init__(self, ima_path):
        self.img = Image(ima_path).scale(320, 240)
        self.hue_peak = self.img.huePeaks()
        self.ima_dist = self.img.hueDistance(self.hue_peak)
        self.imgdistbin = self.ima_dist.invert().threshold(200)
        self.blobs = self.imgdistbin.findBlobs(minsize=1000)

    def count_pills(self):
        result = self.img.sideBySide(self.ima_dist, side='bottom', scale=False)
        result = result.sideBySide(self.imgdistbin, side='right')
        result.show()
        if self.blobs is not None:
            print('Pills detected = ' + str(len(self.blobs)))
            return len(self.blobs)


def run(path):
    result = call_python_version("2.7", "Quality Control", "Blister({}).count_pills".format(path),
                                 [])
    print(result)


if __name__ == '__main__':
    # Blister(ima_path='/Users/eloymarinciudad/Downloads/blister_1.jpg')

    run('/Users/eloymarinciudad/Downloads/blister_1.jpg')
