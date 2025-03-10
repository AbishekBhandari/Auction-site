# Auction Site

## Overview
This is a web-based auction platform built using Django. Users can create, view, and bid on auction listings, add listings to their watchlist, and comment on listings. Listings belong to various categories, and users can close auctions when bidding is complete. An administrator can manage all listings, comments, and bids through the Django admin interface.

## Features
### Models
The application includes the following models:
- **User**: Handles user authentication and management.
- **Listing**: Represents an auction listing with fields like title, description, starting bid, image URL, and category.
- **Bid**: Tracks bids placed on listings, ensuring they meet bidding criteria.
- **Comment**: Stores user comments on auction listings.

### Functionalities
#### 1. Create Listing
- Users can create new auction listings by providing a title, description, starting bid, optional image URL, and category.

#### 2. Active Listings Page
- Displays all currently active auction listings, showing title, description, current price, and an image if available.

#### 3. Listing Page
- Shows complete details of a listing.
- Signed-in users can:
  - Add or remove the listing from their watchlist.
  - Place a bid if it meets the criteria.
  - Comment on the listing.
  - Close the auction (if they created the listing).
- If the auction is closed, the winner is displayed.

#### 4. Watchlist
- A page where users can see all the listings they have added to their watchlist.

#### 5. Categories
- Users can browse listings by category.

#### 6. Django Admin Interface
- Administrators can manage listings, bids, and comments.

## Installation
### Prerequisites
- Python 3.x
- Django

### Setup
1. Clone the repository:
   ```sh
   git clone https://github.com/AbishekBhandari/Auction-site.git
   cd Auction-site
   ```
2. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```
3. Run database migrations:
   ```sh
   python manage.py migrate
   ```
4. Create a superuser for the admin interface:
   ```sh
   python manage.py createsuperuser
   ```
5. Start the development server:
   ```sh
   python manage.py runserver
   ```
6. Access the application at `http://127.0.0.1:8000/`.

## Usage
- Register or log in.
- Create, view, and bid on listings.
- Manage your watchlist.
- Close auctions if you are the listing owner.
- Browse by categories.
- Comment on listings.

## Contributing
Contributions are welcome! Feel free to submit issues or pull requests.

## License
This project is done as part of CS50 web

