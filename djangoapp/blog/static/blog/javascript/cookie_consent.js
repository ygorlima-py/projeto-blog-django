(function () {
    'use strict';

    const COOKIE_NAME = 'asia_de_perto_cookie_consent';
    const COOKIE_VERSION = 1;
    const COOKIE_MAX_AGE = 60 * 60 * 24 * 180;
    const DEFAULT_PREFERENCES = Object.freeze({
        necessary: true,
        analytics: false,
        preferences: false,
    });

    function normalizePreferences(value) {
        if (!value || value.version !== COOKIE_VERSION) {
            return null;
        }

        return {
            necessary: true,
            analytics: value.analytics === true,
            preferences: value.preferences === true,
        };
    }

    function readPreferences() {
        const prefix = `${COOKIE_NAME}=`;
        const cookie = document.cookie
            .split(';')
            .map((item) => item.trim())
            .find((item) => item.startsWith(prefix));

        if (!cookie) {
            return null;
        }

        try {
            const value = JSON.parse(decodeURIComponent(cookie.slice(prefix.length)));
            return normalizePreferences(value);
        } catch (error) {
            return null;
        }
    }

    function writePreferences(preferences) {
        const value = encodeURIComponent(JSON.stringify({
            version: COOKIE_VERSION,
            analytics: preferences.analytics,
            preferences: preferences.preferences,
            updatedAt: new Date().toISOString(),
        }));
        const secure = window.location.protocol === 'https:' ? '; Secure' : '';

        document.cookie = `${COOKIE_NAME}=${value}; Path=/; Max-Age=${COOKIE_MAX_AGE}; SameSite=Lax${secure}`;
    }

    function consentIsGranted(category, preferences) {
        return category === 'necessary' || preferences[category] === true;
    }

    function activateConsentScripts(preferences) {
        const scripts = document.querySelectorAll(
            'script[type="text/plain"][data-cookie-category]:not([data-cookie-activated])'
        );

        scripts.forEach((sourceScript) => {
            const category = sourceScript.dataset.cookieCategory;

            if (!consentIsGranted(category, preferences)) {
                return;
            }

            const activeScript = document.createElement('script');

            Array.from(sourceScript.attributes).forEach((attribute) => {
                if (
                    attribute.name !== 'type'
                    && attribute.name !== 'data-cookie-category'
                    && attribute.name !== 'data-cookie-activated'
                ) {
                    activeScript.setAttribute(attribute.name, attribute.value);
                }
            });

            activeScript.dataset.cookieCategory = category;
            activeScript.dataset.cookieActivated = 'true';
            activeScript.textContent = sourceScript.textContent;
            sourceScript.dataset.cookieActivated = 'true';
            sourceScript.insertAdjacentElement('afterend', activeScript);
        });
    }

    function googleAnalyticsId() {
        const meta = document.querySelector('meta[name="google-analytics-id"]');
        return meta ? meta.content.trim() : '';
    }

    function deleteCookie(name, domain) {
        const secure = window.location.protocol === 'https:' ? '; Secure' : '';
        const domainAttribute = domain ? `; Domain=${domain}` : '';

        document.cookie = `${name}=; Path=/; Max-Age=0; SameSite=Lax${domainAttribute}${secure}`;
    }

    function removeAnalyticsCookies() {
        const hostname = window.location.hostname;
        const hostnameParts = hostname.split('.');
        const rootDomain = hostnameParts.length > 1
            ? `.${hostnameParts.slice(-2).join('.')}`
            : '';
        const analyticsCookies = document.cookie
            .split(';')
            .map((item) => item.trim().split('=')[0])
            .filter((name) => /^(_ga|_gid|_gat)/.test(name));

        analyticsCookies.forEach((name) => {
            deleteCookie(name, '');
            deleteCookie(name, hostname);

            if (rootDomain) {
                deleteCookie(name, rootDomain);
            }
        });
    }

    function applyAnalyticsChoice(isAllowed) {
        const measurementId = googleAnalyticsId();

        if (measurementId) {
            window[`ga-disable-${measurementId}`] = !isAllowed;
        }

        if (typeof window.gtag === 'function') {
            window.gtag('consent', 'update', {
                analytics_storage: isAllowed ? 'granted' : 'denied',
            });
        }

        if (!isAllowed) {
            removeAnalyticsCookies();
        }
    }

    function emitChange(preferences, eventName) {
        document.dispatchEvent(new CustomEvent(eventName, {
            detail: { ...preferences },
        }));
    }

    function applyPreferences(preferences, eventName) {
        document.documentElement.dataset.cookieAnalytics = preferences.analytics
            ? 'granted'
            : 'denied';
        document.documentElement.dataset.cookiePreferences = preferences.preferences
            ? 'granted'
            : 'denied';

        applyAnalyticsChoice(preferences.analytics);
        activateConsentScripts(preferences);
        emitChange(preferences, eventName);
    }

    function initialize() {
        const banner = document.querySelector('[data-cookie-banner]');
        const preferencesDialog = document.querySelector('[data-cookie-preferences]');
        const analyticsToggle = document.querySelector('[data-cookie-analytics]');
        const preferencesToggle = document.querySelector('[data-cookie-preferences-toggle]');
        let currentPreferences = readPreferences();

        function syncToggles(preferences) {
            if (analyticsToggle) {
                analyticsToggle.checked = preferences.analytics;
            }

            if (preferencesToggle) {
                preferencesToggle.checked = preferences.preferences;
            }
        }

        function showBanner() {
            if (banner) {
                banner.hidden = false;
            }
        }

        function hideBanner() {
            if (banner) {
                banner.hidden = true;
            }
        }

        function openPreferences() {
            const preferences = currentPreferences || DEFAULT_PREFERENCES;
            syncToggles(preferences);

            if (!preferencesDialog) {
                return;
            }

            if (typeof preferencesDialog.showModal === 'function') {
                preferencesDialog.showModal();
            } else {
                preferencesDialog.setAttribute('open', '');
            }
        }

        function closePreferences() {
            if (!preferencesDialog) {
                return;
            }

            if (typeof preferencesDialog.close === 'function') {
                preferencesDialog.close();
            } else {
                preferencesDialog.removeAttribute('open');
            }
        }

        function save(preferences) {
            currentPreferences = {
                necessary: true,
                analytics: preferences.analytics === true,
                preferences: preferences.preferences === true,
            };

            writePreferences(currentPreferences);
            syncToggles(currentPreferences);
            applyPreferences(currentPreferences, 'cookieconsent:change');
            hideBanner();
            closePreferences();
        }

        document.querySelectorAll('[data-cookie-open-preferences]').forEach((button) => {
            button.addEventListener('click', openPreferences);
        });

        document.querySelectorAll('[data-cookie-reject-optional]').forEach((button) => {
            button.addEventListener('click', () => {
                save({ analytics: false, preferences: false });
            });
        });

        document.querySelectorAll('[data-cookie-accept-all]').forEach((button) => {
            button.addEventListener('click', () => {
                save({ analytics: true, preferences: true });
            });
        });

        document.querySelectorAll('[data-cookie-save-preferences]').forEach((button) => {
            button.addEventListener('click', () => {
                save({
                    analytics: Boolean(analyticsToggle && analyticsToggle.checked),
                    preferences: Boolean(preferencesToggle && preferencesToggle.checked),
                });
            });
        });

        window.blogCookieConsent = Object.freeze({
            getPreferences: () => ({ ...(currentPreferences || DEFAULT_PREFERENCES) }),
            openPreferences,
        });

        if (currentPreferences) {
            syncToggles(currentPreferences);
            applyPreferences(currentPreferences, 'cookieconsent:ready');
            hideBanner();
        } else {
            syncToggles(DEFAULT_PREFERENCES);
            applyPreferences(DEFAULT_PREFERENCES, 'cookieconsent:ready');
            showBanner();
        }
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initialize, { once: true });
    } else {
        initialize();
    }
}());
