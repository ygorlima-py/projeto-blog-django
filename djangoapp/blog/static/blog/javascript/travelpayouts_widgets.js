(() => {
    'use strict';

    const WIDGET_SELECTOR =
        '.travelpayouts-widget[data-travelpayouts-src]';
    const MAX_URL_LENGTH = 4096;
    const ALLOWED_HOSTS = new Set(['tpemd.com']);
    const ALLOWED_PATHS = new Set(['/content']);
    const UNSAFE_URL_CHARACTERS = /[\\\u0000-\u001f\u007f]/;

    const parseWidgetUrl = (rawUrl) => {
        if (
            typeof rawUrl !== 'string'
            || rawUrl.length === 0
            || rawUrl.length > MAX_URL_LENGTH
            || rawUrl.trim() !== rawUrl
            || UNSAFE_URL_CHARACTERS.test(rawUrl)
        ) {
            return null;
        }

        let widgetUrl;

        try {
            widgetUrl = new URL(rawUrl);
        } catch (error) {
            return null;
        }

        if (
            widgetUrl.protocol !== 'https:'
            || !ALLOWED_HOSTS.has(widgetUrl.hostname)
            || !ALLOWED_PATHS.has(widgetUrl.pathname)
            || widgetUrl.port !== ''
            || widgetUrl.username !== ''
            || widgetUrl.password !== ''
            || widgetUrl.hash !== ''
        ) {
            return null;
        }

        return widgetUrl;
    };

    const loadWidget = (marker) => {
        if (marker.dataset.travelpayoutsState) {
            return;
        }

        const widgetUrl = parseWidgetUrl(
            marker.getAttribute('data-travelpayouts-src'),
        );

        if (!widgetUrl) {
            marker.dataset.travelpayoutsState = 'invalid';
            return;
        }

        marker.dataset.travelpayoutsState = 'loading';

        const script = document.createElement('script');
        script.async = true;
        script.charset = 'utf-8';
        script.src = widgetUrl.href;
        script.setAttribute('data-cfasync', 'false');

        script.addEventListener('load', () => {
            marker.dataset.travelpayoutsState = 'loaded';
        }, {once: true});

        script.addEventListener('error', () => {
            marker.dataset.travelpayoutsState = 'error';
            script.remove();
        }, {once: true});

        marker.appendChild(script);
    };

    const loadTravelpayoutsWidgets = () => {
        document.querySelectorAll(WIDGET_SELECTOR).forEach(loadWidget);
    };

    if (document.readyState === 'loading') {
        document.addEventListener(
            'DOMContentLoaded',
            loadTravelpayoutsWidgets,
            {once: true},
        );
    } else {
        loadTravelpayoutsWidgets();
    }
})();
