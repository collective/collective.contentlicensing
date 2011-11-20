/******
    Standard popups
******/


jQuery(function($){
    
    if (typeof(common_content_filter) == "undefined") {
	common_content_filter = false;
    }

    $('#other_license_overlay a').prepOverlay(
	{
	    subtype: 'ajax',
            filter: common_content_filter,
            formselector: 'form',
            closeselector:'[name=form.actions.Cancel]',
	    noform: function(el) {
	        return InsertOtherIntoParent('close');},
	}
    );


    function InsertOtherIntoParent(noform) {
	var formvars = $('form').context.forms[2];
        var license_name = formvars['form.license_name'].value;
	var license_url = formvars['form.license_url'].value;
        var license_image = formvars['form.license_image'].value;
	var other_license = window.parent.document.getElementById('other_name1');
	var other_image = window.parent.document.getElementById('license_other_button1');
	var other_license_name = window.parent.document.getElementById('license_other_name');
	var other_license_url = window.parent.document.getElementById('license_other_url');
	var other_license_button = window.parent.document.getElementById('license_other_button');
	var radio_buttons = window.parent.document.getElementsByName('license');
        for (x in radio_buttons)
	{
            if ('Other' == radio_buttons[x].value)
	    {
                radio_buttons[x].checked = true;
                break;
            }
        }
	other_license.setAttribute('href', license_url);
	other_license.innerHTML = license_name;
	other_license_name.setAttribute('value', license_name);
	other_license_url.setAttribute('value', license_url);
	if (license_image) 
        {
            other_image.setAttribute('src', license_image);
	    other_license_button.setAttribute('value', license_image);
	} 
        else 
        {
            other_license_button.setAttribute('value', '');
        }
        return noform;
    }

   
});

