import torch
from torch import nn
import torch.optim as optim

# Hyperparameters
input_size = 28
hidden_size = 256
num_layers = 2
num_classes = 10
sequence_length = 28
learning_rate = 0.005
batch_size = 64
num_epochs = 3

#Set device
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

class RNN(nn.module):
    def __init__(self, input_size, hidden_size, num_layers, num_classes):
        super(RNN, self).__init__()
        self.hidden_size = hidden_size
        self.num_layers = num_layers
        self.rnn = nn.RNN(input_size, hidden_size, num_layers, batch_first=True)
        self.fc = nn.Linear(hidden_size + input_size, num_classes)

    def forward(self, x):
        h0 = torch.zeros(self.num_layers, x.size(0), self.hidden_size).to(device)
        out, _ = self.rnn(x, h0) # _ is hidden state output but ignore
        out = out.reshape(out.shape[0]. -1)
        out = self.fc(out)
        return(out)

#Initiallize network
model = RNN(input_size, hidden_size, num_layers, num_classes).to(device)

# Loss and optimizer
criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=learning_rate)

# Train Network
for epoch in range(num_epochs):
    for batch_idx, (data, targets) in enumerate(tqdm(train_loader)):
        # Get data to cuda if possible
        data = data.to(device=device).squeeze(1)
        targets = targets.to(device=device)

        # forward
        scores = model(data)
        loss = criterion(scores, targets)

        # backward
        optimizer.zero_grad()
        loss.backward()

        # gradient descent update step/adam step
        optimizer.step()

# # Check accuracy on training & test to see how good our model
# def check_accuracy(loader, model):
#     num_correct = 0
#     num_samples = 0
#
#     # Set model to eval
#     model.eval()
#
#     with torch.no_grad():
#         for x, y in loader:
#             x = x.to(device=device).squeeze(1)
#             y = y.to(device=device)
#
#             scores = model(x)
#             _, predictions = scores.max(1)
#             num_correct += (predictions == y).sum()
#             num_samples += predictions.size(0)
#
#     # Toggle model back to train
#     model.train()
#     return num_correct / num_samples
#
#
# print(f"Accuracy on training set: {check_accuracy(train_loader, model)*100:2f}")
# print(f"Accuracy on test set: {check_accuracy(test_loader, model)*100:.2f}")
