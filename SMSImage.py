from PIL import Image, ImageDraw
import math

version = "0"

control = ["ü", "å", "É", "/", "?", "O", "§", "o", "à"]

chars = {
	'@': [0, 128, 0],
	'Δ': [0, 0, 128],
	'0': [0, 128, 128],
	'¡': [128, 128, 128],
	'P': [0, 255, 0],
	'¿': [0, 0, 255],
	'£': [0, 255, 255],
	'_': [0, 0, 135],
	'!': [0, 0, 215],
	'1': [0, 95, 0],
	'A': [0, 95, 135],
	'Q': [0, 95, 215],
	'a': [0, 135, 0],
	'q': [0, 135, 135],
	'$': [0, 175, 0],
	'Φ': [0, 175, 135],
	'2': [0, 175, 215],
	'B': [0, 215, 0],
	'R': [0, 215, 135],
	'b': [0, 215, 215],
	'r': [0, 255, 0],
	'¥': [0, 255, 215],
	'Γ': [95, 0, 0],
	'#': [95, 0, 135],
	'3': [95, 0, 215],
	'C': [95, 95, 0],
	'S': [95, 95, 135],
	'c': [95, 95, 215],
	's': [95, 135, 135],
	'è': [95, 135, 215],
	'Λ': [95, 175, 0],
	'¤': [95, 175, 135],
	'4': [95, 175, 215],
	'D': [95, 215, 0],
	'T': [95, 215, 135],
	'd': [95, 255, 0],
	't': [95, 255, 135],
	'é': [95, 255, 215],
	'Ω': [135, 0, 0],
	'%': [135, 0, 135],
	'5': [135, 0, 215],
	'E': [135, 95, 0],
	'U': [135, 95, 215],
	'e': [135, 135, 0],
	'u': [135, 135, 135],
	'ù': [135, 135, 215],
	'Π': [135, 175, 0],
	'&': [135, 175, 135],
	'6': [135, 175, 215],
	'F': [135, 215, 135],
	'V': [135, 215, 215],
	'f': [135, 255, 0],
	'v': [135, 255, 135],
	'ì': [135, 255, 215],
	'Ψ': [175, 0, 0],
	'7': [175, 0, 135],
	'G': [175, 95, 0],
	'W': [175, 95, 135],
	'g': [175, 95, 215],
	'w': [175, 135, 0],
	'ò': [175, 135, 135],
	'Σ': [175, 135, 215],
	'(': [175, 175, 0],
	'8': [175, 175, 215],
	'H': [175, 215, 0],
	'X': [175, 215, 135],
	'h': [175, 215, 215],
	'x': [175, 255, 0],
	'Ç': [175, 255, 135],
	'Θ': [175, 255, 215],
	')': [215, 0, 135],
	'9': [215, 0, 215],
	'I': [215, 95, 0],
	'Y': [215, 95, 135],
	'i': [215, 95, 215],
	'y': [215, 135, 0],
	'Ξ': [215, 135, 135],
	'*': [215, 175, 0],
	':': [215, 175, 135],
	'J': [215, 175, 215],
	'Z': [215, 215, 0],
	'j': [215, 215, 135],
	'z': [215, 215, 215],
	'Ø': [215, 255, 0],
	'+': [215, 255, 215],
	';': [255, 0, 0],
	'K': [255, 0, 135],
	'Ä': [255, 0, 215],
	'k': [255, 95, 0],
	'ä': [255, 95, 135],
	'ø': [255, 95, 215],
	'Æ': [255, 135, 135],
	',': [255, 135, 215],
	'<': [255, 175, 0],
	'L': [255, 175, 135],
	'Ö': [255, 175, 215],
	'l': [255, 215, 0],
	'ö': [255, 215, 135],
	'æ': [255, 255, 0],
	'-': [255, 255, 135],
	'=': [255, 255, 215],
	'M': [8, 8, 8],
	'Ñ': [28, 28, 28],
	'm': [48, 48, 48],
	'ñ': [68, 68, 68],
	'Å': [108, 108, 108],
	'ß': [128, 128, 128],
	'.': [148, 148, 148],
	'>': [168, 168, 168],
	'N': [188, 188, 188],
	'Ü': [208, 208, 208],
	'n': [228, 228, 228]
}

gsm = list(chars.keys())


def getNearestColour(r, g, b):
	"""Given a set of RGB values, find the nearest colour we can use."""
	closest = None
	diff = 99999999999
	for i in range(0, len(gsm)):
		clr = chars[gsm[i]]
		rd = abs(clr[0] - r)
		gd = abs(clr[1] - g)
		bd = abs(clr[2] - b)
		d = rd + gd + bd
		if d < diff:
			diff = d
			closest = gsm[i]
	return chars[closest]


def buildHeader(width):
	"""Generate the header string."""
	header = str(version) + "/" + str(width) + "/"
	return header


def encodePixel(px):
	"""Given an RGB value, convert it to the nearest usable colour, and encode it as a character."""
	r, g, b = px[0], px[1], px[2]
	rgb = getNearestColour(r, g, b)
	wsrgb = list(chars.keys())[list(chars.values()).index(rgb)]
	return wsrgb


def getPixels(file, res):
	"""Extract pixels from an image at the specified resolution."""
	rim = Image.open(file)
	im = rim.convert('RGB')
	w, h = im.size
	xr = math.floor(w / res)
	yr = math.floor(h / res)

	pixels = []
	for ys in range(0, res):
		y = (ys * yr) + math.floor(yr / 2)
		for xs in range(0, res):
			x = (xs * xr) + math.floor(xr / 2)
			r, g, b = im.getpixel((x, y))
			px = (r, g, b)
			pixels.append(px)

	return pixels


def encode(file, res):
	"""Encode an image. file is the path to the image, res is the resolution to use. Smaller res means smaller but lower quality output."""
	out = buildHeader(res)
	pixels = getPixels(file, res)
	for i in range(0, len(pixels)):
		px = encodePixel(pixels[i])
		out += px
	return out


def decode(data, file):
	"""Decode an image. data is the encoded string from encode, file is the path to save the decoded image to."""
	parts = data.split('/')
	vrs = parts[0]
	res = int(parts[1])
	enc = parts[2]

	im = Image.new('RGB', (res * 10, res * 10), color='black')
	draw = ImageDraw.Draw(im)
	if vrs == '0':
		for y in range(0, res):
			for x in range(0, res):
				pos = (y * res) + x
				char = enc[pos]
				px = chars[char]
				ix1 = x * 10
				ix2 = (x + 1) * 10
				iy1 = y * 10
				iy2 = (y + 1) * 10
				rgb = (px[0], px[1], px[2])
				draw.rectangle([ix1, iy1, ix2, iy2], rgb)
		im.save(file)
		return True
	else:
		return False


def cycle(in_file, out_file, res):
	"""Just for testing. Encodes and immediately decodes an image. in_file is the path to the input file, out_file is the path to save the output file to, and res is the resolution to use."""
	encoded = encode(in_file, res)
	print(encoded)
	decode(encoded, out_file)
