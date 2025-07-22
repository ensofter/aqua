# Админ-панель для телеграм бота

Веб-приложение для управления категориями и товарами телеграм бота.

## Структура проекта

- `backend/` - FastAPI сервер (Python)
- `frontend/` - Vue.js клиент (TypeScript + Tailwind CSS)

## Функциональность

### ✅ Реализовано
- 🔐 **Страница авторизации** с логином и паролем
- 📊 **Главная админ-панель** с вкладками "Категории" и "Товары"
- 📁 **Управление категориями**: просмотр, добавление, редактирование, удаление
- 🛍️ **Управление товарами**: просмотр, добавление, редактирование, удаление
- 💾 **Хранение данных** в оперативной памяти (Python словари)
- 🔄 **REST API** с авторизацией Basic Auth
- 🎨 **Современный UI** с Tailwind CSS

## Запуск проекта

### Backend (FastAPI)
```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend (Vue.js)
```bash
cd frontend
npm install
npm run dev -- --host 0.0.0.0
```

## Доступ к приложению

- **Frontend**: http://localhost:5173
- **Backend API**: http://localhost:8000
- **API документация**: http://localhost:8000/docs

## Данные для входа

- **Логин**: `admin`
- **Пароль**: `admin123`

## API Endpoints

### Категории
- `GET /categories` - получить все категории
- `POST /categories` - создать категорию
- `PUT /categories/{category_name}` - обновить категорию
- `DELETE /categories/{category_name}` - удалить категорию

### Товары
- `GET /items` - получить все товары
- `POST /items` - создать товар
- `PUT /items/{item_id}` - обновить товар
- `DELETE /items/{item_id}` - удалить товар

## Особенности

- Данные хранятся в оперативной памяти и исчезают при перезапуске сервера
- Авторизация сохраняется в localStorage браузера
- Responsive дизайн для мобильных устройств
- Валидация форм и обработка ошибок
