"""
HOTEL MANAGEMENT SYSTEM (Transaction Processing System)
Data Structures & Algorithms Final Project
==================================================
Features:
- CRUDS Operations (Create, Read, Update, Delete, Search, Sort)
- Linear Data Structures (Lists/Arrays)
- Non-Linear Data Structures (Dictionaries simulating Trees)
- No External Libraries (Pure Python)
- Strict Input Validation with Re-prompting
- Manual Date/Time Handling
==================================================
"""

# ============================================================
# GLOBAL DATA STRUCTURES
# ============================================================

# Linear Data Structure: List of all reservations
reservations_list = []

# Non-Linear Data Structure: Dictionary organized by room number
# This simulates a tree-like structure where room numbers are keys
room_reservations = {}

# Dictionary for room types and prices
room_types = {
    "1": {"type": "Standard Single", "price": 1500, "capacity": 1},
    "2": {"type": "Standard Double", "price": 2500, "capacity": 2},
    "3": {"type": "Deluxe Suite", "price": 4500, "capacity": 3},
    "4": {"type": "Executive Suite", "price": 6500, "capacity": 4},
    "5": {"type": "Presidential Suite", "price": 12000, "capacity": 6}
}

# Available rooms per type (Linear structure)
available_rooms = {
    "1": [101, 102, 103, 104, 105],
    "2": [201, 202, 203, 204, 205, 206],
    "3": [301, 302, 303, 304],
    "4": [401, 402, 403],
    "5": [501, 502]
}

# Global counter for reservation IDs
reservation_id_counter = 1000

# ============================================================
# PAYMENT SYSTEM DATA STRUCTURES
# ============================================================

# Linear Data Structure: List of all payments
payments_list = []

# Non-Linear Data Structure: Dictionary organized by reservation ID
# Maps reservation_id -> list of payment records
reservation_payments = {}

# Global counter for payment IDs
payment_id_counter = 5000

# Payment methods
payment_methods = {
    "1": "Cash",
    "2": "Credit Card",
    "3": "Debit Card",
    "4": "Bank Transfer",
    "5": "Digital Wallet"
}


# ============================================================
# UTILITY FUNCTIONS
# ============================================================

def clear_screen():
    """Simulate clearing screen with newlines"""
    print("\n" * 50)


def print_header(title):
    """Print a formatted header"""
    print("=" * 70)
    print(f"{title.center(70)}")
    print("=" * 70)


def print_separator():
    """Print a separator line"""
    print("-" * 70)


def pause():
    """Pause and wait for user to press Enter"""
    input("\nPress Enter to continue...")


def validate_integer_input(prompt, min_val=None, max_val=None):
    """
    Validate integer input with optional min/max constraints
    Re-prompts until valid input is received
    """
    while True:
        try:
            value = input(prompt)
            num = int(value)
            
            if min_val is not None and num < min_val:
                print(f"Error: Value must be at least {min_val}. Please try again.")
                continue
            
            if max_val is not None and num > max_val:
                print(f"Error: Value must be at most {max_val}. Please try again.")
                continue
            
            return num
        except ValueError:
            print("Error: Please enter a valid number. Try again.")


def validate_string_input(prompt, min_length=1, max_length=100):
    """
    Validate string input with length constraints
    Re-prompts until valid input is received
    """
    while True:
        value = input(prompt).strip()
        
        if len(value) < min_length:
            print(f"Error: Input must be at least {min_length} character(s). Please try again.")
            continue
        
        if len(value) > max_length:
            print(f"Error: Input must be at most {max_length} characters. Please try again.")
            continue
        
        # Check if string contains only valid characters (letters, spaces, hyphens)
        valid = True
        for char in value:
            if not (char.isalpha() or char.isspace() or char == '-' or char == '.'):
                valid = False
                break
        
        if not valid:
            print("Error: Please use only letters, spaces, hyphens, and periods. Try again.")
            continue
        
        return value


def validate_phone_input(prompt):
    """
    Validate phone number input (digits only, 10-15 digits)
    Re-prompts until valid input is received
    """
    while True:
        value = input(prompt).strip()
        
        # Remove common separators
        cleaned = value.replace("-", "").replace(" ", "").replace("(", "").replace(")", "")
        
        if not cleaned.isdigit():
            print("Error: Phone number must contain only digits. Please try again.")
            continue
        
        if len(cleaned) < 10 or len(cleaned) > 15:
            print("Error: Phone number must be 10-15 digits. Please try again.")
            continue
        
        return cleaned


def validate_email_input(prompt):
    """
    Validate email input (basic validation)
    Re-prompts until valid input is received
    """
    while True:
        value = input(prompt).strip().lower()
        
        if len(value) < 5:
            print("Error: Email is too short. Please try again.")
            continue
        
        # Check for @ symbol
        if value.count('@') != 1:
            print("Error: Email must contain exactly one @ symbol. Please try again.")
            continue
        
        # Split by @
        parts = value.split('@')
        local = parts[0]
        domain = parts[1]
        
        # Validate local part
        if len(local) < 1:
            print("Error: Email must have characters before @. Please try again.")
            continue
        
        # Validate domain part
        if len(domain) < 3 or '.' not in domain:
            print("Error: Email domain must be valid (e.g., example.com). Please try again.")
            continue
        
        return value


def validate_date_input(prompt):
    """
    Validate date input in format DD/MM/YYYY
    Re-prompts until valid input is received
    Returns a dictionary with day, month, year
    """
    while True:
        value = input(prompt).strip()
        
        # Check format
        if value.count('/') != 2:
            print("Error: Date must be in format DD/MM/YYYY. Please try again.")
            continue
        
        parts = value.split('/')
        
        if len(parts) != 3:
            print("Error: Date must be in format DD/MM/YYYY. Please try again.")
            continue
        
        # Validate each part is numeric
        if not (parts[0].isdigit() and parts[1].isdigit() and parts[2].isdigit()):
            print("Error: Date must contain only numbers. Please try again.")
            continue
        
        day = int(parts[0])
        month = int(parts[1])
        year = int(parts[2])
        
        # Validate ranges
        if year < 2024 or year > 2030:
            print("Error: Year must be between 2024 and 2030. Please try again.")
            continue
        
        if month < 1 or month > 12:
            print("Error: Month must be between 1 and 12. Please try again.")
            continue
        
        # Days in each month
        days_in_month = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
        
        # Check for leap year
        if year % 4 == 0 and (year % 100 != 0 or year % 400 == 0):
            days_in_month[1] = 29
        
        if day < 1 or day > days_in_month[month - 1]:
            print(f"Error: Day must be between 1 and {days_in_month[month - 1]} for month {month}. Please try again.")
            continue
        
        return {
            "day": day,
            "month": month,
            "year": year,
            "formatted": value
        }


def validate_time_input(prompt):
    """
    Validate time input in format HH:MM (24-hour)
    Re-prompts until valid input is received
    Returns a dictionary with hour and minute
    """
    while True:
        value = input(prompt).strip()
        
        # Check format
        if value.count(':') != 1:
            print("Error: Time must be in format HH:MM (e.g., 14:30). Please try again.")
            continue
        
        parts = value.split(':')
        
        if len(parts) != 2:
            print("Error: Time must be in format HH:MM. Please try again.")
            continue
        
        # Validate each part is numeric
        if not (parts[0].isdigit() and parts[1].isdigit()):
            print("Error: Time must contain only numbers. Please try again.")
            continue
        
        hour = int(parts[0])
        minute = int(parts[1])
        
        # Validate ranges
        if hour < 0 or hour > 23:
            print("Error: Hour must be between 0 and 23. Please try again.")
            continue
        
        if minute < 0 or minute > 59:
            print("Error: Minute must be between 0 and 59. Please try again.")
            continue
        
        return {
            "hour": hour,
            "minute": minute,
            "formatted": value
        }


def compare_dates(date1, date2):
    """
    Compare two dates
    Returns: -1 if date1 < date2, 0 if equal, 1 if date1 > date2
    """
    if date1["year"] != date2["year"]:
        return -1 if date1["year"] < date2["year"] else 1
    if date1["month"] != date2["month"]:
        return -1 if date1["month"] < date2["month"] else 1
    if date1["day"] != date2["day"]:
        return -1 if date1["day"] < date2["day"] else 1
    return 0


def calculate_nights(check_in, check_out):
    """
    Calculate number of nights between two dates
    Simple calculation based on days (approximation)
    """
    # Convert dates to day numbers for simple calculation
    days_in_month = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    
    def date_to_days(date):
        total = date["year"] * 365
        for m in range(date["month"] - 1):
            total += days_in_month[m]
        total += date["day"]
        return total
    
    in_days = date_to_days(check_in)
    out_days = date_to_days(check_out)
    
    return out_days - in_days


def generate_reservation_id():
    """Generate unique reservation ID"""
    global reservation_id_counter
    res_id = f"RES{reservation_id_counter}"
    reservation_id_counter += 1
    return res_id


def generate_payment_id():
    """Generate unique payment ID"""
    global payment_id_counter
    pay_id = f"PAY{payment_id_counter}"
    payment_id_counter += 1
    return pay_id


def validate_float_input(prompt, min_val=None, max_val=None):
    """
    Validate float input with optional min/max constraints
    Re-prompts until valid input is received
    """
    while True:
        try:
            value = input(prompt)
            num = float(value)
            
            if min_val is not None and num < min_val:
                print(f"Error: Value must be at least {min_val}. Please try again.")
                continue
            
            if max_val is not None and num > max_val:
                print(f"Error: Value must be at most {max_val}. Please try again.")
                continue
            
            return num
        except ValueError:
            print("Error: Please enter a valid number. Try again.")


def find_reservation_with_search(reservations_to_search, title="Recent Reservations"):
    """
    Helper function to find a reservation with multiple search options and cancel ability
    Returns: reservation object or None if cancelled/not found
    """
    if not reservations_to_search:
        return None

    # Show list of reservations
    print(f"\n{title} ({min(10, len(reservations_to_search))}):")
    print_separator()
    display_list = reservations_to_search[-10:] if len(reservations_to_search) >= 10 else reservations_to_search
    for idx, res in enumerate(display_list, 1):
        status_info = f"Balance: ₱{res['balance']:>10,.2f}" if 'balance' in res and res['balance'] > 0 else f"Status: {res.get('payment_status', 'N/A')}"
        print(f"{idx}. ID: {res['id']:<12} | Guest: {res['guest_name']:<25} | {status_info}")
    print_separator()

    # Search options
    print("\nHow would you like to find the reservation?")
    print("1. Select from list above (enter number)")
    print("2. Enter Reservation ID")
    print("3. Search by Guest Name")
    print("0. Cancel / Go Back to Main Menu")

    search_choice = validate_integer_input("\nSelect option (0-3): ", min_val=0, max_val=3)

    if search_choice == 0:
        return None

    reservation = None

    if search_choice == 1:
        # Select from list
        list_choice = validate_integer_input(f"Select reservation (1-{len(display_list)}): ", min_val=1, max_val=len(display_list))
        reservation = display_list[list_choice - 1]

    elif search_choice == 2:
        # By ID
        res_id = validate_string_input("Enter Reservation ID: ", min_length=4, max_length=20)
        for res in reservations_to_search:
            if res["id"].lower() == res_id.lower():
                reservation = res
                break

    elif search_choice == 3:
        # By name
        guest_name = validate_string_input("Enter Guest Name: ", min_length=2, max_length=50)
        matches = []
        for res in reservations_to_search:
            if guest_name.lower() in res["guest_name"].lower():
                matches.append(res)

        if not matches:
            print("\nNo matching reservations found.")
            return None

        if len(matches) == 1:
            reservation = matches[0]
        else:
            print(f"\nFound {len(matches)} matching reservations:")
            for idx, res in enumerate(matches, 1):
                print(f"{idx}. {res['id']} - {res['guest_name']} - Room {res['room_number']}")

            choice = validate_integer_input(f"Select reservation (1-{len(matches)}): ", min_val=1, max_val=len(matches))
            reservation = matches[choice - 1]

    return reservation


# ============================================================
# CORE FUNCTIONS - CRUDS OPERATIONS
# ============================================================

def create_reservation():
    """
    CREATE Operation: Add a new reservation
    Demonstrates Linear (list) and Non-Linear (dictionary) data structures
    """
    clear_screen()
    print_header("CREATE NEW RESERVATION")

    print("\nPlease provide guest information:")
    print_separator()

    # Collect guest information with validation
    guest_name = validate_string_input("Guest Full Name: ", min_length=2, max_length=50)
    guest_phone = validate_phone_input("Contact Number: ")
    guest_email = validate_email_input("Email Address: ")
    num_guests = validate_integer_input("Number of Guests: ", min_val=1, max_val=10)

    print("\n")
    print_separator()
    print("ROOM SELECTION")
    print_separator()
    display_room_types()

    # Select room type with capacity validation
    while True:
        room_type_choice = validate_integer_input("\nSelect Room Type (1-5): ", min_val=1, max_val=5)
        room_type_key = str(room_type_choice)

        # Check capacity
        if num_guests > room_types[room_type_key]["capacity"]:
            print(f"\nError: Selected room type can accommodate maximum {room_types[room_type_key]['capacity']} guest(s).")
            print(f"You have {num_guests} guest(s). Please select a room type with sufficient capacity.")

            # Find suitable room types
            suitable_rooms = []
            for key, info in room_types.items():
                if info["capacity"] >= num_guests:
                    suitable_rooms.append((key, info))

            if suitable_rooms:
                print(f"\nSuggested room types for {num_guests} guest(s):")
                for key, info in suitable_rooms:
                    print(f"  {key}. {info['type']} (capacity: {info['capacity']} guest(s), ₱{info['price']:,.2f}/night)")
            else:
                print(f"\nSorry, no single room can accommodate {num_guests} guest(s).")
                print(f"Maximum capacity per room is 6 guests (Presidential Suite).")
                print("\nSuggestions:")
                print("  1. Book multiple rooms for your group")
                print("  2. Reduce number of guests")
                print("  3. Cancel and create separate reservations")

                print("\nWould you like to:")
                print("1. Continue anyway (select best available room)")
                print("2. Cancel this reservation")

                choice = validate_integer_input("\nSelect option (1-2): ", min_val=1, max_val=2)
                if choice == 2:
                    print("\nReservation cancelled.")
                    pause()
                    return
                else:
                    print(f"\nContinuing with room selection. Note: Room may not fit all {num_guests} guests.")

            continue
        else:
            break

    # Display and select available room
    print(f"\nAvailable {room_types[room_type_key]['type']} Rooms:")
    available = []
    for room in available_rooms[room_type_key]:
        if room not in room_reservations or not room_reservations[room]:
            available.append(room)
            print(f"  - Room {room}")

    if not available:
        print("\nSorry, no rooms available for this type.")
        print("Please try again later or select a different room type.")
        pause()
        return

    room_number = validate_integer_input(f"\nSelect Room Number: ", min_val=min(available), max_val=max(available))

    # Validate selected room is in available list
    while room_number not in available:
        print(f"Error: Room {room_number} is not available. Please select from the list above.")
        room_number = validate_integer_input(f"Select Room Number: ", min_val=min(available), max_val=max(available))

    print("\n")
    print_separator()
    print("CHECK-IN & CHECK-OUT DATES")
    print_separator()
    print("Enter dates in DD/MM/YYYY format")

    check_in = validate_date_input("\nCheck-in Date (DD/MM/YYYY): ")

    # Validate check-out is after check-in
    while True:
        check_out = validate_date_input("Check-out Date (DD/MM/YYYY): ")
        if compare_dates(check_out, check_in) <= 0:
            print("Error: Check-out date must be after check-in date. Please try again.")
        else:
            break

    check_in_time = validate_time_input("Check-in Time (HH:MM, 24-hour format): ")
    check_out_time = validate_time_input("Check-out Time (HH:MM, 24-hour format): ")

    # Calculate total cost
    nights = calculate_nights(check_in, check_out)
    if nights < 1:
        nights = 1

    price_per_night = room_types[room_type_key]["price"]
    total_cost = price_per_night * nights

    # Generate reservation ID
    res_id = generate_reservation_id()

    # Create reservation record (Dictionary - Non-Linear Structure)
    reservation = {
        "id": res_id,
        "guest_name": guest_name,
        "phone": guest_phone,
        "email": guest_email,
        "num_guests": num_guests,
        "room_type": room_types[room_type_key]["type"],
        "room_number": room_number,
        "check_in_date": check_in,
        "check_out_date": check_out,
        "check_in_time": check_in_time,
        "check_out_time": check_out_time,
        "nights": nights,
        "price_per_night": price_per_night,
        "total_cost": total_cost,
        "additional_charges": 0.0,  # For room service, minibar, etc.
        "total_paid": 0.0,  # Total amount paid so far
        "balance": total_cost,  # Remaining balance
        "payment_status": "Pending",  # Pending, Partial, Paid
        "status": "Active"
    }

    # Add to Linear Structure (List)
    reservations_list.append(reservation)

    # Add to Non-Linear Structure (Dictionary by room number)
    if room_number not in room_reservations:
        room_reservations[room_number] = []
    room_reservations[room_number].append(reservation)

    # Initialize payment tracking (Non-Linear Structure)
    reservation_payments[res_id] = []

    # Display confirmation
    print("\n")
    print_separator()
    print("RESERVATION CONFIRMED!")
    print_separator()
    display_reservation_details(reservation)

    pause()


def read_reservations():
    """
    READ Operation: Display all reservations
    Demonstrates traversal of Linear data structure
    """
    clear_screen()
    print_header("VIEW ALL RESERVATIONS")

    if not reservations_list:
        print("\nNo reservations found in the system.")
        pause()
        return

    print(f"\nTotal Reservations: {len(reservations_list)}")
    print_separator()

    for reservation in reservations_list:
        display_reservation_summary(reservation)
        print_separator()

    pause()


def update_reservation():
    """
    UPDATE Operation: Modify existing reservation
    Demonstrates search and update in both Linear and Non-Linear structures
    """
    clear_screen()
    print_header("UPDATE RESERVATION")

    if not reservations_list:
        print("\nNo reservations found in the system.")
        pause()
        return

    # Search for reservation
    print("\nSearch for reservation:")
    print("1. By Reservation ID")
    print("2. By Guest Name")
    print("3. By Room Number")

    search_choice = validate_integer_input("\nSelect search method (1-3): ", min_val=1, max_val=3)

    reservation = None

    if search_choice == 1:
        res_id = validate_string_input("Enter Reservation ID: ", min_length=4, max_length=20)
        # Linear search in list
        for res in reservations_list:
            if res["id"].lower() == res_id.lower():
                reservation = res
                break

    elif search_choice == 2:
        guest_name = validate_string_input("Enter Guest Name: ", min_length=2, max_length=50)
        # Linear search in list
        matches = []
        for res in reservations_list:
            if guest_name.lower() in res["guest_name"].lower():
                matches.append(res)

        if not matches:
            print("\nNo reservations found for this name.")
            pause()
            return

        if len(matches) == 1:
            reservation = matches[0]
        else:
            print(f"\nFound {len(matches)} reservations:")
            for idx, res in enumerate(matches, 1):
                print(f"{idx}. {res['id']} - {res['guest_name']} - Room {res['room_number']}")

            choice = validate_integer_input(f"Select reservation (1-{len(matches)}): ", min_val=1, max_val=len(matches))
            reservation = matches[choice - 1]

    else:  # search_choice == 3
        room_num = validate_integer_input("Enter Room Number: ", min_val=101, max_val=999)
        # Search in Non-Linear structure (dictionary)
        if room_num in room_reservations and room_reservations[room_num]:
            # Find active reservation
            for res in room_reservations[room_num]:
                if res["status"] == "Active":
                    reservation = res
                    break

    if not reservation:
        print("\nReservation not found.")
        pause()
        return

    # Display current reservation
    print("\n")
    print_separator()
    print("CURRENT RESERVATION DETAILS")
    print_separator()
    display_reservation_details(reservation)

    # Update menu
    print("\n")
    print_separator()
    print("What would you like to update?")
    print("1. Guest Contact Information")
    print("2. Check-out Date")
    print("3. Number of Guests")
    print("4. Cancel Reservation")

    update_choice = validate_integer_input("\nSelect option (1-4): ", min_val=1, max_val=4)

    if update_choice == 1:
        print("\nUpdate Contact Information:")
        new_phone = validate_phone_input("New Contact Number (or press Enter to skip): " )
        if new_phone:
            reservation["phone"] = new_phone

        new_email = validate_email_input("New Email Address (or press Enter to skip): ")
        if new_email:
            reservation["email"] = new_email

        print("\nContact information updated successfully!")

    elif update_choice == 2:
        print("\nUpdate Check-out Date:")
        while True:
            new_checkout = validate_date_input("New Check-out Date (DD/MM/YYYY): ")
            if compare_dates(new_checkout, reservation["check_in_date"]) <= 0:
                print("Error: Check-out date must be after check-in date. Please try again.")
            else:
                break

        new_checkout_time = validate_time_input("New Check-out Time (HH:MM): ")

        # Recalculate costs
        nights = calculate_nights(reservation["check_in_date"], new_checkout)
        if nights < 1:
            nights = 1

        reservation["check_out_date"] = new_checkout
        reservation["check_out_time"] = new_checkout_time
        reservation["nights"] = nights
        reservation["total_cost"] = reservation["price_per_night"] * nights

        print("\nCheck-out date updated successfully!")
        print(f"New total nights: {nights}")
        print(f"New total cost: ₱{reservation['total_cost']:,.2f}")

    elif update_choice == 3:
        new_num = validate_integer_input("New Number of Guests: ", min_val=1, max_val=10)

        # Check room capacity
        room_type_key = None
        for key, info in room_types.items():
            if info["type"] == reservation["room_type"]:
                room_type_key = key
                break

        if room_type_key and new_num > room_types[room_type_key]["capacity"]:
            print(f"\nError: Room capacity is {room_types[room_type_key]['capacity']} guests.")
            print("Cannot update to more guests than room capacity.")
        else:
            reservation["num_guests"] = new_num
            print("\nNumber of guests updated successfully!")

    elif update_choice == 4:
        confirm = validate_string_input("Are you sure you want to cancel this reservation? (yes/no): ", min_length=2, max_length=3)
        if confirm.lower() == "yes":
            reservation["status"] = "Cancelled"
            print("\nReservation cancelled successfully!")
        else:
            print("\nCancellation aborted.")

    pause()


def delete_reservation():
    """
    DELETE Operation: Remove reservation from system
    Demonstrates deletion from both Linear and Non-Linear structures
    """
    clear_screen()
    print_header("DELETE RESERVATION")

    if not reservations_list:
        print("\nNo reservations found in the system.")
        pause()
        return

    print("\nEnter reservation details to delete:")
    res_id = validate_string_input("Reservation ID: ", min_length=4, max_length=20)

    # Search in Linear structure
    reservation = None
    index = -1

    for idx, res in enumerate(reservations_list):
        if res["id"].lower() == res_id.lower():
            reservation = res
            index = idx
            break

    if not reservation:
        print("\nReservation not found.")
        pause()
        return

    # Display reservation details
    print("\n")
    print_separator()
    display_reservation_details(reservation)
    print_separator()

    # Confirm deletion
    confirm = validate_string_input("\nAre you sure you want to DELETE this reservation? (yes/no): ", min_length=2, max_length=3)

    if confirm.lower() != "yes":
        print("\nDeletion cancelled.")
        pause()
        return

    # Delete from Linear structure (List)
    reservations_list.pop(index)

    # Delete from Non-Linear structure (Dictionary)
    room_num = reservation["room_number"]
    if room_num in room_reservations:
        # Remove from room's reservation list
        room_reservations[room_num] = [r for r in room_reservations[room_num] if r["id"] != reservation["id"]]

    print("\nReservation deleted successfully!")
    pause()


def search_reservations():
    """
    SEARCH Operation: Find reservations based on various criteria
    Demonstrates different search algorithms on data structures
    """
    clear_screen()
    print_header("SEARCH RESERVATIONS")

    if not reservations_list:
        print("\nNo reservations found in the system.")
        pause()
        return

    print("\nSearch Options:")
    print("1. By Reservation ID")
    print("2. By Guest Name")
    print("3. By Room Number")
    print("4. By Status (Active/Cancelled)")
    print("5. By Date Range")

    search_choice = validate_integer_input("\nSelect search method (1-5): ", min_val=1, max_val=5)

    results = []

    if search_choice == 1:
        # Linear search by ID
        res_id = validate_string_input("Enter Reservation ID: ", min_length=4, max_length=20)
        for res in reservations_list:
            if res_id.lower() in res["id"].lower():
                results.append(res)

    elif search_choice == 2:
        # Linear search by name (partial match)
        name = validate_string_input("Enter Guest Name (or part of it): ", min_length=2, max_length=50)
        for res in reservations_list:
            if name.lower() in res["guest_name"].lower():
                results.append(res)

    elif search_choice == 3:
        # Search using Non-Linear structure (Dictionary)
        room_num = validate_integer_input("Enter Room Number: ", min_val=101, max_val=999)
        if room_num in room_reservations:
            results = room_reservations[room_num]

    elif search_choice == 4:
        # Filter by status
        print("\nSelect Status:")
        print("1. Active")
        print("2. Cancelled")
        status_choice = validate_integer_input("Enter choice (1-2): ", min_val=1, max_val=2)
        status = "Active" if status_choice == 1 else "Cancelled"

        for res in reservations_list:
            if res["status"] == status:
                results.append(res)

    elif search_choice == 5:
        # Search by date range
        print("\nEnter date range:")
        start_date = validate_date_input("Start Date (DD/MM/YYYY): ")
        end_date = validate_date_input("End Date (DD/MM/YYYY): ")

        for res in reservations_list:
            # Check if check-in date is within range
            if (compare_dates(res["check_in_date"], start_date) >= 0 and
                compare_dates(res["check_in_date"], end_date) <= 0):
                results.append(res)

    # Display results
    print("\n")
    print_separator()
    if not results:
        print("No reservations found matching your search criteria.")
    else:
        print(f"Found {len(results)} reservation(s):")
        print_separator()
        for res in results:
            display_reservation_summary(res)
            print_separator()

    pause()


def sort_reservations():
    """
    SORT Operation: Sort and display reservations
    Demonstrates sorting algorithms on Linear data structure
    """
    clear_screen()
    print_header("SORT RESERVATIONS")

    if not reservations_list:
        print("\nNo reservations found in the system.")
        pause()
        return

    print("\nSort Options:")
    print("1. By Guest Name (A-Z)")
    print("2. By Guest Name (Z-A)")
    print("3. By Room Number (Ascending)")
    print("4. By Room Number (Descending)")
    print("5. By Total Cost (Low to High)")
    print("6. By Total Cost (High to Low)")
    print("7. By Check-in Date (Earliest First)")
    print("8. By Check-in Date (Latest First)")

    sort_choice = validate_integer_input("\nSelect sorting method (1-8): ", min_val=1, max_val=8)

    # Create a copy of the list to sort
    sorted_list = []
    for res in reservations_list:
        sorted_list.append(res)

    # Bubble Sort implementation (demonstration of sorting algorithm)
    n = len(sorted_list)

    for i in range(n):
        for j in range(0, n - i - 1):
            swap = False

            if sort_choice == 1:  # Name A-Z
                if sorted_list[j]["guest_name"].lower() > sorted_list[j + 1]["guest_name"].lower():
                    swap = True

            elif sort_choice == 2:  # Name Z-A
                if sorted_list[j]["guest_name"].lower() < sorted_list[j + 1]["guest_name"].lower():
                    swap = True

            elif sort_choice == 3:  # Room ascending
                if sorted_list[j]["room_number"] > sorted_list[j + 1]["room_number"]:
                    swap = True

            elif sort_choice == 4:  # Room descending
                if sorted_list[j]["room_number"] < sorted_list[j + 1]["room_number"]:
                    swap = True

            elif sort_choice == 5:  # Cost low to high
                if sorted_list[j]["total_cost"] > sorted_list[j + 1]["total_cost"]:
                    swap = True

            elif sort_choice == 6:  # Cost high to low
                if sorted_list[j]["total_cost"] < sorted_list[j + 1]["total_cost"]:
                    swap = True

            elif sort_choice == 7:  # Date earliest
                if compare_dates(sorted_list[j]["check_in_date"], sorted_list[j + 1]["check_in_date"]) > 0:
                    swap = True

            elif sort_choice == 8:  # Date latest
                if compare_dates(sorted_list[j]["check_in_date"], sorted_list[j + 1]["check_in_date"]) < 0:
                    swap = True

            if swap:
                sorted_list[j], sorted_list[j + 1] = sorted_list[j + 1], sorted_list[j]

    # Display sorted results
    sort_names = {
        1: "Guest Name (A-Z)",
        2: "Guest Name (Z-A)",
        3: "Room Number (Ascending)",
        4: "Room Number (Descending)",
        5: "Total Cost (Low to High)",
        6: "Total Cost (High to Low)",
        7: "Check-in Date (Earliest First)",
        8: "Check-in Date (Latest First)"
    }

    print("\n")
    print_separator()
    print(f"Sorted by: {sort_names[sort_choice]}")
    print_separator()

    for res in sorted_list:
        display_reservation_summary(res)
        print_separator()

    pause()


# ============================================================
# PAYMENT MANAGEMENT FUNCTIONS
# ============================================================

def process_payment():
    """
    Process a payment for a reservation
    Demonstrates CRUD operations on payment data structures
    """
    clear_screen()
    print_header("PROCESS PAYMENT")

    if not reservations_list:
        print("\nNo reservations found in the system.")
        pause()
        return

    # Show unpaid/partially paid reservations first
    unpaid = []
    for res in reservations_list:
        if res["status"] == "Active" and res["payment_status"] != "Paid":
            unpaid.append(res)

    if not unpaid:
        print("\nAll active reservations are fully paid!")
        pause()
        return

    # Use helper function to find reservation
    reservation = find_reservation_with_search(unpaid, "Reservations with Outstanding Balance")

    if not reservation:
        return

    # Check if already fully paid
    if reservation["payment_status"] == "Paid":
        print("\nThis reservation is already fully paid!")
        print_separator()
        display_payment_summary(reservation)
        pause()
        return

    # Display reservation and payment details
    print("\n")
    print_separator()
    print("RESERVATION DETAILS")
    print_separator()
    display_reservation_details(reservation)
    print("\n")
    display_payment_summary(reservation)

    # Payment processing
    print("\n")
    print_separator()
    print("PAYMENT PROCESSING")
    print_separator()

    # Get payment amount
    print(f"\nOutstanding Balance: ₱{reservation['balance']:,.2f}")
    payment_amount = validate_float_input(f"Enter payment amount (₱): ", min_val=0.01, max_val=reservation['balance'])

    # Select payment method
    print("\nPayment Methods:")
    for key, method in payment_methods.items():
        print(f"  {key}. {method}")

    method_choice = validate_integer_input("\nSelect payment method (1-5): ", min_val=1, max_val=5)
    payment_method = payment_methods[str(method_choice)]

    # Get payment reference (optional)
    print("\nPayment Reference (optional, press Enter to skip):")
    reference = input("Reference Number/Transaction ID: ").strip()
    if not reference:
        reference = "N/A"

    # Get payment date and time
    print("\nPayment Date and Time:")
    payment_date = validate_date_input("Payment Date (DD/MM/YYYY): ")
    payment_time = validate_time_input("Payment Time (HH:MM): ")

    # Notes (optional)
    print("\nPayment Notes (optional, press Enter to skip):")
    notes = input("Notes: ").strip()
    if not notes:
        notes = "N/A"

    # Generate payment ID
    pay_id = generate_payment_id()

    # Create payment record
    payment = {
        "id": pay_id,
        "reservation_id": reservation["id"],
        "guest_name": reservation["guest_name"],
        "amount": payment_amount,
        "payment_method": payment_method,
        "reference": reference,
        "payment_date": payment_date,
        "payment_time": payment_time,
        "notes": notes,
        "status": "Completed"
    }

    # Add to Linear Structure (List)
    payments_list.append(payment)

    # Add to Non-Linear Structure (Dictionary by reservation ID)
    if reservation["id"] not in reservation_payments:
        reservation_payments[reservation["id"]] = []
    reservation_payments[reservation["id"]].append(payment)

    # Update reservation payment status
    reservation["total_paid"] += payment_amount
    reservation["balance"] = (reservation["total_cost"] + reservation["additional_charges"]) - reservation["total_paid"]

    # Update payment status
    if reservation["balance"] <= 0:
        reservation["payment_status"] = "Paid"
        reservation["balance"] = 0
    elif reservation["total_paid"] > 0:
        reservation["payment_status"] = "Partial"

    # Display payment confirmation
    print("\n")
    print_separator()
    print("PAYMENT SUCCESSFUL!")
    print_separator()
    display_payment_receipt(payment, reservation)

    pause()


def view_payments():
    """
    View all payments in the system
    Demonstrates READ operation on payment data
    """
    clear_screen()
    print_header("VIEW ALL PAYMENTS")

    if not payments_list:
        print("\nNo payments found in the system.")
        pause()
        return

    print(f"\nTotal Payments: {len(payments_list)}")

    # Calculate total revenue
    total_revenue = 0
    for payment in payments_list:
        if payment["status"] == "Completed":
            total_revenue += payment["amount"]

    print(f"Total Revenue Collected: ₱{total_revenue:,.2f}")
    print_separator()

    for payment in payments_list:
        display_payment_summary_line(payment)
        print_separator()

    pause()


def view_reservation_payments():
    """
    View all payments for a specific reservation
    Demonstrates search in Non-Linear structure
    """
    clear_screen()
    print_header("VIEW RESERVATION PAYMENTS")

    if not reservations_list:
        print("\nNo reservations found in the system.")
        pause()
        return

    # Use helper function to find reservation
    reservation = find_reservation_with_search(reservations_list, "Recent Reservations")

    if not reservation:
        return

    # Display reservation details
    print("\n")
    print_separator()
    display_reservation_details(reservation)
    print("\n")
    display_payment_summary(reservation)

    # Display payment history
    print("\n")
    print_separator()
    print("PAYMENT HISTORY")
    print_separator()

    if reservation["id"] not in reservation_payments or not reservation_payments[reservation["id"]]:
        print("No payments recorded for this reservation.")
    else:
        payments = reservation_payments[reservation["id"]]
        for idx, payment in enumerate(payments, 1):
            print(f"\nPayment #{idx}")
            display_payment_details(payment)
            print_separator()

    pause()


def add_additional_charges():
    """
    Add additional charges to a reservation (room service, minibar, etc.)
    Updates reservation balance
    """
    clear_screen()
    print_header("ADD ADDITIONAL CHARGES")

    if not reservations_list:
        print("\nNo reservations found in the system.")
        pause()
        return

    # Show active reservations
    active = []
    for res in reservations_list:
        if res["status"] == "Active":
            active.append(res)

    if not active:
        print("\nNo active reservations found.")
        pause()
        return

    # Use helper function to find reservation
    reservation = find_reservation_with_search(active, "Active Reservations")

    if not reservation:
        return

    # Display current charges
    print("\n")
    print_separator()
    display_reservation_details(reservation)
    print("\n")
    display_payment_summary(reservation)

    # Add charges
    print("\n")
    print_separator()
    print("ADD CHARGES")
    print_separator()

    print("\nCharge Categories:")
    print("1. Room Service")
    print("2. Minibar")
    print("3. Laundry")
    print("4. Restaurant")
    print("5. Spa/Wellness")
    print("6. Other")

    category_choice = validate_integer_input("\nSelect category (1-6): ", min_val=1, max_val=6)
    categories = {
        1: "Room Service",
        2: "Minibar",
        3: "Laundry",
        4: "Restaurant",
        5: "Spa/Wellness",
        6: "Other"
    }
    category = categories[category_choice]

    # Get charge details
    description = validate_string_input("Description: ", min_length=2, max_length=100)
    amount = validate_float_input("Amount (₱): ", min_val=0.01)

    # Update reservation
    reservation["additional_charges"] += amount
    reservation["balance"] = (reservation["total_cost"] + reservation["additional_charges"]) - reservation["total_paid"]

    # Update payment status if balance increased
    if reservation["payment_status"] == "Paid" and reservation["balance"] > 0:
        reservation["payment_status"] = "Partial"

    print("\n")
    print_separator()
    print("CHARGE ADDED SUCCESSFULLY!")
    print_separator()
    print(f"Category: {category}")
    print(f"Description: {description}")
    print(f"Amount: ₱{amount:,.2f}")
    print(f"\nNew Additional Charges: ₱{reservation['additional_charges']:,.2f}")
    print(f"New Balance: ₱{reservation['balance']:,.2f}")
    print(f"Payment Status: {reservation['payment_status']}")

    pause()


def issue_refund():
    """
    Issue a refund for a cancelled reservation
    Demonstrates DELETE/UPDATE operations on payment data
    """
    clear_screen()
    print_header("ISSUE REFUND")

    if not reservations_list:
        print("\nNo reservations found in the system.")
        pause()
        return

    # Show cancelled reservations with payments
    cancelled = []
    for res in reservations_list:
        if res["status"] == "Cancelled" and res.get("total_paid", 0) > 0:
            cancelled.append(res)

    if not cancelled:
        print("\nNo cancelled reservations with payments found.")
        pause()
        return

    # Use helper function to find reservation
    reservation = find_reservation_with_search(cancelled, "Cancelled Reservations with Payments")

    if not reservation:
        return

    # Check if reservation is cancelled
    if reservation["status"] != "Cancelled":
        print("\nRefunds can only be issued for cancelled reservations.")
        print("Please cancel the reservation first.")
        pause()
        return

    # Check if there are payments to refund
    if reservation["total_paid"] <= 0:
        print("\nNo payments found for this reservation. Nothing to refund.")
        pause()
        return

    # Display reservation and payment details
    print("\n")
    print_separator()
    display_reservation_details(reservation)
    print("\n")
    display_payment_summary(reservation)

    # Refund processing
    print("\n")
    print_separator()
    print("REFUND PROCESSING")
    print_separator()

    print(f"\nTotal Paid: ₱{reservation['total_paid']:,.2f}")
    print("\nRefund Policy:")
    print("  - Full Refund (100%): Cancellation 7+ days before check-in")
    print("  - Partial Refund (50%): Cancellation 3-6 days before check-in")
    print("  - No Refund: Cancellation less than 3 days before check-in")

    print("\nRefund Options:")
    print("1. Full Refund (100%)")
    print("2. Partial Refund (50%)")
    print("3. Custom Refund Amount")
    print("4. No Refund")

    refund_choice = validate_integer_input("\nSelect refund option (1-4): ", min_val=1, max_val=4)

    if refund_choice == 4:
        print("\nNo refund issued.")
        pause()
        return

    # Calculate refund amount
    if refund_choice == 1:
        refund_amount = reservation["total_paid"]
    elif refund_choice == 2:
        refund_amount = reservation["total_paid"] * 0.5
    else:  # Custom amount
        refund_amount = validate_float_input(f"Enter refund amount (₱, max {reservation['total_paid']:,.2f}): ",
                                             min_val=0.01, max_val=reservation['total_paid'])

    # Get refund details
    print("\nRefund Method:")
    for key, method in payment_methods.items():
        print(f"  {key}. {method}")

    method_choice = validate_integer_input("\nSelect refund method (1-5): ", min_val=1, max_val=5)
    refund_method = payment_methods[str(method_choice)]

    print("\nRefund Reference:")
    reference = input("Reference Number/Transaction ID: ").strip()
    if not reference:
        reference = "N/A"

    # Get refund date and time
    print("\nRefund Date and Time:")
    refund_date = validate_date_input("Refund Date (DD/MM/YYYY): ")
    refund_time = validate_time_input("Refund Time (HH:MM): ")

    # Generate payment ID for refund (negative payment)
    pay_id = generate_payment_id()

    # Create refund record (stored as negative payment)
    refund = {
        "id": pay_id,
        "reservation_id": reservation["id"],
        "guest_name": reservation["guest_name"],
        "amount": -refund_amount,  # Negative amount for refund
        "payment_method": refund_method,
        "reference": reference,
        "payment_date": refund_date,
        "payment_time": refund_time,
        "notes": f"REFUND - {refund_choice} option",
        "status": "Refunded"
    }

    # Add to payment structures
    payments_list.append(refund)
    if reservation["id"] not in reservation_payments:
        reservation_payments[reservation["id"]] = []
    reservation_payments[reservation["id"]].append(refund)

    # Update reservation
    reservation["total_paid"] -= refund_amount
    reservation["balance"] = (reservation["total_cost"] + reservation["additional_charges"]) - reservation["total_paid"]

    # Update payment status
    if reservation["total_paid"] <= 0:
        reservation["payment_status"] = "Refunded"
    else:
        reservation["payment_status"] = "Partial Refund"

    # Display refund confirmation
    print("\n")
    print_separator()
    print("REFUND PROCESSED SUCCESSFULLY!")
    print_separator()
    print(f"Refund ID: {refund['id']}")
    print(f"Amount Refunded: ₱{refund_amount:,.2f}")
    print(f"Refund Method: {refund_method}")
    print(f"Reference: {reference}")
    print(f"\nUpdated Payment Status: {reservation['payment_status']}")
    print(f"Remaining Amount Paid: ₱{reservation['total_paid']:,.2f}")

    pause()


def payment_reports():
    """
    Generate payment and revenue reports
    """
    clear_screen()
    print_header("PAYMENT REPORTS")

    if not payments_list:
        print("\nNo payment data available.")
        pause()
        return

    print("\nReport Options:")
    print("1. Overall Payment Summary")
    print("2. Payment Method Analysis")
    print("3. Outstanding Balances")
    print("4. Refund Report")

    report_choice = validate_integer_input("\nSelect report (1-4): ", min_val=1, max_val=4)

    if report_choice == 1:
        display_payment_summary_report()
    elif report_choice == 2:
        display_payment_method_analysis()
    elif report_choice == 3:
        display_outstanding_balances()
    elif report_choice == 4:
        display_refund_report()

    pause()


def display_payment_summary_report():
    """Display overall payment statistics"""
    print("\n")
    print_separator()
    print("OVERALL PAYMENT SUMMARY")
    print_separator()

    total_payments = 0
    total_refunds = 0
    total_revenue = 0

    for payment in payments_list:
        if payment["amount"] > 0:
            total_payments += payment["amount"]
            total_revenue += payment["amount"]
        else:
            total_refunds += abs(payment["amount"])
            total_revenue += payment["amount"]  # Subtract refunds

    paid_count = 0
    partial_count = 0
    pending_count = 0
    refunded_count = 0

    for res in reservations_list:
        if res["payment_status"] == "Paid":
            paid_count += 1
        elif res["payment_status"] == "Partial":
            partial_count += 1
        elif res["payment_status"] == "Pending":
            pending_count += 1
        elif "Refund" in res["payment_status"]:
            refunded_count += 1

    print(f"\nTotal Payments Received: ₱{total_payments:,.2f}")
    print(f"Total Refunds Issued: ₱{total_refunds:,.2f}")
    print(f"Net Revenue: ₱{total_revenue:,.2f}")
    print(f"\nTotal Transactions: {len(payments_list)}")
    print(f"Average Payment: ₱{total_payments / len([p for p in payments_list if p['amount'] > 0]):,.2f}" if any(p['amount'] > 0 for p in payments_list) else "N/A")

    print("\n")
    print("Payment Status Distribution:")
    print(f"  Fully Paid: {paid_count} reservations")
    print(f"  Partially Paid: {partial_count} reservations")
    print(f"  Pending Payment: {pending_count} reservations")
    print(f"  Refunded: {refunded_count} reservations")


def display_payment_method_analysis():
    """Display payment method breakdown"""
    print("\n")
    print_separator()
    print("PAYMENT METHOD ANALYSIS")
    print_separator()

    method_totals = {}
    method_counts = {}

    for payment in payments_list:
        if payment["amount"] > 0:  # Only count actual payments, not refunds
            method = payment["payment_method"]
            if method not in method_totals:
                method_totals[method] = 0
                method_counts[method] = 0
            method_totals[method] += payment["amount"]
            method_counts[method] += 1

    if not method_totals:
        print("\nNo payment data available.")
        return

    total = sum(method_totals.values())

    print("\nPayment Method Breakdown:")
    print_separator()
    print(f"{'Method':<20} {'Count':<10} {'Amount':<20} {'Percentage':<15}")
    print_separator()

    # Sort by amount (bubble sort)
    methods = list(method_totals.keys())
    for i in range(len(methods)):
        for j in range(len(methods) - i - 1):
            if method_totals[methods[j]] < method_totals[methods[j + 1]]:
                methods[j], methods[j + 1] = methods[j + 1], methods[j]

    for method in methods:
        count = method_counts[method]
        amount = method_totals[method]
        percentage = (amount / total * 100) if total > 0 else 0
        print(f"{method:<20} {count:<10} ₱{amount:>15,.2f}   {percentage:>6.2f}%")

    print_separator()
    print(f"{'TOTAL':<20} {sum(method_counts.values()):<10} ₱{total:>15,.2f}   100.00%")


def display_outstanding_balances():
    """Display reservations with outstanding balances"""
    print("\n")
    print_separator()
    print("OUTSTANDING BALANCES")
    print_separator()

    outstanding = []
    total_outstanding = 0

    for res in reservations_list:
        if res["balance"] > 0 and res["status"] == "Active":
            outstanding.append(res)
            total_outstanding += res["balance"]

    if not outstanding:
        print("\nNo outstanding balances! All active reservations are paid.")
        return

    print(f"\nTotal Outstanding: ₱{total_outstanding:,.2f}")
    print(f"Number of Reservations: {len(outstanding)}")
    print_separator()

    # Sort by balance (highest first)
    for i in range(len(outstanding)):
        for j in range(len(outstanding) - i - 1):
            if outstanding[j]["balance"] < outstanding[j + 1]["balance"]:
                outstanding[j], outstanding[j + 1] = outstanding[j + 1], outstanding[j]

    print(f"\n{'Reservation':<15} {'Guest':<25} {'Total':<15} {'Paid':<15} {'Balance':<15}")
    print_separator()

    for res in outstanding:
        total = res["total_cost"] + res["additional_charges"]
        print(f"{res['id']:<15} {res['guest_name']:<25} ₱{total:>12,.2f} ₱{res['total_paid']:>12,.2f} ₱{res['balance']:>12,.2f}")


def display_refund_report():
    """Display refund statistics"""
    print("\n")
    print_separator()
    print("REFUND REPORT")
    print_separator()

    refunds = []
    total_refunded = 0

    for payment in payments_list:
        if payment["amount"] < 0:  # Refunds are negative amounts
            refunds.append(payment)
            total_refunded += abs(payment["amount"])

    if not refunds:
        print("\nNo refunds have been issued.")
        return

    print(f"\nTotal Refunds Issued: ₱{total_refunded:,.2f}")
    print(f"Number of Refunds: {len(refunds)}")
    print_separator()

    print(f"\n{'Refund ID':<15} {'Reservation':<15} {'Guest':<25} {'Amount':<15}")
    print_separator()

    for refund in refunds:
        print(f"{refund['id']:<15} {refund['reservation_id']:<15} {refund['guest_name']:<25} ₱{abs(refund['amount']):>12,.2f}")


# ============================================================
# PAYMENT DISPLAY FUNCTIONS
# ============================================================

def display_payment_summary(reservation):
    """Display payment summary for a reservation"""
    print("PAYMENT SUMMARY")
    print_separator()

    room_charges = reservation["total_cost"]
    additional = reservation["additional_charges"]
    total = room_charges + additional
    paid = reservation["total_paid"]
    balance = reservation["balance"]

    print(f"Room Charges: ₱{room_charges:,.2f}")
    if additional > 0:
        print(f"Additional Charges: ₱{additional:,.2f}")
    print(f"Total Amount: ₱{total:,.2f}")
    print(f"Amount Paid: ₱{paid:,.2f}")
    print(f"Balance: ₱{balance:,.2f}")
    print(f"Payment Status: {reservation['payment_status']}")


def display_payment_summary_line(payment):
    """Display brief payment information"""
    amount_str = f"₱{payment['amount']:,.2f}" if payment['amount'] > 0 else f"-₱{abs(payment['amount']):,.2f}"
    status = "REFUND" if payment['amount'] < 0 else payment['status']
    print(f"ID: {payment['id']:<15} | Res: {payment['reservation_id']:<15} | Amount: {amount_str:>15}")
    print(f"Guest: {payment['guest_name']:<25} | Method: {payment['payment_method']:<15} | Status: {status}")
    print(f"Date: {payment['payment_date']['formatted']} {payment['payment_time']['formatted']}")


def display_payment_details(payment):
    """Display complete payment information"""
    print(f"Payment ID: {payment['id']}")
    print(f"Reservation ID: {payment['reservation_id']}")
    print(f"Guest: {payment['guest_name']}")
    print(f"Amount: ₱{payment['amount']:,.2f}")
    print(f"Payment Method: {payment['payment_method']}")
    print(f"Reference: {payment['reference']}")
    print(f"Date: {payment['payment_date']['formatted']} at {payment['payment_time']['formatted']}")
    print(f"Status: {payment['status']}")
    if payment['notes'] != "N/A":
        print(f"Notes: {payment['notes']}")


def display_payment_receipt(payment, reservation):
    """Display payment receipt"""
    print("PAYMENT RECEIPT")
    print(f"Payment ID: {payment['id']}")
    print(f"Reservation ID: {payment['reservation_id']}")
    print()
    print(f"Guest Name: {payment['guest_name']}")
    print(f"Room Number: {reservation['room_number']}")
    print()
    print(f"Amount Paid: ₱{payment['amount']:,.2f}")
    print(f"Payment Method: {payment['payment_method']}")
    print(f"Reference: {payment['reference']}")
    print(f"Date: {payment['payment_date']['formatted']} at {payment['payment_time']['formatted']}")
    print()
    print("Updated Billing:")
    print(f"  Total Bill: ₱{reservation['total_cost'] + reservation['additional_charges']:,.2f}")
    print(f"  Total Paid: ₱{reservation['total_paid']:,.2f}")
    print(f"  Balance: ₱{reservation['balance']:,.2f}")
    print(f"  Status: {reservation['payment_status']}")





# ============================================================
# DISPLAY FUNCTIONS
# ============================================================

def display_room_types():
    """Display available room types and prices"""
    print("\nAvailable Room Types:")
    print("-" * 70)
    print(f"{'Type':<5} {'Room Type':<25} {'Capacity':<12} {'Price/Night':<15}")
    print("-" * 70)

    for key, info in room_types.items():
        print(f"{key:<5} {info['type']:<25} {info['capacity']} guest(s)   ₱{info['price']:>10,.2f}")


def display_reservation_summary(reservation):
    """Display brief reservation information"""
    print(f"ID: {reservation['id']:<15} | Guest: {reservation['guest_name']:<25}")
    print(f"Room: {reservation['room_number']:<12} | Type: {reservation['room_type']:<25}")
    print(f"Check-in: {reservation['check_in_date']['formatted']:<12} | Nights: {reservation['nights']:<5} | Total: ₱{reservation['total_cost']:>10,.2f}")
    print(f"Status: {reservation['status']:<12} | Payment: {reservation['payment_status']}")


def display_reservation_details(reservation):
    """Display complete reservation information"""
    print(f"Reservation ID: {reservation['id']}")
    print(f"Status: {reservation['status']}")
    print()
    print("Guest Information:")
    print(f"  Name: {reservation['guest_name']}")
    print(f"  Phone: {reservation['phone']}")
    print(f"  Email: {reservation['email']}")
    print(f"  Number of Guests: {reservation['num_guests']}")
    print()
    print("Room Information:")
    print(f"  Room Number: {reservation['room_number']}")
    print(f"  Room Type: {reservation['room_type']}")
    print(f"  Price per Night: ₱{reservation['price_per_night']:,.2f}")
    print()
    print("Stay Information:")
    print(f"  Check-in: {reservation['check_in_date']['formatted']} at {reservation['check_in_time']['formatted']}")
    print(f"  Check-out: {reservation['check_out_date']['formatted']} at {reservation['check_out_time']['formatted']}")
    print(f"  Number of Nights: {reservation['nights']}")
    print()
    print("Billing Information:")
    print(f"  Room Charges: ₱{reservation['total_cost']:,.2f}")
    if reservation.get('additional_charges', 0) > 0:
        print(f"  Additional Charges: ₱{reservation['additional_charges']:,.2f}")
        print(f"  Total Amount: ₱{reservation['total_cost'] + reservation['additional_charges']:,.2f}")
    else:
        print(f"  Total Amount: ₱{reservation['total_cost']:,.2f}")
    print(f"  Amount Paid: ₱{reservation.get('total_paid', 0):,.2f}")
    print(f"  Balance: ₱{reservation.get('balance', reservation['total_cost']):,.2f}")
    print(f"  Payment Status: {reservation.get('payment_status', 'Pending')}")


# ============================================================
# REPORT & STATISTICS FUNCTIONS
# ============================================================

def generate_reports():
    """Generate statistical reports from the data"""
    clear_screen()
    print_header("SYSTEM REPORTS & STATISTICS")

    if not reservations_list:
        print("\nNo data available for reports.")
        pause()
        return

    print("\nReport Options:")
    print("1. Occupancy Report")
    print("2. Revenue Report")
    print("3. Guest Statistics")

    report_choice = validate_integer_input("\nSelect report (1-3): ", min_val=1, max_val=3)

    if report_choice == 1:
        display_occupancy_report()
    elif report_choice == 2:
        display_revenue_report()
    elif report_choice == 3:
        display_guest_statistics()

    pause()


def display_occupancy_report():
    """Display room occupancy statistics"""
    print("\n")
    print_separator()
    print("OCCUPANCY REPORT")
    print_separator()

    total_rooms = 0
    occupied_rooms = 0

    for key in available_rooms:
        total_rooms += len(available_rooms[key])

    # Count occupied rooms (with active reservations)
    occupied_set = []
    for res in reservations_list:
        if res["status"] == "Active" and res["room_number"] not in occupied_set:
            occupied_set.append(res["room_number"])
            occupied_rooms += 1

    occupancy_rate = (occupied_rooms / total_rooms * 100) if total_rooms > 0 else 0

    print(f"Total Rooms: {total_rooms}")
    print(f"Occupied Rooms: {occupied_rooms}")
    print(f"Available Rooms: {total_rooms - occupied_rooms}")
    print(f"Occupancy Rate: {occupancy_rate:.2f}%")

    print("\nOccupancy by Room Type:")
    for key, info in room_types.items():
        total = len(available_rooms[key])
        occupied = 0
        for res in reservations_list:
            if res["status"] == "Active" and res["room_type"] == info["type"]:
                occupied += 1
        print(f"  {info['type']}: {occupied}/{total} occupied")


def display_revenue_report():
    """Display revenue statistics"""
    print("\n")
    print_separator()
    print("REVENUE REPORT")
    print_separator()

    total_revenue = 0
    active_revenue = 0
    cancelled_count = 0

    for res in reservations_list:
        total_revenue += res["total_cost"]
        if res["status"] == "Active":
            active_revenue += res["total_cost"]
        else:
            cancelled_count += 1

    print(f"Total Reservations: {len(reservations_list)}")
    print(f"Active Reservations: {len(reservations_list) - cancelled_count}")
    print(f"Cancelled Reservations: {cancelled_count}")
    print()
    print(f"Total Revenue (All): ₱{total_revenue:,.2f}")
    print(f"Active Revenue: ₱{active_revenue:,.2f}")
    print(f"Average per Reservation: ₱{total_revenue / len(reservations_list):,.2f}" if reservations_list else "N/A")

    # Revenue by room type
    print("\nRevenue by Room Type:")
    for key, info in room_types.items():
        type_revenue = 0
        for res in reservations_list:
            if res["room_type"] == info["type"]:
                type_revenue += res["total_cost"]
        if type_revenue > 0:
            print(f"  {info['type']}: ₱{type_revenue:,.2f}")


def display_guest_statistics():
    """Display guest-related statistics"""
    print("\n")
    print_separator()
    print("GUEST STATISTICS")
    print_separator()

    total_guests = 0
    guest_count_distribution = {}

    for res in reservations_list:
        if res["status"] == "Active":
            total_guests += res["num_guests"]

            if res["num_guests"] not in guest_count_distribution:
                guest_count_distribution[res["num_guests"]] = 0
            guest_count_distribution[res["num_guests"]] += 1

    print(f"Total Guests (Active Reservations): {total_guests}")
    print(f"Average Guests per Reservation: {total_guests / (len(reservations_list) - sum(1 for r in reservations_list if r['status'] == 'Cancelled')):.2f}" if reservations_list else "N/A")

    print("\nGuest Count Distribution:")
    for count in sorted(guest_count_distribution.keys()):
        print(f"  {count} guest(s): {guest_count_distribution[count]} reservation(s)")


# ============================================================
# MAIN MENU
# ============================================================

def display_main_menu():
    """Display the main menu"""
    clear_screen()
    print_header("HOTEL MANAGEMENT SYSTEM")
    print("\n" + "=" * 70)
    print("MAIN MENU".center(70))
    print("=" * 70)
    print("\n[RESERVATION OPERATIONS]")
    print("  1. CREATE - New Reservation")
    print("  2. READ - View All Reservations")
    print("  3. UPDATE - Modify Reservation")
    print("  4. DELETE - Remove Reservation")
    print("  5. SEARCH - Find Reservations")
    print("  6. SORT - Sort & Display Reservations")
    print("\n[PAYMENT MANAGEMENT]")
    print("  7. Process Payment")
    print("  8. View All Payments")
    print("  9. View Reservation Payments")
    print(" 10. Add Additional Charges")
    print(" 11. Issue Refund")
    print(" 12. Payment Reports")
    print("\n[REPORTS & INFORMATION]")
    print(" 13. Generate Reports")
    print(" 14. View Room Types & Prices")
    print("\n[SYSTEM]")
    print(" 15. About the System")
    print("  0. Exit")
    print("\n" + "=" * 70)


def display_about():
    """Display information about the system"""
    clear_screen()
    print_header("ABOUT THE SYSTEM")

    print("\nHotel Management System v1.0")
    print("Data Structures & Algorithms Final Project")
    print_separator()

    print("\nTECHNICAL FEATURES:")
    print("  ✓ CRUDS Operations: Create, Read, Update, Delete, Search, Sort")
    print("  ✓ Linear Data Structures: Lists/Arrays for reservation & payment storage")
    print("  ✓ Non-Linear Data Structures: Dictionaries for room & payment indexing")
    print("  ✓ Pure Python: No external libraries used")
    print("  ✓ Input Validation: All inputs validated with re-prompting")
    print("  ✓ Manual Date/Time: Custom date and time handling")
    print("  ✓ Sorting Algorithms: Bubble sort implementation")
    print("  ✓ Search Algorithms: Linear search and dictionary lookups")
    print("  ✓ Payment System: Comprehensive payment tracking and management")

    print("\nDATA STRUCTURES USED:")
    print("  1. Lists (Linear): Reservation & payment storage")
    print("  2. Dictionaries (Non-Linear): Room-based & reservation-based indexing")
    print("  3. Nested Dictionaries: Complex data representation")

    print("\nFEATURES:")
    print("  • Multiple room types with different capacities and prices")
    print("  • Complete guest information management")
    print("  • Check-in/Check-out date and time tracking")
    print("  • Automatic cost calculation")
    print("  • Reservation status tracking")
    print("  • Comprehensive search capabilities")
    print("  • Multiple sorting options")
    print("  • Statistical reports")
    print("\nPAYMENT FEATURES:")
    print("  • Multiple payment methods (Cash, Card, Bank Transfer, etc.)")
    print("  • Payment status tracking (Pending, Partial, Paid)")
    print("  • Additional charges management (Room service, minibar, etc.)")
    print("  • Refund processing with flexible options")
    print("  • Payment history for each reservation")
    print("  • Comprehensive payment reports and analytics")
    print("  • Outstanding balance tracking")

    pause()


def main():
    """Main program loop"""
    print_header("WELCOME TO HOTEL MANAGEMENT SYSTEM")
    print("\nInitializing system...")
    print("Loading data structures...")
    print("Payment system ready...")
    print("System ready!")
    pause()

    while True:
        display_main_menu()

        choice = validate_integer_input("\nEnter your choice (0-15): ", min_val=0, max_val=15)

        if choice == 1:
            create_reservation()
        elif choice == 2:
            read_reservations()
        elif choice == 3:
            update_reservation()
        elif choice == 4:
            delete_reservation()
        elif choice == 5:
            search_reservations()
        elif choice == 6:
            sort_reservations()
        elif choice == 7:
            process_payment()
        elif choice == 8:
            view_payments()
        elif choice == 9:
            view_reservation_payments()
        elif choice == 10:
            add_additional_charges()
        elif choice == 11:
            issue_refund()
        elif choice == 12:
            payment_reports()
        elif choice == 13:
            generate_reports()
        elif choice == 14:
            clear_screen()
            print_header("ROOM TYPES & PRICES")
            display_room_types()
            pause()
        elif choice == 15:
            display_about()
        elif choice == 0:
            clear_screen()
            print_header("THANK YOU")
            print("\nThank you for using the Hotel Management System!")
            print("Goodbye!")
            print("\n" + "=" * 70)
            break


# ============================================================
# PROGRAM ENTRY POINT
# ============================================================

if __name__ == "__main__":
    main()