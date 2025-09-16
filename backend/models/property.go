package models

import (
	"time"
)

type Property struct {
	ID               uint              `gorm:"primaryKey" json:"id"`
	OwnerID          uint              `gorm:"not null" json:"owner_id"`
	StreetAddress    string            `gorm:"not null" json:"street_address"`
	Owner            User              `gorm:"foreignKey:OwnerID" json:"owner"`
	FinancialRecords []FinancialRecord `gorm:"foreignKey:PropertyID" json:"financial_records"`
	CreatedAt        time.Time         `json:"created_at"`
	UpdatedAt        time.Time         `json:"updated_at"`
}
