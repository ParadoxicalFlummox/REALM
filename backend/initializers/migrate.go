package initializers

import (
	"gorm.io/gorm"
)

// RunMigrations runs gorm AutoMigrate on the provided models.
func RunMigrations(db *gorm.DB, models ...interface{}) error {
	return db.AutoMigrate(models...)
}
