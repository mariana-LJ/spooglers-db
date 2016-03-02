$(document).ready(function() {
    var signup_form = $("#signup");

    // Validate that the required fields have been filled and have the correct format
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

      // Automatically scroll to the top of the form if there where errors with the required fields
      $("html, body").animate({ scrollTop: 0}, 500);
      event.preventDefault();
      return false;
    });

    // Show a text box for the user to fill out if the option "Other" is selected among the options for address
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

    // Show a text box for the user to fill out if the option "Other" is selected among the language options
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