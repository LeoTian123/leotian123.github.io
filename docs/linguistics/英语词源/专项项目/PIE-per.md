这个是一个知名PIE词根，各个意思之间有时候会被认为是同源的，而且衍生词过于多，所以单开一个文件。

<div style="width:100%;">
    <iframe id="myIframe" src="../PIE-per.html" style="width:100%; border:none;" scrolling="no"></iframe>
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
