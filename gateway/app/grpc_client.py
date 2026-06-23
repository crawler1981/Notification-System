import grpc
from proto import library_pb2, library_pb2_grpc

async def send_to_library(user_id: str, message: str):
    # توجه: 'library' نام سرویس در docker-compose است
    async with grpc.aio.insecure_channel('library:50051') as channel:
        stub = library_pb2_grpc.LibraryServiceStub(channel)
        request = library_pb2.MessageRequest(user_id=user_id, message=message)
        response = await stub.SendMessage(request)
        return response