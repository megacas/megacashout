$(document).ready(function(){
    let host = window.location.origin;
    $('.search__input').keyup(function(e){
        let searchKey = $("#search__input").val();
      
	    
	 k=e.key,
	 els=$('.navigation__header').data('categories'),
         i=$(this).val().trim(),
	 o=$('.search_-header'),
	 b=$('.dropdown_menu__header',o),
	 f=0;

	 b.html('').hide();

      if (k=='Enter') return;
      if (i.length<2) return;
        // console.log(i);
	$.ajax({
    		type : "POST",
    		url : host+"/live/search.php",
    		data : {
    			search : i
    		},
    		dataType: 'JSON',
    		success : function(response) {
    		  //  let html = [];
    		  //  let f = 0;
    		  //  let b = $('.dropdown_menu__header',o);
    		   if(response){
    		        response.forEach(element =>{
    		      //  console.log(element.b_name);
    		      //  html.push(`<p class="yellow_text__sitebar"><a href="./pages?bk=${element.b_id}" target="_blank">${element.b_name}</a></p>`);
    		        	$('<a href="/../pages?bk='+element.b_id+'" class="link__menu">'+element.b_name+'</a>').appendTo(b)
    		        f++;
    		    });
    		   }
    		  //  console.log(response);
    		  if(f) 
                    b.show();
                    
// 			$("#search-result").html("");
// 			$("#search-result").html(html);
    		}
    	});
    
//       for (el in els) { 
// 	      var v=els[el], re=new RegExp(i,'i');
// 	      if(v.search(re)!=-1) { 
// 		f++;
// 		var l = !isNaN(parseInt(el)) ? ('/cat/'+el) : el;
// 		$('<a href="'+l+'" class="link__menu">'+v+'</a>').appendTo(b)
// 	      } 
//       }	    

// 	if(f) 
// 	   b.show();

    })

    $('a.addtocart').click(function(event) {
        event.preventDefault();
    });
   
    $('a.addtocart').click(function(){

        // var link = $(this);
        // var rel = $(this).attr('rel');
        // var cat = $(this).attr('cat');
        // var uri = '/cart/add/'+rel;
        // if(cat)	uri+="/"+cat;
        // var lw = $('.link_cart__header')[0];
        // var i = lw.getAttribute('data-incart');

        // $.get(uri, {}, function(data){
        //     $('.link_cart__header').html('<span class="coll_product__heder">'+data['count_item']+'<span>');
        //     link.removeClass('add_to_cart_-table').addClass('checked_cart_-table').html('<img src="/assets/img/icon/c1.png" alt=""></i> ' + i);
        // },'json');

        // return false;
    });

    $('a.deletefromcart').click(function(){

        var rel = $(this).attr('rel');
        var cat = $(this).attr('cat');
        var uri = '/cart/delete/'+rel;
        if(cat) uri+="/"+cat;

        $.get(uri, {}, function(data){
            alert(data);
        },'json');

        return false;
    });

    var formatDate=function(seconds) {
        seconds = Number(seconds);
        var hours = Math.floor(seconds / 3600),
            minutes = Math.floor(seconds % 3600 / 60),
            seconds = Math.floor(seconds % 3600 % 60);
        return ((hours > 0 ? hours + ":" + (minutes < 10 ? "0" : "") : "") + minutes + ":" + (seconds < 10 ? "0" : "") + seconds);
    }
    var timer=function(o){
        if (Number(o.data('time')) <= 0) {
            o.html('<span class="timer-box">'+formatDate(0)+'</span>');
            if (o.data('item'))
                o.removeAttr('onclick').attr('disabled', 'disabled').html('');
            return;
        }
        if(o.data('item')){
            o.attr('onclick', 'javascript:if(confirm("Вы хотите вернуть товар? / Do you want to return the goods?")){document.location="/user/orders/cancel_cancel/?ck='+ o.data('order') + '/"}')
        }
        o.data('time',o.data('time')>=1?(o.data('time')-1):0);
        o.html('<span class="timer-box">'+formatDate(o.data('time'))+'</span>');
        setTimeout(timer, 1000, o)
    }
    $('i.icon-exclamation-sign[data-time]:not([disabled])').each(function(){timer($(this))})

    $('body').on('click', 'div.flash-msg', function() {
        $(this).hide();
    });

    $('[data-action="copy"]').click(function(){ console.log('111'); copyTextToClipboard($(this).text().trim()) })
});

(function(){
    var d=$(document),
        o = function($v){
            var o = $('#searchResult option').filter(function(){return this.value.toUpperCase() === $v.toUpperCase();})
            if(o.length){var u=$(o).data('id'); window.location.href=isNaN(u)?u:('/cat/'+u);}
        },
        s = function(str){
            if(!str) return;
            var key, obj=$('ul.memu').data('categories');r();
            for (key in obj)
                if (obj.hasOwnProperty(key) && obj[key].toLowerCase().search(str.toLowerCase()) != -1)
                    $("#searchResult").append($("<option>").attr('value', obj[key]).data('id', key));
        },
        f=function(){$('#searchBox').show().focus(); $('#searchBox').blur(c)},
        c=function(){$('#searchBox').hide().val('');r()},
        r=function(){$("#searchResult option").remove()}
        ;
    d.on('click',"#searchIcon",f);
    window.onkeydown = function(e) {
        var ck = e.keyCode ? e.keyCode : e.which;
        if ( !$('#searchBox').is(":visible") && (( ck == 70 && ( e.ctrlKey || e.metaKey ) ) || ( e.keyCode == 191 )) ) {f();e.preventDefault();}
    }
    d.on('input', "#searchBox", function () {o(this.value)});
    d.on('keyup', '#searchBox',function(e){
        if (e.keyCode === 27) return c();
        if (e.keyCode === 13) {if(!$(this).val()) return;o(this.value);}
        s($(this).val());
    });
})();

function flash(msg, type){
    type = type || 'success';
    $('div.flash-msg').remove();
    $('<div class="flash-msg '+type+'_modal alert-'+type+'"><div class="close_modal"></div>'+msg+'</div>').appendTo('body')
}

function copyTextToClipboard(text) {
    var textArea = document.createElement("textarea");
    textArea.style.position = 'fixed';
    textArea.style.top = 0;
    textArea.style.left = 0;
    textArea.style.width = '1em';
    textArea.style.height = '1em';
    textArea.style.padding = 0;
    textArea.style.border = 'none';
    textArea.style.outline = 'none';
    textArea.style.boxShadow = 'none';
    textArea.style.background = 'transparent';
    textArea.value = text;
    document.body.appendChild(textArea);
    textArea.focus();
    textArea.select();
    try {
        var successful = document.execCommand('copy');
        var msg = successful ? 'successful' : 'unsuccessful';
        flash('Copying to clipboard: ' + text);
    } catch (err) {
        console.error('Oops, unable to copy');
    }
    $(textArea).remove();
    //document.body.removeChild(textArea);

}
