(function () {
    if (typeof CodeMirror == 'undefined') return;

    const codes = document.querySelectorAll('pre');

    for (const code of codes) {
    const language = code.dataset.language || null;
    const text = code.textContent || code.innerText;

    const config = {
        value: text,
        tabSize: 2,
        mode: language,
        theme: 'dracula',
        lineNumbers: true,
        styleActiveLine: true,
        styleActiveSelected: true,
        lineWrapping: false,
        line: true,
        readOnly: true,
        viewportMargin: 50,
        matchBrackets: true,
    };

    const editor = CodeMirror(function (node) {
        code.parentNode.replaceChild(node, code);
    }, config);
    }
})();
