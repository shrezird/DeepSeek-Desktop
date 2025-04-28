import webview
import webbrowser

OVERLAY_HTML = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Open+Sans:wght@300;400;600&display=swap');
    #custom-overlay {
        position: fixed;
        bottom: 0px;
        right: 10px;
        color: rgba(255, 255, 255, 0.3);
        font-family: 'Open Sans', sans-serif;
        font-size: 12px;
        font-weight: 100;
        z-index: 999999999;
        pointer-events: auto;
    }
    #deepseek-link { color: inherit; text-decoration: underline; cursor: pointer; }
</style>
<div id="custom-overlay">An open-source desktop application for <a id="deepseek-link">DeepSeek</a>.</div>
"""

def on_loaded():
    window.evaluate_js(f"""
        var overlay = document.createElement('div');
        overlay.innerHTML = `{OVERLAY_HTML}`;
        document.body.appendChild(overlay);
        var link = document.getElementById('deepseek-link');
        if (link) {{
            link.addEventListener('click', function (e) {{
                e.preventDefault();
                window.pywebview.api.open_external();
            }});
        }}
    """)

    window.evaluate_js("""
        (function () {
            const api = window.pywebview?.api;
            if (!api) { return; }

            function getActiveTitle() {
                const rows = document.querySelectorAll('div._83421f9');
                if (!rows.length) return '';
                const active = Array.from(rows).find(r =>
                    r.classList.contains('b64fb9ae') ||
                    r.className.includes('_83421f9_b64fb9ae')
                );
                if (!active) return '';
                const el = active.querySelector('.c08e6e93');
                return el ? el.textContent.trim() : '';
            }

            function update() {
                const title = getActiveTitle();
                api.set_title('DeepSeek - ' + (title || 'New chat'));
            }

            new MutationObserver(update)
                .observe(document.body, { attributes: true, childList: true, subtree: true });

            update();
        })();
    """)

if __name__ == '__main__':
    window = webview.create_window(
        'DeepSeek',
        'https://chat.deepseek.com/',
        min_size=(900, 650),
        maximized=True,
        text_select=True,
    )

    def set_title(title: str):
        window.set_title(title)

    def open_external():
        webbrowser.open('https://www.deepseek.com/en')

    window.expose(set_title)
    window.expose(open_external)
    window.events.loaded += on_loaded
    webview.settings['ALLOW_DOWNLOADS'] = True
    webview.start(private_mode=False)