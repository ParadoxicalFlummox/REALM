# Use the official Golang image as a base image
FROM golang:1.24

# Set the working directory inside the container
WORKDIR /app

# Copy the source code into the container
COPY . .

# Check if go.mod exists, if not, initialize a new Go module
RUN [ ! -f go.mod ] && go mod init gin || true

# Check if go.sum exists, if not, create an empty one
RUN [ ! -f go.sum ] && touch go.sum || true

# Download all dependencies. Dependencies will be cached if the go.mod and go.sum files are not changed
RUN go mod tidy

# Install the Gin web framework
RUN go get -u github.com/gin-gonic/gin

# Build the Go application
RUN go build -o main .

# Expose the port the app runs on
EXPOSE 8080

# Command to run the executable
CMD ["./main"]