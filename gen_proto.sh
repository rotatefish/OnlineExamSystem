mkdir -p gen

protoc -I=. --python_out=gen proto/db.proto
protoc -I=. --python_out=gen proto/api.proto
