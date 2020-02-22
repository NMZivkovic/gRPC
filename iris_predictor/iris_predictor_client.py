import grpc
import logging

import tensorflow as tf
from tensorflow_serving.apis import predict_pb2
from tensorflow_serving.apis import prediction_service_pb2_grpc

class IrisPredictorClient(object):
    def __init__(self, ip_port):
        channel = grpc.insecure_channel(ip_port)
        self.stub = prediction_service_pb2_grpc.PredictionServiceStub(channel)

    def predict(self, input_data):
        # Create request
        request = predict_pb2.PredictRequest()
        request.model_spec.name = 'saved_model'

        # Fill inputs
        request.inputs['dense_input'].CopyFrom(tf.make_tensor_proto(input_data, shape=[1, 4]))

        return self.stub.Predict(request, 10.0)

def run():

    client = IrisPredictorClient('127.0.0.1:8500')
    prediction = client.predict([7.1, 3.0, 6.1, 2.3])

    print('--------Prediction--------')
    print(prediction)
    print('----------------------------')

if __name__ == '__main__':
    logging.basicConfig()
    run()