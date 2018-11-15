# -*- coding:utf-8 -*-

import os
import re
import click
import http.server
import socketserver

INDEX_FILE_NAME = 'image.html'

IMAGE_FILE_REGEX = '^.+\.(png|jpg|jpeg|tif|tiff|gif|bmp|webp)$'

IMAGES_PER_ROW = 3

PORT = 8000


def _create_index_file(root_dir, location, image_files, dirs):
    header_text = \
        'ImageGallery: ' + location + ' [' + str(len(image_files)) + ' image(s)]'
    html = [
        '<!DOCTYPE html>',
        '<html>',
        '    <head>',
        '<meta charset="UTF-8">',
        '<meta http-equiv="X-UA-Compatible" content="IE=edge,chrome=1"> ',
        '<meta name="viewport" content="width=device-width, initial-scale=1.0">',
        '        <title>Image Gallery</title>'
        '    <style>',
        '     /* Reset */ *, *:after, *:before { -webkit-box-sizing: border-box; -moz-box-sizing: border-box; box-sizing: border-box; }  /* Clearfix hack by Nicolas Gallagher: http://nicolasgallagher.com/micro-clearfix-hack/ */ .clearfix:before, .clearfix:after { content: " "; display: table; }  .clearfix:after { clear: both; }   .zzsc-container{ margin: 0 auto; }   .no-color{ background: transparent; }  .center{text-align: center;}    /*! * baguetteBox.js * @author  feimosi * @version 1.8.2 * @url https://github.com/feimosi/baguetteBox.js */#baguetteBox-overlay{display:none;opacity:0;position:fixed;overflow:hidden;top:0;left:0;width:100%;height:100%;z-index:1000000;background-color:#222;background-color:rgba(0,0,0,.8);-webkit-transition:opacity .5s ease;transition:opacity .5s ease}#baguetteBox-overlay.visible{opacity:1}#baguetteBox-overlay .full-image{display:inline-block;position:relative;width:100%;height:100%;text-align:center}#baguetteBox-overlay .full-image figure{display:inline;margin:0;height:100%}#baguetteBox-overlay .full-image img{display:inline-block;width:auto;height:auto;max-height:100%;max-width:100%;vertical-align:middle;-moz-box-shadow:0 0 8px rgba(0,0,0,.6);box-shadow:0 0 8px rgba(0,0,0,.6)}#baguetteBox-overlay .full-image figcaption{display:block;position:absolute;bottom:0;width:100%;text-align:center;line-height:1.8;white-space:normal;color:#ccc;background-color:#000;background-color:rgba(0,0,0,.6);font-family:sans-serif}#baguetteBox-overlay .full-image:before{content:"";display:inline-block;height:50%;width:1px;margin-right:-1px}#baguetteBox-slider{position:absolute;left:0;top:0;height:100%;width:100%;white-space:nowrap;-webkit-transition:left .4s ease,-webkit-transform .4s ease;transition:left .4s ease,-webkit-transform .4s ease;transition:left .4s ease,transform .4s ease;transition:left .4s ease,transform .4s ease,-webkit-transform .4s ease,-moz-transform .4s ease}#baguetteBox-slider.bounce-from-right{-webkit-animation:bounceFromRight .4s ease-out;animation:bounceFromRight .4s ease-out}#baguetteBox-slider.bounce-from-left{-webkit-animation:bounceFromLeft .4s ease-out;animation:bounceFromLeft .4s ease-out}@-webkit-keyframes bounceFromRight{0%,100%{margin-left:0}50%{margin-left:-30px}}@keyframes bounceFromRight{0%,100%{margin-left:0}50%{margin-left:-30px}}@-webkit-keyframes bounceFromLeft{0%,100%{margin-left:0}50%{margin-left:30px}}@keyframes bounceFromLeft{0%,100%{margin-left:0}50%{margin-left:30px}}.baguetteBox-button#next-button,.baguetteBox-button#previous-button{top:50%;top:calc(50% - 30px);width:44px;height:60px}.baguetteBox-button{position:absolute;cursor:pointer;outline:0;padding:0;margin:0;border:0;-moz-border-radius:15%;border-radius:15%;background-color:#323232;background-color:rgba(50,50,50,.5);color:#ddd;font:1.6em sans-serif;-webkit-transition:background-color .4s ease;transition:background-color .4s ease}.baguetteBox-button:focus,.baguetteBox-button:hover{background-color:rgba(50,50,50,.9)}.baguetteBox-button#next-button{right:2%}.baguetteBox-button#previous-button{left:2%}.baguetteBox-button#close-button{top:20px;right:2%;right:calc(2% + 6px);width:30px;height:30px}.baguetteBox-button svg{position:absolute;left:0;top:0}.baguetteBox-spinner{width:40px;height:40px;display:inline-block;position:absolute;top:50%;left:50%;margin-top:-20px;margin-left:-20px}.baguetteBox-double-bounce1,.baguetteBox-double-bounce2{width:100%;height:100%;-moz-border-radius:50%;border-radius:50%;background-color:#fff;opacity:.6;position:absolute;top:0;left:0;-webkit-animation:bounce 2s infinite ease-in-out;animation:bounce 2s infinite ease-in-out}.baguetteBox-double-bounce2{-webkit-animation-delay:-1s;animation-delay:-1s}@-webkit-keyframes bounce{0%,100%{-webkit-transform:scale(0);transform:scale(0)}50%{-webkit-transform:scale(1);transform:scale(1)}}@keyframes bounce{0%,100%{-webkit-transform:scale(0);-moz-transform:scale(0);transform:scale(0)}50%{-webkit-transform:scale(1);-moz-transform:scale(1);transform:scale(1)}}   body { /*background-image: linear-gradient(to top, #ecedee 0%, #eceeef 75%, #e7e8e9 100%);*/ background: #494A5F; min-height: 100vh; font: normal 16px sans-serif; padding: 60px 0; }  .container.gallery-container { background-color: #fff; color: #35373a; min-height: 100vh; border-radius: 20px; box-shadow: 0 8px 15px rgba(0, 0, 0, 0.06); }  .gallery-container h1 { text-align: center; margin-top: 70px; font-family: sans-serif; font-weight: bold; }  .gallery-container p.page-description { text-align: center; max-width: 800px; margin: 25px auto; color: #888; font-size: 18px; }  .tz-gallery { padding: 40px; }  .tz-gallery .lightbox img { width: 100%; margin-bottom: 30px; transition: 0.2s ease-in-out; box-shadow: 0 2px 3px rgba(0,0,0,0.2); }   .tz-gallery .lightbox img:hover { transform: scale(1.05); box-shadow: 0 8px 15px rgba(0,0,0,0.3); }  .tz-gallery img { border-radius: 4px; }  .baguetteBox-button { background-color: transparent !important; }   @media(max-width: 768px) { body { padding: 0; }  .container.gallery-container { border-radius: 0; } }  .row { margin-right: -15px; margin-left: -15px; }  .row:before, .row:after,  .col-xs-1, .col-sm-1, .col-md-1, .col-lg-1, .col-xs-2, .col-sm-2, .col-md-2, .col-lg-2, .col-xs-3, .col-sm-3, .col-md-3, .col-lg-3, .col-xs-4, .col-sm-4, .col-md-4, .col-lg-4, .col-xs-5, .col-sm-5, .col-md-5, .col-lg-5, .col-xs-6, .col-sm-6, .col-md-6, .col-lg-6, .col-xs-7, .col-sm-7, .col-md-7, .col-lg-7, .col-xs-8, .col-sm-8, .col-md-8, .col-lg-8, .col-xs-9, .col-sm-9, .col-md-9, .col-lg-9, .col-xs-10, .col-sm-10, .col-md-10, .col-lg-10, .col-xs-11, .col-sm-11, .col-md-11, .col-lg-11, .col-xs-12, .col-sm-12, .col-md-12, .col-lg-12 { position: relative; min-height: 1px; padding-right: 15px; padding-left: 15px; }  @media (min-width: 768px) { .col-sm-1, .col-sm-2, .col-sm-3, .col-sm-4, .col-sm-5, .col-sm-6, .col-sm-7, .col-sm-8, .col-sm-9, .col-sm-10, .col-sm-11, .col-sm-12 { float: left; }  .col-sm-6 { width: 50%; }  }  @media (min-width: 992px) { .col-md-1, .col-md-2, .col-md-3, .col-md-4, .col-md-5, .col-md-6, .col-md-7, .col-md-8, .col-md-9, .col-md-10, .col-md-11, .col-md-12 { float: left; }  .col-md-4 { width: 33.33333333%; }  } ',
        '    </style>',
        '    </head>',
        '    <body>',
        '    <div class="zzsc-container">',
        '        <h2>' + header_text + '</h2>'
    ]
    directories = []
    if root_dir != location:
        directories = ['..']
    directories += dirs
    if len(directories) > 0:
        html.append('<hr>')
    for directory in directories:
        link = directory + '/' + INDEX_FILE_NAME
        html += [
            '    <h3>',
            '    <a href="' + link + '">' + directory + '</a>',
            '    </h3>'
        ]
    html += [
            '    <hr>',
            '    <div class="tz-gallery">',
            '    <div class="row">',
    ]
    for image_file in image_files:
        html += [
                '    <div class="col-sm-6 col-md-4">',
                '    <a class="lightbox" href="' + image_file + '">',
                '    <img src="' + image_file + '" >',
                '    </a>',
                '    </div>',
        ]
    html += [
        '    </div>',
        '    </div>',
        '    </div>',
        '    <script type="text/javascript" >',
        '    !function(t,e){"use strict";"function"==typeof define&&define.amd?define(e):"object"==typeof exports?module.exports=e():t.baguetteBox=e()}(this,function(){"use strict";function t(t,n){M.transforms=w(),M.svg=k(),i(),o(t),e(t,n)}function e(t,e){var n=document.querySelectorAll(t),o={galleries:[],nodeList:n};U[t]=o,[].forEach.call(n,function(t){e&&e.filter&&(V=e.filter);var n=[];if(n="A"===t.tagName?[t]:t.getElementsByTagName("a"),n=[].filter.call(n,function(t){return V.test(t.href)}),0!==n.length){var i=[];[].forEach.call(n,function(t,n){var o=function(t){t.preventDefault?t.preventDefault():t.returnValue=!1,u(i,e),c(n)},a={eventHandler:o,imageElement:t};E(t,"click",o),i.push(a)}),o.galleries.push(i)}})}function n(){for(var t in U)U.hasOwnProperty(t)&&o(t)}function o(t){if(U.hasOwnProperty(t)){var e=U[t].galleries;[].forEach.call(e,function(t){[].forEach.call(t,function(t){B(t.imageElement,"click",t.eventHandler)}),R===t&&(R=[])}),delete U[t]}}function i(){if(S=T("baguetteBox-overlay"))return P=T("baguetteBox-slider"),F=T("previous-button"),H=T("next-button"),void(L=T("close-button"));S=N("div"),S.setAttribute("role","dialog"),S.id="baguetteBox-overlay",document.getElementsByTagName("body")[0].appendChild(S),P=N("div"),P.id="baguetteBox-slider",S.appendChild(P),F=N("button"),F.setAttribute("type","button"),F.id="previous-button",F.setAttribute("aria-label","Previous"),F.innerHTML=M.svg?I:"&lt;",S.appendChild(F),H=N("button"),H.setAttribute("type","button"),H.id="next-button",H.setAttribute("aria-label","Next"),H.innerHTML=M.svg?Y:"&gt;",S.appendChild(H),L=N("button"),L.setAttribute("type","button"),L.id="close-button",L.setAttribute("aria-label","Close"),L.innerHTML=M.svg?q:"&times;",S.appendChild(L),F.className=H.className=L.className="baguetteBox-button",r()}function a(t){switch(t.keyCode){case 37:v();break;case 39:h();break;case 27:m()}}function r(){E(S,"click",J),E(F,"click",K),E(H,"click",Q),E(L,"click",Z),E(S,"touchstart",$),E(S,"touchmove",_),E(S,"touchend",tt),E(document,"focus",et,!0)}function l(){B(S,"click",J),B(F,"click",K),B(H,"click",Q),B(L,"click",Z),B(S,"touchstart",$),B(S,"touchmove",_),B(S,"touchend",tt),B(document,"focus",et,!0)}function u(t,e){if(R!==t){for(R=t,s(e);P.firstChild;)P.removeChild(P.firstChild);W.length=0;for(var n,o=[],i=[],a=0;a<t.length;a++)n=N("div"),n.className="full-image",n.id="baguette-img-"+a,W.push(n),o.push("baguetteBox-figure-"+a),i.push("baguetteBox-figcaption-"+a),P.appendChild(W[a]);S.setAttribute("aria-labelledby",o.join(" ")),S.setAttribute("aria-describedby",i.join(" "))}}function s(t){t||(t={});for(var e in X)j[e]=X[e],void 0!==t[e]&&(j[e]=t[e]);P.style.transition=P.style.webkitTransition="fadeIn"===j.animation?"opacity .4s ease":"slideIn"===j.animation?"":"none","auto"===j.buttons&&("ontouchstart"in window||1===R.length)&&(j.buttons=!1),F.style.display=H.style.display=j.buttons?"":"none";try{S.style.backgroundColor=j.overlayBackgroundColor}catch(t){}}function c(t){j.noScrollbars&&(document.documentElement.style.overflowY="hidden",document.body.style.overflowY="scroll"),"block"!==S.style.display&&(E(document,"keydown",a),z=t,D={count:0,startX:null,startY:null},p(z,function(){x(z),C(z)}),y(),S.style.display="block",j.fullScreen&&f(),setTimeout(function(){S.className="visible",j.afterShow&&j.afterShow()},50),j.onChange&&j.onChange(z,W.length),G=document.activeElement,d())}function d(){j.buttons?F.focus():L.focus()}function f(){S.requestFullscreen?S.requestFullscreen():S.webkitRequestFullscreen?S.webkitRequestFullscreen():S.mozRequestFullScreen&&S.mozRequestFullScreen()}function g(){document.exitFullscreen?document.exitFullscreen():document.mozCancelFullScreen?document.mozCancelFullScreen():document.webkitExitFullscreen&&document.webkitExitFullscreen()}function m(){j.noScrollbars&&(document.documentElement.style.overflowY="auto",document.body.style.overflowY="auto"),"none"!==S.style.display&&(B(document,"keydown",a),S.className="",setTimeout(function(){S.style.display="none",g(),j.afterHide&&j.afterHide()},500),G.focus())}function p(t,e){var n=W[t],o=R[t];if(void 0!==n&&void 0!==o){if(n.getElementsByTagName("img")[0])return void(e&&e());var i=o.imageElement,a=i.getElementsByTagName("img")[0],r="function"==typeof j.captions?j.captions.call(R,i):i.getAttribute("data-caption")||i.title,l=b(i),u=N("figure");if(u.id="baguetteBox-figure-"+t,u.innerHTML=' + '\'' + '<div class="baguetteBox-spinner"><div class="baguetteBox-double-bounce1"></div><div class="baguetteBox-double-bounce2"></div></div>' + '\'' + ',j.captions&&r){var s=N("figcaption");s.id="baguetteBox-figcaption-"+t,s.innerHTML=r,u.appendChild(s)}n.appendChild(u);var c=N("img");c.onload=function(){var n=document.querySelector("#baguette-img-"+t+" .baguetteBox-spinner");u.removeChild(n),!j.async&&e&&e()},c.setAttribute("src",l),c.alt=a?a.alt||"":"",j.titleTag&&r&&(c.title=r),u.appendChild(c),j.async&&e&&e()}}function b(t){var e=t.href;if(t.dataset){var n=[];for(var o in t.dataset)"at-"!==o.substring(0,3)||isNaN(o.substring(3))||(n[o.replace("at-","")]=t.dataset[o]);for(var i=Object.keys(n).sort(function(t,e){return parseInt(t,10)<parseInt(e,10)?-1:1}),a=window.innerWidth*window.devicePixelRatio,r=0;r<i.length-1&&i[r]<a;)r++;e=n[i[r]]||e}return e}function h(){var t;return z<=W.length-2?(z++,y(),x(z),t=!0):j.animation&&(P.className="bounce-from-right",setTimeout(function(){P.className=""},400),t=!1),j.onChange&&j.onChange(z,W.length),t}function v(){var t;return z>=1?(z--,y(),C(z),t=!0):j.animation&&(P.className="bounce-from-left",setTimeout(function(){P.className=""},400),t=!1),j.onChange&&j.onChange(z,W.length),t}function y(){var t=100*-z+"%";"fadeIn"===j.animation?(P.style.opacity=0,setTimeout(function(){M.transforms?P.style.transform=P.style.webkitTransform="translate3d("+t+",0,0)":P.style.left=t,P.style.opacity=1},400)):M.transforms?P.style.transform=P.style.webkitTransform="translate3d("+t+",0,0)":P.style.left=t}function w(){var t=N("div");return void 0!==t.style.perspective||void 0!==t.style.webkitPerspective}function k(){var t=N("div");return t.innerHTML="<svg/>","http://www.w3.org/2000/svg"===(t.firstChild&&t.firstChild.namespaceURI)}function x(t){t-z>=j.preload||p(t+1,function(){x(t+1)})}function C(t){z-t>=j.preload||p(t-1,function(){C(t-1)})}function E(t,e,n,o){t.addEventListener?t.addEventListener(e,n,o):t.attachEvent("on"+e,function(t){t=t||window.event,t.target=t.target||t.srcElement,n(t)})}function B(t,e,n,o){t.removeEventListener?t.removeEventListener(e,n,o):t.detachEvent("on"+e,n)}function T(t){return document.getElementById(t)}function N(t){return document.createElement(t)}function A(){l(),n(),B(document,"keydown",a),document.getElementsByTagName("body")[0].removeChild(document.getElementById("baguetteBox-overlay")),U={},R=[],z=0}var S,P,F,H,L,I=' + '\'' + '<svg width="44" height="60"><polyline points="30 10 10 30 30 50" stroke="rgba(255,255,255,0.5)" stroke-width="4"stroke-linecap="butt" fill="none" stroke-linejoin="round"/></svg>' + '\'' + ',Y=' + '\'' + '<svg width="44" height="60"><polyline points="14 10 34 30 14 50" stroke="rgba(255,255,255,0.5)" stroke-width="4"stroke-linecap="butt" fill="none" stroke-linejoin="round"/></svg>' + '\'' + ',q=' + '\'' + '<svg width="30" height="30"><g stroke="rgb(160,160,160)" stroke-width="4"><line x1="5" y1="5" x2="25" y2="25"/><line x1="5" y1="25" x2="25" y2="5"/></g></svg>' + '\'' + ',j={},X={captions:!0,fullScreen:!1,noScrollbars:!1,titleTag:!1,buttons:"auto",async:!1,preload:2,animation:"slideIn",afterShow:null,afterHide:null,onChange:null,overlayBackgroundColor:"rgba(0,0,0,.8)"},M={},R=[],z=0,D={},O=!1,V=/.+\.(gif|jpe?g|png|webp)/i,U={},W=[],G=null,J=function(t){t.target.id.indexOf("baguette-img")!==-1&&m()},K=function(t){t.stopPropagation?t.stopPropagation():t.cancelBubble=!0,v()},Q=function(t){t.stopPropagation?t.stopPropagation():t.cancelBubble=!0,h()},Z=function(t){t.stopPropagation?t.stopPropagation():t.cancelBubble=!0,m()},$=function(t){D.count++,D.count>1&&(D.multitouch=!0),D.startX=t.changedTouches[0].pageX,D.startY=t.changedTouches[0].pageY},_=function(t){if(!O&&!D.multitouch){t.preventDefault?t.preventDefault():t.returnValue=!1;var e=t.touches[0]||t.changedTouches[0];e.pageX-D.startX>40?(O=!0,v()):e.pageX-D.startX<-40?(O=!0,h()):D.startY-e.pageY>100&&m()}},tt=function(){D.count--,D.count<=0&&(D.multitouch=!1),O=!1},et=function(t){"block"===S.style.display&&S.contains&&!S.contains(t.target)&&(t.stopPropagation(),d())};return[].forEach||(Array.prototype.forEach=function(t,e){for(var n=0;n<this.length;n++)t.call(e,this[n],n,this)}),[].filter||(Array.prototype.filter=function(t,e,n,o,i){for(n=this,o=[],i=0;i<n.length;i++)t.call(e,n[i],i,n)&&o.push(n[i]);return o}),{run:t,destroy:A,showNext:h,showPrevious:v}});',

        '    </script>',
        '    <script type="text/javascript">',
        '       baguetteBox.run(".tz-gallery");',
        '    </script>',
        '    </body>',
        '</html>'
    ]
    index_file_path = _get_index_file_path(location)
    print('Creating index file %s' % index_file_path)
    index_file = open(index_file_path, 'w')
    index_file.write('\n'.join(html))
    index_file.close()
    return index_file_path

def _create_index_files(root_dir):
    created_files = []
    for here, dirs, files in os.walk(root_dir):
        print('Processing %s' % here)
        dirs = sorted(dirs)
        image_files = [f for f in files if re.match(IMAGE_FILE_REGEX, f,re.IGNORECASE)]
        image_files = sorted(image_files)
        created_files.append(
            _create_index_file(
                root_dir, here, image_files, dirs
            )
        )
    return created_files



def _get_index_file_path(location):
    return os.path.join(location, INDEX_FILE_NAME)

@click.command('server',short_help='initial server to view image')
@click.argument('path',default='.')
@click.argument('port',type=int,default=PORT)
def run_server(path,port):

    path = os.path.abspath(path)
    Handler = http.server.SimpleHTTPRequestHandler
    os.chdir(path)
    httpd = socketserver.TCPServer(("",port), Handler)
    try:
        print("Your ImageGallery at http://127.0.0.1:{}/{} ".format(port,INDEX_FILE_NAME))
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("ImageGallery stopping")


@click.command('create',short_help='create html file')
@click.argument('path',default='.')
def create(path):
    path = os.path.abspath(path)
    _create_index_files(path)


@click.command('clean',short_help='clean html file')
@click.argument('path',default='.')
def cleanup(path):
    for root,dirs,files in os.walk(path):
        for file in files:
            filename = os.path.join(root,file)
            if file == "image.html":
                print("Removing {}".format(filename))
                os.unlink(filename)
@click.group()
def main():
    pass
main.add_command(create)
main.add_command(cleanup)
main.add_command(run_server)

if __name__ =='__main__':
    main()
