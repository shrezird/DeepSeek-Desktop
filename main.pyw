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

    window.evaluate_js("""
        (function(){
            const style=document.createElement('style');
            style.textContent=`
                #custom-menu{
                    position:absolute;
                    background:#343541;
                    color:#ececec;
                    font-family:'Open Sans',sans-serif;
                    font-size:13px;
                    padding:2px 0;
                    border-radius:10px;
                    width:140px;
                    box-shadow:0 4px 12px rgba(0,0,0,0.35);
                    display:none;
                    user-select:none;
                    z-index:1000000000;
                }
                #custom-menu .item{
                    padding:4px 12px;
                    margin:1px 3px;
                    border-radius:6px;
                    cursor:pointer;
                }
                #custom-menu .item:hover{
                    background:#444654;
                    border-radius:6px;
                }
            `;
            document.head.appendChild(style);

            const menu=document.createElement('div');
            menu.id='custom-menu';
            menu.innerHTML=`
                <div class="item" data-action="copy">Copy</div>
                <div class="item" data-action="paste">Paste</div>
                <div class="item" data-action="speak">Speak</div>
                <div class="item" data-action="refresh">Refresh</div>
            `;
            document.body.appendChild(menu);

            let lastSel='', pasteTarget=null;

            const hide=()=>menu.style.display='none';
            const show=(x,y,target)=>{
                lastSel=window.getSelection().toString();
                pasteTarget=target;
                menu.style.display='block';
                const {innerWidth,innerHeight}=window;
                const rect=menu.getBoundingClientRect();
                if(x+rect.width>innerWidth) x=innerWidth-rect.width-5;
                if(y+rect.height>innerHeight) y=innerHeight-rect.height-5;
                menu.style.left=x+'px';
                menu.style.top=y+'px';
            };

            document.addEventListener('contextmenu',e=>{
                if(e.target.closest('#custom-menu')) return;
                if(e.button!==2) return;
                e.preventDefault();
                show(e.pageX,e.pageY,e.target);
            });

            document.addEventListener('click',e=>{
                if(!e.target.closest('#custom-menu')) hide();
            });
            document.addEventListener('scroll',hide,true);

            menu.addEventListener('click',e=>{
                e.preventDefault();
                const el=e.target.closest('.item');
                if(!el) return;
                hide();
                switch(el.dataset.action){
                    case'copy':
                        navigator.clipboard.writeText(lastSel);
                        break;
                    case'paste':
                        navigator.clipboard.readText().then(t=>{
                            if(!t||!pasteTarget) return;
                            const el=pasteTarget;
                            if(el.tagName==='TEXTAREA'||(el.tagName==='INPUT'&&el.type==='text')){
                                el.focus();
                                const s=el.selectionStart??el.value.length,
                                      d=el.selectionEnd??el.value.length;
                                el.setRangeText(t,s,d,'end');
                                el.dispatchEvent(new Event('input',{bubbles:true}));
                            }else if(el.isContentEditable){
                                el.focus();
                                document.execCommand('insertText',false,t);
                            }
                        });
                        break;
                    case'speak':
                        if(lastSel) speechSynthesis.speak(new SpeechSynthesisUtterance(lastSel));
                        break;
                    case'refresh':
                        location.reload();
                        break;
                }
            });
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