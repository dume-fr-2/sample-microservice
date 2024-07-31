import logging
import os
import random
import time
from typing import Optional
from concurrent import futures
import grpc
import requests
import httpx
import uvicorn
#import pika
import send_text_pb2
import send_text_pb2_grpc

from fastapi import FastAPI, Response, File
from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import (
    OTLPSpanExporter as OTLPSpanExporterGRPC,
)
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.instrumentation.logging import LoggingInstrumentor
#from opentelemetry.instrumentation.httpx import HTTPXClientInstrumentor
#from opentelemetry.instrumentation.grpc import GrpcInstrumentorClient
#from opentelemetry.instrumentation.grpc import GrpcInstrumentorServer
#from opentelemetry.instrumentation.pika import PikaInstrumentor

from opentelemetry.propagate import inject
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from starlette.types import ASGIApp

#HTTPXClientInstrumentor().instrument()

EXPOSE_PORT = os.environ.get("EXPOSE_PORT", 8000)

# otlp-grpc, otlp-http
#MODE = os.environ.get("MODE", "otlp-grpc")

OTLP_GRPC_ENDPOINT = os.environ.get("OTLP_GRPC_ENDPOINT", "jaeger-collector:4317")
#OTLP_HTTP_ENDPOINT = os.environ.get(
#    "OTLP_HTTP_ENDPOINT", "http://jaeger-collector:4318/v1/traces"
#)

TARGET_ONE_HOST   = os.environ.get("TARGET_ONE_HOST", "")
TARGET_TWO_HOST   = os.environ.get("TARGET_TWO_HOST", "")
TARGET_THREE_HOST = os.environ.get("TARGET_THREE_HOST", "")

BROKER_ONE_HOST   = os.environ.get("BROKER_ONE_HOST", "")
BROKER_TWO_HOST   = os.environ.get("BROKER_TWO_HOST", "")
BROKER_THREE_HOST = os.environ.get("BROKER_THREE_HOST", "")

app = FastAPI()

def setting_jaeger(app: ASGIApp, log_correlation: bool = True) -> None:
    # set the tracer provider
    tracer = TracerProvider()
    trace.set_tracer_provider(tracer)

    # default otlp-grpc
    tracer.add_span_processor(
        BatchSpanProcessor(
            OTLPSpanExporterGRPC(endpoint=OTLP_GRPC_ENDPOINT, insecure=True)
        )
    )

    # override logger format which with trace id and span id
    if log_correlation:
        LoggingInstrumentor().instrument(set_logging_format=True)

    FastAPIInstrumentor.instrument_app(app, tracer_provider=tracer)
#    GrpcInstrumentorClient().instrument(app, tracer_provider=tracer)
#    GrpcInstrumentorServer().instrument(app, tracer_provider=tracer)
#    PikaInstrumentor().instrument(app, tracer_provider=tracer)

# Setting jaeger exporter
setting_jaeger(app)

# grpc server
#class SendTextServicer(send_text_pb2_grpc.SendTextServicer):
#    def Send(self, request, context):
#        logging.info(request)
#        headers = {}
#        inject(headers)  # inject trace info to header
#        logging.critical(headers)
#
#        if TARGET_ONE_HOST != "":
#            with grpc.insecure_channel(TARGET_ONE_HOST) as channel:
#                stub = send_text_pb2_grpc.SendTextStub(channel)  # Use the correct stub class
#                request = send_text_pb2.Text(text=text)    # Create the request message
#                response1 = stub.Send(request)              # Send the request message
#                if response1.sucess:
#                    logging.info(f"Sending text to {TARGET_ONE_HOST} using gRPC speed:{time.time() - start_time}")
#
#        if TARGET_TWO_HOST != "":
#            with grpc.insecure_channel(TARGET_TWO_HOST) as channel:
#                stub = send_text_pb2_grpc.SendTextStub(channel)  # Use the correct stub class
#                request = send_text_pb2.Text(text=text)    # Create the request message
#                response2 = stub.Send(request)              # Send the request message
#                if response2.sucess:
#                    logging.info(f"Sending text to {TARGET_TWO_HOST} using gRPC speed:{time.time() - start_time}")
#    
#        if TARGET_THREE_HOST != "":
#            with grpc.insecure_channel(TARGET_THREE_HOST) as channel:
#                stub = send_text_pb2_grpc.SendTextStub(channel)  # Use the correct stub class
#                request = send_text_pb2.Text(text=text)    # Create the request message
#                response3 = stub.Send(request)              # Send the request message
#                if response3.sucess:
#                    logging.info(f"Sending text to {TARGET_THREE_HOST} using gRPC speed:{time.time() - start_time}")
#
#        return send_text_pb2.SendResponse(sucess=True)

#def serve():
#    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
#    send_text_pb2_grpc.add_SendTextServicer_to_server(SendTextServicer(), server)
#    server.add_insecure_port("[::]:50001")
#    server.start()
#    logging.info("gRPC server started on port 50001")
#    server.wait_for_termination()

## subscribe
#def on_message(channel, method_frame, header_frame, body):
#    logging.info(channel, method_frame, header_frame, body)
#    channel.basic_ack(delivery_tag=method_frame.delivery_tag)

#def consume():
#    if BROKER_ONE_HOST != "":
#        conn_param = pika.ConnectionParameters(host=BROKER_ONE_HOST)
#        conn = pika.BlockingConnection(conn_param)
#        channel1 = conn.channel()
#
#        channel1.basic_qos(prefetch_count=1)
#        channel1.basic_consume(on_message, 'task_queue')
#        channel1.start_consuming()
#
#    if BROKER_TWO_HOST != "":
#        conn_param = pika.ConnectionParameters(host=BROKER_TWO_HOST)
#        conn = pika.BlockingConnection(conn_param)
#        channel2 = conn.channel()
#    
#        channel2.basic_qos(prefetch_count=1)
#        channel2.basic_consume(on_message, 'task_queue')
#        channel2.start_consuming()
#
#    if BROKER_THREE_HOST != "":
#        conn_param = pika.ConnectionParameters(host=BROKER_THREE_HOST)
#        conn = pika.BlockingConnection(conn_param)
#        channel3 = conn.channel()
#    
#        channel3.basic_qos(prefetch_count=1)
#        channel3.basic_consume(on_message, 'task_queue')
#        channel3.start_consuming()

@app.get("/")
async def read_root():
    logging.error("Hello World")
    return {"Hello": "World"}


@app.get("/items/{item_id}")
async def read_item(item_id: int, q: Optional[str] = None):
    logging.error("items")
    return {"item_id": item_id, "q": q}


@app.get("/io_task")
async def io_task():
    time.sleep(1)
    logging.error("io task")
    return "IO bound task finish!"


@app.get("/cpu_task")
async def cpu_task():
    for i in range(1000):
        _ = i * i * i
    logging.error("cpu task")
    return "CPU bound task finish!"


@app.get("/random_status")
async def random_status(response: Response):
    response.status_code = random.choice([200, 200, 300, 400, 500])
    logging.error("random status")
    return {"path": "/random_status"}


@app.get("/random_sleep")
async def random_sleep(response: Response):
    time.sleep(random.randint(0, 5))
    logging.error("random sleep")
    return {"path": "/random_sleep"}


@app.get("/error_test")
async def error_test(response: Response):
    logging.error("got error!!!!")
    raise ValueError("value error")


@app.get("/chain")
async def chain(response: Response):
    headers = {}
    inject(headers)  # inject trace info to header
    logging.critical(headers)

    async with httpx.AsyncClient() as client:
        await client.get(
            "http://localhost:8000/",
            headers=headers,
        )
    if TARGET_ONE_HOST != "":
        async with httpx.AsyncClient() as client:
            await client.get(
                f"http://{TARGET_ONE_HOST}",
                headers=headers,
            )
    if TARGET_TWO_HOST != "":
        async with httpx.AsyncClient() as client:
            await client.get(
                f"http://{TARGET_TWO_HOST}",
                headers=headers,
            )
    if TARGET_THREE_HOST != "":
        async with httpx.AsyncClient() as client:
            await client.get(
                f"http://{TARGET_THREE_HOST}",
                headers=headers,
            )

    logging.info("Chain Finished")
    return {"path": "/chain"}

#@app.post("/chain_grpc")
#async def chain_grpc(text: str):
#    headers = {}
#    inject(headers)  # inject trace info to header
#    logging.critical(headers)
#
#    start_time = time.time()
#
#    if TARGET_ONE_HOST != "":
#        with grpc.insecure_channel(TARGET_ONE_HOST) as channel:
#            stub = send_text_pb2_grpc.SendTextStub(channel)  # Use the correct stub class
#            request = send_text_pb2.Text(text=text)    # Create the request message
#            response1 = stub.Send(request)              # Send the request message
#            if response1.sucess:
#                logging.info(f"Sending text to {TARGET_ONE_HOST} using gRPC speed:{time.time() - start_time}")
#
#    if TARGET_TWO_HOST != "":
#        with grpc.insecure_channel(TARGET_TWO_HOST) as channel:
#            stub = send_text_pb2_grpc.SendTextStub(channel)  # Use the correct stub class
#            request = send_text_pb2.Text(text=text)    # Create the request message
#            response2 = stub.Send(request)              # Send the request message
#            if response2.sucess:
#                logging.info(f"Sending text to {TARGET_TWO_HOST} using gRPC speed:{time.time() - start_time}")
#
#    if TARGET_THREE_HOST != "":
#        with grpc.insecure_channel(TARGET_THREE_HOST) as channel:
#            stub = send_text_pb2_grpc.SendTextStub(channel)  # Use the correct stub class
#            request = send_text_pb2.Text(text=text)    # Create the request message
#            response3 = stub.Send(request)              # Send the request message
#            if response3.sucess:
#                logging.info(f"Sending text to {TARGET_THREE_HOST} using gRPC speed:{time.time() - start_time}")
#
#    return {"path": "/chain_grpc"}


#@app.post("/chain_publish")
#async def chain_publish(text: str):
#
#    if TARGET_ONE_HOST != "":
#        connection1 = pika.BlockingConnection(
#            pika.ConnectionParameters(host=TARGET_ONE_HOST))
#        # チャンネルの確立
#        channel1 = connection1.channel()
#        # キュー(task_queue)作成
#        channel1.queue_declare(queue="task_queue", durable=True)
#    
#        channel1.basic_publish(
#            exchange="",
#            routing_key="task_queue",
#            body=text,
#            properties=pika.BasicProperties(
#                delivery_mode=2,  # メッセージの永続化
#            ))
#        connection1.close()
#
#    if TARGET_TWO_HOST != "":
#        connection2 = pika.BlockingConnection(
#            pika.ConnectionParameters(host=TARGET_TWO_HOST))
#        # チャンネルの確立
#        channel2 = connection2.channel()
#        # キュー(task_queue)作成
#        channel2.queue_declare(queue="task_queue", durable=True)
#    
#        channel2.basic_publish(
#            exchange="",
#            routing_key="task_queue",
#            body=text,
#            properties=pika.BasicProperties(
#                delivery_mode=2,  # メッセージの永続化
#            ))
#        connection2.close()
#
#    if TARGET_THREE_HOST != "":
#        connection3 = pika.BlockingConnection(
#            pika.ConnectionParameters(host=TARGET_THREE_HOST))
#        # チャンネルの確立
#        channel3 = connection3.channel()
#        # キュー(task_queue)作成
#        channel3.queue_declare(queue="task_queue", durable=True)
#    
#        channel3.basic_publish(
#            exchange="",
#            routing_key="task_queue",
#            body=text,
#            properties=pika.BasicProperties(
#                delivery_mode=2,  # メッセージの永続化
#            ))
#        connection3.close()
#
#    return {"send": text}

if __name__ == "__main__":

    # grpc
    #serve()

    # cosumer
    #consume()

    # update uvicorn access logger format
    log_config = uvicorn.config.LOGGING_CONFIG
    log_config["formatters"]["access"][
        "fmt"
    ] = "%(asctime)s %(levelname)s [%(name)s] [%(filename)s:%(lineno)d] [trace_id=%(otelTraceID)s span_id=%(otelSpanID)s resource.service.name=%(otelServiceName)s] - %(message)s"

    uvicorn.run(app, host="0.0.0.0", port=EXPOSE_PORT, log_config=log_config)
