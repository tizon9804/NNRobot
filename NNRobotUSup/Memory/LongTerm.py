import NNRobotUSup.Entities.Conscience as Con
from Libraries.NNET import NNCostFunction as nncost, NeuralNetwork as NN, Think, Train as train

class LongTerm:
    def __init__(self):
        self.consciences = []
        self.id = 0

    def createConscience(self, name, inputSize, numHidLayer, hidLayerSize, outputSize):
        input_layer_size = inputSize
        num_hidden_layer = numHidLayer
        hidden_layer_size = hidLayerSize
        num_output_Layers = outputSize
        NNGen = NN.CNNET(type,
                         input_layer_size,
                         num_hidden_layer,
                         hidden_layer_size,
                         num_output_Layers)
        mind = Think.assemble([], NNGen.brain,
                              input_layer_size, num_hidden_layer,
                              hidden_layer_size, num_output_Layers)
        newCons = Con.Conscience(self.id, name, mind)
        self.id += 1
        self.consciences.append(newCons)

    def trainConscience(self):
        todo = True

    def updateConscience(self):
        todo = True
