# Your-Little-Outlet (YLO)

## Overview

**Your-Little-Outlet (YLO)** is a feature-rich e-commerce platform built with Django. This project demonstrates my proficiency in building scalable web applications with a focus on user experience and functionality. It includes user authentication, product management, and order processing capabilities, all designed to provide a seamless shopping experience.

## Key Features

- **User Authentication**: Secure registration and login system using Django's built-in user model.
- **Profile Management**: Customers can manage their profiles, including personal information and profile pictures.
- **Product Catalog**: Comprehensive product listings categorized for easy browsing, with detailed descriptions and images.
- **Shopping Cart**: Users can add products to their cart, manage quantities, and proceed to checkout.
- **Order Management**: Users can view their order history and track the status of their orders.
- **Image Uploads**: Support for uploading product and profile images, ensuring a rich visual experience.

## Technologies Used

- **Backend**: Django
- **Database**: SQLite (Django’s built-in database)
- **Frontend**: HTML, CSS, JavaScript (Django templating)

## Models

- **Customer**: Extends the user model with additional fields for profile information.
- **Categorie**: Manages product categories.
- **Product**: Represents products with attributes like name, description, price, and stock.
- **OrderItem**: Details of items in a user's order, including quantity and size.
- **Order**: Tracks user orders, including order history and payment details.
