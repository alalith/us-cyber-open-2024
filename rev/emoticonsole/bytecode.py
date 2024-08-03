import dis
import marshal
with open('./runtime.pyc', 'rb') as f:
    _ = f.read(16)
    loaded = marshal.load(f)

dis.dis(loaded)
