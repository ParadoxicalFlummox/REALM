package handlers

import (
	"TAPRE/backend/models"
	"TAPRE/backend/repositories"
	"net/http"

	"github.com/gin-gonic/gin"
)

type PropertyHandler struct {
	Repo repositories.PropertyRepository
}

func NewPropertyHandler(repo repositories.PropertyRepository) *PropertyHandler {
	return &PropertyHandler{Repo: repo}
}

func (h *PropertyHandler) CreateProperty(c *gin.Context) {
	var property models.Property
	if err := c.ShouldBindJSON(&property); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
		return
	}

	if err := h.Repo.Create(&property); err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": "Could not create property"})
		return
	}

	c.JSON(http.StatusCreated, property)
}

func (h *PropertyHandler) GetProperty(c *gin.Context) {
	id := c.Param("id")
	property, err := h.Repo.FindByID(id)
	if err != nil {
		c.JSON(http.StatusNotFound, gin.H{"error": "Property not found"})
		return
	}

	c.JSON(http.StatusOK, property)
}

func (h *PropertyHandler) UpdateProperty(c *gin.Context) {
	id := c.Param("id")
	var property models.Property
	if err := c.ShouldBindJSON(&property); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
		return
	}

	property.ID = id
	if err := h.Repo.Update(&property); err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": "Could not update property"})
		return
	}

	c.JSON(http.StatusOK, property)
}

func (h *PropertyHandler) DeleteProperty(c *gin.Context) {
	id := c.Param("id")
	if err := h.Repo.Delete(id); err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": "Could not delete property"})
		return
	}

	c.JSON(http.StatusNoContent, nil)
}
