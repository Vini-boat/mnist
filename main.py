import torch
import torch.nn as nn
from torch import Tensor
from torch.utils.data import Dataset, DataLoader
from torch.optim import Adam

import torchvision
import torchvision.transforms.v2 as transforms
import torchvision.transforms.functional as F
import matplotlib.pyplot as plt

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

train_set = torchvision.datasets.MNIST("./data/", train=True,download=True)
valid_set = torchvision.datasets.MNIST("./data/", train=False,download=True)

x_0, y_0 = train_set[0]

trans = transforms.Compose([
    transforms.ToTensor()
])

x_0_tensor = trans(x_0)

train_set.transform = trans
valid_set.transform = trans

BATCH_SIZE = 32

train_loader = DataLoader(train_set, batch_size=BATCH_SIZE, shuffle=True)
valid_loader = DataLoader(valid_set, batch_size=BATCH_SIZE)

input_size = 1 * 28 * 28
n_classes = 10

layers = [
    nn.Flatten(),
    nn.Linear(input_size, 512),
    nn.ReLU(),
    nn.Linear(512,512),
    nn.ReLU(),
    nn.Linear(512,n_classes)
]

model = nn.Sequential(*layers)

model.to(device)
model.compile()

loss_function = nn.CrossEntropyLoss()

optimizer = Adam(model.parameters())

# TODO: Treinar e validar o modelo

train_N = len(train_loader.dataset)
valid_N = len(valid_loader.dataset)

def get_batch_accuracy(output: Tensor, y: Tensor, N):
    pred = output.argmax(dim=1,keepdim=True)
    correct = pred.eq(y.view_as(pred)).sum().item()
    return correct / N

def train():
    loss = 0 
    accuracy = 0

    model.train()
    for x, y in train_loader:
        x, y = x.to(device), y.to(device)

        output = model(x)
        optimizer.zero_grad()
        batch_loss = loss_function(output,y)
        batch_loss.backward()
        optimizer.step()

        loss += batch_loss.item()
        accuracy += get_batch_accuracy(output,y, train_N)
    print('Train - Loss: {:.4f} Accuracy: {:.4f}'.format(loss, accuracy))


def validate():
    loss =0
    accuracy = 0 

    model.eval()
    with torch.no_grad():
        for x, y in valid_loader:
            x, y = x.to(device), y.to(device)
            output = model(x)
            
            loss += loss_function(output,y).item()
            accuracy += get_batch_accuracy(output,y, train_N)
    print('Valid - Loss: {:.4f} Accuracy: {:.4f}'.format(loss, accuracy))


if __name__ == "__main__":
    epochs = 5

    for epoch in range(epochs):
        print("Epoch: {}".format(epoch))
        train()
        validate()














