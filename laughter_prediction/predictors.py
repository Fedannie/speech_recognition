import torch

class Predictor:
    """
    Wrapper class used for loading serialized model and
    using it in classification task.
    Defines unified interface for all inherited predictors.
    """

    def predict(self, X):
        """
        Predict target values of X given a model

        :param X: numpy.ndarray, dtype=float, shape=[n_samples, n_features]
        :return: numpy.array predicted classes
        """
        raise NotImplementedError("Should have implemented this")

    def predict_proba(self, X):
        """
        Predict probabilities of target class

        :param X: numpy.ndarray, dtype=float, shape=[n_samples, n_features]
        :return: numpy.array target class probabilities
        """
        raise NotImplementedError("Should have implemented this")

class RnnPredictor(Predictor):
    def __init__(self, model_):
        self.model = model_

    def predict(self, X):
        p = self.predict_proba(X)
        return p[:, 1] > p[:, 0], p
    
    def predict_proba(self, X):
        X1, X2 = X[:, :20], X[:, 20:]
        X1 = torch.Tensor(X1)
        X2 = torch.Tensor(X2)
        with torch.no_grad():
            self.model.clear()
            _, out2 = self.model((X1, X2))
            p = torch.nn.functional.softmax(out2, dim=1)
        return p.data
