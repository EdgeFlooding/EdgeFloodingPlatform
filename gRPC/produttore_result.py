import grpc

# import the generated classes
import grpc_services_pb2
import grpc_services_pb2_grpc

# data encoding
import json


if __name__ == '__main__':
    # open a gRPC channel
    channel = grpc.insecure_channel('127.0.0.1:5004')

    # create a stub (client)
    stub = grpc_services_pb2_grpc.ResultProcedureStub(channel)

    try:
        while True:
            result = {}

            print(result)
            result_req = grpc_services_pb2.Result(result_dict = json.dumps(result).encode('utf-8'))

            # make the call
            response = stub.AggregateResult(result_req)
            print("Result sent")
            input("Press Enter to send another frame...")
    except KeyboardInterrupt as ex:
        print("Exiting...")

