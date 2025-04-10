这个有时候被认为和PIE*per同源，姑临时这样整理。

<div style="width:100%;">
    <iframe id="myIframe" src="../PIE-pere.html" style="width:100%; border:none;" scrolling="no"></iframe>
</div>
<script>
    const iframe = document.getElementById('myIframe');

    function adjustIframeHeight() {
        if (iframe.contentWindow.document.body) {
            iframe.style.height = iframe.contentWindow.document.body.scrollHeight + 50 + 'px';
        }
    }

    // 页面加载完成后调整高度
    iframe.onload = function () {
        adjustIframeHeight();
        // 监听 iframe 内容的变化，实时调整高度
        const observer = new MutationObserver(adjustIframeHeight);
        const config = { attributes: true, childList: true, subtree: true };
        observer.observe(iframe.contentWindow.document.body, config);
    };
</script>
