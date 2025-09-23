package main

import (
	"TAPRE/backend/handlers"
	"TAPRE/backend/initializers"
	"TAPRE/backend/middleware"

	"github.com/gin-gonic/gin"
)

func main() {
	// Initialize the database connection
	initializers.LoadEnvVariables()
	initializers.ConnectToDB()

	// Set up Gin router
	router := gin.Default()

	// Apply middleware
	router.Use(middleware.AuthMiddleware())

	// Register routes
	router.POST("/api/v1/auth/signup", handlers.Signup)
	router.POST("/api/v1/auth/login", handlers.Login)
	router.GET("/api/v1/properties", handlers.GetProperties)
	router.POST("/api/v1/properties", handlers.CreateProperty)
	router.PUT("/api/v1/properties/:id", handlers.UpdateProperty)
	router.DELETE("/api/v1/properties/:id", handlers.DeleteProperty)

	// Start the server
	router.Run(":8000")
}
