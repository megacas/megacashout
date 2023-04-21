$(".table_page tr").click(function() {
    let data = [];
    $(this).addClass('selected').siblings().removeClass('selected');
    //var value = $(this).find('td:nth-child(7)').html();
    var tds = $(this).children('td');
    //change the button
      var cart_btn = $(this).find('td:nth-child(3)').find('a').html();
       console.log(cart_btn);
      var inCart = '<img src="../assets/c1.png" alt=""> In cart';
     
      $(this).find('td:nth-child(3)').find('a').html('<img src="../assets/c1.png" alt=""></i> In cart');
      
      var cart_btn_div = $(this).find('td:nth-child(3)').find('div').html();
      var cart_btn_span = $(this).find('td:nth-child(3)').find('span').html();
      //  console.log(cart_btn_span);

      $(this).find('td:nth-child(3)').find('div').html(`<span class="line_table__left">${cart_btn_span}</span> <a  class="checked_cart_-table addtocart" cat="357" rel="2180956"><img src="../assets/c1.png" alt=""></i> In cart</a>`); 
      // console.log(cart_btn_div);
      // cart_btn.removeClass('add_to_cart_-table').addClass('checked_cart_-table').html('<img src="../assets/c1.png" alt=""></i> ');
      // link.removeClass('add_to_cart_-table').addClass('checked_cart_-table').html('<img src="/assets/img/icon/c1.png" alt=""></i> ' + i);

  
    //
    for(i=1; i<=tds.length; i++){
      let td_spanvalue = $(this).find(`td:nth-child(${i})`).find('span').html();
      
      if(i==tds.length){
        let price = td_spanvalue.match(/(\d+)/);
        data.push(price[0])
        //console.log(price[0]);
      }else{
        data.push(td_spanvalue);
       // console.log(td_spanvalue);
      }
      
    }
    // console.log(data[0]);
    let title = $('.main__title').html();
    let onlytitle = title.split('</i>')
    // console.log(onlytitle[1].toString());
    // send data based on data
    if(cart_btn != inCart){
      var addcart = $('.coll_product_cart').html();
      ++addcart;
      var addcart = $('.coll_product_cart').html(addcart);
    
      console.log('yes');
      if(data.length==4){
        $.ajax({
            url: '../process/process.php',
            type: 'POST',
            data:  {'city':data[0],'state':data[1],'zip':data[2],'price':data[3],'title':onlytitle[1],'type':'four', 'cart':1},
            dataType: 'JSON',
        success: function(response)
        {
           
        },
        error: function() 
        {
            
        } 	        
        });
    }else if(data.length==3){
        $.ajax({
            url: '../process/process.php',
            type: 'POST',
            data:  {'balance':data[0],'accounts':data[1],'price':data[2],'title':onlytitle[1],'type':'three', 'cart':1},
            dataType: 'JSON',
        success: function(response)
        {
           
        },
        error: function() 
        {
            
        } 	        
        });
    }else if(data.length==2){
        $.ajax({
            url: '../process/process.php',
            type: 'POST',
            data:  {'info':data[0],'price':data[1],'title':onlytitle[1], 'type':'two', 'cart':1},
            dataType: 'JSON',
        success: function(response)
        {
           
        },
        error: function() 
        {
            
        } 	        
        });
    }
    }else{
      console.log('no');
    }
   
    
  //   alert(value);
   // console.log(tds.length);
  });
  $('a.checked_cart_-table').click(function(event) {
    event.preventDefault();
  });
  $('.ok').on('click', function(e) {
    alert($("#table tr.selected td").html());
  });