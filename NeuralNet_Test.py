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

    def Sigmoid(self, x):
        return 1/(1 + np.exp(-x))

    def SigmoidPrime(self, x):
        if(type(x) is np.matrixlib.defmatrix.matrix):
            return np.apply_along_axis(self.Sigmoid, 0, x)
        else:
            return(self.Sigmoid(x) * (1-self.Sigmoid(x)))

    def Forward(self, Input1, Input2):
        Inputs = np.matrix([[Input1,Input2]])
        self.HiddenLayerInputs = np.dot(Inputs, self.TestW1)
        self.HiddenLayerOutputs = self.Sigmoid(self.HiddenLayerInputs)
        self.OutputLayerInputs = np.dot(self.HiddenLayerOutputs, self.TestW2)
        self.Output = self.Sigmoid(self.OutputLayerInputs)


    def Backward(self, target):
        DeltaOutputSum = self.SigmoidPrime(self.OutputLayerInputs) * (target - self.Output)
        DeltaHiddenSum = (DeltaOutputSum / self.TestW2) * self.SigmoidPrime(self.HiddenLayerInputs)
        self.TestW2 = DeltaOutputSum.item(0) / self.HiddenLayerOutputs


        print(self.TestW2)


Test = NeuralNetwork()
Test.Forward(1, 1)
Test.Backward(0)

