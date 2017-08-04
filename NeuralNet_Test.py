import numpy as np


class NeuralNetwork:

    def __init__(self):
        self.InputLayerSize = 2
        self.OutputLayerSize = 1
        self.HiddenLayerSize = 3
        self.W1 = np.random.randn(self.InputLayerSize,
                                  self.HiddenLayerSize)

        self.TestW1 = np.matrix('0.8 0.4 0.3; 0.2 0.9 0.5')
        self.TestW2 = np.matrix('0.3; 0.5; 0.9')
        self.Output = None
        self.OutputLayerInputs = None
        self.HiddenLayerOutputs = None
        self.HiddenLayerInputs = None
        self.Inputs = None
        self.SigmoidPrimeMatrix = np.frompyfunc(self.SigmoidPrime, 1, 1)
        self.SigmoidMatrix = np.frompyfunc(self.Sigmoid, 1, 1)

    def Reset(self):
        self.Output = None
        self.OutputLayerInputs = None
        self.HiddenLayerOutputs = None
        self.HiddenLayerInputs = None
        self.Inputs = None

    def Sigmoid(self, x):
        return 1/(1 + np.exp(-x))

    def SigmoidPrime(self, x):
        return(self.Sigmoid(x) * (1-self.Sigmoid(x)))

    def Forward(self, Input1, Input2):
        self.Inputs = np.matrix([[Input1,Input2]])
        self.HiddenLayerInputs = np.dot(self.Inputs, self.TestW1)
        self.HiddenLayerOutputs = self.SigmoidMatrix(self.HiddenLayerInputs)
        self.OutputLayerInputs = np.dot(self.HiddenLayerOutputs, self.TestW2)
        self.Output = self.SigmoidMatrix(self.OutputLayerInputs)

    def Backward(self, target):
        DeltaOutputSum = self.SigmoidPrimeMatrix(self.OutputLayerInputs) * (target - self.Output)
        DeltaHiddenSum = np.multiply(np.transpose((DeltaOutputSum / self.TestW2)), self.SigmoidPrimeMatrix(self.HiddenLayerInputs))
        self.TestW2 = np.transpose(np.divide(DeltaOutputSum.item(0), self.HiddenLayerOutputs))
        self.TestW1 = self.TestW1 + np.divide(DeltaHiddenSum, np.transpose(self.Inputs))

Test = NeuralNetwork()

for i in range(0, 10000000000):
    Test.Forward(1, 1)
    print(Test.Output)
    Test.Backward(0)


