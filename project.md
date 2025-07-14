${{ content_synopsis }} This image will run paperless-ngx with s6, but rootless.

${{ content_uvp }} Good question! Because ...

${{ github:> [!IMPORTANT] }}
${{ github:> }}* ... this image runs [rootless](https://github.com/11notes/RTFM/blob/main/linux/container/image/rootless.md) as 1000:1000
${{ github:> }}* ... this image is auto updated to the latest version via CI/CD
${{ github:> }}* ... this image has a health check
${{ github:> }}* ... this image is automatically scanned for CVEs before and after publishing
${{ github:> }}* ... this image is created via a secure and pinned CI/CD process

If you value security, simplicity and optimizations to the extreme, then this image might be for you.

${{ title_volumes }}
* **/usr/src/paperless/consume** - Directory of the documents you want to consume
* **/usr/src/paperless/media/documents/originals** - Directory of the original imported documents
* **/usr/src/paperless/media/documents/archive** - Directory of the processed documents
* **/usr/src/paperless/media/documents/thumbnails** - Directory of the thumbnails of each document
* **/usr/src/paperless/data** - Directory of internal app relevant files and configs
* **/usr/src/paperless/export** - Directory of document exports

${{ content_compose }}

${{ content_defaults }}

${{ content_environment }}

${{ content_source }}

${{ content_parent }}

${{ content_built }}

${{ content_tips }}

${{ title_caution }}
${{ github:> [!CAUTION] }}
${{ github:> }}* Since this image is rootless, unlike the official one, it will only work with EN, DE, FR, IT and ES. If you need another language for OCR, please fork this image and install the ```tesseract-ocr-{LANGUAGE}``` package that you need. I can't add all the languages to this image by default