import asyncio
import grpc
from proto import library_pb2, library_pb2_grpc

class LibraryService(library_pb2_grpc.LibraryServiceServicer):
    async def SendMessage(self, request, context):
        print(f"[LIBRARY] Received: user_id={request.user_id}, message={request.message}")
        return library_pb2.MessageResponse(status="OK", details="Message printed successfully")

async def serve():
    server = grpc.aio.server()
    library_pb2_grpc.add_LibraryServiceServicer_to_server(LibraryService(), server)
    server.add_insecure_port('[::]:50051')
    await server.start()
    print("Library gRPC server started on port 50051")
    await server.wait_for_termination()

if __name__ == "__main__":
    asyncio.run(serve())