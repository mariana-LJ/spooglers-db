// Show a list of U.S. states if the country of origin is the U.S.
var country = $("#spoogler_country")
var us_state = $("#spoogler_us_state")
var us_state_label = $("#spoogler_us_state_label")
us_state.hide();
us_state_label.hide();
country.change(function(){
  if($("#spoogler_country option:selected").text() == "United States of America"){
    us_state_label.show();
    us_state.show();
  } else {
    us_state.hide();
    us_state_label.hide();
    us_state.val(0);
  }
});