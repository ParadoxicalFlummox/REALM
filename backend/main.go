package main

import (
	"log"
	"github.com/gin-gonic/gin"
	""
)

func init() {
	initalizers.LoadEnvVariables()
}

func main() {
	r := gin.Default()

	r.GET("/", func(c *gin.Context) {
		c.JSON(200, gin.H{
			"message": "pong",
		})
	})

	r.Run()
}