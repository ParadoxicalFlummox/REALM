package initializers

import (
	"os"

	"gorm.io/driver/postgres"
	"gorm.io/gorm"
)

var DB *gorm.DB

// ConnectToDB opens a gorm DB using the provided DSN. It returns the DB and any error.
func ConnectToDB() (*gorm.DB, error) {
	dsn := os.Getenv("DB_CREDS")
	db, err := gorm.Open(postgres.Open(dsn), &gorm.Config{})
	if err != nil {
		return nil, err
	}
	DB = db
	return db, nil
}
