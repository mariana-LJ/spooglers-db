$(document).ready(function() {
    var signup_form = $("#signup");

    signup_form.submit(function (event) {
      signup_form.validate({
        rules: {
          full_name: "required",
          spoogler_email: {
            required: true,
            email: true
          },
          spoogler_fb_email: {
            required: false,
            email: true
          },
          googler_ldap: "required",
        },
        messages:{
          full_name: "Please enter the Spoogler's full name",
          spoogler_email: {
            required: "Please enter the Spoogler's email",
            email: "Please enter a valid email"
          },
          googler_ldap: "Please enter the Googler's ldap",
        },
      });

      if(signup_form.valid()) {
        signup_form.unbind('submit').submit();
        return;
      }

      $("html, body").animate({ scrollTop: 0}, 500);
      event.preventDefault();
      return false;
    });

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
      }
    });

    var address = $("#address")
    var other_address = $("#other_address")
    other_address.hide();
    address.change(function() {
      if($("#address option:selected").text() == "Other") {
        other_address.show();
      } else {
        other_address.hide();
        other_address.val("");
      }
    });

    var native_lang = $("#native_lang")
    var other_native_lang = $("#native_lang_other")
    other_native_lang.hide();
    native_lang.change(function() {
      if($("#native_lang option:selected").text() == "Other") {
        other_native_lang.show();
      } else {
        other_native_lang.hide();
        other_native_lang.val("");
      }
    });

});