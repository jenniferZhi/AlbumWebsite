function logout(){

	$.ajax({
		type : 'POST',
		contentType: "application/json; charset=UTF-8",
		url : "/7dzyltg7/p3/api/v1/logout",
		success : function(data){
			window.location.href = "/7dzyltg7/p3/";
		},
		error : function(error){
			alert("Didn't work!");
			window.location.href = "/7dzyltg7/p3/";
		} 
	});
}