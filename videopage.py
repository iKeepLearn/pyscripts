#!/usr/bin/python

import os, re, sys

INDEX_FILE_NAME = 'video.html'


def create_index_file(dir_path):
    
    html = [
             '       <!doctype html>',
             '<html lang="en">',
             
             '<head>',
             '    <meta charset="utf-8" />',
             '    <title>Video Index</title>',
             '    <meta name="description" property="og:description" content="A simple HTML5 media player with custom controls and WebVTT captions.">',
             '    <meta name="author" content="Sam Potts">',
             '    <meta name="viewport" content="width=device-width, initial-scale=1">',
             
             '    <!-- Icons -->',
             '    <link rel="icon" href="https://cdn.plyr.io/static/icons/favicon.ico">',
             '    <link rel="icon" type="image/png" href="https://cdn.plyr.io/static/icons/32x32.png" sizes="32x32">',
             '    <link rel="icon" type="image/png" href="https://cdn.plyr.io/static/icons/16x16.png" sizes="16x16">',
             '    <link rel="apple-touch-icon" sizes="180x180" href="https://cdn.plyr.io/static/icons/180x180.png">',
             
             '    <style>',
             '     /* Reset */ *, *:after, *:before { -webkit-box-sizing: border-box; -moz-box-sizing: border-box; box-sizing: border-box; }  /* Clearfix hack by Nicolas Gallagher: http://nicolasgallagher.com/micro-clearfix-hack/ */ .clearfix:before, .clearfix:after { content: " "; display: table; }  .clearfix:after { clear: both; }   .zzsc-container{ margin: 0 auto; }   .no-color{ background: transparent; }  .center{text-align: center;}    /*! * baguetteBox.js * @author  feimosi * @version 1.8.2 * @url https://github.com/feimosi/baguetteBox.js */#baguetteBox-overlay{display:none;opacity:0;position:fixed;overflow:hidden;top:0;left:0;width:100%;height:100%;z-index:1000000;background-color:#222;background-color:rgba(0,0,0,.8);-webkit-transition:opacity .5s ease;transition:opacity .5s ease}#baguetteBox-overlay.visible{opacity:1}#baguetteBox-overlay .full-image{display:inline-block;position:relative;width:100%;height:100%;text-align:center}#baguetteBox-overlay .full-image figure{display:inline;margin:0;height:100%}#baguetteBox-overlay .full-image img{display:inline-block;width:auto;height:auto;max-height:100%;max-width:100%;vertical-align:middle;-moz-box-shadow:0 0 8px rgba(0,0,0,.6);box-shadow:0 0 8px rgba(0,0,0,.6)}#baguetteBox-overlay .full-image figcaption{display:block;position:absolute;bottom:0;width:100%;text-align:center;line-height:1.8;white-space:normal;color:#ccc;background-color:#000;background-color:rgba(0,0,0,.6);font-family:sans-serif}#baguetteBox-overlay .full-image:before{content:"";display:inline-block;height:50%;width:1px;margin-right:-1px}#baguetteBox-slider{position:absolute;left:0;top:0;height:100%;width:100%;white-space:nowrap;-webkit-transition:left .4s ease,-webkit-transform .4s ease;transition:left .4s ease,-webkit-transform .4s ease;transition:left .4s ease,transform .4s ease;transition:left .4s ease,transform .4s ease,-webkit-transform .4s ease,-moz-transform .4s ease}#baguetteBox-slider.bounce-from-right{-webkit-animation:bounceFromRight .4s ease-out;animation:bounceFromRight .4s ease-out}#baguetteBox-slider.bounce-from-left{-webkit-animation:bounceFromLeft .4s ease-out;animation:bounceFromLeft .4s ease-out}@-webkit-keyframes bounceFromRight{0%,100%{margin-left:0}50%{margin-left:-30px}}@keyframes bounceFromRight{0%,100%{margin-left:0}50%{margin-left:-30px}}@-webkit-keyframes bounceFromLeft{0%,100%{margin-left:0}50%{margin-left:30px}}@keyframes bounceFromLeft{0%,100%{margin-left:0}50%{margin-left:30px}}.baguetteBox-button#next-button,.baguetteBox-button#previous-button{top:50%;top:calc(50% - 30px);width:44px;height:60px}.baguetteBox-button{position:absolute;cursor:pointer;outline:0;padding:0;margin:0;border:0;-moz-border-radius:15%;border-radius:15%;background-color:#323232;background-color:rgba(50,50,50,.5);color:#ddd;font:1.6em sans-serif;-webkit-transition:background-color .4s ease;transition:background-color .4s ease}.baguetteBox-button:focus,.baguetteBox-button:hover{background-color:rgba(50,50,50,.9)}.baguetteBox-button#next-button{right:2%}.baguetteBox-button#previous-button{left:2%}.baguetteBox-button#close-button{top:20px;right:2%;right:calc(2% + 6px);width:30px;height:30px}.baguetteBox-button svg{position:absolute;left:0;top:0}.baguetteBox-spinner{width:40px;height:40px;display:inline-block;position:absolute;top:50%;left:50%;margin-top:-20px;margin-left:-20px}.baguetteBox-double-bounce1,.baguetteBox-double-bounce2{width:100%;height:100%;-moz-border-radius:50%;border-radius:50%;background-color:#fff;opacity:.6;position:absolute;top:0;left:0;-webkit-animation:bounce 2s infinite ease-in-out;animation:bounce 2s infinite ease-in-out}.baguetteBox-double-bounce2{-webkit-animation-delay:-1s;animation-delay:-1s}@-webkit-keyframes bounce{0%,100%{-webkit-transform:scale(0);transform:scale(0)}50%{-webkit-transform:scale(1);transform:scale(1)}}@keyframes bounce{0%,100%{-webkit-transform:scale(0);-moz-transform:scale(0);transform:scale(0)}50%{-webkit-transform:scale(1);-moz-transform:scale(1);transform:scale(1)}}   body { /*background-image: linear-gradient(to top, #ecedee 0%, #eceeef 75%, #e7e8e9 100%);*/ background: #494A5F; min-height: 100vh; font: normal 16px sans-serif; padding: 60px 0; }  .container.gallery-container { background-color: #fff; color: #35373a; min-height: 100vh; border-radius: 20px; box-shadow: 0 8px 15px rgba(0, 0, 0, 0.06); }  .gallery-container h1 { text-align: center; margin-top: 70px; font-family: sans-serif; font-weight: bold; }  .gallery-container p.page-description { text-align: center; max-width: 800px; margin: 25px auto; color: #888; font-size: 18px; } p { font-size:20px; } .tz-gallery { padding: 40px; }  .tz-gallery .lightbox img { width: 100%; margin-bottom: 30px; transition: 0.2s ease-in-out; box-shadow: 0 2px 3px rgba(0,0,0,0.2); }   .tz-gallery .lightbox img:hover { transform: scale(1.05); box-shadow: 0 8px 15px rgba(0,0,0,0.3); }  .tz-gallery img { border-radius: 4px; }  .baguetteBox-button { background-color: transparent !important; }   @media(max-width: 768px) { body { padding: 0; }  .container.gallery-container { border-radius: 0; } }  .row { margin-right: -15px; margin-left: -15px; }  .row:before, .row:after,  .col-xs-1, .col-sm-1, .col-md-1, .col-lg-1, .col-xs-2, .col-sm-2, .col-md-2, .col-lg-2, .col-xs-3, .col-sm-3, .col-md-3, .col-lg-3, .col-xs-4, .col-sm-4, .col-md-4, .col-lg-4, .col-xs-5, .col-sm-5, .col-md-5, .col-lg-5, .col-xs-6, .col-sm-6, .col-md-6, .col-lg-6, .col-xs-7, .col-sm-7, .col-md-7, .col-lg-7, .col-xs-8, .col-sm-8, .col-md-8, .col-lg-8, .col-xs-9, .col-sm-9, .col-md-9, .col-lg-9, .col-xs-10, .col-sm-10, .col-md-10, .col-lg-10, .col-xs-11, .col-sm-11, .col-md-11, .col-lg-11, .col-xs-12, .col-sm-12, .col-md-12, .col-lg-12 { position: relative; min-height: 1px; padding-right: 15px; padding-left: 15px; }  @media (min-width: 768px) { .col-sm-1, .col-sm-2, .col-sm-3, .col-sm-4, .col-sm-5, .col-sm-6, .col-sm-7, .col-sm-8, .col-sm-9, .col-sm-10, .col-sm-11, .col-sm-12 { float: left; }  .col-sm-6 { width: 50%; }  }  @media (min-width: 992px) { .col-md-1, .col-md-2, .col-md-3, .col-md-4, .col-md-5, .col-md-6, .col-md-7, .col-md-8, .col-md-9, .col-md-10, .col-md-11, .col-md-12 { float: left; }  .col-md-4 { width: 33.33333333%; }  } ',
             '    </style>',
             '    </head>',
             '    <body>',
             '    <div class="zzsc-container">',
             '        <h2>Video page</h2>',
             '<hr>',
             '    <p>',
    ]
    video_files = []
    
    for root,dirs,files in os.walk(dir_path):
        for file in files:
            if file.endswith('.mp4') or file.endswith('.MP4'):
                video_files.append(file)
    
    
    for video_file in video_files:
        url = video_file[:-3] + 'html'
        html.append('<a href="' + url +'">' + video_file + '</a>')
    html += [
        '   </p>',
        '    <hr>',
        '    <div class="tz-gallery">',
        '    <div class="row">',
        '    </div>',
        '    </div>',
        '    </div>',
        '     </body>',
        '</html>',
    ]
    index_file_path = os.path.join(dir_path,INDEX_FILE_NAME)
    print('Creating index file %s' % index_file_path)
    index_file = open(index_file_path, 'w')
    index_file.write('\n'.join(html))
    index_file.close()
    return index_file_path

def create_video_play_files(video_file):
    html = [
            '<!doctype html>',
            '<html lang="en">',
            '<head>',
            '    <meta charset="utf-8" />',
            '    <title>Plyr - A simple, customizable HTML5 Video, Audio, YouTube and Vimeo player</title>',
            '    <meta name="description" property="og:description" content="A simple HTML5 media player with custom controls and WebVTT captions.">',
            '    <meta name="author" content="Sam Potts">',
            '    <meta name="viewport" content="width=device-width, initial-scale=1">',
            '    <!-- Icons -->',
            '    <link rel="icon" href="https://cdn.plyr.io/static/icons/favicon.ico">',
            '    <link rel="icon" type="image/png" href="https://cdn.plyr.io/static/icons/32x32.png" sizes="32x32">',
            '    <link rel="icon" type="image/png" href="https://cdn.plyr.io/static/icons/16x16.png" sizes="16x16">',
            '    <link rel="apple-touch-icon" sizes="180x180" href="https://cdn.plyr.io/static/icons/180x180.png">',
            '    <!-- Docs styles -->',
            '    <link rel="stylesheet" href="https://cdn.plyr.io/3.4.3/demo.css?v=2">',
            '    <!-- Preload -->',
            '    <link rel="preload" as="font" crossorigin type="font/woff2" href="https://cdn.plyr.io/static/fonts/gordita-medium.woff2">',
            '    <link rel="preload" as="font" crossorigin type="font/woff2" href="https://cdn.plyr.io/static/fonts/gordita-bold.woff2">',
            '</head>',
            '<body>',
            '    <div class="grid">',
            '        <main>',
            '            <div id="container">',
            '                <video controls crossorigin playsinline  id="player">',
            '                    <!-- Video files -->',
            '                    <source src="' + video_file +'" type="video/mp4" size="576">',
            '                </video>',
            '            </div>',
            '    <!-- Polyfills -->',
            '    <script src="https://cdn.polyfill.io/v2/polyfill.min.js?features=es6,Array.prototype.includes,CustomEvent,Object.entries,Object.values,URL"',
            '        crossorigin="anonymous"></script>',
            '    <!-- Plyr core script -->',
            '    <script src="https://cdn.plyr.io/3.4.3/plyr.js" crossorigin="anonymous"></script>',
            '    <!-- Rangetouch to fix <input type="range"> on touch devices (see https://rangetouch.com) -->',
            '    <script src="https://cdn.rangetouch.com/1.0.1/rangetouch.js" async crossorigin="anonymous"></script>',
            '    <!-- Docs script -->',
            '    <script src="https://cdn.plyr.io/3.4.3/demo.js" crossorigin="anonymous"></script>',
            '</body>',
            '</html>',
            ]
    filename = video_file[:-3] + 'html'
    filepath = os.path.join(dir_path,filename)
    t = open(filepath,'w')
    t.write('\n'.join(html))
    t.close
    
def scan_video_file(dir_path):
    for root,dirs,files in os.walk(dir_path):
        for file in files:
            if file.endswith('.mp4') or file.endswith('.MP4'):
                create_video_play_files(file)
                
                
    


if __name__ == '__main__':
    dir_path = sys.argv[-1]
    create_index_file(dir_path)
    scan_video_file(dir_path)

