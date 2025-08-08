import torch
import torch.nn as nn
import torch.nn.functional as F
from matplotlib import pyplot as plt
from sklearn.model_selection import train_test_split
from src.chap04.neural_networks.benchmark import SRBenchmark

def plot_xy(samples, prediction):
    x = [sample[0] for sample in samples]
    y = [p for p in prediction]
    plt.plot(x, y, 'o')
    plt.show()

class FeedForward(nn.Module):

    def __init__(self, num_inputs, num_units, num_outputs):
        super(FeedForward, self).__init__()
        self.l1 = nn.Linear(num_inputs, num_units)
        self.l2 = nn.Linear(num_units, num_units)
        self.l3 = nn.Linear(num_units, num_outputs)
        self.activation = nn.Sigmoid

    def forward(self, x):
        out = self.l1(x)
        out = F.sigmoid(out)
        out = self.l2(out)
        out = F.sigmoid(out)
        out = self.l3(out)
        return out


def main():
    X, y = SRBenchmark.random_set(min=-1.0, max=1.0, n=50, objective=SRBenchmark.koza2, dim=1)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.4, random_state=42)

    num_inputs = 1
    num_units = 100
    num_outputs = 1
    num_epochs = 10000
    learning_rate = 0.01
    batch_size = 1
    report_interval = 10
    ideal = 0.02

    train_dataset = torch.utils.data.TensorDataset(
        torch.from_numpy(X_train), torch.from_numpy(y_train)
    )

    test_dataset = torch.utils.data.TensorDataset(
        torch.from_numpy(X_test), torch.from_numpy(y_test)
    )

    train_dataloader = torch.utils.data.DataLoader(
        train_dataset, batch_size=batch_size, shuffle=True
    )

    test_dataloader = torch.utils.data.DataLoader(
        test_dataset, batch_size=batch_size, shuffle=False
    )

    model = FeedForward(num_inputs, num_units, num_outputs)
    loss_fn = nn.MSELoss()
    optimizer = torch.optim.SGD(model.parameters(), lr=learning_rate)

    n_train = len(X_train)
    n_test = len(X_test)

    for epoch in range(num_epochs):
        running_train_loss = 0.0
        for step, (inputs, targets) in enumerate(train_dataloader):
            output = model(inputs)
            train_loss = loss_fn(output, targets)
            optimizer.zero_grad()
            train_loss.backward()
            optimizer.step()
            running_train_loss += train_loss.item()

        if epoch % report_interval == 0:
            predictions = []
            with torch.no_grad():
                running_test_loss = 0.0
                for idx, (inputs, targets) in enumerate(test_dataloader):
                    output = model(inputs)
                    predictions.append(output)
                    test_loss = loss_fn(output, targets)
                    running_test_loss += test_loss.item()
            train_loss = running_train_loss / n_train
            test_loss =  running_test_loss / n_test
            print(f"epoch: {epoch} train_loss: {train_loss} test_loss: {test_loss}")
            if test_loss <= ideal:
                plot_xy(predictions,y_test)
                break

if __name__ == "__main__":
    main()