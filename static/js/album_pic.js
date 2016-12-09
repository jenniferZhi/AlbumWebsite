
//=========================================AlbumPart=========================================
function album(albumid){
	flag = -1;
	userdata = 1;
	$.ajax({
		type : "GET",
		async : false,
		contentType : "application/json; charset=UTF-8",
		url : "/7dzyltg7/p3/api/v1/user",
		success : function(data){
			userdata = data;
			flag = 1;

		},
		error : function(error){

			flag = 0;
		}
	});

//-----------------------------------------------------------------


	album_url = "/7dzyltg7/p3/api/v1/album/" + albumid;
	album_info = 1;
	$.ajax({
		type : "GET",
		async : true,
		contentType : "application/json; charset=UTF-8",
		url : album_url,
		success : function(data){
			album_info = data;
			console.log(data);
			load_album_list(data, flag);
		},
		error : function(error){
			if (error.status == 401){
				$("p").empty();
				$("#content").empty();

				url = window.location.href;

				nextUrl = "/7dzyltg7/p3/login?url=" + url;
	
				$("#content").append("<p>Please click <a href=\""+nextUrl+"\">Here</a> to Log In</p>");
				
				for(var i = 0; i < error.responseJSON['errors'].length; i++){
					var new_error_p = $("<p />");
					new_error_p.addClass("error");
					new_error_p.text(error.responseJSON['errors'][i]["message"]);
					$("#errors_div").append(new_error_p);
				}

			}
			else {
				$("p").empty();

				for(var i = 0; i < error.responseJSON['errors'].length; i++){
					var new_error_p = $("<p />");
					new_error_p.addClass("error");
					new_error_p.text(error.responseJSON['errors'][i]["message"]);
					$("#errors_div").append(new_error_p);
				}
			}


		}
	});


	console.log(album_info);
	;


}



function load_album_list(album_info, flag){
	$("#content").empty();
	
	home_url = "/7dzyltg7/p3/"
	$("#content").append("<a href=\""+home_url+"\" id=\"nav_home\"><botton>Back to Home</botton></a>");
	$("#content").append("<br>");
	$("#content").append("<br>");

	if (flag == 1){
		editAccount_url = "/7dzyltg7/p3/user/edit"
		$("#content").append("<a href=\""+editAccount_url+"\" id=\"nav_edit\"><botton>Edit Account</botton></a>");
		$("#content").append("<br>");
		$("#content").append("<br>");


		Albums_url = "/7dzyltg7/p3/albums"
		$("#content").append("<a href=\""+Albums_url+"\" id=\"nav_albums\"><botton>My Albums</botton></a>");
		$("#content").append("<br>");
		$("#content").append("<br>");

		var logout = $("<a href=\"\" id=\"nav_logout\"><botton>Log Out</botton></a>")
		$("#content").append(logout);

		logout.on("click", function(){
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
		});

		$("#content").append("<br>");


	}

	$("#content").append("<h1>ALBUM</h1>");

	var new_p = $("<p />");
	new_p.text("Album ID: " + album_info['albumid']);
	$("#content").append(new_p);

	var new_p = $("<p />");
	new_p.text("Album Title: " + album_info['title']);
	$("#content").append(new_p);

	var new_p = $("<p />");
	new_p.text("Album User: " + album_info['username']);
	$("#content").append(new_p);

	var new_p = $("<p />");
	new_p.text("Created: " + album_info['created']);
	$("#content").append(new_p);

	var new_p = $("<p />");
	new_p.text("LastUpdated: " + album_info['lastupdated']);
	$("#content").append(new_p);


//----------------------------------------------------------------------------------------------------
	flag_input = -1;
	input_url = "/7dzyltg7/p3/api/v1/input/" + album_info['albumid'];
	$.ajax({
		type : 'GET',
		async : false,
		contentType: "application/json; charset=UTF-8",
		url : input_url,
		success : function(data){
			console.log(data);
			flag_input = 1;
		},
		error : function(error){
			if (error.status == 401 || error.status == 403 || error.status == 404)
				flag_input = 0;
		}
	});

	if (flag_input == 1){
		album_edit_url = "/7dzyltg7/p3/album/edit?albumid=" + album_info['albumid'];
		$("#content").append("<p>To edit this album, please click <a href=\""+album_edit_url+"\">Here</a>.</p>");
	}


//----------------------------------------------------------------------------------------------------
	photo_list = album_info['pics'];

	for (var i = 0; i < photo_list.length; i++){
		var picid = photo_list[i].picid;
		var format = photo_list[i].format;
		
		var new_p = $("<p />");
		new_p.text("PICID: " + picid);
		$("#content").append(new_p);

		var pic = $("<img src=\"/static/images/" + picid + "." + format + "\" id=\"pic_"+picid+"_link\">");
		$("#content").append(pic);
		pic.on("click", function(){
			picid = this.id.substring(4, this.id.length - 5);
			var pic_url = "/7dzyltg7/p3/pic?picid=" + picid;
			var pic_title = "Pic Page";
			var stateObj = { stateVariable : picid, stateType : "pic"};
			history.pushState(stateObj, pic_title, pic_url);



			showPic(picid);

		});
	}



}






//=========================================PicPart=========================================


function showPic(picid){

	flag = -1;
	userdata = 1;
	$.ajax({
		type : "GET",
		async : false,
		contentType : "application/json; charset=UTF-8",
		url : "/7dzyltg7/p3/api/v1/user",
		success : function(data){
			userdata = data;
			flag = 1;

		},
		error : function(error){
			flag = 0;
		}
	});

//---------------------------------------------------


	pic_url = "/7dzyltg7/p3/api/v1/pic/" + picid;

	picdata = 1;
	$.ajax({
		type : 'GET',
		contentType: "application/json; charset=UTF-8",
		url : pic_url,
		success : function(data){
			console.log(data);
			load_pic_list(data, flag);
		},
		error : function(error){
			if (error.status == 401){
				$("p").empty();
				$("#content").empty();

				url = window.location.href;

				nextUrl = "/7dzyltg7/p3/login?url=" + url;
	
				$("#content").append("<p>Please click <a href=\""+nextUrl+"\">Here</a> to Log In</p>");
				
				for(var i = 0; i < error.responseJSON['errors'].length; i++){
					var new_error_p = $("<p />");
					new_error_p.addClass("error");
					new_error_p.text(error.responseJSON['errors'][i]["message"]);
					$("#errors_div").append(new_error_p);
				}

			}
			else {
				$("p").empty();

				for(var i = 0; i < error.responseJSON['errors'].length; i++){
					var new_error_p = $("<p />");
					new_error_p.addClass("error");
					new_error_p.text(error.responseJSON['errors'][i]["message"]);
					$("#errors_div").append(new_error_p);
				}
			}
		}
	});

}
function load_pic_list(picdata, flag){
	format = picdata['format'];
	picid = picdata['picid'];
	albumid = picdata['albumid'];
	nextid = picdata['next'];
	previd = picdata['prev'];

//----------------------------------------------------------------------
	flag_input = -1;
	input_url = "/7dzyltg7/p3/api/v1/input/" + albumid;
	$.ajax({
		type : 'GET',
		async : false,
		contentType: "application/json; charset=UTF-8",
		url : input_url,
		success : function(data){
			console.log(data);
			flag_input = 1;
		},
		error : function(error){
			if (error.status == 401 || error.status == 403 || error.status == 404)
				flag_input = 0;
		}
	});

	console.log(flag_input);


//----------------------------------------------------------------------


	$("#content").empty();
	$("errors_div").empty();

	home_url = "/7dzyltg7/p3/"
	$("#content").append("<a href=\""+home_url+"\" id=\"nav_home\"><botton>Back to Home</botton></a>");
	$("#content").append("<br>");
	$("#content").append("<br>");

	if (flag == 1){
		editAccount_url = "/7dzyltg7/p3/user/edit"
		$("#content").append("<a href=\""+editAccount_url+"\" id=\"nav_edit\"><botton>Edit Account</botton></a>");
		$("#content").append("<br>");
		$("#content").append("<br>");


		Albums_url = "/7dzyltg7/p3/albums"
		$("#content").append("<a href=\""+Albums_url+"\" id=\"nav_albums\"><botton>My Albums</botton></a>");
		$("#content").append("<br>");
		$("#content").append("<br>");

		var logout = $("<a href=\"\" id=\"nav_logout\"><botton>Log Out</botton></a>")
		$("#content").append(logout);

		logout.on("click", function(){
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
		});

		$("#content").append("<br>");


	}

	$("#content").append("<h1>PICTURE</h1>");

	var new_p = $("<p />");
	new_p.text("Pic ID: " + picdata['picid']);
	$("#content").append(new_p);


	if (flag_input == 1){
		var new_input = $("<input type=\"text\" name=\"caption\" value=\""+picdata['caption']+"\" id=\"pic_caption_input\">");
		$("#content").append(new_input);
		$('#pic_caption_input').bind('keypress', function(event){
			if(event.keyCode == "13"){
				$.ajax({
					type : "PUT",
					async : true,
					contentType: "application/json; charset=UTF-8",
					url : "/7dzyltg7/p3/api/v1/pic/" + picid,
					data : JSON.stringify({"albumid" : picdata['albumid'], "format" : picdata['format'], "next" : picdata['next'], "prev" : picdata['prev'] ,"picid" : picdata['picid'], "caption" : $("#pic_caption_input").val()}),
					success : function(data){
						alert("User Information Update Success!");

					},
					error : function(error){
						alert("Error Happened")

					}
				});
			};
		});
	}
	else{
		var new_p = $("<p />");
		new_p.text("Caption: " + picdata['caption']);
		$("#content").append(new_p);
	}

	$("#content").append("<br>");
	$("#content").append("<br>");

	var pic = $("<img src=\"/static/images/" + picid + "." + format + "\" id=\"pic_"+picid+"_link\">");
	$("#content").append(pic);


	var prev_nav = $("<button name=\""+previd+"\" id=\"prev_pic\">Previous Pic</button>");
	$("#content").append(prev_nav);
	prev_nav.on("click", function(){
		previd = this.name;

		var pic_url = "/7dzyltg7/p3/pic?picid=" + previd;
		var pic_title = "Pic Page";	
		var stateObj = { stateVariable : previd, stateType : "pic"};
		history.pushState(stateObj, pic_title, pic_url);
		
		showPic(previd);


	});




	var next_nav = $("<button name=\""+nextid+"\" id=\"next_pic\">Next Pic</button>");
	$("#content").append(next_nav);
	next_nav.on("click", function(){
		nextid = this.name;
		
		var pic_url = "/7dzyltg7/p3/pic?picid=" + nextid;
		var pic_title = "Pic Page";	
		var stateObj = { stateVariable : nextid, stateType : "pic"};
		history.pushState(stateObj, pic_title, pic_url);
		
		showPic(nextid);



	});

}





















