import torch
import torch.nn as nn
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
model = torch.compile(model)

loss_function = nn.CrossEntropyLoss()

optimizer = Adam(model.parameters())

# TODO: Continuar implementação

