$(document).ready(function() {
  $(".on_google_group").click(function(){
    var on_gg = $(this)
    $.ajax({
      method: "POST",
      url: "admin/google_group",
      data: { googler_ldap: on_gg.val(), status: this.checked }
    })
    .done(function( msg ) {
      alert( "Data Saved: " + msg );
      if(msg.indexOf("Error") == 0) {
        on_gg.attr("checked", false);
      } else {
        on_gg.attr("disabled", true);
      }
    });
  });

  $(".on_facebook").click(function(){
    var on_fb = $(this)
    $.ajax({
      method: "POST",
      url: "admin/facebook",
      data: { googler_ldap: on_fb.val(), status: this.checked }
    })
    .done(function( msg ) {
      alert( "Data Saved: " + msg );
      if(msg.indexOf("Error") == 0) {
        on_fb.attr("checked", false);
      } else {
        on_fb.attr("disabled", true);
      }
    });
  });

  $(".on_fb_kidsZone").click(function(){
    var on_fb_kids = $(this)
    $.ajax({
      method: "POST",
      url: "admin/fb_kids",
      data: { googler_ldap: on_fb_kids.val(), status: this.checked }
    })
    .done(function( msg ) {
      alert( "Data Saved: " + msg );
      if(msg.indexOf("Error") == 0) {
        on_fb_kids.attr("checked", false);
      } else {
        on_fb_kids.attr("disabled", true);
      }
    });
  });

  // Show filter options
  $("#show").click(function(){
      $("#filters").show();
  });

  // Hide filter options
  $("#hide").click(function(){
    $("#filters").hide();
  });
  $("#filters").hide();

  // Apply selected filters
  $("#apply").click(function(){
    $("#filters_form").submit();
  });

  // Remove all previously selected filters
  $("#clear").click(function(){
    var myform = document.getElementById("filters_form");
    var elements = myform.elements;

    for(i = 0; i < elements.length; i++){
      field_type = elements[i].type.toLowerCase();
      switch(field_type) {
        case "text":
        case "textarea":
          elements[i].value = "";
          break;
        case "checkbox":
          elements[i].checked = false;
          break;
        case "select-one":
          elements[i].selectedIndex = 0;
          break;
        case "radio":
          elements[i].value = 0;
      }
    }


    $("#filters_form").submit();
  });

  function reset_filters(myform){
  }

  // Hide questions that are difficult to use with filters
  var other_native_lang = $("#native_lang_other")
  other_native_lang.hide();
  var other_address = $("#other_address")
  other_address.hide();
  var moving_challenge = $("#spoogler_relo")
  moving_challenge.hide();
  var support_others_other = $("#support_others_other")
  support_others_other.hide();
});