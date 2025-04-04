import webview

OVERLAY_HTML = """
<style>
    #custom-overlay {
        position: fixed;
        bottom: 2px;
        right: 10px;
        color: rgba(255, 255, 255, 0.3);
        font-family: 'Segoe UI', 'Helvetica Neue', Arial, sans-serif;
        font-size: 13px;
        font-weight: 300;
        z-index: 9999;
        pointer-events: none;
    }
</style>
<div id="custom-overlay">An unofficial desktop application for DeepSeek.</div>
"""

def on_loaded():
    window.evaluate_js(f"""
        var overlay = document.createElement('div');
        overlay.innerHTML = `{OVERLAY_HTML}`;
        document.body.appendChild(overlay);
    """)

if __name__ == '__main__':
    window = webview.create_window(
        'DeepSeek',
        'https://chat.deepseek.com/',
        width=1200,
        height=800,
        text_select=True,
    )
    
    window.events.loaded += on_loaded
    webview.start(private_mode=False)