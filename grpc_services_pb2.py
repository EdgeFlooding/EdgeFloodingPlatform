# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: grpc_services.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='grpc_services.proto',
  package='',
  syntax='proto3',
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n\x13grpc_services.proto\"q\n\x05\x46rame\x12\n\n\x02id\x18\x01 \x01(\x05\x12\x0f\n\x07id_slot\x18\x02 \x01(\x05\x12\x10\n\x08\x62\x36\x34image\x18\x03 \x01(\t\x12\r\n\x05width\x18\x04 \x01(\x05\x12\x0e\n\x06height\x18\x05 \x01(\x05\x12\x1a\n\x12\x63reation_timestamp\x18\x06 \x01(\x03\"S\n\x06Result\x12\x0f\n\x07id_node\x18\x01 \x01(\x05\x12\x10\n\x08id_frame\x18\x02 \x01(\x05\x12\x11\n\tid_camera\x18\x03 \x01(\x05\x12\x13\n\x0bresult_dict\x18\x04 \x01(\t\"\x07\n\x05\x45mpty24\n\x0e\x46rameProcedure\x12\"\n\x0eHandleNewFrame\x12\x06.Frame\x1a\x06.Empty\"\x00\x32\x37\n\x0fResultProcedure\x12$\n\x0f\x41ggregateResult\x12\x07.Result\x1a\x06.Empty\"\x00\x62\x06proto3'
)




_FRAME = _descriptor.Descriptor(
  name='Frame',
  full_name='Frame',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='id', full_name='Frame.id', index=0,
      number=1, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='id_slot', full_name='Frame.id_slot', index=1,
      number=2, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='b64image', full_name='Frame.b64image', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='width', full_name='Frame.width', index=3,
      number=4, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='height', full_name='Frame.height', index=4,
      number=5, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='creation_timestamp', full_name='Frame.creation_timestamp', index=5,
      number=6, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=23,
  serialized_end=136,
)


_RESULT = _descriptor.Descriptor(
  name='Result',
  full_name='Result',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='id_node', full_name='Result.id_node', index=0,
      number=1, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='id_frame', full_name='Result.id_frame', index=1,
      number=2, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='id_camera', full_name='Result.id_camera', index=2,
      number=3, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='result_dict', full_name='Result.result_dict', index=3,
      number=4, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=138,
  serialized_end=221,
)


_EMPTY = _descriptor.Descriptor(
  name='Empty',
  full_name='Empty',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=223,
  serialized_end=230,
)

DESCRIPTOR.message_types_by_name['Frame'] = _FRAME
DESCRIPTOR.message_types_by_name['Result'] = _RESULT
DESCRIPTOR.message_types_by_name['Empty'] = _EMPTY
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

Frame = _reflection.GeneratedProtocolMessageType('Frame', (_message.Message,), {
  'DESCRIPTOR' : _FRAME,
  '__module__' : 'grpc_services_pb2'
  # @@protoc_insertion_point(class_scope:Frame)
  })
_sym_db.RegisterMessage(Frame)

Result = _reflection.GeneratedProtocolMessageType('Result', (_message.Message,), {
  'DESCRIPTOR' : _RESULT,
  '__module__' : 'grpc_services_pb2'
  # @@protoc_insertion_point(class_scope:Result)
  })
_sym_db.RegisterMessage(Result)

Empty = _reflection.GeneratedProtocolMessageType('Empty', (_message.Message,), {
  'DESCRIPTOR' : _EMPTY,
  '__module__' : 'grpc_services_pb2'
  # @@protoc_insertion_point(class_scope:Empty)
  })
_sym_db.RegisterMessage(Empty)



_FRAMEPROCEDURE = _descriptor.ServiceDescriptor(
  name='FrameProcedure',
  full_name='FrameProcedure',
  file=DESCRIPTOR,
  index=0,
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_start=232,
  serialized_end=284,
  methods=[
  _descriptor.MethodDescriptor(
    name='HandleNewFrame',
    full_name='FrameProcedure.HandleNewFrame',
    index=0,
    containing_service=None,
    input_type=_FRAME,
    output_type=_EMPTY,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
])
_sym_db.RegisterServiceDescriptor(_FRAMEPROCEDURE)

DESCRIPTOR.services_by_name['FrameProcedure'] = _FRAMEPROCEDURE


_RESULTPROCEDURE = _descriptor.ServiceDescriptor(
  name='ResultProcedure',
  full_name='ResultProcedure',
  file=DESCRIPTOR,
  index=1,
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_start=286,
  serialized_end=341,
  methods=[
  _descriptor.MethodDescriptor(
    name='AggregateResult',
    full_name='ResultProcedure.AggregateResult',
    index=0,
    containing_service=None,
    input_type=_RESULT,
    output_type=_EMPTY,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
])
_sym_db.RegisterServiceDescriptor(_RESULTPROCEDURE)

DESCRIPTOR.services_by_name['ResultProcedure'] = _RESULTPROCEDURE

# @@protoc_insertion_point(module_scope)
