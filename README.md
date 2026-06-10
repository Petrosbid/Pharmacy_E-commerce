# 💊 Modern Pharmacy Digital Platform

### A high-performance, fully localized, and secure E-commerce & Prescription Management system for modern pharmacies.

[![Django Version](https://img.shields.io/badge/Django-6.0-092E20?style=for-the-badge&logo=django)](https://www.djangoproject.com/)
[![Python Version](https://img.shields.io/badge/Python-3.13+-3776AB?style=for-the-badge&logo=python)](https://www.python.org/)
[![Localization](https://img.shields.io/badge/Locale-fa--IR-red?style=for-the-badge)](https://en.wikipedia.org/wiki/Languages_of_Iran)
[![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](https://opensource.org/licenses/MIT)
[![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-blue?style=for-the-badge)](https://github.com/)

---

## ✨ Features

- **📱 Secure Phone-based Authentication:** Custom user model utilizing phone numbers as primary identifiers, optimized for the Iranian market.
- **📄 Digital Prescription System:** Seamless file upload interface for prescriptions with real-time status tracking (Pending → Reviewed → Confirmed).
- **🛒 Robust E-commerce Engine:**
  - Dynamic product catalog with category filtering.
  - Advanced product badges (New, Sale, Bestseller).
  - Persistent shopping cart and order lifecycle management.
- **💳 Payment Gateway Integration:** Native support for the **Zarinpal** payment provider, ensuring secure local transactions.
- **💬 Social Proof & Engagement:**
  - Verified purchase review system.
  - Integrated blog for health news and pharmaceutical updates.
- **📊 Enterprise Admin Dashboard:** Powered by `Material Admin`, providing a sleek, responsive interface for managing inventory, orders, and prescriptions.
- **🌍 Full Localization:** Built-in RTL (Right-to-Left) support, Persian (Farsi) translations, and Tehran timezone configuration.

---

## 🏗️ Tech Stack

| Component | Technology |
| :--- | :--- |
| **Backend** | Django 6.0, Python 3.13+ |
| **Database** | SQLite (Development) / PostgreSQL (Production Ready) |
| **Frontend** | Django Templates, Vanilla CSS/JS, Material Design Assets |
| **Authentication** | Custom User Model (Phone-based) |
| **Payments** | Zarinpal PG Integration |
| **Localization** | Django i18n (fa-ir) |

---

## ⚡ Getting Started

### Prerequisites

- **Python:** 3.13 or higher
- **Virtual Environment:** `venv` or `pipenv`

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/your-username/pharmacy-platform.git
   cd pharmacy-platform
   ```

2. **Set up the virtual environment:**
   ```bash
   python -m venv .venv
   # Windows
   .venv\Scripts\activate
   # Linux/macOS
   source .venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Initialize the database:**
   ```bash
   python manage.py migrate
   ```

5. **Create a superuser (for admin access):**
   ```bash
   python manage.py createsuperuser
   ```

### Running the Application

```bash
python manage.py runserver
```
Access the application at `http://127.0.0.1:8000/`. The admin dashboard is available at `/admin/`.

---

## 🚀 Usage & API Highlights

### Prescription Workflow
1. **User Upload:** Users upload a scan/photo of their prescription via `/prescriptions/upload/`.
2. **Admin Review:** Pharmacists review the file in the Material Dashboard.
3. **Confirmation:** Once reviewed, the status is updated, and the user can proceed to payment if applicable.

### Payment Integration
The system uses a modular Gateway pattern:
```python
# payment/gateways.py
gateway = ZarinpalGateway(merchant_id="YOUR_ID")
response = gateway.request_payment(amount=10000, description="Order #123", callback_url=...)
```

---

## 🗺️ Roadmap

- [x] Initial Core Architecture & Database Schema
- [x] Custom Phone-based Authentication
- [x] Prescription Upload System
- [x] Zarinpal Gateway Integration
- [ ] SMS Gateway Integration for OTP (Verification)
- [ ] PWA Support for Mobile App experience
- [ ] Advanced Inventory Analytics Dashboard

---

## 🤝 Contributing & License

Contributions are welcome! Please feel free to submit a Pull Request.

This project is licensed under the **MIT License**.

---

> **Note:** This project is designed for pharmaceutical businesses looking to digitize their operations with a focus on regional compliance and user experience.
