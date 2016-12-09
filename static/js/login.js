$(document).ready(function(){
	$("#login_form" ).submit(function(event){
			
		var data = {};
		var temp = $( this ).serializeArray();
			
		$.each(temp,function(){
			data[this.name] = this.value || '';
		});


		var username = data['username'];
        var password = data['password']; 

        data = JSON.stringify({"username" : username, "password" : password});

		$("p").empty();

		$.ajax({
			type : 'POST',
			contentType: "application/json; charset=UTF-8",
			url : "/7dzyltg7/p3/api/v1/login",
			data : data,
			success : function(data){
				var url = window.location.href;
				var flag = url.indexOf("url");
				if (flag == -1)
					window.location.href = "/7dzyltg7/p3/";
				else{
					var nextUrl = url.substring(flag+4, url.length);
					window.location.href = nextUrl;

				}
			},
			error : function(error){
				console.log(error.status);
				console.log(error);
				$("p").empty();

				for(var i = 0; i < error.responseJSON['errors'].length; i++){
					var new_error_p = $("<p />");
					new_error_p.addClass("error");
					new_error_p.text(error.responseJSON['errors'][i]["message"]);
					$("#errors_div").append(new_error_p);
				}
				document.user_login.reset();	
				
			} 
		});
		event.preventDefault();

	});
});

