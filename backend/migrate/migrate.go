package migrate

import (
	"github.com/ParadoxicalFlummox/TAPRE/backend/initializers"
	"github.com/ParadoxicalFlummox/TAPRE/backend/models"
)

// Run will run AutoMigrate for core models using the initializers DB.
func Run() error {
	if initializers.DB == nil {
		return nil
	}
	return initializers.DB.AutoMigrate(&models.User{}, &models.Property{}, &models.FinancialRecord{})
}
