# way to upload image: endpoint
# way to save the image
# function to make prediction on the image
# show the results
import os

import torch
import torch.nn as nn
import torch.nn.functional as F
from torchvision import models
import torchvision.transforms as transforms

from PIL import Image

from flask import Flask
from flask import request
from flask import render_template



classes = ['Buildings', 'Forest', 'Glacier', 'Mountain', 'Sea', 'Street']
app = Flask(__name__)
UPLOAD_FOLDER = "/home/goku/app/static"
DEVICE = "cpu"
MODEL = None


class Model(nn.Module):
    def __init__(self):
        super(Model,self).__init__()
        
        self.backbone =  models.vgg19()
        num_features = self.backbone.classifier[6].in_features
        self.backbone.classifier[6] = nn.Linear(num_features, len(classes))
        
    def forward(self,image):
        x = self.backbone(image)
        return x

def transform_image(image_bytes):
    my_transforms = transforms.Compose([transforms.Resize((150, 150)),
                                        transforms.ToTensor(),
                                        transforms.Normalize([0.485, 0.456, 0.406],
                                                                [0.229, 0.224, 0.225])])
    image = Image.open(image_bytes)
    return my_transforms(image).unsqueeze(0)

def predict(image,model):
    tensor = transform_image(image)
    outputs = model.forward(tensor)
    _, y_hat = outputs.max(1)
    predicted_idx = str(y_hat.item())
    print(outputs,y_hat,predicted_idx)
    return classes[int(predicted_idx)]



@app.route("/", methods=["GET", "POST"])
def upload_predict():
    if request.method == "POST":
        image_file = request.files["image"]
        if image_file:
            image_location = os.path.join(
                UPLOAD_FOLDER,
                image_file.filename
            )
            image_file.save(image_location)
            pred = predict(image_location, MODEL)
            return render_template("index.html", prediction=pred, image_loc=image_file.filename)
    return render_template("index.html", prediction=0, image_loc=None)


if __name__ == "__main__":
    MODEL = Model()
    MODEL.load_state_dict(torch.load("vgg19-10.pt", map_location=torch.device(DEVICE)))
    MODEL.to(DEVICE)
    app.run(host="0.0.0.0",port=8080)
