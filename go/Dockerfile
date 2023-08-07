FROM golang:1.20-alpine

WORKDIR /mkv

COPY go.mod go.sum /mkv/
RUN go mod download && go mod verify

COPY main.go /mkv/main.go

RUN go build -v -o /mkv/mkv

ENV MKV_HOST=0.0.0.0

CMD ["/mkv/mkv"]
