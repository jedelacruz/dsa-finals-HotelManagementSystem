# 🏨 Hotel Management System

A comprehensive console-based hotel reservation and payment management system built with **pure Python** (no external libraries). Implements advanced data structures and algorithms for real-world business operations.

## ✨ Features

### Core Operations
- **CRUDS** - Create, Read, Update, Delete, Search, Sort reservations
- **Room Management** - 5 room types with different capacities and pricing
- **Flexible Updates** - Change room type, dates, guest count, contact info
- **Smart Search** - Find by ID, name, room number, status, or date range
- **Multiple Sort Options** - Sort by name, room, cost, or date

### Payment System
- **Payment Processing** - Cash, Credit/Debit Card, Bank Transfer, Digital Wallet
- **Payment Tracking** - Full history per reservation with status updates
- **Additional Charges** - Room service, minibar, laundry, restaurant, spa
- **Refund Management** - Full, partial, or custom refund amounts
- **Financial Reports** - Revenue, payment methods, outstanding balances

### Smart Features
- **Auto Cost Calculation** - Updates when dates or rooms change
- **Real-time Balance Tracking** - Always accurate payment status
- **Room Availability** - Only shows available rooms, handles cancellations
- **Comprehensive Validation** - All inputs validated with helpful error messages
- **Error Handling** - Never crashes, always shows clear error messages

## 🏗️ Technical Implementation

### Data Structures
- **Linear (Lists)** - Sequential storage of reservations and payments
- **Non-Linear (Dictionaries)** - Fast lookup by room number and reservation ID
- **Nested Structures** - Complex data representation

### Algorithms
- **Bubble Sort** - Demonstrated on multiple sorting options
- **Linear Search** - Name and attribute searching
- **Dictionary Lookup** - O(1) access by key

### Key Highlights
- ✅ Pure Python (no imports except `os`)
- ✅ Manual date/time handling
- ✅ Input validation with re-prompting
- ✅ No crashes - comprehensive error handling
- ✅ Professional user interface

## 📋 Room Types & Pricing

| Room Type | Capacity | Price/Night |
|-----------|----------|-------------|
| Standard Single | 1 guest | ₱1,500 |
| Standard Double | 2 guests | ₱2,500 |
| Deluxe Suite | 3 guests | ₱4,500 |
| Executive Suite | 4 guests | ₱6,500 |
| Presidential Suite | 6 guests | ₱12,000 |

## 🚀 Getting Started

### Prerequisites
- Python 3.6 or higher
- No external libraries required!

### Installation
```bash
# Clone the repository
git clone https://github.com/yourusername/hotel-management-system.git

# Navigate to directory
cd hotel-management-system

# Run the program
python hotel_management_system_with_payment.py
```

## 💡 Usage Examples

### Create a Reservation
1. Select option `1` from main menu
2. Enter guest information (validated automatically)
3. Select room type based on guest count
4. Choose available room
5. Set check-in/check-out dates and times
6. Reservation created with automatic cost calculation

### Process Payment
1. Select option `7` from main menu
2. Choose from list of unpaid reservations
3. Enter payment amount (partial or full)
4. Select payment method
5. Payment recorded, balance updated automatically

### Update Reservation
1. Select option `3` from main menu
2. Find reservation (by list, ID, or name)
3. Choose what to update:
   - Contact information
   - Check-in/out dates
   - Room type or number (with cost comparison!)
   - Number of guests
   - Cancel reservation

### Generate Reports
- Occupancy rates by room type
- Revenue analysis (total, active, cancelled)
- Guest statistics
- Payment method breakdown
- Outstanding balances

## 🎯 Key Operations

### Search Options
- By Reservation ID
- By Guest Name (partial match)
- By Room Number
- By Status (Active/Cancelled)
- By Date Range

### Sort Options
- Guest Name (A-Z or Z-A)
- Room Number (Ascending/Descending)
- Total Cost (Low to High or High to Low)
- Check-in Date (Earliest/Latest First)

## 🏆 Project Highlights

### Data Structures & Algorithms
- Implements both **Linear** and **Non-Linear** data structures
- Demonstrates **Bubble Sort** algorithm
- Uses **Linear Search** and **Hash-based Lookup**
- Manual date comparison and calculation functions

### Software Engineering
- **Error Handling** - Try-catch blocks prevent all crashes
- **Input Validation** - Comprehensive checking with helpful messages
- **User Experience** - Cancel options everywhere, clear navigation
- **Data Integrity** - Automatic balance and status updates

### Business Logic
- Room availability checking (active reservations only)
- Payment status auto-update (Pending → Partial → Paid)
- Cost recalculation on any changes
- Balance tracking with additional charges
- Refund processing with policy options

## 📊 Menu Structure

```
Main Menu (15 options)
├── Reservation Operations (1-6)
│   ├── Create, Read, Update, Delete
│   ├── Search (5 methods)
│   └── Sort (8 options)
├── Payment Management (7-12)
│   ├── Process Payment
│   ├── View Payments
│   ├── View Reservation Payments
│   ├── Add Additional Charges
│   ├── Issue Refund
│   └── Payment Reports (4 types)
├── Reports & Information (13-14)
│   └── Generate Reports (3 types)
└── System (15, 0)
    ├── About the System
    └── Exit
```

## 🎓 Academic Project

This project was created for a **Data Structures & Algorithms** course, demonstrating:
- Linear data structures (arrays/lists)
- Non-linear data structures (dictionaries/hash maps)
- Sorting algorithms (bubble sort)
- Search algorithms (linear search)
- CRUDS operations
- Input validation and error handling
- Real-world application development

## 🔒 Data Validation

All inputs are validated:
- **Phone Numbers** - 10-15 digits only
- **Email** - Proper format with domain validation
- **Dates** - DD/MM/YYYY format, 2026-2035 range
- **Time** - HH:MM format, 24-hour clock
- **Numbers** - Min/max range checking
- **Text** - Length constraints

## ⚠️ Known Limitations

- **No Data Persistence** - Data stored in memory only (resets on exit)
- **Single User** - No concurrent access support
- **No Date Conflicts** - Doesn't check overlapping reservations
- **Manual Date Entry** - No auto-fill or calendar picker

These are by design for the educational scope of the project.

## 🛠️ Future Enhancements

- [ ] File-based data persistence (JSON/CSV)
- [ ] Database integration (SQLite)
- [ ] Date conflict checking
- [ ] Discount/promo codes
- [ ] Receipt printing
- [ ] Multi-user support
- [ ] GUI interface

## 📝 License

This project is open source and available for educational purposes.

## 👨‍💻 Author

Created as a final project for Data Structures & Algorithms course.

---

**⭐ If you find this project helpful, please consider giving it a star!**
