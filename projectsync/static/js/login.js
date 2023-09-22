$(".outline").on('click', function(e){
  e.preventDefault();
  let id = $(this).attr("name");
  if (id === "login") {
    $("form").animate({
      "right": null,
      "left": "440px"
    }, "swing");
		$("input[name*='Name']").fadeOut("slow").slideUp("slow");
    $("input[name*='univ']").fadeOut("slow").slideUp("slow");
		$(".formButton").text('Login');
    $(".formButton").attr("name","login");
  } 
  
  else if (id === "studentsignup") {
    $("form").animate({
      "left": null,
			"right": "440px"
    });
		$("input[name*='Name']").fadeIn("slow").slideDown("slow");
    $("input[name*='univ']").fadeIn("slow").slideDown("slow");
		$(".formButton").text('Student SignUp');
    $(".formButton").attr("name","studentsignup");
  }
  
  else if (id === "univsignup") {
    $("form").animate({
      "left": null,
			"right": "440px"
    });
		$("input[name*='univ']").fadeIn("slow").slideDown("slow");
    $("input[name*='Name']").fadeOut("slow").slideUp("slow");
		$(".formButton").text('Univ Sign Up');
    $(".formButton").attr("name","univsignup");
  }
});