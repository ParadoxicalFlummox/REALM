package migrate

import (
	"TAPRE/backend/models"

	"github.com/jinzhu/gorm"
)

// RunMigrations applies the necessary migrations to the database.
func RunMigrations(db *gorm.DB) error {
	// Automatically create or update the database tables based on the models
	return db.AutoMigrate(&models.User{}, &models.Property{}, &models.FinancialRecord{}).Error
}
