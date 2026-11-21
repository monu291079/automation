import sys, numpy as np, onnxruntime as ort
from PIL import Image, ImageOps, ImageFilter
U='/root/.claude/uploads/30a7b273-6306-55c3-bec0-ca5f0409b214/'
S=sys.argv[1]
names0={'8812':'23564187','8803':'d3602f35','8805':'1b753d16','8808':'1c0b0416','8806':'cb340e4d','8816':'f532dbb8','8836':'52227463','8855':'1380de7c','8854':'416ab4fa','8875':'6d8dc3b6','8884':'88d8fd41','8886':'869bc56d'}
names={'receipt': '/tmp/claude-0/-home-user-automation/30a7b273-6306-55c3-bec0-ca5f0409b214/scratchpad/r/receipt_blur.jpg', 'rate': '/root/.claude/uploads/30a7b273-6306-55c3-bec0-ca5f0409b214/282aee70-image.jpg', 'closed': '/root/.claude/uploads/30a7b273-6306-55c3-bec0-ca5f0409b214/3b460a94-image.jpg', 'roof1': '/root/.claude/uploads/30a7b273-6306-55c3-bec0-ca5f0409b214/6ff200af-image.jpg', 'crowdL': '/root/.claude/uploads/30a7b273-6306-55c3-bec0-ca5f0409b214/2b399675-image.jpg', 'selfie_flag': '/root/.claude/uploads/30a7b273-6306-55c3-bec0-ca5f0409b214/5e5d59bb-image.jpg', 'selfie_pillar': '/root/.claude/uploads/30a7b273-6306-55c3-bec0-ca5f0409b214/7926f9a2-image.jpg', 'selfie_queue': '/root/.claude/uploads/30a7b273-6306-55c3-bec0-ca5f0409b214/f763ea53-image.jpg', 'roof2': '/root/.claude/uploads/30a7b273-6306-55c3-bec0-ca5f0409b214/cf46533b-image.jpg', 'roofL': '/root/.claude/uploads/30a7b273-6306-55c3-bec0-ca5f0409b214/e39fb4e5-image.jpg', 'queue': '/root/.claude/uploads/30a7b273-6306-55c3-bec0-ca5f0409b214/02534e39-image.jpg', 'ai_savitri': '/home/user/automation/plans/pushkar-guide/assets/ai/savitri.jpg'}
sess=ort.InferenceSession(S+'/src/u2net_human_seg.onnx',providers=['CPUExecutionProvider'])
def seg(im):
    w,h=im.size
    x=np.asarray(im.convert('RGB').resize((320,320),Image.LANCZOS)).astype(np.float32)/255.
    x=(x-[0.485,0.456,0.406])/[0.229,0.224,0.225]
    x=x.transpose(2,0,1)[None].astype(np.float32)
    o=sess.run(None,{sess.get_inputs()[0].name:x})[0][0,0]
    o=(o-o.min())/(o.max()-o.min()+1e-8)
    m=Image.fromarray((o*255).astype(np.uint8)).resize((w,h),Image.LANCZOS)
    return m
for k,v in names.items():
    im=ImageOps.exif_transpose(Image.open(v)).convert('RGB')
    # cover 1080x1920 at 1.0, store at 1.3x for zoom
    W,H=1080*1.3,1920*1.3
    s=max(W/im.width,H/im.height)
    im=im.resize((round(im.width*s),round(im.height*s)),Image.LANCZOS)
    im.save(f'{S}/rprep/{k}.jpg',quality=95)
    m=seg(im).filter(ImageFilter.GaussianBlur(1.5))
    m.save(f'{S}/rprep/{k}_m.png'); print(k,im.size)
