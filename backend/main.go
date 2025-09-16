package main

import (
	"log"

	"github.com/ParadoxicalFlummox/TAPRE/backend/initializers"
	"github.com/ParadoxicalFlummox/TAPRE/backend/models"
	"github.com/gin-gonic/gin"
)

func main() {
	if err := initializers.LoadEnv(".env"); err != nil {
		log.Println("warning: .env not loaded:", err)
	}

	cfg, err := initializers.NewConfigFromEnv()
	if err != nil {
		log.Fatalf("config: %v", err)
	}

	db, err := initializers.ConnectToDB()
	if err != nil {
		log.Fatalf("failed to connect to db: %v", err)
	}

	if err := initializers.RunMigrations(db, &models.User{}, &models.Property{}, &models.FinancialRecord{}); err != nil {
		log.Fatalf("migrate: %v", err)
	}

	r := gin.Default()

	r.GET("/", func(c *gin.Context) {
		c.JSON(200, gin.H{"message": "pong"})
	})

	r.Run(":" + cfg.Port)
}
