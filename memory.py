import math
import sys
import Tkinter
import Image, ImageTk, ImageDraw
import tkFont
import tkSimpleDialog
import tkMessageBox
import tkFileDialog
from pydega import *

columns = 32
lines = 28
size = 8
im_width = columns * size
im_height = 24 * size


colors = {
    0x00: (0, 0, 192),
    0x35: (0, 0, 192),
    0x36: (0, 0, 192),
    0x37: (0, 0, 192),
    0x38: (0, 0, 192),
    0x47: (0, 0, 192),  # rock corner void

    # clouds
    0x27: (0, 64, 192),
    0x28: (0, 64, 192),
    0x29: (0, 64, 192),
    0x2a: (0, 64, 192),
    0x2b: (0, 64, 192),
    0x2c: (0, 64, 192),
    0x2d: (0, 64, 192),
    0x2e: (0, 64, 192),

    # Bag of Money!
    0x25: (255, 255, 255),
    0x26: (255, 255, 255),

    # star box
    0x09: (192, 192, 0),
    0x0a: (192, 192, 0),
    0x0b: (192, 192, 0),
    0x0c: (192, 192, 0),

    # question box
    0x05: (192, 64, 192),
    0x06: (192, 64, 192),
    0x07: (192, 64, 192),
    0x08: (192, 64, 192),

    # death box
    0x01: (64, 64, 64),
    0x02: (64, 64, 64),
    0x03: (64, 64, 64),
    0x04: (64, 64, 64),

    # skull box
    0x1D: (255, 64, 128),
    0x1E: (255, 64, 128),
    0x1F: (255, 64, 128),
    0x20: (255, 64, 128),

    # grass
    0x41: (0, 128, 0),
    0x42: (0, 128, 0),
    0x45: (0, 128, 0), # Tip corner
    0x46: (0, 128, 0), # Pre-Tip corner

    # ground
    0x3d: (128, 64, 0),
    0x3e: (128, 64, 0),
    0x3f: (128, 64, 0),
    0x40: (128, 64, 0),
    0x43: (128, 64, 0),
    0x44: (128, 64, 0),
    0x48: (128, 64, 0),
    0x49: (128, 64, 0), # corner solid
    0x4a: (128, 64, 0), # between corners
    0x4b: (128, 64, 0), # plain close to a...
    0x4c: (128, 64, 0), # ...straight sky.
    0x4e: (128, 64, 0), # same...
    0x4d: (128, 64, 0), # same...

    # rock
    0x39: (192, 192, 128),
    0x3a: (192, 192, 128),
    0x3b: (192, 192, 128),
    0x3c: (192, 192, 128),

    # water
    0x78: (0, 128, 192),
    0x79: (0, 128, 192),
    0x7a: (0, 128, 192),
    0x7b: (0, 128, 192),
    0x88: (20, 148, 212), # top
    0x89: (20, 148, 212), # top

    # sea weed
    0x8a: (0, 192, 128),
    0x8b: (0, 192, 128),
    0x8c: (0, 192, 128),
    0x8d: (0, 192, 128),
    0x8e: (0, 192, 128),
    0x8f: (0, 192, 128),

    0x90: (0, 192, 128),
    0x91: (0, 192, 128),
    0x92: (0, 192, 128),
    0x93: (0, 192, 128),
    0x94: (0, 192, 128),
    0x95: (0, 192, 128),

    # sea blocks
    0x80: (0, 192, 0),
    0x81: (0, 192, 0),
    0x82: (0, 192, 0),
    0x83: (0, 192, 0),
    0x84: (0, 192, 0),
    0x85: (0, 192, 0),
    0x86: (0, 192, 0),
    0x87: (0, 192, 0),

    # breakable sea blocks
    0x7c: (132, 192, 96),
    0x7d: (132, 192, 96),
    0x7e: (132, 192, 96),
    0x7f: (132, 192, 96),

    # test
    # 0x88: (255, 0, 0),
    # 0x89: (255, 0, 0),
}

def askhex(prompt, validate = lambda v: None):
    v = None
    while v == None:
        s = tkSimpleDialog.askstring("Enter value", prompt+"\nFor hexadecimal prefix with 0x")
        if s == None:
            break
        try:
            v = int(eval(s))
            validate(v)
        except:
            tkMessageBox.showerror("Invalid Value", "Could not parse value: %s (%s)" % (s, sys.exc_info()[1]))
            v = None
    return v

class TerrainView(Tkinter.Canvas):
    
    def __init__(self, master, realdata, offset):
        self.realdata = realdata
        self.offset = offset
        self.scroll = 0
        self.previous_types = None

        Tkinter.Canvas.__init__(self, master, width=im_width, height=im_height,
                background="white")

        self.tkimage = ImageTk.PhotoImage("RGB", (im_width, im_height))
        self.image = self.create_image((im_width / 2, im_height / 2), 
                image=self.tkimage)

        self.refresh()

    def get_sprite_types(self):
        scroll = math.floor(self.realdata[0x00be] / 8.0)
        offset = self.offset + scroll * columns * 2
        start = offset
        stop = offset + (lines - scroll) * columns * 2
        chunk_a = [self.realdata[i] for i in range(start, stop, 2)]

        start = self.offset
        stop = self.offset + scroll * columns * 2
        chunk_b = [self.realdata[i] for i in range(start, stop, 2)]

        return (chunk_a + chunk_b)[:(lines * columns)]

    def get_color_from_type(self, type):
        if type not in colors:
            print("UNKNOWN: 0x%02X" % type)
            type = 0
        return colors[type]

    def refresh(self):
        sprite_types = self.get_sprite_types()
        if self.previous_types == sprite_types:
            return

        self.im = Image.new("RGB", (im_width, im_height))
        draw = ImageDraw.Draw(self.im)
        for y in range(lines):
            for x in range(columns):
                col = self.get_color_from_type(sprite_types[y * columns + x])
                draw.rectangle([x * size, y * size, x * size + size, y * size + size], fill=col)
        del draw
        self.tkimage.paste(self.im)
        self.previous_types = sprite_types

class HexView(Tkinter.Canvas):

    def getdata(self):
        return getattr(self.data[0], self.data[1])

    def userchange(self, index, event):
        v = askhex("Please enter new value for address %04X" % (self.offset+index))
        if v != None:
            self.realdata[index] = v
            x = self.canvasx(event.x)
            y = self.canvasy(event.y)
            self.itemconfig(self.find_closest(x, y), text=("%02X" % v))
        
    def builditems(self):
        data = self.getdata()
        width = self.fwidth*(4 + self.columns*3) # header + data columns
        height = self.fheight*len(self.offsets)
        self.configure(scrollregion=(0, 0, width, height))

        for item in self.colitems:
            self.delete(item)
        for item in self.hexitems:
            self.delete(item)
        self.colitems = []
        self.hexitems = []
        for o in range(len(self.offsets)):
            off = self.offsets[o]
            y = o*self.fheight
            self.colitems.append(self.create_text((0, y), anchor=Tkinter.NW, text=("%04X" % (self.offset+off)), font=self.font))
            for i in range(self.columns):
                uc = lambda addr: lambda e: self.userchange(addr, e)
                text = self.create_text((self.fwidth*(5+3*i), y), anchor=Tkinter.NW, text=("%02X" % data[off+i]), font=self.font)
                self.tag_bind(text, "<Button-1>", uc(off+i))
                self.hexitems.append(text)
        self.olddata = data

    def updateitems(self):
        data = self.getdata()
        for o in range(len(self.offsets)):
            off = self.offsets[o]
            for i in range(self.columns):
                if self.olddata[off+i] <> data[off+i]:
                    self.itemconfig(self.hexitems[o*self.columns+i], text=("%02X" % data[off+i]))
        self.olddata = data

    def __init__(self, master, offsets, data, realdata, columns, offset=0):
        self.font = tkFont.Font(family="Courier",size=12)

        self.fwidth = self.font.measure("A")
        self.fheight = self.font.metrics("linespace")

        width = self.fwidth*(4 + columns*3) # header + data columns
        height = self.fheight*len(offsets)

        Tkinter.Canvas.__init__(self, master, width=width,
                height=self.fheight*16, background="white",
            scrollregion=(0, 0, width, height))

        self.offsets = offsets
        self.data = data
        self.realdata = realdata
        self.columns = columns
        self.offset = offset

        self.colitems = []
        self.hexitems = []
        self.builditems()

class Trainer:

    def getdata(self):
        return getattr(self.data[0], self.data[1])

    def __init__(self, data):
        self.data = data
        ddata = self.getdata()
        self.olddata = ddata
        self.addresses = range(len(ddata))

    def reset(self):
        data = self.getdata()
        self.olddata = data
        self.addresses = range(len(data))

    def apply(self, fn):
        data = self.getdata()
        self.addresses = filter(lambda a: fn(data[a], self.olddata[a]), self.addresses)
        self.olddata = data

    def gt(self):
        self.apply(lambda x,y: x>y)

    def gte(self):
        self.apply(lambda x,y: x>=y)

    def lt(self):
        self.apply(lambda x,y: x<y)

    def lte(self):
        self.apply(lambda x,y: x<=y)

    def eq(self):
        self.apply(lambda x,y: x==y)

    def ne(self):
        self.apply(lambda x,y: x<>y)

    def eqv(self, v):
        self.apply(lambda x,y: x==v)

    def nev(self, v):
        self.apply(lambda x,y: x<>v)


class MemoryViewer:

    def __init__(self, master):
        # self.frame = Frame(master)
        # self.frame.pack()

        self.frame_ram = tuple(dega.ram)
        self.frame_update = False

        self.frame = master

        self.ramtrain = Trainer((self, "frame_ram"))
        dp = lambda fn: lambda: self.doprint(fn)
        dpp = lambda fn: lambda: self.doprintprompt(fn)

        self.trainframe = Tkinter.Frame(master)
        self.trainframe.pack(side=Tkinter.BOTTOM)

        l = Tkinter.Label(self.trainframe, text="Trainer:")
        l.pack(side=Tkinter.LEFT)

        b = Tkinter.Button(self.trainframe, text="=", command=dp(self.ramtrain.eq))
        b.pack(side=Tkinter.LEFT)

        b = Tkinter.Button(self.trainframe, text="<>", command=dp(self.ramtrain.ne))
        b.pack(side=Tkinter.LEFT)

        b = Tkinter.Button(self.trainframe, text="<", command=dp(self.ramtrain.lt))
        b.pack(side=Tkinter.LEFT)

        b = Tkinter.Button(self.trainframe, text="<=", command=dp(self.ramtrain.lte))
        b.pack(side=Tkinter.LEFT)

        b = Tkinter.Button(self.trainframe, text=">", command=dp(self.ramtrain.gt))
        b.pack(side=Tkinter.LEFT)

        b = Tkinter.Button(self.trainframe, text=">=", command=dp(self.ramtrain.gte))
        b.pack(side=Tkinter.LEFT)

        b = Tkinter.Button(self.trainframe, text="= value", command=dpp(self.ramtrain.eqv))
        b.pack(side=Tkinter.LEFT)

        b = Tkinter.Button(self.trainframe, text="<> value", command=dpp(self.ramtrain.nev))
        b.pack(side=Tkinter.LEFT)

        b = Tkinter.Button(self.trainframe, text="Reset", command=dp(self.ramtrain.reset))
        b.pack(side=Tkinter.LEFT)

        b = Tkinter.Button(self.trainframe, text="Add Watch", command=self.addwatch)
        b.pack(side=Tkinter.LEFT)

        b = Tkinter.Button(self.trainframe, text="Save List", command=self.savelist)
        b.pack(side=Tkinter.LEFT)

        b = Tkinter.Button(self.trainframe, text="Load List", command=self.loadlist)
        b.pack(side=Tkinter.LEFT)

        self.tv = TerrainView(self.frame, realdata=dega.ram, offset=0x0800)
        self.tv.pack(side=Tkinter.LEFT, fill=Tkinter.BOTH, expand=1)

        self.hv = HexView(self.frame, offsets=range(0, len(self.frame_ram), 16),
                data=(self, "frame_ram"), realdata=dega.ram, columns=16,
                offset=0xc000)
        self.hv.pack(side=Tkinter.LEFT, fill=Tkinter.BOTH, expand=1)

        self.sb = Tkinter.Scrollbar(self.frame, orient=Tkinter.VERTICAL)
        self.sb.pack(side=Tkinter.LEFT, fill=Tkinter.Y)

        self.hv['yscrollcommand'] = self.sb.set
        self.sb['command'] = self.hv.yview

        self.wc = Tkinter.Label(self.frame, text="8192 matches")
        self.wc.pack(side=Tkinter.TOP)

        self.wv = HexView(self.frame, offsets=[], data=(self, "frame_ram"), 
                realdata=dega.ram, columns=1, offset=0xc000)
        self.wv.pack(side=Tkinter.LEFT, fill=Tkinter.Y)

        self.sb2 = Tkinter.Scrollbar(self.frame, orient=Tkinter.VERTICAL)
        self.sb2.pack(side=Tkinter.RIGHT, fill=Tkinter.Y)

        self.wv['yscrollcommand'] = self.sb2.set
        self.sb2['command'] = self.wv.yview

        self.frameskip = 3
        self.curframe = 0

        dega.postframe = self.post_frame
        self.update_controls()

    def doprint(self, fn):
        fn()
        if len(self.ramtrain.addresses) < 128:
            self.wv.offsets = self.ramtrain.addresses
        else:
            self.wv.offsets = []
        self.wc['text'] = "%d matches" % len(self.ramtrain.addresses)
        self.wv.builditems()

    def doprintprompt(self, fn):
        v = askhex("Please enter value to compare memory to")
        if v != None:
            self.doprint(lambda: fn(v))

    def ramcheck(self, v):
        if v < 0xC000 or v >= 0xDFFF:
            raise Exception, "value outside of RAM range"

    def addwatch(self):
        v = askhex("Please enter RAM address to watch", self.ramcheck)
        if v != None:
            if len(self.ramtrain.addresses) >= 128:
                self.ramtrain.addresses = []
            self.ramtrain.addresses.append(v-0xC000)
            self.doprint(lambda: None)

    def savelist(self):
        WriteFileName = tkFileDialog.asksaveasfilename()
        WriteFile = open(WriteFileName, "w")
        print >> WriteFile, self.ramtrain.addresses
        WriteFile.close()

    def loadlist(self):
        self.ramtrain.addresses = []
        ReadFileName = tkFileDialog.askopenfilename()
        ReadFile = open(ReadFileName, "r")
        invalue = eval(ReadFile.readline())
        for s in invalue:
            self.ramtrain.addresses.append(s)
        self.doprint(lambda: None)
        ReadFile.close()

    def update_controls(self):
        self.frame.after(100, self.update_controls)
        if dega.exiting:
            sys.exit(0)
        if self.frame_update:
            self.frame_update = False
            self.hv.updateitems()
            self.wv.updateitems()
            self.tv.refresh()
    
    def post_frame(self):
        self.frame_ram = tuple(dega.ram)
        self.frame_update = True

root = Tkinter.Tk()
app = MemoryViewer(root)
root.mainloop()
