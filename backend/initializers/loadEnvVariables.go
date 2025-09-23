package initializers

import (
    "log"
    "os"

    "github.com/joho/godotenv"
)

func LoadEnvVariables() {
    err := godotenv.Load()
    if err != nil {
        log.Fatalf("Error loading .env file")
    }

    // Example of accessing an environment variable
    dbCreds := os.Getenv("DB_CREDS")
    if dbCreds == "" {
        log.Fatal("DB_CREDS environment variable is not set")
    }
}