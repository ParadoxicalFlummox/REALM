package models

import(
	"time"
)

type Property struct {
	ID            uint			`gorm:"primaryKey"`
	OwnerID		  uint			`gorm:"not null"`
	streetAddress string		`gorm:"not null"`
	Owner		User		`gorm:"foreignKey:OwnerID"`
	financialRecords []financialRecord `gorm:"foreignKey:PropertyID"`
}
