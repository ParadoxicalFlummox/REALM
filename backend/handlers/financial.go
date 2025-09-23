package handlers

import (
	"TAPRE/backend/models"
	"TAPRE/backend/repositories"
	"net/http"

	"github.com/gin-gonic/gin"
)

type FinancialHandler struct {
	Repo repositories.FinancialRepository
}

func NewFinancialHandler(repo repositories.FinancialRepository) *FinancialHandler {
	return &FinancialHandler{Repo: repo}
}

// CreateFinancialRecord handles the creation of a financial record
func (h *FinancialHandler) CreateFinancialRecord(c *gin.Context) {
	var record models.FinancialRecord
	if err := c.ShouldBindJSON(&record); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
		return
	}

	if err := h.Repo.Create(&record); err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
		return
	}

	c.JSON(http.StatusCreated, record)
}

// GetFinancialRecords handles retrieving all financial records
func (h *FinancialHandler) GetFinancialRecords(c *gin.Context) {
	records, err := h.Repo.GetAll()
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
		return
	}

	c.JSON(http.StatusOK, records)
}
