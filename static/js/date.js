var date = new Date();

function getDate(register){
	
	var iYear, fYear;
	if( register ) {
		iYear = date.getFullYear()-100;
		fYear = date.getFullYear();
	}
	else{
		iYear = date.getFullYear();
		fYear = date.getFullYear()+1;
	}
	$(function(){
	    var $select = $(".year");
	    for (i=iYear;i<=fYear;i++){
	    	if( i == date.getFullYear() ) {
	    		$select.append($('<option selected="selected"></option>').val(i).html(i))	
	    	}
	    	else{
	    		$select.append($('<option></option>').val(i).html(i))
	    	}
	    }
	})

	$(function(){
	    var $select = $(".month");
	    for (i=1;i<=12;i++){
	    	if( i == date.getMonth()+1 ) {
	    		$select.append($('<option selected="selected"></option>').val(i).html(i))	
	    	}
	    	else{
	    		$select.append($('<option></option>').val(i).html(i))
	    	}
	    }
	})

	var monthStart = new Date(date.getFullYear(), date.getMonth(), 1);
	var monthEnd = new Date(date.getFullYear(), date.getMonth() + 1, 1);
	var monthLength = (monthEnd - monthStart) / (1000 * 60 * 60 * 24)

	$(function(){
	    var $select = $(".day");
	    for (i=1;i<=monthLength;i++){
	    	if( i == date.getUTCDate() ) {
	    		$select.append($('<option selected="selected"></option>').val(i).html(i))	
	    	}
	    	else{
	    		$select.append($('<option></option>').val(i).html(i))
	    	}
	    }
	})
}
function getHour(){
	$(function(){
	    var $select = $(".h");
	    for (i=1;i<=24;i++){
	    	if( i == date.getHours() ) {
	    		$select.append($('<option selected="selected"></option>').val(i).html(i))	
	    	}
	    	else{
	    		$select.append($('<option></option>').val(i).html(i))
	    	}
	    }
	})

	$(function(){
	    var $select = $(".min");
	    for (i=1;i<=59;i++){
	    	if( i == date.getMinutes() ) {
	    		$select.append($('<option selected="selected"></option>').val(i).html(i))	
	    	}
	    	else{
	    		$select.append($('<option></option>').val(i).html(i))
	    	}
	    }
	})
}