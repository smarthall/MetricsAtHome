import PicScreen
import random

class RandomPicScreen(PicScreen.PicScreen):
  def __init__(self, width, height, args):
    args['picture'] = random.choice(args.get('pictures', ['img/sample.jpg']))
    PicScreen.PicScreen.__init__(self, width, height, args)

