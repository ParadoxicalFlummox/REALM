package initializers

import (
    "gorm.io/driver/postgres"
    "gorm.io/gorm"
    "log"
    "os"
)

var DB *gorm.DB

func ConnectToDB() {
    var err error
    dsn := os.Getenv("DB_CREDS") // Database connection string from environment variable
    DB, err = gorm.Open(postgres.Open(dsn), &gorm.Config{})
    if err != nil {
        log.Fatalf("Could not connect to the database: %v", err)
    }
    log.Println("Database connection established")
}