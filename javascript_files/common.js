// Disable the facebook email text box if it is the same as the primary email
var fb_is_primary_email = $("#same_as_spoogler_email")
var spoogler_fb_email = $("#spoogler_fb_email")
var spoogler_email = $("#spoogler_email")
fb_is_primary_email.click(function(){
  if (this.checked) {
    document.getElementById("spoogler_fb_email").disabled = true;
    spoogler_fb_email.val(spoogler_email.val());
  } else {
    document.getElementById("spoogler_fb_email").disabled = false;
    spoogler_fb_email.val("");
  }
});

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

// Show a list of options for children age only if the Spoogler is a parent/expecting
var spoogler_is_parent = $("#spoogler_is_parent")
var children_ages = $("#ages")
var children_ages_label = $("#children_ages_label")
if($("#spoogler_is_parent option:selected").text() == "Yes"){
children_ages_label.show();
children_ages.show();
} else {
children_ages_label.hide();
children_ages.hide();
}
//children_ages_label.hide()
//children_ages.hide()
spoogler_is_parent.change(function(){
  if($("#spoogler_is_parent option:selected").text() == "Yes"){
    children_ages_label.show();
    children_ages.show();
  } else {
    children_ages_label.hide();
    children_ages.hide();
  }
});
