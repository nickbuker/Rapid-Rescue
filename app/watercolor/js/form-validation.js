$(document).ready(function(){

	// hide messages 
	$("#error").hide();
	$("#success").hide();
	
	// on submit...
	$("#send").click(function() {
		$("#error").hide();
		
		//required:
		
		//name
		var name = $("input#name").val();
		if(name == ""){
			$("#error").fadeIn().text("Name required.");
			$("input#name").focus();
			return false;
		}
		
		// email
		var email = $("input#email").val();
		if(email == ""){
			$("#error").fadeIn().text("Email required");
			$("input#email").focus();
			return false;
		}
		
		// web
		var web = $("input#web").val();
		if(web == ""){
			$("#error").fadeIn().text("Web required");
			$("input#web").focus();
			return false;
		}
		
		// comments
		var comments = $("#comments").val();
		
		// data string
		var dataString = 'name='+ name
						+ '&email=' + email        
						+ '&web=' + web
						+ '&comments=' + comments;
						         
		// ajax
		$.ajax({
			type:"POST",
			url: "send-mail.php",
			data: dataString,
			success: success()
		});
	});  
		
		
	// on success...
	 function success(){
	 	$("#success").fadeIn();
	 	$("#formMail").fadeOut();
	 }
	
    return false;
});

