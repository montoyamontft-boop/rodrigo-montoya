import sys, numpy as np, onnxruntime as ort
from PIL import Image
s = ort.InferenceSession('u2net.onnx', providers=['CPUExecutionProvider'])
for a, b in zip(sys.argv[1::2], sys.argv[2::2]):
    im = Image.open(a).convert('RGB'); W, H = im.size
    x = np.asarray(im.resize((1024, 1024), Image.LANCZOS), np.float32) / 255
    x = (x - 0.5) / 1.0
    y = s.run(None, {s.get_inputs()[0].name: x.transpose(2, 0, 1)[None]})[0][0, 0]
    y = (y - y.min()) / (y.max() - y.min())
    Image.fromarray((y * 255).astype(np.uint8)).resize((W, H), Image.LANCZOS).save(b)
