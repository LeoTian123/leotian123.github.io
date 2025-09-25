import os
import glob

def generate_md_from_html():
    # 获取当前目录下所有的 HTML 文件
    html_files = glob.glob('*.html')
    
    # 遍历所有 HTML 文件
    for html_file in html_files:
        # 生成对应的 MD 文件名
        md_file = html_file.replace('.html', '.md')
        
        # 创建 MD 文件内容
        md_content = '''<div style="width:100%;">
    <iframe id="myIframe" src="../''' + html_file + '''" style="width:100%; border:none;" scrolling="no"></iframe>
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
'''
        
        # 写入 MD 文件
        with open(md_file, 'w', encoding='utf-8') as f:
            f.write(md_content)
        
        print(f'- linguistics/英语词源/按照意义分类的/{md_file}')

if __name__ == '__main__':
    generate_md_from_html()
