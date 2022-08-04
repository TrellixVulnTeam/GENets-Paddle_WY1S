import torch
from torchvision import transforms
import PIL, math
import GENet

if __name__=="__main__":
    input_image_size = 256
    input_image_crop = 0.875
    resize_image_size = int(math.ceil(input_image_size / input_image_crop))
    test_transform = transforms.Compose([
        transforms.Resize(resize_image_size),
        transforms.CenterCrop(input_image_size),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
    ])
    img_path = "/home/lingbao/data/imagenet/imgs/ILSVRC2012_val_00000001.JPEG"
    img = PIL.Image.open(img_path).convert('RGB')
    data = test_transform(img)
    print(data, data.dtype, data[0, 0, 0].item())
    data = data.unsqueeze(0)
    print(data.size())
    model = GENet.genet_large(pretrained=True, root=".")
    model.eval()
    model = model.cuda(0)
    model.half()
    data = data.to(device="cuda:0", dtype=torch.float16)
    output = model(data)
    print(output.argmax(1), output[0, output.argmax(1)])
