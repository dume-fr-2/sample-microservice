# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: send_text.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x0fsend_text.proto\x12\x08sendtext\"\x14\n\x04Text\x12\x0c\n\x04text\x18\x01 \x01(\t\"\x1e\n\x0cSendResponse\x12\x0e\n\x06sucess\x18\x01 \x01(\x08\x32:\n\x08SendText\x12.\n\x04Send\x12\x0e.sendtext.Text\x1a\x16.sendtext.SendResponseb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'send_text_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _globals['_TEXT']._serialized_start=29
  _globals['_TEXT']._serialized_end=49
  _globals['_SENDRESPONSE']._serialized_start=51
  _globals['_SENDRESPONSE']._serialized_end=81
  _globals['_SENDTEXT']._serialized_start=83
  _globals['_SENDTEXT']._serialized_end=141
# @@protoc_insertion_point(module_scope)