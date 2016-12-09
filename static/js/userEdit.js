$(document).ready(function(){
	$("#useredit_form" ).submit(function(event){
			
		var data = {};
		var temp = $( this ).serializeArray();
			
		$.each(temp,function(){
			data[this.name] = this.value || '';
		})

		alert("success")

        var firstname = data['firstname']; 
       	var lastname = data['lastname'];
    	var password1 = data['password1']; 
    	var password2 = data['password2']; 
    	var email = data['email'];


    	userdata = 1;
		$.ajax({
			type : 'GET',
			async : false,
			contentType: "application/json; charset=UTF-8",
			url : "/7dzyltg7/p3/api/v1/user",
			success : function(data){
				alert("success");
				console.log(data);
				userdata = data;
			},
			error : function(error){
				alert("error happens!");
				
			
			}
		});

		username = userdata['username']

    	data = JSON.stringify({"username" : username, "firstname" : firstname, "lastname" : lastname, "password1" : password1, "password2" : password2, "email" : email})
		

		var flag = 1;

		flag = addErrorEditPage(firstname, lastname, password1, password2, email);
		//Get User Data



		if (flag == 1){
			$.ajax({
				type : "PUT",
				async : false,
				contentType: "application/json; charset=UTF-8",
				url : "/7dzyltg7/p3/api/v1/user",
				data : data,
				success : function(data){
					alert("User Information Update Success!");
					window.location.href = "/7dzyltg7/p3/user/edit";

				},
				error : function(error){

					console.log(error.status);
					alert("response.responseText");
					$("p").empty();


					for(var i = 0; i < error.responseJSON['errors'].length; i++){
						var new_error_p = $("<p />");
						new_error_p.addClass("error");
						new_error_p.text(error.responseJSON['errors'][i]["message"]);
						$("#errors_div").append(new_error_p);
					}
					document.edit_user.reset();	

				}

			});
			event.preventDefault();

		}
		else{
			alert("Username Update failed")
			document.edit_user.reset();			
			flag = 1;
			return false;
		}





	});
});

function addErrorEditPage(firstname, lastname, password1, password2, email){
	var new_error_p = $("<p />");

	flag = 1;

	$("p").empty();

	if (firstname.length > 20){
		var new_error_p = $("<p />");
		new_error_p.addClass("error");
		new_error_p.text("Firstname must be no longer than 20 characters");
		$("#errors_div").append(new_error_p);
		flag = 0;
	}

	if (lastname.length > 20){
		var new_error_p = $("<p />");
		new_error_p.addClass("error");
		new_error_p.text("Lastname must be no longer than 20 characters");
		$("#errors_div").append(new_error_p);
		flag = 0;
	}

	if (password1.length < 8){
		if (password1.length != 0){
			var new_error_p = $("<p />");
			new_error_p.addClass("error");
			new_error_p.text("Passwords must be at least 8 characters long");
			$("#errors_div").append(new_error_p);
			flag = 0;
		}
	}

	if (!/^[0-9a-zA-Z_]*$/.test(password1)){
		if (password1.length != 0){
			var new_error_p = $("<p />");
			new_error_p.addClass("error");
			new_error_p.text("Passwords may only contain letters, digits, and underscores");
			$("#errors_div").append(new_error_p);
			flag = 0;
			//password1Pattern1
		}
	}

	if (/^[0-9]*$/.test(password1) || /^[a-zA-Z]*$/.test(password1)){
		if (password1.length != 0){
			var new_error_p = $("<p />");
			new_error_p.addClass("error");
			new_error_p.text("Passwords must contain at least one letter and one number");
			$("#errors_div").append(new_error_p);
			flag = 0;
		}
	}



	if (password1 != password2) {
		var new_error_p = $("<p />");
		new_error_p.addClass("error");
		new_error_p.text("Passwords do not match");
		$("#errors_div").append(new_error_p);
		flag = 0;
	}


	if (!/[^@]+@[^@]+\.[^@]+/.test(email)) {
		var new_error_p = $("<p />");
		new_error_p.addClass("error");
		new_error_p.text("Email address must be valid");
		$("#errors_div").append(new_error_p);
		flag = 0;
	}

	if (email.length > 40){
		var new_error_p = $("<p />");
		new_error_p.addClass("error");
		new_error_p.text("Email must be no longer than 40 characters");
		$("#errors_div").append(new_error_p);
		flag = 0;
	}
	return flag; 


}
