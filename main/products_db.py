from main.schemas.product_details import Product
from typing import Dict

products_db: Dict[str, Product] = {
    "iPhone 15 Pro Max": Product(
        name="iPhone 15 Pro Max",
        category="smartphone",
        description="Apple smartphone with A17 Pro chip, 6.7-inch OLED display, 256GB storage.",
        price=1199.00
    ),
    "Samsung Galaxy S24 Ultra": Product(
        name="Samsung Galaxy S24 Ultra",
        category="smartphone",
        description="Android flagship with Snapdragon 8 Gen 3, 200MP camera, 6.8-inch QHD+ display, 512GB storage.",
        price=1299.99
    ),
    "Sony Bravia XR A80L 65-inch OLED TV": Product(
        name="Sony Bravia XR A80L 65-inch OLED TV",
        category="television",
        description="65-inch 4K OLED TV with Google TV, HDR10, Dolby Vision, and Acoustic Surface Audio+.",
        price=1999.99
    ),
    "LG C3 55-inch OLED TV": Product(
        name="LG C3 55-inch OLED TV",
        category="television",
        description="4K OLED with α9 AI Processor Gen6, Dolby Vision IQ, 120Hz refresh rate, HDMI 2.1.",
        price=1499.00
    ),
    "NVIDIA GeForce RTX 4090": Product(
        name="NVIDIA GeForce RTX 4090",
        category="graphics-card",
        description="High-end GPU with 24GB GDDR6X memory, DLSS 3.0, Ray Tracing, PCIe 4.0.",
        price=1599.00
    ),
    "AMD Radeon RX 7900 XTX": Product(
        name="AMD Radeon RX 7900 XTX",
        category="graphics-card",
        description="Graphics card with 24GB GDDR6, RDNA 3 architecture, Ray Tracing, DisplayPort 2.1.",
        price=999.99
    ),
    "MacBook Pro 14 (M3 Pro, 2023)": Product(
        name="MacBook Pro 14 (M3 Pro, 2023)",
        category="smartphone",
        description="14-inch Liquid Retina XDR display, M3 Pro chip (11-core CPU, 14-core GPU), 1TB SSD.",
        price=2199.00
    ),
    "ASUS ROG Zephyrus G14": Product(
        name="ASUS ROG Zephyrus G14",
        category="laptop",
        description="Gaming laptop with AMD Ryzen 9 7940HS, NVIDIA RTX 4070, 1TB SSD, 165Hz QHD display.",
        price=1899.99
    ),
    "Sony WH-1000XM5": Product(
        name="Sony WH-1000XM5",
        category="headphone",
        description="Wireless noise-canceling headphones with 30-hour battery, LDAC, and speak-to-chat.",
        price=399.99
    ),
    "Samsung Galaxy Tab S9 Ultra": Product(
        name="Samsung Galaxy Tab S9 Ultra",
        category="smartphone",
        description="Android tablet with 14.6-inch AMOLED display, Snapdragon 8 Gen 2, 512GB storage.",
        price=1199.99
    )
}
