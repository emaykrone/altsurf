// pixel.js

(function() {
    // Конфигурация пикселя
    // ВНИМАНИЕ: Для продакшена 'http://127.0.0.1:8000' нужно будет заменить на домен твоего сервера!
    const API_ENDPOINT = 'http://127.0.0.1:8000/api/event/';
    const PROJECT_ID = 1; // ID проекта. Для MVP пока 1. Позже будем получать из настроек.

    function generateUniqueId() {
        return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function(c) {
            var r = Math.random() * 16 | 0, v = c == 'x' ? r : (r & 0x3 | 0x8);
            return v.toString(16);
        });
    }

    function getCookie(name) {
        const value = `; ${document.cookie}`;
        const parts = value.split(`; ${name}=`);
        if (parts.length === 2) return parts.pop().split(';').shift();
        return null;
    }

    function setCookie(name, value, days) {
        const d = new Date();
        d.setTime(d.getTime() + (days * 24 * 60 * 60 * 1000));
        const expires = `expires=${d.toUTCString()}`;
        document.cookie = `${name}=${value};${expires};path=/;SameSite=Lax`;
    }

    // Получаем или генерируем client_id (аналог _ym_uid)
    let clientId = getCookie('_my_pixel_cid');
    if (!clientId) {
        clientId = generateUniqueId();
        setCookie('_my_pixel_cid', clientId, 365); // Храним год
    }

    // Отправка события на наш API
    function trackEvent(eventName, payload = {}) {
        const data = {
            project_id: PROJECT_ID,
            event_name: eventName,
            client_timestamp: Date.now(), // Время события на клиенте
            client_id: clientId,
            url: window.location.href,
            referrer: document.referrer,
            ...payload // Дополнительные данные, например, em, ph, lid, uid, data
        };

        fetch(API_ENDPOINT, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                // 'Accept': 'application/json', // Не всегда нужно для пикселей, т.к. ответ 204
            },
            body: JSON.stringify(data),
            mode: 'cors', // Обязательно для кросс-доменных запросов
            credentials: 'omit' // Не отправляем куки из домена клиента на наш сервер пикселя
        })
        .then(response => {
            if (response.status === 204) {
                console.log(`Pixel event '${eventName}' sent successfully (204 No Content)`);
            } else if (!response.ok) {
                console.error(`Failed to send pixel event '${eventName}'. Status: ${response.status}`);
                // Для отладки можно распечатать текст ошибки
                response.text().then(text => console.error('Response text:', text));
            }
        })
        .catch(error => {
            console.error(`Error sending pixel event '${eventName}':`, error);
        });
    }

    // Отслеживание просмотра страницы при загрузке
    trackEvent('page_view');

    // Глобальная функция для отслеживания кастомных событий (например, lead_submit)
    // Аналогично tomi.track, но названа myPixel.track, чтобы не конфликтовать.
    window.myPixel = {
        track: trackEvent,
        // Дополнительные утилиты, если понадобятся
        generateUniqueId: generateUniqueId
    };

    console.log("My Pixel initialized.");
})();