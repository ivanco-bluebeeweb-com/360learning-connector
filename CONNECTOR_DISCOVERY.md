# 360Learning Connector — Discovery & Vendor API Specification

**Официальный сайт:** https://360learning.com  
**Базовый эндпоинт API:** `https://api.360learning.com/api/v1`  
**Схема авторизации:** API Key (Authorization: <api-key>)

## Поддерживаемые сущности API
- курсы programs (/programs)
- сессии обучения sessions (/sessions)
- пользователи learners
- группы групп

## Архитектурные требования
- Использование безопасного клиента с контролем таймаутов, повторных попыток (backoff) и обработкой rate limit.
- Валидация входных данных через Pydantic-схемы без утечки чувствительных полей в логи.
- Тестовая точка проверки подключения: `GET /api/v1/programs`.
