/*! jQuery & Zepto Lazy - Picture Plugin v1.3 - http://jquery.eisbehr.de/lazy - MIT&GPL-2.0 license - Copyright 2012-2018 Daniel 'Eisbehr' Kern */
!function(t){function e(e,a,n){var o=e.prop("attributes"),c=t("<"+a+">");return t.each(o,function(t,e){"srcset"!==e.name&&e.name!==i||(e.value=r(e.value,n)),c.attr(e.name,e.value)}),e.replaceWith(c),c}function a(e,a,r){var i=t("<img>").one("load",function(){r(!0)}).one("error",function(){r(!1)}).appendTo(e).attr("src",a);i.complete&&i.load()}function r(t,e){if(e){var a=t.split(",");t="";for(var r=0,i=a.length;r<i;r++)t+=e+a[r].trim()+(r!==i-1?",":"")}return t}var i="data-src";t.lazy(["pic","picture"],["picture"],function(n,o){if("picture"===n[0].tagName.toLowerCase()){var c=n.find(i),s=n.find("data-img"),u=this.config("imageBase")||"";c.length?(c.each(function(){e(t(this),"source",u)}),1===s.length?(s=e(s,"img",u),s.on("load",function(){o(!0)}).on("error",function(){o(!1)}),s.attr("src",s.attr(i)),this.config("removeAttribute")&&s.removeAttr(i)):n.attr(i)?(a(n,u+n.attr(i),o),this.config("removeAttribute")&&n.removeAttr(i)):o(!1)):n.attr("data-srcset")?(t("<source>").attr({media:n.attr("data-media"),sizes:n.attr("data-sizes"),type:n.attr("data-type"),srcset:r(n.attr("data-srcset"),u)}).appendTo(n),a(n,u+n.attr(i),o),this.config("removeAttribute")&&n.removeAttr(i+" data-srcset data-media data-sizes data-type")):o(!1)}else o(!1)})}(window.jQuery||window.Zepto);