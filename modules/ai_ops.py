import torch
import torchvision.transforms as transforms
from torchvision.models import resnet152
from PIL import Image
import requests
import json

class AiTaggedImage:
    def __init__(self, image_file_path):
        self.tag_list = get_image_tags(image_file_path)

    def tag(self, index):
        if index < len(self.tag_list) + 1:
            return self.tag_list[index - 1]
        else:
            return None


def get_image_tags(image_file_path):
    # Load the pre-trained ResNet-152 model
    model = resnet152(pretrained=True)

    # Set the model to evaluation mode
    model.eval()

    # Load and preprocess the image
    image_path = image_file_path
    image = Image.open(image_path).convert('RGB')

    # Define the image transformation pipeline
    transform = transforms.Compose([
        transforms.Resize(256),
        transforms.CenterCrop(224),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
    ])

    # Apply the transformation to the image
    input_tensor = transform(image)
    input_batch = input_tensor.unsqueeze(0)

    # Move the input tensor to the available device (CPU or GPU)
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    input_batch = input_batch.to(device)

    # Make predictions
    with torch.no_grad():
        output = model(input_batch)

    # Load the labels for ImageNet classes
    LABELS_FILE_URL = 'https://raw.githubusercontent.com/anishathalye/imagenet-simple-labels/master/imagenet-simple-labels.json'
    response = requests.get(LABELS_FILE_URL)
    labels = json.loads(response.content.decode('utf-8'))

    # Get the top predicted class indices and probabilities
    _, top_indices = torch.topk(output, k=5, dim=1)
    predicted_labels = [labels[idx] for idx in top_indices[0]]
    probabilities = torch.nn.functional.softmax(output, dim=1)[0]

    return_list = []
    # Print the top predicted labels and probabilities
    # print("Top Predictions:")
    for label, prob in zip(predicted_labels, probabilities[top_indices][0]):
        return_list.append(label)
        # return_dict[label] = prob.item()

    # print(return_list)
    return return_list


ai_image = AiTaggedImage(r'C:\Users\jacks\PycharmProjects\ImageTournament\images\4.jpg')
print(ai_image.tag(1))
