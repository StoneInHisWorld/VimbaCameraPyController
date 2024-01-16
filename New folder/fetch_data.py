from torchvision.datasets.cifar import CIFAR100

dataset = CIFAR100(root='../data', download=True)
train_data = CIFAR100.train_list
test_data = CIFAR100.test_list
