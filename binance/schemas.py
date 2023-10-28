import trafaret as t
from marshmallow import Schema, fields
from marshmallow.validate import Length, Range

config_schema = t.Dict(
    mongodb=t.Dict(
        dsn=t.String,
        db_name=t.String,
    ),
    debug=t.Bool,
    RMQ_CONN_STR=t.String,
    RMQ_CHANNEL_NAME=t.String,
    REST_URL_BINANCE=t.String,
    STREAM_URL_URL_BINANCE=t.String
)


class DepthUpdateSchema(Schema):
    e = fields.String(required=True)
    E = fields.Int(required=True)
    s = fields.String(required=True)
    U = fields.Int(required=True)
    u = fields.Int(required=True)
    b = fields.List(fields.List(fields.String()), required=True)
    a = fields.List(fields.List(fields.String()), required=True)

    class Meta:
        strict = True