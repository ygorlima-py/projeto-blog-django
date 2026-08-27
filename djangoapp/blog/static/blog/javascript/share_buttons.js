(function () {
    'use strict';

    function fallbackCopy(value) {
        const input = document.createElement('textarea');
        input.value = value;
        input.setAttribute('readonly', '');
        input.style.position = 'fixed';
        input.style.opacity = '0';
        document.body.appendChild(input);
        input.select();

        const copied = document.execCommand('copy');
        input.remove();

        if (!copied) {
            throw new Error('Copy command failed');
        }
    }

    async function copyToClipboard(value) {
        if (navigator.clipboard && window.isSecureContext) {
            await navigator.clipboard.writeText(value);
            return;
        }

        fallbackCopy(value);
    }

    function initializeShareBar(shareBar) {
        const url = shareBar.dataset.shareUrl;
        const title = shareBar.dataset.shareTitle;
        const feedback = shareBar.querySelector('[data-share-feedback]');
        const nativeShareButton = shareBar.querySelector('[data-native-share]');
        const copyButton = shareBar.querySelector('[data-copy-share-link]');
        let feedbackTimer;

        function showFeedback(message) {
            if (!feedback) {
                return;
            }

            window.clearTimeout(feedbackTimer);
            feedback.textContent = message;
            feedbackTimer = window.setTimeout(() => {
                feedback.textContent = '';
            }, 5000);
        }

        async function copyLink(message) {
            try {
                await copyToClipboard(url);
                showFeedback(message);
            } catch (error) {
                showFeedback('Não foi possível copiar. Copie o endereço pela barra do navegador.');
            }
        }

        if (nativeShareButton) {
            nativeShareButton.addEventListener('click', async () => {
                if (typeof navigator.share === 'function') {
                    try {
                        await navigator.share({ title, text: title, url });
                        return;
                    } catch (error) {
                        if (error.name === 'AbortError') {
                            return;
                        }
                    }
                }

                await copyLink('Link copiado. Abra o Instagram e cole onde deseja compartilhar.');
            });
        }

        if (copyButton) {
            copyButton.addEventListener('click', () => {
                copyLink('Link copiado para a área de transferência.');
            });
        }
    }

    function initialize() {
        document.querySelectorAll('[data-share-bar]').forEach(initializeShareBar);
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initialize, { once: true });
    } else {
        initialize();
    }
}());
